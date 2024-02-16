<script lang="ts">
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";
	import { checkSession } from "../../services/sessionManager";
	import { browser } from "$app/environment";
	import { Body } from "svelte-body";
	import Select from "svelte-select";
	import Modal from "../../components/Modal.svelte";

	let isLoading = true;
	let projects: any = [];
	let headers: any = [];

	let applicants: any = [];
	let applicantNames: any = [];
	let selectedApplicants: any = [];
	let value: any = "";

	let showModal = false;
	$: bodyStyle = {
		filter: showModal ? "blur(5px)" : "none",
	};

	onMount(async () => {
		try {
			let projectUrl = "http://localhost:8000/projects/";
			let response = await fetch(projectUrl, {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
			});
			projects = await response.json().then((data) => {
				headers = Object.keys(data[0]);
				console.log(data);
				console.log(headers);
				return data;
			});

			let applicantsUrl = "http://localhost:8000/participants/";
			let applicantsResponse = await fetch(applicantsUrl, {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
			});
			applicants = await applicantsResponse.json().then((data) => {
				return data;
			}).then((data) => {
				applicantNames = data.map((applicant: any) => {
					return applicant.name;
				});
				return applicantNames;
			});
		} catch (error) {
			console.log(error);
		}

	});

	if (browser) {
		async () => {
			const sessionValid = await checkSession();
			if (sessionValid) {
				window.location.href = "/dashboard";
			} else {
				isLoading = false;
			}
		};

		setTimeout(() => {
			isLoading = false;
		}, 500);
	}
</script>

{#if isLoading}
	<div class="flex items-center justify-center min-h-screen transition-main">
		<div
			class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"
		></div>
	</div>
{:else}
	<div
		class="flex items-start justify-center transition-main"
		id="swup"
		in:fade={{ duration: 400 }}
	>
		<div class="flex justify-between mt-16 items-start w-4/5">
			<div
				class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform flex-1"
			>
				<div class="flex items-center justify-between mb-16">
					<h1 class="text-4xl font-bold">Projects</h1>
					<button
						class="bg-white text-teal-500 border border-teal-500 p-2 rounded shadow transition-all duration-500 hover:bg-teal-500 hover:text-white hover:shadow-lg hover:scale-105 transform-gpu flex items-center"
						on:click={() => (showModal = true)}
					>
						<span class="material-icons mr-2"> add </span>
						New Project
					</button>
				</div>
				<table class="mx-auto w-full border border-collapse">
					<thead>
						<tr>
							{#each headers as header}
								{#if header !== "id"}
									<th
										class="bg-gray-200 text-gray-600 border border-gray-300 px-4 py-2"
										>{header.toUpperCase()}</th
									>
								{/if}
							{/each}
							<th
								class="bg-gray-200 text-gray-600 border border-gray-300 px-4 py-2"
								>Actions</th
							>
						</tr>
					</thead>
					<tbody class="text-center">
						{#each projects as project (project.id)}
							<tr
								class="hover:bg-gray-300 transition-all duration-500"
							>
								{#each headers as header, index (header)}
									{#if index !== 0}
										<td class="border px-4">
											{project[header]}
										</td>
									{/if}
								{/each}
								<td
									class="border px-4 py-4 items-center justify-center"
								>
									<a
										href={`/projects/${project.id}`}
										class="bg-teal-400 text-white p-2 rounded hover:bg-teal-500 transition-all duration-500 text-center"
									>
										Details
									</a>
								</td>
							</tr>
						{/each}
					</tbody>
				</table>
			</div>
		</div>
	</div>
{/if}

<Body style={bodyStyle} />

<Modal bind:showModal>
	<h2
		slot="header"
		class="text-2xl font-semibold mb-8 text-center text-black-600"
	>
		Create a new project
	</h2>

	<div
		slot="body"
		class="w-full mb-8 p-4 bg-gray-100 rounded shadow"
		style="width: 400px"
	>
		<form>
			{#each headers as header}
				{#if header !== "id"}
					{#if header === "participants"}
						<label
							for={header}
							class="block text-gray-600 font-semibold mb-2"
							>{header.charAt(0).toUpperCase() +
								header.slice(1)}</label
						>
						<Select
							items={applicantNames}
							bind:value
						/>
						{#if value}
							<p class="text-gray-600 mt-2">
								Selected: {value}
							</p>
						{/if}
					{:else}
						<div class="mb-4">
							<label
								for={header}
								class="block text-gray-600 font-semibold mb-2"
								>{header.charAt(0).toUpperCase() +
									header.slice(1)}</label
							>
							<input
								type="text"
								id={header}
								name={header}
								class="w-full p-2 border border-gray-300 rounded"
							/>
						</div>
					{/if}
				{/if}
			{/each}
		</form>
	</div>
</Modal>

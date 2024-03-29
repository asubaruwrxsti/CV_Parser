<script lang="ts">
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";
	import { checkSession } from "../../services/sessionManager";
	import { browser } from "$app/environment";
	import { Body } from "svelte-body";
	import { truncate, isJson } from "../../utils/utils";
	import { fetchData, postData } from "../../services/dataManager";

	import Modal from "../../components/Modal.svelte";
	import ParticipantsSelect from "../../components/ParticipantsSelect.svelte";
	import ToRselect from "../../components/TORselect.svelte";
	import StatusEdit from "../../components/StatusEdit.svelte";
	import ImageEdit from "../../components/ImageEdit.svelte";

	// TODO: Add pagination to the projects page

	// Loading state
	let isLoading = true;

	// Projects data
	let projects: any = [];
	let headers: any = [];

	// Modal state
	let showModal = false;
	$: bodyStyle = {
		filter: showModal ? "blur(5px)" : "none",
	};

	// TOR tags
	let tags: string[] = [];

	// Modal status state
	let status = "inactive";

	onMount(async () => {
		try {
			projects = await fetchData("projects").then((res) => {
				headers = Object.keys(res[0]);
				return res;
			});
		} catch (error) {
			console.log(error);
		}
	});

	// Create a new project submission
	async function createProject(event: any) {
		event.preventDefault();
		let formData = new FormData(event.target);
		const fileField = event.target.querySelector('input[type="file"]');
		const reader = new FileReader();
		let fileBase64: string = "";

		reader.onloadend = function () {
			if (reader.result === null) {
				console.error("Failed to read file");
			} else {
				fileBase64 = reader.result as string;
			}

			// Add the base64 string to formData
			formData.set(fileField.name, fileBase64);

			// Send the request
			sendRequest(formData);
		};

		if (fileField.files.length > 0) {
			// If a file is present, read it
			reader.readAsDataURL(fileField.files[0]);
		} else {
			// If no file is present, send the request immediately
			sendRequest(formData);
		}
	}

	async function sendRequest(formData: FormData) {
		// Add the tags to formData
		formData.set("tor", JSON.stringify(tags));

		for(let pair of formData.entries()) {
			console.log(pair[0]+ ', '+ pair[1]);
		}

		await postData(
			"projects",
			"",
			JSON.stringify(Object.fromEntries(formData)),
		).then((res) => {
			console.log(res);
			showModal = false;
		});
	}

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
								{#if header !== "id" && header !== "image"}
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
					<tbody class="items-center justify-start">
						{#each projects as project (project.id)}
							<tr
								class="hover:bg-teal-100 transition-all duration-500"
							>
								{#each headers as header, index (header)}
									{#if index !== 0 && header !== "image"}
										<td class="border px-4">
											{#if isJson(project[header])}
												{#each JSON.parse(project[header]).slice(0, 3) as tag (tag)}
													<div
														class="tag mt-2 bg-teal-200 rounded px-3 py-1 text-sm text-blue-700 mr-2 mb-2 flex items-center inline-flex justify-start"
													>
														<span
															>{tag.label ||
																tag}</span
														>
													</div>
												{/each}
												{#if JSON.parse(project[header]).length > 3}
													<div
														class="tag mt-2 bg-teal-200 rounded px-3 py-1 text-sm text-blue-700 mr-2 mb-2 flex items-center inline-flex justify-start"
													>
														<span>...</span>
													</div>
												{/if}
											{:else}
												{truncate(project[header], 100)}
											{/if}
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

<Modal bind:showModal showCloseButton={false}>
	<h2
		slot="header"
		class="text-2xl font-semibold m-8 text-center text-black-600"
	>
		Create a new project
	</h2>

	<div
		slot="body"
		class="w-full mb-8 p-4 bg-gray-100 rounded shadow"
		style="width: 400px"
	>
		<form on:submit|preventDefault={createProject}>
			{#each headers as header}
				{#if header !== "id"}
					{#if header === "participants"}
						<ParticipantsSelect
							{header}
							data={{ key: "", projectID: 0, value: [] }}
							showSaveButton={false}
						/>
					{:else if header === "image"}
						<ImageEdit
							{header}
							data={{ key: "image", projectID: "" }}
							showSaveButton={false}
						/>
					{:else if header === "status"}
						<StatusEdit
							{header}
							data={{ status }}
							showSaveButton={false}
						/>
					{:else if header === "tor"}
						<ToRselect
							{header}
							data={{ value: { tags } }}
							on:tagsUpdated={(event) => (tags = event.detail)}
						/>
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
			<button
				type="submit"
				class="bg-teal-500 text-white p-2 rounded hover:bg-teal-600 transition-all duration-500 w-full"
			>
				Create
			</button>
		</form>
	</div>
</Modal>

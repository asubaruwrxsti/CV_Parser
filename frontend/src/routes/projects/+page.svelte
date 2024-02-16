<script lang="ts">
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";
	import { checkSession } from "../../services/sessionManager";
	import { browser } from "$app/environment";

	let isLoading = true;
	let projects: any = [];
	let headers: any = [];

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
				return data;
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
										href="{`/projects/${project.id}`}"
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

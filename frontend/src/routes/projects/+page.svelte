<script lang="ts">
	import { onMount } from "svelte";
	import { checkSession } from "../../services/sessionManager";
	import { browser } from "$app/environment";

	let isLoading = true;
	let projects: any = [];

	onMount(async () => {
		try {
			let projectUrl = "http://localhost:8000/projects/user";
			let response = await fetch(projectUrl, {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
			});
			projects = await response.json().then((data) => {
				if (data.detail) {
					localStorage.removeItem("session");
					window.location.href = "/login";
				}
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
	<div class="flex items-start justify-center transition-main" id="swup">
		<div class="flex justify-between mt-16 items-start" style="gap: 4rem;">
			<div
				class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform hover:scale-105 flex-1"
			>
				<h2 class="text-2xl font-bold mb-2">You are participant in:</h2>
				<div class="flex flex-col">
					{#if projects.userParticipatingProjects.length > 0}
						{#each projects.userParticipatingProjects.slice(0, 3) as project (project.id)}
							<a
								href="#!"
								class="text-gray-700 mb-2 transition-all duration-500 border border-gray-200 p-2 rounded hover:border-teal-400 hover:bg-teal-200"
							>
								{project.name}
							</a>
						{/each}
						{#if projects.userParticipatingProjects.length > 3}
							<a
								href="#!"
								class="mt-2 bg-teal-400 text-white p-2 rounded hover:bg-teal-500 transition-all duration-500"
								>View All</a
							>
						{/if}
					{:else}
						<p class="text-gray-700">No projects found.</p>
					{/if}
				</div>
			</div>
			<div
				class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform hover:scale-105 flex-1"
			>
				<h2 class="text-2xl font-bold mb-2">You are leader in:</h2>
				<div class="flex flex-col">
					{#if projects.userLeadingProjects.length > 0}
						{#each projects.userLeadingProjects.slice(0, 3) as project (project.id)}
							<a
								href="#!"
								class="text-gray-700 mb-2 transition-all duration-500 border border-gray-200 p-2 rounded hover:border-teal-400 hover:bg-teal-200"
							>
								{project.name}
							</a>
						{/each}
						{#if projects.userLeadingProjects.length > 3}
							<button
								class="mt-2 bg-teal-400 text-white p-2 rounded hover:bg-teal-500 transition-all duration-500"
								>View All</button
							>
						{/if}
					{:else}
						<p class="text-gray-700">No projects found.</p>
					{/if}
				</div>
			</div>
		</div>
	</div>
{/if}

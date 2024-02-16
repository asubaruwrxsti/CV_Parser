<script lang="ts">
	/** @type {import('./$types').PageData} */
	export let data: any;
	import { onMount } from "svelte";
	import { browser } from "$app/environment";
	import { fade } from "svelte/transition";
	import { checkSession } from "../../../services/sessionManager";

	let isLoading = true;
	let project: any = [];

	onMount(async () => {
		try {
			let projectUrl =
				"http://localhost:8000/projects/" + data.props.data.id;
			let response = await fetch(projectUrl, {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
			});
			project = await response.json().then((data) => {
				console.log(data);
				data[0].image = "No-Image-Placeholder.svg.png";
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
	<div class="container mx-auto px-4 mt-6 flex">
		<div
			class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform flex-1 flex flex-row"
			in:fade={{ duration: 400 }}
		>
			<div class="w-2/3">
				{#each Object.keys(project[0]) as key (key)}
					{#if Array.isArray(project[key])}
						<h2 class="text-2xl font-bold text-gray-800">{key}:</h2>
					{:else if key !== "image"}
						{#if key === "participants"}
							<hr class="my-4" />
							<div class="flex">
								<div class="w-1/2">
									<h2 class="text-lg font-bold text-gray-800">
										{key.charAt(0).toUpperCase() +
											key.slice(1)}:
									</h2>
								</div>
								<div class="w-1/2">
									{#each project[0][key] as participant (participant)}
										{#each Object.keys(participant) as key (key)}
											<div class="flex items-center">
												<p
													class="text-lg text-gray-600 flex-grow"
												>
													{participant[key].name}
												</p>
											</div>
										{/each}
									{/each}
								</div>
							</div>
							<hr class="my-4" />
						{:else if key !== "id" && key !== "image"}
							<div class="flex items-center">
								<strong
									class="mr-16 flex-grow-0 flex-shrink-0 w-24"
								>
									{key.charAt(0).toUpperCase() +
										key.slice(1)}:
								</strong>
								<p class="text-lg text-gray-600 flex-grow">
									{project[0][key]}
								</p>
							</div>
						{/if}
					{/if}
				{/each}
			</div>
			{#each Object.keys(project[0]) as key (key)}
				{#if key === "image"}
					<div class="w-1/3 ml-16">
						<img
							class="w-full h-auto shadow-2xl scale-105"
							src="/No-Image-Placeholder.svg.png"
							alt={key}
						/>
					</div>
				{/if}
			{/each}
		</div>
	</div>
{/if}

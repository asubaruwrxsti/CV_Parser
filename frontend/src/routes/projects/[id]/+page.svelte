<script lang="ts">
	/** @type {import('./$types').PageData} */
	export let data: any;
	import { onMount } from "svelte";
	import { browser } from "$app/environment";
	import { checkSession } from "../../../services/sessionManager";

	let isLoading = true;
	let project: any = [];

	onMount(async () => {
		console.log(data.props.data.id);

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
{/if}

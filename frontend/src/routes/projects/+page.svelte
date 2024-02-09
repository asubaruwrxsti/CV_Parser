<script lang="ts">
    import { onMount } from "svelte";
    import Swup from "swup";

    let isLoading = true;
    let projects: any = [];

    onMount(async () => {
        const swup = new Swup();

        // TODO: Check if session exists, and has not expired
        if (!localStorage.getItem("session")) {
            window.location.href = "/login";
        }
		try{
			let projectUrl = "http://localhost:8000/projects/user";
			let response = await fetch(projectUrl, {
				method: "GET",
				headers: {
					"session": localStorage.getItem("session"),
				}
			});
            projects = await response.json().then((data) => {
                console.log(data)
            });
		} catch (error) {
            console.log(error);
        }

        setTimeout(() => {
            isLoading = false;
        }, 500);
    });
</script>

{#if isLoading}
	<div class="flex items-center justify-center min-h-screen transition-main">
		<div
			class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"
		></div>
	</div>
{:else}
	<div
		class="flex items-start justify-center min-h-screen transition-main"
		id="swup"
	>
		<div class="grid grid-cols-2 gap-16 mt-16">
			<div class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition duration-500 transform hover:scale-105">
				<h2 class="text-2xl font-bold mb-2">You are participant in:</h2>
				<p class="text-gray-700">This is a sample project name.</p>
			</div>
			<div class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition duration-500 transform hover:scale-105">
				<h2 class="text-2xl font-bold mb-2">You are leader in:</h2>
				<p class="text-gray-700">This is a sample participant.</p>
			</div>
		</div>
	</div>
{/if}


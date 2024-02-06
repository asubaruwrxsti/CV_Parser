<script lang="ts">
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";

	let isLoading = true;
	let showButtons = false;

	onMount(() => {
		setTimeout(() => {
			isLoading = false;
		}, 1000);
	});
</script>

<div class="h-screen flex">
	{#if isLoading}
		<div
			class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500 m-auto"
		></div>
	{:else}
		<div class="flex flex-row h-full w-full">
			<div class="h-full w-2/3">
				<img
					src="VIRNA-01.svg"
					alt="Project Logo"
					class="w-full h-full"
				/>
			</div>
            <div
                class="h-full w-1/3 bg-black text-white p-8 flex flex-col items-center justify-center"
				in:fade={{ duration: 500 }}
			>
                <div class="mb-4">
                    <h2 class="text-4xl">Welcome</h2>
                </div>
                <div class="flex flex-row items-center justify-center w-full">
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-10 rounded text-xl mr-4 transform transition duration-500 ease-in-out"
                        >Login</button
                    >
                    <button
                        class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-10 rounded text-xl transform transition duration-500 ease-in-out"
                        >Signup</button
                    >
                </div>
            </div>
		</div>
	{/if}
</div>

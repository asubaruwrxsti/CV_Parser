<script lang="ts">
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";
	import Modal from "../components/Modal.svelte";
	import LoginForm from "../components/LoginForm.svelte";
	import Swup from "swup";

	let isLoading = true;
	let showModal = false;
	let showLogin = false;

	onMount(() => {
		const swup = new Swup({
			containers: ["#swup"],
		});

		setTimeout(() => {
			isLoading = false;
		}, 500);
	});
</script>

<div class="h-screen flex transition-main" id="swup">
	{#if isLoading}
		<div
			class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500 m-auto"
		></div>
	{:else}
		<div class="flex flex-row h-full w-full">
			<div
				class="h-full md:w-1/2 lg:w-3/5 xl:w-3/5 p-16"
				in:fade={{ duration: 400 }}
			>
				<img
					src="VIRNA-01.svg"
					alt="Project Logo"
					class="w-full h-full"
				/>
			</div>
			<div
				class="h-full md:w-1/2 lg:w-2/5 xl:w-2/5 bg-black text-white p-8 flex flex-col items-center justify-center"
			>
				{#if showLogin}
					<LoginForm />
					<!-- Render LoginForm when showLogin is true -->
				{:else}
					<div in:fade={{ duration: 500 }}>
						<div class="mb-6">
							<h2 class="text-4xl">Welcome</h2>
						</div>
						<div
							class="flex flex-row items-center justify-center w-full"
						>
							<button
								class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-10 rounded text-xl mr-4 transform transition duration-500 ease-in-out"
								on:click={() => (showLogin = true)}
							>
								Login
							</button>
							<button
								class="bg-blue-500 hover:bg-blue-700 text-white py-2 px-10 rounded text-xl transform transition duration-500 ease-in-out"
								on:click={() => (showModal = true)}
								>Signup</button
							>
						</div>
					</div>
				{/if}
			</div>
		</div>
	{/if}
</div>
<div class="overlay transition-overlay"></div>

<Modal bind:showModal>
	<h2
		slot="header"
		class="text-2xl font-semibold mb-8 text-center text-blue-600"
	>
		Signup
	</h2>

	<div slot="body" class="mb-8 p-4 bg-gray-100 rounded shadow">
		<p class="text-lg text-gray-700 font-bold">
			Account creation is currently disabled.
		</p>
		<p class="text-lg text-gray-700">
			Please contact the site owner to create a new account.
		</p>
	</div>
</Modal>

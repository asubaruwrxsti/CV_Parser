<script lang="ts">
	import { onMount } from "svelte";
	import { fade } from "svelte/transition";
	import { browser } from "$app/environment";
	import { checkSession } from "../../services/sessionManager";
	import { fetchData } from "../../services/dataManager";
	import DataTable from "../../components/DataTable.svelte";

	import Modal from "../../components/Modal.svelte";
	import { Body } from "svelte-body";
	$: bodyStyle = {
		filter: showModal ? "blur(5px)" : "none",
	};

	// Loading state
	let isLoading = true;

	// Show modal state
	let showModal = false;

	// Participants data
	let participants: any = [];
	let headers: any = [];
	let dataLoaded = false;

	onMount(async () => {
		try {
			participants = await fetchData("participants").then((res) => {
				headers = Object.keys(res[0]);
				return res;
			});
			dataLoaded = true;
		} catch (error) {
			console.error(error);
		}
		console.log(participants);
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
					<h1 class="text-4xl font-bold">Participants</h1>
					<button
						class="bg-white text-teal-500 border border-teal-500 p-2 rounded shadow transition-all duration-500 hover:bg-teal-500 hover:text-white hover:shadow-lg hover:scale-105 transform-gpu flex items-center"
						on:click={() => (showModal = true)}
					>
						<span class="material-icons mr-2"> add </span>
						New Participant
					</button>
				</div>
                {#if dataLoaded}
                    <DataTable
                        data={participants}
                        hideableCols={headers.slice(2)}
                    />
                {/if}
			</div>
		</div>
	</div>
{/if}
<Body style={bodyStyle} />

<Modal bind:showModal showCloseButton={false}></Modal>

<script lang="ts">
	import Select from "svelte-select";
	import { postData } from "../services/dataManager";
	export let header: string;
	export let data: { key: string; projectID: number; value: any[] };
	export let showSaveButton: boolean = false;

	let selectedParticipants: any[] = data.value;

	// Load options for the select component
	async function loadOptions(name: string) {
		let response = await postData(
			"participants/search",
			"",
			JSON.stringify({ name }),
		);
		let options = await response.json();
		return options.map((applicant: any) => {
			return {
				value: applicant.id,
				label: applicant.name,
			};
		});
	}

	function handle(event: any) {
		if (showSaveButton) {
			selectedParticipants = event.detail;
			if (selectedParticipants === null) {
				selectedParticipants = [];
			}
		}
		console.log(selectedParticipants);
	}
</script>

<div class="mb-4">
	<label for={header} class="block text-gray-600 font-semibold mb-2"
		>{header.charAt(0).toUpperCase() + header.slice(1)}</label
	>
	<Select
		{loadOptions}
		multiple={true}
		name={header}
		value={data.value}
		on:input={handle}
	/>
</div>
{#if showSaveButton}
	<button
		class="mt-2 bg-teal-400 hover:bg-teal-700 text-white py-2 px-10 rounded text-xl transform transition duration-200 ease-in-out w-full"
		on:click={() => {
			postData(
				"projects",
				data.projectID,
				JSON.stringify({ [data.key]: selectedParticipants }),
				"PUT"
			);
		}}
	>
		Save
	</button>
{/if}

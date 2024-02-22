<script lang="ts">
	import Select from "svelte-select";
	export let header: string;
	export let data: { value: any[] };
	export let showSaveButton: boolean = false;

	// Load options for the select component
	async function loadOptions(name: string) {
		let applicantUrl = `http://localhost:8000/participants/search`;
		let response = await fetch(applicantUrl, {
			method: "POST",
			headers: {
				Authorization: `Bearer ${localStorage.getItem("session")}`,
			},
			body: JSON.stringify({ name: name }),
		});
		let options = await response.json();
		console.log(data);
		return options.map((applicant: any) => {
			return {
				value: applicant.id,
				label: applicant.name,
			};
		});
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
		items={data.value}
		value={data.value}
	/>
</div>
{#if showSaveButton}
	<button
		class="mt-2 bg-teal-400 hover:bg-teal-700 text-white py-2 px-10 rounded text-xl transform transition duration-200 ease-in-out w-full"
	>
		Save
	</button>
{/if}

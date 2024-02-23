<script lang="ts">
	export let header: string;
	export let showSaveButton: boolean = true;
	export let data: {
		projectID: string
	};
</script>

<div class="mb-4">
	<label for={header} class="block text-gray-600 font-semibold mb-2"
		>{header.charAt(0).toUpperCase() + header.slice(1)}</label
	>
	<input
		type="file"
		id={header}
		name={header}
		class="w-full p-10 border border-gray-300 rounded-xl"
	/>
</div>
{#if showSaveButton}
	<button
		class="mt-2 bg-teal-400 hover:bg-teal-700 text-white py-2 px-10 rounded text-xl transform transition duration-200 ease-in-out w-full"
	>
		Save
	</button>
{/if}

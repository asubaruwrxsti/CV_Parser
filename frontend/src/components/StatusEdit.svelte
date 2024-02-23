<script lang="ts">
	export let header: string;
	export let showSaveButton: boolean = true;
	export let data: {
		status: string;
	};
</script>

<div class="mb-4">
	<label
		for={header}
		class="block text-gray-600 font-semibold mb-2 {data.status === 'active'
			? 'text-green-500'
			: 'text-red-500'}"
	>
		{header.charAt(0).toUpperCase() + header.slice(1)}
	</label>
	<select
		bind:value={data.status}
		id={header}
		name={header}
		class="w-full p-2 border border-gray-300 rounded"
	>
		<option value="inactive">Inactive</option>
		<option value="active">Active</option>
	</select>
</div>
{#if showSaveButton}
	<button
		class="mt-2 bg-teal-400 hover:bg-teal-700 text-white py-2 px-10 rounded text-xl transform transition duration-200 ease-in-out w-full"
	>
		Save
	</button>
{/if}

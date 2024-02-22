<script lang="ts">
	import { createEventDispatcher } from "svelte";
	const dispatch = createEventDispatcher();

	export let header: string;
	export let data: {
		value: string[];
	};
	export let showSaveButton: boolean = false;

	let tags: string[] = data.value || [];
	let newTag = "";

	function addTag() {
		if (newTag) {
			tags = [...tags, newTag];
			newTag = "";
			dispatch("tagsUpdated", tags);
		}
	}

	function removeTag(tagToRemove: string) {
		tags = tags.filter((tag) => tag !== tagToRemove);
		dispatch("tagsUpdated", tags);
	}
</script>

<div class="mb-4">
	<label for={header} class="block text-gray-600 font-semibold mb-2">
		{header.charAt(0).toUpperCase() + header.slice(1)}
	</label>
	<div class="flex items-center justify-between">
		<input
			bind:value={newTag}
			type="text"
			placeholder="Enter tag"
			class="mr-2 border border-gray-300 rounded"
		/>
		<button
			type="button"
			class="bg-teal-500 text-white p-2 rounded-full hover:bg-teal-600 transition-all duration-500 flex items-center"
			on:click={addTag}
		>
			<span class="material-icons"> add </span>
		</button>
	</div>
	{#each tags as tag (tag)}
		<div
			class="tag mt-2 bg-teal-200 rounded px-3 py-1 text-sm text-blue-700 mr-2 mb-2 flex items-center inline-flex"
		>
			<span>{tag}</span>
			<button
				class="ml-2 bg-red-500 hover:bg-red-700 text-white rounded-full h-4 w-4 flex items-center justify-center"
				on:click={() => removeTag(tag)}
			>
				<span class="material-icons" style="font-size: 14px;">
					close
				</span>
			</button>
		</div>
	{/each}
</div>
{#if showSaveButton}
	<button
		class="mt-2 bg-teal-400 hover:bg-teal-700 text-white py-2 px-10 rounded text-xl transform transition duration-200 ease-in-out w-full"
	>
		Save
	</button>
{/if}

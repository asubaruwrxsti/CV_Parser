<script lang="ts">
	import { postData } from "../services/dataManager";
	import { toBase64 } from "../utils/utils";
	export let header: string;
	export let showSaveButton: boolean = true;
	export let data: {
		key: string;
		projectID: string;
	};

	async function postImage() {
		const fileField = document.getElementById(header) as HTMLInputElement;
		let file = new File([], "empty");
		if (fileField.files) {
			file = fileField.files[0];
		}
		const base64 = await toBase64(file);
		postData(
			"projects",
			data.projectID,
			JSON.stringify({ [data.key]: base64 }),
			"PUT",
		);
	}
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
		on:click={postImage}
	>
		Save
	</button>
{/if}

<script lang="ts">
	/** @type {import('./$types').PageData} */
	export let data: any;
	console.log(data);

	import { onMount } from "svelte";
	import { browser } from "$app/environment";
	import { fade } from "svelte/transition";
	import { checkSession } from "../../../services/sessionManager";
	import { parseJsonValues } from "../../../utils/utils";
	import { fetchData, postData } from "../../../services/dataManager";
	import type { ModalData, EditType } from "../../../interfaces/Interfaces";

	import { Body } from "svelte-body";

	import Modal from "../../../components/Modal.svelte";
	import ParticipantsSelect from "../../../components/ParticipantsSelect.svelte";
	import TorEdit from "../../../components/TOREdit.svelte";
	import ImageEdit from "../../../components/ImageEdit.svelte";
	import StatusEdit from "../../../components/StatusEdit.svelte";

	// Hidden fields
	let hiddenFields = ["id", "image"];

	// Project data
	let isLoading = true;
	let project: any = [];

	// Modal state
	let showModal = false;
	let modalData: ModalData = {
		title: "",
		body: {
			projectID: 0,
			key: "",
			value: "",
		},
		relatedComponent: "",
	};
	$: bodyStyle = {
		filter: showModal ? "blur(5px)" : "none",
	};

	// Editing
	let editingKey: string | null = null;
	let editedValue = "";

	$: rows = Math.ceil(editedValue.length / 80);

	let components: { [key: string]: any } = {
		ParticipantsSelect,
		TorEdit,
		ImageEdit,
		StatusEdit,
	};

	const editTypes: Record<string, EditType> = {
		tor: { title: "Terms of Reference", component: "TorEdit", key: "tor" },
		participants: {
			title: "Participants",
			component: "ParticipantsSelect",
			key: "participants",
		},
		image: { title: "Image", component: "ImageEdit", key: "image" },
		status: { title: "Status", component: "StatusEdit", key: "status" },
	};

	function startEditing(key: string) {
		if (key in editTypes) {
			startCustomEdit(key, editTypes[key]);
		} else {
			startDefaultEdit(key);
		}
	}

	function startCustomEdit(key: string, editType: EditType) {
		console.log(`Editing ${key}`);
		modalData = {
			title: editType.title,
			body: {
				projectID: data.props.data.id,
				key,
				value: project[key],
			},
			relatedComponent: editType.component,
		};
		showModal = true;
	}

	function startDefaultEdit(key: string) {
		editingKey = key;
		editedValue = project[key];
	}

	onMount(async () => {
		try {
			project = await fetchData("projects", data.props.data.id).then(
				(res) => {
					if (res.image) {
						res.image = "data:image/jpeg;base64," + res.image;
					}
					return parseJsonValues(res);
				},
			);
		} catch (error) {
			console.error(error);
		}
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
	<div class="container mx-auto px-4 mt-6 flex">
		<div
			class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform flex-1 flex flex-row"
			in:fade={{ duration: 400 }}
		>
			<div class="w-2/3">
				{#each Object.keys(project) as key (key)}
					{#if Array.isArray(project[key])}
						<hr class="my-4" />
						<div
							class="flex items-center relative group hover:bg-gray-300 rounded-lg p-2 transition-all duration-400"
						>
							<strong
								class="mr-16 flex-grow-0 flex-shrink-0 w-24"
							>
								{key.charAt(0).toUpperCase() + key.slice(1)}:
							</strong>
							{#each project[key] as item, index (index)}
								<div
									class="tag mt-2 bg-teal-200 rounded p-2 text-sm text-blue-700 mr-2 mb-2 flex items-center inline-flex justify-start"
								>
									<span>
										{typeof item === "object" &&
										item !== null &&
										!Array.isArray(item)
											? item.label
											: item}
									</span>
								</div>
							{/each}
							<button
								class="absolute right-0 mr-5 opacity-0 group-hover:opacity-100 transition-opacity duration-200 text-gray-600"
								on:click={() => startEditing(key)}
							>
								<!-- Replace with your Material icon -->
								<i
									class="material-icons hover:bg-black rounded-full p-1 transition-all duration-300 hover:text-white mt-2"
									>edit</i
								>
							</button>
						</div>
					{:else if !hiddenFields.includes(key)}
						<hr class="my-4" />
						<div
							class="flex items-center relative group hover:bg-gray-300 rounded-lg p-2 transition-all duration-400"
						>
							<strong class="mr-4 flex-grow-0 flex-shrink-0 w-24">
								{key.charAt(0).toUpperCase() + key.slice(1)}:
							</strong>
							{#if editingKey === key}
								<textarea
									bind:value={editedValue}
									class="text-lg text-gray-600 flex-grow rounded-lg pr-5"
									on:introend={() => {
										project[key] = editedValue;
									}}
									{rows}
								/>
							{:else}
								<p
									class="text-lg text-gray-600 flex-grow rounded-lg p-2"
								>
									{project[key]}
								</p>
							{/if}
							{#if editingKey === key}
								<div
									class="flex space-x-2 absolute right-0 opacity-0 p-5 group-hover:opacity-100 transition-all duration-200 transform"
								>
									<button
										class="material-icons hover:bg-black hover:text-white rounded-full p-2 transition-all duration-300 text-gray-600"
										on:click={() =>
											postData(
												"projects",
												data.props.data.id,
												JSON.stringify({
													[key]: editedValue,
												}),
											)}
									>
										save
									</button>
									<button
										class="material-icons hover:bg-black hover:text-white rounded-full p-2 transition-all duration-300 text-gray-600"
										on:click={() => (editingKey = null)}
									>
										cancel
									</button>
								</div>
							{:else}
								<button
									class="material-icons mr-5 absolute right-0 opacity-0 p-2 group-hover:opacity-100 transition-all duration-300 transform hover:bg-black hover:text-white rounded-full text-gray-600"
									on:click={() => startEditing(key)}
								>
									edit
								</button>
							{/if}
						</div>
					{/if}
				{/each}
			</div>
			{#each Object.keys(project) as key (key)}
				{#if key === "image"}
					<div
						class="w-1/3 ml-16 relative group flex justify-center items-start"
					>
						<div class="relative group">
							<img
								class="w-full h-auto shadow-2xl scale-105 rounded-lg blur-on-hover"
								src={project[key] !== null
									? project[key]
									: "/No-Image-Placeholder.svg.png"}
								alt={key}
							/>
							<div
								class="absolute inset-0 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity"
								on:click={() => startEditing(key)}
								on:keydown={(event) => {
									if (event.key === "Enter") startEditing(key);
								}}
								tabindex="0"
								role="button"
							>
								<button
									class="material-icons m-0 p-0 opacity-0 p-5 group-hover:opacity-100 transition-all duration-300 transform hover:bg-black hover:text-white rounded-full text-gray-600 text-6xl"
									>edit</button
								>
							</div>
						</div>
					</div>
				{/if}
			{/each}
		</div>
	</div>
{/if}

<Body style={bodyStyle} />

<Modal bind:showModal showCloseButton={false}>
	<h2
		slot="header"
		class="text-2xl font-semibold m-8 text-center text-black-600"
	>
		Edit {modalData.title}
	</h2>
	<div
		slot="body"
		class="w-full mb-8 mt-8 p-4 bg-gray-100 rounded shadow"
		style="width: 400px"
	>
		<svelte:component
			this={components[modalData.relatedComponent]}
			header={modalData.title}
			data={modalData.body}
			showSaveButton={true}
		/>
	</div>
</Modal>

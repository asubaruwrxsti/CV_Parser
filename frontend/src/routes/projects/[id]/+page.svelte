<script lang="ts">
	/** @type {import('./$types').PageData} */
	export let data: any;
	import { onMount } from "svelte";
	import { browser } from "$app/environment";
	import { fade } from "svelte/transition";
	import { checkSession } from "../../../services/sessionManager";
	import { parseJsonValues } from "../../../utils/utils";
	import Modal from "../../../components/Modal.svelte";
	import { Body } from "svelte-body";

	// Hidden fields
	let hiddenFields = ["id", "image"];

	// Data mapping
	let dataMap = {
		"tor": "tag",
		"participants": "select",
	};

	// Project data
	let isLoading = true;
	let project: any = [];

	// Modal state
	let showModal = false;
	$: bodyStyle = {
		filter: showModal ? "blur(5px)" : "none",
	};

	// Editing
	let editingKey: string | null = null;
	let editedValue = "";
	$: rows = Math.ceil(editedValue.length / 80);

	function handleEdit(key: string) {
		console.log(`Editing ${key}`);
		editingKey = key;
		editedValue = project[key];
	}

	async function handleSave(key: string) {
		console.log(`Saving ${key}`);
		if (editingKey === key) {
			// Save logic here
			fetch(`http://localhost:8000/projects/${project.id}`, {
				method: "PUT",
				headers: {
					"Content-Type": "application/json",
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
				body: JSON.stringify({
					[key]: editedValue,
				}),
			})
				.then((response) => {
					if (response.status === 200) {
						window.location.reload();
					}
				})
				.catch((error) => {
					console.log(error);
				});
		}
	}

	onMount(async () => {
		try {
			let projectUrl = `http://localhost:8000/projects/${data.props.data.id}`;
			let response = await fetch(projectUrl, {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
			});
			project = await response.json().then((data) => {
				if (data.image) {
					data.image = "data:image/jpeg;base64," + data.image;
				}
				data = parseJsonValues(data);
				console.log(data);
				return data;
			});
		} catch (error) {
			console.log(error);
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
						<div class="flex items-center">
							<strong
								class="mr-16 flex-grow-0 flex-shrink-0 w-24"
							>
								{key.charAt(0).toUpperCase() + key.slice(1)}:
							</strong>
							{#each project[key] as item, index (index)}
								<div
									class="tag mt-2 bg-teal-200 rounded px-3 py-1 text-sm text-blue-700 mr-2 mb-2 flex items-center inline-flex justify-start"
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
									class="text-lg text-gray-600 flex-grow rounded-lg pr-5"
								>
									{project[key]}
								</p>
							{/if}
							{#if editingKey === key}
								<div
									class="flex space-x-2 absolute right-0 opacity-0 p-5 group-hover:opacity-100 transition-all duration-200 transform group-hover:-translate-y-1"
								>
									<button
										class="material-icons"
										on:click={() => handleSave(key)}
									>
										save
									</button>
									<button
										class="material-icons"
										on:click={() => (editingKey = null)}
									>
										cancel
									</button>
								</div>
							{:else}
								<button
									class="material-icons absolute right-0 opacity-0 p-5 group-hover:opacity-100 transition-all duration-200 transform group-hover:-translate-y-1"
									on:click={() => handleEdit(key)}
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
					{#if project[key] !== null}
						<div class="w-1/3 ml-16">
							<img
								class="w-full h-auto shadow-2xl scale-105 rounded-lg"
								src={project[key]}
								alt={key}
							/>
						</div>
					{:else}
						<div class="w-1/3 ml-16">
							<img
								class="w-full h-auto shadow-2xl scale-105 rounded-lg"
								src="/No-Image-Placeholder.svg.png"
								alt={key}
							/>
						</div>
					{/if}
				{/if}
			{/each}
		</div>
	</div>
{/if}

<Body style={bodyStyle} />

<Modal bind:showModal showCloseButton={false}></Modal>

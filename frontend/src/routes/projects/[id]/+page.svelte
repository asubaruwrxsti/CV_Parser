<script lang="ts">
	/** @type {import('./$types').PageData} */
	export let data: any;
	import { onMount } from "svelte";
	
	let projects: any = [];

	onMount(async () => {
		console.log(data.props.data.id);

		try {
			let projectUrl = "http://localhost:8000/projects/" + data.props.data.id;
			let response = await fetch(projectUrl, {
				method: "GET",
				headers: {
					Authorization: `Bearer ${localStorage.getItem("session")}`,
				},
			});
			projects = await response.json().then((data) => {
				console.log(data);
			});
		} catch (error) {
			console.log(error);
		}
	});
</script>

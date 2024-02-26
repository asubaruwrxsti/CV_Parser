<script>
	import Footer from "../../components/Footer.svelte";
	import Navbar from "../../components/Navbar.svelte";
</script>

<Navbar />
<div class="app">
	<main>
		<slot />
	</main>
</div>
<Footer />

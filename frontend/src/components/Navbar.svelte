<script lang="ts">
    import { Navbar, NavBrand, NavLi, NavUl, Skeleton } from "flowbite-svelte";

    import { onMount } from "svelte";

    let routes: any;

    onMount(async () => {
        let url = "http://localhost:8000/routing/routes";
        try {
            const response = await fetch(url, { method: "GET" });
            routes = await response.json();
            console.log(routes);
        } catch (error) {
            console.log(error);
        }
    });
</script>

<Navbar>
    <NavBrand href="/">
        <img
            src="/VIRNA-min.png"
            class="me-3 h-16 clip-image"
            alt="Flowbite Logo"
        />
    </NavBrand>
    <NavUl>
        {#if routes}
            {#each routes as route}
                <NavLi href='/{route}' class="hover:text-purple-500">
                    {route}
                </NavLi>
            {/each}
        {:else}
        {/if}
    </NavUl>
</Navbar>

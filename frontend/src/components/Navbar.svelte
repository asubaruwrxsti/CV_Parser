<script lang="ts">
    import { Navbar, NavBrand, NavLi, NavUl, Skeleton } from "flowbite-svelte";

    import { onMount } from "svelte";

    let routes: any = [];
    let isLoading = true;

    onMount(async () => {
        let url = "http://localhost:8000/routing/routes";
        try {
            const response = await fetch(url, { method: "GET" });
            routes = await response.json().then((data) => {
                return data.routes;
            });
            isLoading = false;
        } catch (error) {
            console.log(error);
        }
    });
</script>

{#if isLoading}
    <Navbar>
        <NavBrand href="/">
            <img
                src="/VIRNA-min.png"
                class="me-3 h-16 clip-image"
                alt="Flowbite Logo"
            />
        </NavBrand>
    </Navbar>
{:else}
    <Navbar>
        <NavBrand href="/">
            <img
                src="/VIRNA-min.png"
                class="me-3 h-16 clip-image"
                alt="Flowbite Logo"
            />
        </NavBrand>
        <NavUl>
            <NavLi href="/">Home</NavLi>
            {#each routes as route}
                <NavLi href="/{route}">
                    {route.charAt(0).toUpperCase() + route.slice(1)}
                </NavLi>
            {/each}
            <NavLi href="/">Profile</NavLi>
        </NavUl>
    </Navbar>
{/if}

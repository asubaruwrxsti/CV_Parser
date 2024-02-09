<script lang="ts">
  import { Navbar, NavBrand, NavLi, NavUl, NavHamburger, Avatar, Dropdown, DropdownItem, DropdownHeader, DropdownDivider } from 'flowbite-svelte';

    import { onMount } from "svelte";

    let routes: any = [];
    let isLoading = true;
	let browserTheme = "";

    onMount(async () => {
        let url = "http://localhost:8000/routing/routes";
        try {
            const response = await fetch(url, { method: "GET" });
            routes = await response.json().then((data) => {
                return data.routes;
            });
            isLoading = false;

			// TODO: Dark light theme
			if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
				browserTheme = "black text-white"
			} else {
				browserTheme = "white text-black"
			}

        } catch (error) {
            console.log(error);
        }
    });
</script>

{#if isLoading}
	<Navbar rounded color="form">
        <NavBrand href="/">
            <img
                src="/VIRNA-min.png"
                class="me-3 h-16 clip-image"
                alt="Flowbite Logo"
            />
        </NavBrand>
    </Navbar>
{:else}
    <Navbar class="bg-{browserTheme}">
        <NavBrand href="/">
            <img
                src="/VIRNA-min.png"
                class="me-3 h-16 clip-image"
                alt="Flowbite Logo"
            />
        </NavBrand>
		<div class="flex items-center md:order-2">
			<Avatar id="avatar-menu" src="/defaultavatar/Male-Default.png" />
			<NavHamburger class1="w-full md:flex md:w-auto md:order-1" />
		</div>
		<Dropdown placement="bottom" triggeredBy="#avatar-menu">
			<DropdownHeader>
				<span class="block text-sm">Bonnie Green</span>
				<span class="block truncate text-sm font-medium">name@flowbite.com</span>
			</DropdownHeader>
			<DropdownItem>Profile</DropdownItem>
			<DropdownItem>Settings</DropdownItem>
			<DropdownDivider />
			<DropdownItem>Sign out</DropdownItem>
		</Dropdown>
        <NavUl>
            <NavLi href="/" nonActiveClass="text-white hover:text-gray-400 transition-colors duration-200">
				Home
			</NavLi>
            {#each routes as route}
                <NavLi href="/{route}" nonActiveClass="text-white hover:text-gray-400 transition-colors duration-200">
                    {route.charAt(0).toUpperCase() + route.slice(1)}
                </NavLi>
            {/each}
        </NavUl>
    </Navbar>
{/if}

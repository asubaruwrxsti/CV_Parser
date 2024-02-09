<script lang="ts">
    import { onMount } from "svelte";
    import Swup from "swup";

    let isLoading = true;

    onMount(() => {
        const swup = new Swup();

        // TODO: Check if session exists, and has not expired
        // if (!localStorage.getItem("session")) {
        //     window.location.href = "/dashboard";
        // }

        setTimeout(() => {
            isLoading = false;
        }, 500);
    });
</script>

<div
    class="flex items-center justify-center min-h-screen transition-main"
    id="swup"
>
    {#if isLoading}
        <div
            class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"
        ></div>
    {:else}
        DASHBOARDDDDDDDD
    {/if}
</div>

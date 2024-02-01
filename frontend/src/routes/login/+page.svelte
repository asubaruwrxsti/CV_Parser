<script lang="ts">
    import { onMount } from "svelte";
    import LoginForm from "../../components/LoginForm.svelte";

    let isLoading = true;

    onMount(() => {
        setTimeout(() => {
            isLoading = false;
        }, 1000);
    });
</script>

<div class="flex items-center justify-center min-h-screen">
    {#if isLoading}
        <div
            class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"
        ></div>
    {:else}
        <LoginForm />
    {/if}
</div>

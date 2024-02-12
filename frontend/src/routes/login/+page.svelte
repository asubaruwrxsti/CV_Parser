<script lang="ts">
    import { browser } from "$app/environment";
    import { checkSession } from "../../services/sessionManager";
    import LoginForm from "../../components/LoginForm.svelte";

    let isLoading = true;

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

<div
    class="flex items-center justify-center min-h-screen transition-main"
    id="swup"
>
    {#if isLoading}
        <div
            class="animate-spin rounded-full h-32 w-32 border-t-2 border-b-2 border-purple-500"
        ></div>
    {:else}
        <LoginForm />
    {/if}
</div>

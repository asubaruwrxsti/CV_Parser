<script lang="ts">
    import { onMount } from "svelte";
    import { checkSession } from "../../services/sessionManager";
    import { browser } from "$app/environment";

    let isLoading = true;
    let dashboard: any = [];

    onMount(async () => {
        try {
            let dashboardUrl = "http://localhost:8000/dashboard/";
            let response = await fetch(dashboardUrl, {
                method: "GET",
                headers: {
                    Authorization: `Bearer ${localStorage.getItem("session")}`,
                },
            });
            dashboard = await response.json().then((data) => {
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
    <div
        class="flex flex-wrap justify-center items-start transition-main"
        id="swup"
    >
        <div class="flex flex-wrap justify-between items-start mt-16 gap-16">
            <div
                class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform hover:scale-105 flex-1"
            >
                <h2 class="text-2xl font-bold mb-2">You are leader in:</h2>
                <div class="flex flex-col">
                </div>
            </div>
        </div>
    </div>
{/if}

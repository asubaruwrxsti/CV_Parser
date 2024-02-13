<script lang="ts">
    import { onMount } from "svelte";
	import { fade } from "svelte/transition";
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
		in:fade={{ duration: 400 }}
    >
        <div class="flex flex-wrap justify-center items-start mt-16 gap-16">
            <!-- Render all cards -->
            {#each Object.keys(dashboard) as key}
                <div
                    class="bg-white rounded-2xl shadow-2xl p-20 hover:shadow-white transition-all duration-500 transform w-1/3 {key.startsWith(
                        'all_',
                    )
                        ? ''
                        : 'hover:scale-105'}"
                    style={key.startsWith("all_") ? "width: 90%" : ""}
                >
                    <!-- Card title -->
                    <h2 class="text-2xl font-bold mb-6">
                        {key
                            .split("_")
                            .map(
                                (part) =>
                                    part.charAt(0).toUpperCase() +
                                    part.slice(1),
                            )
                            .join(" ")}
                    </h2>
                    <!-- Card Content -->
                    <div class="flex flex-col">
                        <!-- If key name is all_, render as table -->
                        {#if key.startsWith("all_")}
                            <div class="flex justify-center">
                                <table
                                    class="w-full lg:w-4/5 mx-auto w-full"
                                >
                                    <thead>
                                        <tr>
                                            {#each Object.keys(dashboard[key][0]) as tableKey}
                                                {#if tableKey !== "id"}
                                                    <th
                                                        class="bg-gray-200 text-gray-600 border border-gray-300 px-4 py-2"
                                                    >
                                                        {tableKey
                                                            .split("_")
                                                            .map(
                                                                (part) =>
                                                                    part
                                                                        .charAt(
                                                                            0,
                                                                        )
                                                                        .toUpperCase() +
                                                                    part.slice(
                                                                        1,
                                                                    ),
                                                            )
                                                            .join(" ").toUpperCase()}
                                                    </th>
                                                {/if}
                                            {/each}
                                            <th
                                                class="bg-gray-200 text-gray-600 border border-gray-300 px-4 py-2"
                                            >
                                                ACTIONS
                                            </th>
                                        </tr>
                                    </thead>
                                    <tbody>
                                        {#each dashboard[key].slice(0, 4) as item, index (item.id)}
                                            <tr>
                                                {#each Object.keys(item) as key}
                                                    {#if key !== "id"}
                                                        <td
                                                            class="border border-gray-300 px-4 py-2"
                                                        >
                                                            {item[key]}
                                                        </td>
                                                    {/if}
                                                {/each}
                                                <td
                                                    class="border border-gray-300 px-4 py-2"
                                                >
                                                    <div
                                                        class="flex justify-center"
                                                    >
                                                        <a
                                                            href={`/dashboard/${key}/${item.id}`}
                                                            class="bg-teal-400 text-white p-2 rounded hover:bg-teal-500 transition-all duration-500"
                                                        >
                                                            View
                                                        </a>
                                                    </div>
                                                </td>
                                            </tr>
                                        {/each}
                                    </tbody>
                                </table>
                            </div>
                        {:else}
                            <!-- Else, render as flex div -->
                            {#each dashboard[key] as item, index (item.id)}
                                {#if index < 3}
                                    <div class="flex flex-wrap">
                                        {#each Object.keys(item) as key}
                                            {#if key !== "id" && item[key] !== null}
                                                <div
                                                    class="flex flex-col mb-4 mr-4"
                                                >
                                                    <span class="text-gray-500">
                                                        {key
                                                            .split("_")
                                                            .map(
                                                                (part) =>
                                                                    part
                                                                        .charAt(
                                                                            0,
                                                                        )
                                                                        .toUpperCase() +
                                                                    part.slice(
                                                                        1,
                                                                    ),
                                                            )
                                                            .join(" ")}
                                                    </span>
                                                    <span
                                                        class="text-lg font-bold"
                                                        >{item[key]}</span
                                                    >
                                                </div>
                                            {/if}
                                        {/each}
                                    </div>
                                {/if}
                            {/each}
                        {/if}
                        <!-- View all button -->
                        {#if dashboard[key].length > 3}
                            <div
                                style="display: flex; justify-content: center;"
                            >
                                <a
                                    href={`/dashboard/${key}`}
                                    class="mt-6 bg-teal-400 text-white p-2 rounded hover:bg-teal-500 transition-all duration-500 text-center"
                                    style={key.startsWith("all_")
                                        ? "width: 30%"
                                        : "width: 60%"}
                                >
                                    View All
                                </a>
                            </div>
                        {/if}
                    </div>
                </div>
            {/each}
        </div>
    </div>
{/if}

<script>
    import { slide } from "svelte/transition";
    import { cubicOut } from "svelte/easing";

    let username = "";
    let password = "";

    function handleLogin() {
        let form = new FormData();
        form.append("username", username);
        form.append("password", password);

        let url = "http://localhost:8000/auth/login";
        fetch(url, {
            method: "POST",
            body: form,
        })
            .then((response) => response.json())
            .then((data) => {
                if (data.token) {
                    localStorage.setItem("session", JSON.stringify(data["token"], data["session_id"]));
                    window.location.href = "/dashboard";
                }
            })
            .catch((error) => {
                console.log(error);
            });
    }
</script>

<div
    class="bg-white p-6 rounded-lg shadow-md"
    in:slide={{ delay: 100, duration: 500, easing: cubicOut }}
>
    <div class="flex items-center justify-center text-center">
        <span class="material-icons text-6xl mr-2">account_circle</span>
        <h2 class="text-3xl text-gray-900">Sign in to your account</h2>
    </div>
    <form class="mt-8 space-y-6" on:submit|preventDefault={handleLogin}>
        <input type="hidden" name="remember" value="true" />
        <div class="rounded-md shadow-sm -space-y-px">
            <div class="mb-2">
                <label for="userame" class="sr-only">Username</label>
                <input
                    bind:value={username}
                    id="username"
                    name="username"
                    class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-t-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm hover:border-indigo-500 transition"
                    placeholder="Username"
                />
            </div>
            <div>
                <label for="password" class="sr-only">Password</label>
                <input
                    bind:value={password}
                    id="password"
                    name="password"
                    type="password"
                    required
                    class="appearance-none rounded-none relative block w-full px-3 py-2 border border-gray-300 placeholder-gray-500 text-gray-900 rounded-b-md focus:outline-none focus:ring-indigo-500 focus:border-indigo-500 focus:z-10 sm:text-sm hover:border-indigo-500 transition"
                    placeholder="Password"
                />
            </div>
        </div>

        <div>
            <button
                type="submit"
                class="group relative w-full flex justify-center py-2 px-4 border border-transparent text-sm font-medium rounded-md text-white bg-blue-500 hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-blue-400 transition-colors duration-200"
            >
                Sign in
            </button>
        </div>
    </form>
</div>

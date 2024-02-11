// sessionManager.ts
export function getSession() {
    return localStorage.getItem("session");
}

export function setSession(session: string) {
    localStorage.setItem("session", session);
}

export function removeSession() {
    localStorage.removeItem("session");
}

export async function checkSession() {
    const session = getSession();
    if (!session) return false;

    const res = await fetch("/auth/me", {
        method: "GET",
        headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${session}`,
        },
    });

    if (res.status === 200) {
        return true;
    } else {
        removeSession();
        return false;
    }
}
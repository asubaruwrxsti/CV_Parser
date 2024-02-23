export async function fetchData(property: string, id: number | string = "") {
	console.log("fetchData", property, id);
	let response = await fetch(`http://localhost:8000/${property}/${id}`, {
		method: "GET",
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${localStorage.getItem("session")}`,
		},
	});
	return response.json();
}

export function postData(property: string, id: number | string = "", data: any, type: string = "POST") {
	return fetch(`http://localhost:8000/${property}/${id}`, {
		method: type,
		headers: {
			"Content-Type": "application/json",
			Authorization: `Bearer ${localStorage.getItem("session")}`,
		},
		body: data,
	});
}
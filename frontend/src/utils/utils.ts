// Truncate text
export function truncate(text: string, length: number) {
	if (text === null || text === undefined) {
		return "";
	}
	return text.length > length ? text.substring(0, length) + "..." : text;
}

// Check if JSON is valid
export function isJson(str: string) {
	try {
		if (str === null || str === undefined) {
			return false;
		}
		let parsed=JSON.parse(str);
		console.log(parsed);
	} catch (e) {
		return false;
	}
	return true;
}
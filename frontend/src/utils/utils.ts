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

		if (Number.isInteger(str)) {
			return false;
		}

		JSON.parse(str);
	} catch (e) {
		return false;
	}
	return true;
}

// JSON parse
export function parseJsonValues(obj: any) {
    for (let key in obj) {
        if (typeof obj[key] === 'string') {
            try {
                obj[key] = JSON.parse(obj[key]);
            } catch (e) {
                // Not a JSON string, do nothing
            }
        } else if (typeof obj[key] === 'object' && obj[key] !== null) {
            // Recurse into the object
            obj[key] = parseJsonValues(obj[key]);
        }
    }
    return obj;
}
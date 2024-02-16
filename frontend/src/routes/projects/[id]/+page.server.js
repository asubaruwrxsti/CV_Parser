import { error } from '@sveltejs/kit';
/** @type {import('./$types').PageServerLoad} */ export async function load({ params }) {
	// TODO: error if product not found

	return {
		props: {
			// @ts-ignore
			data: params,
		}
	};
};
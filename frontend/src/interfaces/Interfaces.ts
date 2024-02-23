export interface ModalData {
	title: string;
	body: {
		projectID: number;
		key: string;
		value: any;
	};
	relatedComponent: string;
}

export type EditType = {
	key: string;
	title: string;
	component: string;
};
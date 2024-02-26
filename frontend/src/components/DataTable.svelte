<script lang="ts">
	export let property: string;

	import { fetchData } from "../services/dataManager";
	import { createTable, Render, Subscribe } from "svelte-headless-table";
	import { readable } from "svelte/store";
	import * as Table from "$lib/components/ui/table";

	import { addPagination } from "svelte-headless-table/plugins";
	import { Button } from "$lib/components/ui/button";

	let data: any = [];
	let headers: any = [];
	let table: any;
	let columns: any;

	let headerRows: any;
	let pageRows: any;
	let tableAttrs: any;
	let tableBodyAttrs: any;
	let pluginStates: any;

	let hasNextPage: boolean;
	let hasPreviousPage: boolean;
	let pageIndex: number;

	async function loadData() {
		data = await fetchData(property);
		headers = Object.keys(data[0]);
		table = createTable(readable(data), {
			page: addPagination(),
		});
		columns = table.createColumns(
			Object.keys(data[0]).map((key) => {
				return table.column({
					accessor: key,
					header: key,
				});
			}),
		);
		({ headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } =
			table.createViewModel(columns));

		({ hasNextPage, hasPreviousPage, pageIndex } = pluginStates.page);
	}

	loadData();
</script>

{#if headerRows && pageRows}
	<div class="rounded-md border">
		<Table.Root {...$tableAttrs}>
			<Table.Header>
				{#each $headerRows as headerRow}
					<Subscribe rowAttrs={headerRow.attrs()}>
						<Table.Row>
							{#each headerRow.cells as cell (cell.id)}
								<Subscribe
									attrs={cell.attrs()}
									let:attrs
									props={cell.props()}
								>
									<Table.Head>
										<Render of={cell.render()} />
									</Table.Head>
								</Subscribe>
							{/each}
						</Table.Row>
					</Subscribe>
				{/each}
			</Table.Header>
			<Table.Body {...$tableBodyAttrs}>
				{#each $pageRows as row (row.id)}
					<Subscribe rowAttrs={row.attrs()} let:rowAttrs>
						<Table.Row>
							{#each row.cells as cell (cell.id)}
								<Subscribe attrs={cell.attrs()} let:attrs>
									<Table.Cell>
										<Render of={cell.render()} />
									</Table.Cell>
								</Subscribe>
							{/each}
						</Table.Row>
					</Subscribe>
				{/each}
			</Table.Body>
		</Table.Root>
	</div>
	<div class="flex items-center justify-end space-x-4 py-4">
		<Button
			variant="outline"
			size="sm"
			on:click={() => ($pageIndex = $pageIndex - 1)}
			disabled={!$hasPreviousPage}>Previous</Button
		>
		<Button
			variant="outline"
			size="sm"
			disabled={!$hasNextPage}
			on:click={() => ($pageIndex = $pageIndex + 1)}>Next</Button
		>
	</div>
{:else}
	<p>Loading...</p>
{/if}

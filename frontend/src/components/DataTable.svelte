<script lang="ts">
	export let property: string;

	import { fetchData } from "../services/dataManager";
	import {
		createTable,
		Render,
		Subscribe,
		createRender,
	} from "svelte-headless-table";
	import { readable } from "svelte/store";
	import * as Table from "$lib/components/ui/table";
	import DataTableActions from "./DataTableActions.svelte";
	import ArrowUpDown from "lucide-svelte/icons/arrow-up-down";

	import {
		addPagination,
		addSortBy,
		addTableFilter,
	} from "svelte-headless-table/plugins";
	import { Button } from "$lib/components/ui/button";
	import { Input } from "$lib/components/ui/input";

	let data: any = [];
	let headers: any = [];
	let table: any;
	let columns: any;

	let headerRows: any;
	let pageRows: any;
	let tableAttrs: any;
	let tableBodyAttrs: any;
	let pluginStates: any;
	let filterValue: any;

	let hasNextPage: any;
	let hasPreviousPage: any;
	let pageIndex: any;

	async function loadData() {
		data = await fetchData(property);
		headers = Object.keys(data[0]);
		headers.push(" ");
		table = createTable(readable(data), {
			page: addPagination(),
			sort: addSortBy(),
			filter: addTableFilter({
				fn: ({ filterValue, value }) =>
					value.toLowerCase().includes(filterValue.toLowerCase()),
			}),
		});

		function createColumn(key: string) {
			return table.column({
				accessor: key,
				header: key.charAt(0).toUpperCase() + key.slice(1),
				cell:
					key === " "
						? ({ value }) =>
								createRender(DataTableActions, { id: value })
						: undefined,
			});
		}

		columns = table.createColumns(headers.map(createColumn));
		({ headerRows, pageRows, tableAttrs, tableBodyAttrs, pluginStates } =
			table.createViewModel(columns));

		({ hasNextPage, hasPreviousPage, pageIndex } = pluginStates.page);
		filterValue = pluginStates.filter;
	}

	loadData();
</script>

{#if headerRows && pageRows}
	<div>
		<div class="flex items-center py-4">
			<Input
				class="max-w-sm"
				placeholder="Filter emails..."
				type="text"
				bind:value={$filterValue}
			/>
		</div>
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
										let:props
									>
										<Table.Head {...attrs}>
											{#if cell.id === " "}
												<div class="text-right">
													<Render
														of={cell.render()}
													/>
												</div>
											{:else if cell.id === "name"}
												<Button
													variant="ghost"
													on:click={props.sort.toggle}
												>
													<Render
														of={cell.render()}
													/>
													<ArrowUpDown
														class={"ml-2 h-4 w-4"}
													/>
												</Button>
											{:else}
												<Render of={cell.render()} />
											{/if}
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
											{#if cell.id === " "}
												<div class="text-right">
													<Render
														of={cell.render()}
													/>
												</div>
											{:else}
												<Render of={cell.render()} />
											{/if}
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
	</div>
{:else}
	<p>Loading...</p>
{/if}

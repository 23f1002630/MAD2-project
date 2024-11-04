<template>
    <div id="app">
        <ProviderBar />
        <div class="container">
            <section>
                <h2>Today Services</h2>
                <DataTable :value="todayServices" class="p-datatable-striped">
                    <Column field="id" header="ID"></Column>
                    <Column field="customerName" header="Customer Name"></Column>
                    <Column field="phone" header="Phone"></Column>
                    <Column field="location" header="Location"></Column>
                    <Column header="Action">
                        <template #body>
                            <Button label="Accept" class="p-button-success p-mr-2" />
                            <Button label="Reject" class="p-button-danger" />
                        </template>
                    </Column>
                </DataTable>
            </section>

            <section>
                <h2>Closed Services</h2>
                <DataTable :value="closedServices" class="p-datatable-striped">
                    <Column field="id" header="ID"></Column>
                    <Column field="customerName" header="Customer Name"></Column>
                    <Column field="phone" header="Phone"></Column>
                    <Column field="location" header="Location"></Column>
                    <Column field="date" header="Date"></Column>
                    <Column field="rating" header="Rating"></Column>
                </DataTable>
            </section>
        </div>
    </div>
</template>

<script>
import ProviderBar from '../components/ProviderBar.vue';
import { DataTable, Column, Button } from 'primevue';

export default {
    name: 'ProviderDash',
    components: {
        ProviderBar,
        DataTable,
        Column,
        Button
    },
    data() {
        return {
            todayServices: [
                { id: 1, customerName: 'John Doe', phone: '123-456-7890', location: 'New York' }
            ],
            closedServices: [
                { id: 1, customerName: 'Jane Smith', phone: '987-654-3210', location: 'Los Angeles', date: '2023-10-01', rating: 5 }
            ]
        };
    }
};
</script>

<style>
.container {
    margin-top: 20px;
}

h2 {
    margin-top: 20px;
    font-weight: bold;
}
</style>
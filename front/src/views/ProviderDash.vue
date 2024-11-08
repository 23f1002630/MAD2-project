<template>
    <div id="app" class="container my-5">
        <ProviderBar />

        <div class="card p-4 mb-4 container">
            <h3 class="text-center text-primary mb-4">Today Services</h3>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Phone</th>
                        <th>Location</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in todayServices" :key="service.id">
                        <td>{{ service.id }}</td>
                        <td>{{ service.customerName }}</td>
                        <td>{{ service.phone }}</td>
                        <td>{{ service.location }}</td>
                        <td>
                            <button class="btn btn-primary btn-sm me-2">Approve</button>
                            <button class="btn btn-primary btn-sm me-2">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="card p-4">
            <h3 class="text-center text-primary mb-4">Closed Services</h3>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Phone</th>
                        <th>Location</th>
                        <th>Date</th>
                        <th>Rating</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in closedServices" :key="service.id">
                        <td>{{ service.id }}</td>
                        <td>{{ service.customerName }}</td>
                        <td>{{ service.phone }}</td>
                        <td>{{ service.location }}</td>
                        <td>{{ service.date }}</td>
                        <td>{{ service.rating }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import ProviderBar from '../components/ProviderBar.vue';

export default {
    name: 'ProviderDash',
    components: {
        ProviderBar
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

.card {
    margin-bottom: 20px;
}

h3 {
    margin-top: 20px;
    font-weight: bold;
}

.table th,
.table td {
    vertical-align: middle;
}

.btn {
    margin-right: 5px;
}
</style>
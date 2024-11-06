<template>
    <div class="container my-5">
        <CustomerBar />
        <div class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Services</h3>
            <div class="d-flex justify-content-around flex-wrap">
                <button class="btn btn-outline-primary m-2">Cleaning Services</button>
                <button class="btn btn-outline-primary m-2">Maintenance and Repair</button>
                <button class="btn btn-outline-primary m-2">Landscaping and Gardening</button>
                <button class="btn btn-outline-primary m-2">Pest Control</button>
                <button class="btn btn-outline-primary m-2">Home Improvement and Renovation</button>
                <button class="btn btn-outline-primary m-2">Security and Safety</button>
                <button class="btn btn-outline-primary m-2">Moving and Storage</button>
                <button class="btn btn-outline-primary m-2">Specialty Services</button>
                <button class="btn btn-outline-primary m-2">Organizing and Decluttering</button>
                <button class="btn btn-outline-primary m-2">Pet Services</button>
            </div>
        </div>

        <div class="card mt-4 p-4">
            <h4 class="mb-3">Service History</h4>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Service Name</th>
                        <th>Professional Name</th>
                        <th>Phone</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td>1</td>
                        <td>Cleaning Services</td>
                        <td>John Doe</td>
                        <td>123-456-7890</td>
                        <td><span class="badge bg-warning text-dark">Close it?</span></td>
                    </tr>
                    <tr>
                        <td>2</td>
                        <td>Maintenance and Repair</td>
                        <td>Jane Smith</td>
                        <td>987-654-3210</td>
                        <td><span class="badge bg-success text-white">Closed</span></td>
                    </tr>
                    <tr>
                        <td>3</td>
                        <td>Landscaping and Gardening</td>
                        <td>Mike Johnson</td>
                        <td>555-555-5555</td>
                        <td><span class="badge bg-info text-white">Requested</span></td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import CustomerBar from '../components/CustomerBar.vue';
export default {
    name: 'CustomerDash',
    components: {
        CustomerBar
    }
};
</script>

<style>
body {
    font-family: 'Comic Sans MS', cursive, sans-serif;
}

.card {
    border-radius: 10px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.btn {
    font-size: 1rem;
    padding: 0.5rem 1rem;
}

.table th,
.table td {
    vertical-align: middle;
}

.badge {
    padding: 0.5em 1em;
    border-radius: 5px;
}
</style>
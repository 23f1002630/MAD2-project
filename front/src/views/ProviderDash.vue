<template>
    <div v-if="isProvider" id="app" class="container my-5">
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
                            <button class="btn btn-primary btn-sm me-2"
                                @click="approveService(service.id)">Approve</button>
                            <button class="btn btn-primary btn-sm me-2"
                                @click="rejectService(service.id)">Reject</button>
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
    <div v-else>
        <p>Unauthorized access. Redirecting...</p>
    </div>
</template>

<script>
import axios from 'axios';
import ProviderBar from '../components/ProviderBar.vue';

export default {
    name: 'ProviderDash',
    components: {
        ProviderBar
    },
    data() {
        return {
            isProvider: false,
            todayServices: [],
            closedServices: []
        };
    },

    created() {
        this.checkProviderStatus();
    },

    mounted() {
        if (this.isProvider) {
            this.fetchTodayServices();
            this.fetchClosedServices();
        }
    },

    methods: {
        checkProviderStatus() {
            const role = localStorage.getItem('role');
            const token = localStorage.getItem('jwt');

            if (!token || role !== 'provider') {
                this.$router.push('/');
                return;
            }

            this.isProvider = true;
        },

        async fetchTodayServices() {
            if (!this.isProvider) return;

            try {
                const token = localStorage.getItem('jwt');
                const providerId = localStorage.getItem('userId'); // Assuming you store provider ID

                const response = await axios.get(`http://127.0.0.1:5000/api/provider/today-services/${providerId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    this.todayServices = response.data;
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error fetching today's services:", error);
            }
        },

        async fetchClosedServices() {
            if (!this.isProvider) return;

            try {
                const token = localStorage.getItem('jwt');
                const providerId = localStorage.getItem('userId');

                const response = await axios.get(`http://127.0.0.1:5000/api/provider/closed-services/${providerId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    this.closedServices = response.data;
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error fetching closed services:", error);
            }
        },

        async approveService(serviceId) {
            if (!this.isProvider) return;

            try {
                const token = localStorage.getItem('jwt');
                const response = await axios.post(`http://127.0.0.1:5000/api/provider/approve-service/${serviceId}`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    // Refresh the services lists
                    this.fetchTodayServices();
                    this.fetchClosedServices();
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error approving service:", error);
            }
        },

        async rejectService(serviceId) {
            if (!this.isProvider) return;

            try {
                const token = localStorage.getItem('jwt');
                const response = await axios.post(`http://127.0.0.1:5000/api/provider/reject-service/${serviceId}`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    // Refresh the services lists
                    this.fetchTodayServices();
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error rejecting service:", error);
            }
        }
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
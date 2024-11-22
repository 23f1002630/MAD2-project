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
                        <td>{{ service.customer_name }}</td>
                        <td>{{ service.phone }}</td>
                        <td>{{ service.location }}</td>
                        <td class="text-center">
                            <div v-if="service.status === 'closed'">
                                <p>Closed</p>
                            </div>
                            <div v-else>
                                <button class="btn btn-primary btn-sm me-2"
                                    @click="closeService(service.id)">Close</button>
                            </div>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <div class="card p-4 mb-4 container">
            <h3 class="text-center text-primary mb-4">Service Requests</h3>
            <table class="table table-bordered">
                <thead>
                    <tr>
                        <th>ID</th>
                        <th>Customer Name</th>
                        <th>Phone</th>
                        <th>Date</th>
                        <th>Location</th>
                        <th>Action</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="booking in bookings" :key="booking.id">
                        <td>{{ booking.id }}</td>
                        <td>{{ booking.customer }}</td>
                        <td>{{ booking.phone }}</td>
                        <td>{{ booking.date }}</td>
                        <td>{{ booking.address }} <br> pin: {{ booking.pincode }}</td>
                        <td>
                            <button v-if="booking.status === 'pending'" class="btn btn-primary btn-sm me-2"
                                @click="approveService(booking.id)">Approve</button>
                            <button v-if="booking.status === 'pending'" class="btn btn-primary btn-sm me-2"
                                @click="rejectService(booking.id)">Reject</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- <div class="card p-4">
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
        </div> -->
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
            closedServices: [],
            bookings: []
        };
    },

    created() {
        this.checkProviderStatus();
        this.fetchBookings();
    },

    mounted() {
        if (this.isProvider) {
            this.fetchTodayServices();
            // this.fetchClosedServices();
            this.fetchBookings();
        }
    },

    methods: {
        // async fetchTodayServices() {
        //     if (!this.isProvider) return;

        //     try {
        //         const token = localStorage.getItem('jwt');
        //         const providerId = localStorage.getItem('userId');

        //         const response = await axios.get(`http://127.0.0.1:5000//api/today-services/${providerId}`, {
        //             headers: {
        //                 Authorization: `Bearer ${token}`
        //             },
        //             withCredentials: true
        //         });

        //         if (response.data && response.data.status === 'success') {
        //             this.todayServices = response.data.data;
        //         }
        //     } catch (error) {
        //         if (error.response && error.response.status === 401) {
        //             localStorage.removeItem('jwt');
        //             localStorage.removeItem('role');
        //             this.$router.push('/');
        //         }
        //         console.error("Error fetching today's services:", error);
        //     }
        // },

        async closeService(serviceId) {
            if (!this.isProvider) return;

            try {
                const token = localStorage.getItem('jwt');
                const providerId = localStorage.getItem('userId');

                const response = await axios.post(`http://127.0.0.1:5000/api/close-service/${serviceId}`, {
                    providerId: providerId
                }, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data && response.data.status === 'success') {
                    this.fetchTodayServices();
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error closing service:", error);
            }
        },

        // async fetchClosedServices() {
        //     if (!this.isProvider) return;

        //     try {
        //         const token = localStorage.getItem('jwt');
        //         const providerId = localStorage.getItem('userId');

        //         const response = await axios.get(`http://127.0.0.1:5000/api/provider/closed-services/${providerId}`, {
        //             headers: {
        //                 Authorization: `Bearer ${token}`
        //             },
        //             withCredentials: true
        //         });

        //         if (response.data && response.data.status === 'success') {
        //             this.closedServices = response.data.data;
        //         }
        //     } catch (error) {
        //         if (error.response && error.response.status === 401) {
        //             localStorage.removeItem('jwt');
        //             localStorage.removeItem('role');
        //             this.$router.push('/');
        //         }
        //         console.error("Error fetching closed services:", error);
        //     }
        // },
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

        // async fetchClosedServices() {
        //     if (!this.isProvider) return;

        //     try {
        //         const token = localStorage.getItem('jwt');
        //         const providerId = localStorage.getItem('userId');

        //         const response = await axios.get(`http://127.0.0.1:5000/api/provider/closed-services/${providerId}`, {
        //             headers: {
        //                 Authorization: `Bearer ${token}`
        //             },
        //             withCredentials: true
        //         });

        //         if (response.data) {
        //             this.closedServices = response.data;
        //         }
        //     } catch (error) {
        //         if (error.response && error.response.status === 401) {
        //             localStorage.removeItem('jwt');
        //             localStorage.removeItem('role');
        //             this.$router.push('/');
        //         }
        //         console.error("Error fetching closed services:", error);
        //     }
        // },

        async approveService(bookingId) {
            if (!this.isProvider) return;

            try {
                const token = localStorage.getItem('jwt');
                const response = await axios.post(`http://127.0.0.1:5000/api/service-requests/approve/${bookingId}`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    // Refresh the services lists
                    this.fetchBookings();
                    window.location.reload();
                    // this.fetchClosedServices();
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
                const response = await axios.post(`http://127.0.0.1:5000/api/service-requests/reject/${bookingId}`, {}, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    // Refresh the services lists
                    this.fetchBookings();
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error rejecting service:", error);
            }
        },


        fetchBookings() {
            // Check if the user is an admin before proceeding
            console.log('Hi hello');

            // Retrieve the JWT token from localStorage
            let your_jwt_token = localStorage.getItem('jwt');

            // Make an API call to fetch bookings
            axios.get('http://127.0.0.1:5000/api/service-requests', {
                headers: {
                    Authorization: `Bearer ${your_jwt_token}`
                },
                withCredentials: true
            })
                .then(response => {
                    // Assign the response data to the bookings property
                    this.bookings = response.data.data;
                    console.log(this.bookings);
                })
                .catch(error => {
                    // Handle unauthorized access by redirecting to the home page
                    if (error.response && error.response.status === 401) {
                        this.$router.push('/');
                    }
                    // Log any errors encountered during the API call
                    console.error("Error fetching bookings:", error);
                });
        },
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
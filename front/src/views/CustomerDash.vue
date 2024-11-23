vue
<template>
    <div v-if="isCustomer" class="container my-5">
        <CustomerBar />
        <div v-if="selectedprofessional.length === 0" class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Services</h3>
            <div class="d-flex justify-content-around flex-wrap">
                <button v-for="service in services" :key="service.id" @click="selectService(service.id)"
                    class="btn btn-outline-primary m-2">{{ service.services }}</button>
            </div>
        </div>

        <div v-else class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Professionals</h3>
            <div v-for="professional in selectedprofessional" :key="professional.id" class="card p-4">
                <h4>{{ professional.name }}</h4>
                <p>{{ professional.experience }}</p>
                <p>{{ professional.service }}</p>
                <p>{{ professional.phone }}</p>
                <button @click="requestProfessional(professional)" class="btn btn-primary">Request</button>
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
                        <th>Date</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    <tr v-for="service in bookings" :key="service.id">
                        <td>{{ service.id }}</td>
                        <td>{{ service.service_name }}</td>
                        <td>{{ service.professional_name }}</td>
                        <td>{{ service.date }}</td>
                        <td>
                            <p>{{ service.status }}</p>
                            <button v-if="service.status === 'pending'" class="btn btn-primary"
                                @click="editBooking(service.id)">
                                Edit</button>
                            <button v-if="service.status === 'pending'" class="btn btn-danger"
                                @click="deleteBooking(service.id)"> Delete</button>
                            <button v-if="service.status === 'closed'" class="btn btn-success"
                                @click="rateBooking(service.id)">Close</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Modal -->
        <div v-show="requestModal" class="modal fade" id="requestModal" tabindex="-1"
            aria-labelledby="requestModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="requestModalLabel">Book Service</h1>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="sendRequest">
                            <div class="mb-3">
                                <label for="service-name" class="col-form-label">Service:</label>
                                <p>{{ selectedService.services }}</p>
                            </div>
                            <div class="mb-3">
                                <label for="professional-name" class="col-form-label">Professional:</label>
                                <p>{{ selectedProfessional.name }}</p>
                            </div>
                            <div class="mb-3">
                                <label for="phone" class="col-form-label">Phone:</label>
                                <p>{{ selectedProfessional.phone }}</p>
                            </div>
                            <div class="mb-3">
                                <label for="remarks" class="col-form-label">Remarks:</label>
                                <textarea class="form-control" id="remarks" v-model="bookingDetails.remarks"></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="date" class="col-form-label">Date:</label>
                                <input type="date" class="form-control" id="date" v-model="bookingDetails.date"
                                    required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button @click="closeModal" type="button" class="btn btn-secondary"
                            data-bs-dismiss="modal">Cancel</button>
                        <button @click="sendRequest" type="submit" class="btn btn-primary">Book</button>
                    </div>
                </div>
            </div>
        </div>
    </div>
    <div v-else>
        <p>Unauthorized access. Redirecting...</p>
    </div>
</template>

<script>
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js';
import CustomerBar from '../components/CustomerBar.vue';
import axios from 'axios';

export default {
    name: 'CustomerDash',
    components: {
        CustomerBar
    },
    data() {
        return {
            isCustomer: false,
            selectedprofessional: [],
            services: [],
            selectedService: {},
            selectedProfessional: {},
            bookings: [], // Ensure this is used for service history
            bookingDetails: {
                date: '',
                remarks: ''
            },
            requestModal: null,
        }
    },

    created() {
        this.checkCustomerStatus();
    },

    mounted() {
        if (this.isCustomer) {
            this.fetchServices();
            this.fetchServiceHistory();
        }
    },

    methods: {
        async fetchServiceHistory() {
            try {
                const token = localStorage.getItem('jwt');
                const customerId = localStorage.getItem('userId');

                const response = await axios.get(`http://127.0.0.1:5000/api/service-history/${customerId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data && response.status === 200) {
                    console.log('Service History:', response.data); // Log the data
                    this.bookings = response.data; // Ensure this is the correct assignment
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error fetching service history:", error);
            }
        },

        async deleteBooking(id) {
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.delete('http://127.0.0.1:5000/api/bookings/' + id, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                console.log("Booking deleted:", response.data);
                this.fetchServiceHistory();
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    this.$router.push('/');
                }
                console.error("Error deleting booking:", error);
            }
        },
                
        checkCustomerStatus() {
            const role = localStorage.getItem('role');
            const token = localStorage.getItem('jwt');

            if (!token || role !== 'customer') {
                this.$router.push('/');
                return;
            }

            this.isCustomer = true;
        },

        async selectService(id) {
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/getprovidersbyservice/' + id, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                if (response.data) {
                    this.selectedprofessional = response.data;
                    this.selectedService = this.services.find(service => service.id === id);
                }
            } catch (error) {
                this.handleError(error);
            }
        },

        requestProfessional(professional) {
            if (!this.isCustomer) return;

            this.selectedProfessional = professional;
            this.requestModal = new bootstrap.Modal('#requestModal', {
                keyboard: false
            });
            this.requestModal.show();
        },

        async sendRequest() {
            if (!this.isCustomer) return;

            if (!this.bookingDetails.date) {
                alert('Please select a date for the booking');
                return;
            }

            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const customerId = localStorage.getItem('userId');

                const response = await axios.post('http://127.0.0.1:5000/api/bookings', {
                    provider_id: this.selectedProfessional.id,
                    customer_id: customerId,
                    service_id: this.selectedService.id,
                    date: this.bookingDetails.date,
                    remarks: this.bookingDetails.remarks
                }, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    alert('Booking successful!');
                    this.closeModal();
                }

            } catch (error) {
                this.handleError(error);
            }
        },

        closeModal() {
            if (this.requestModal) {
                this.requestModal.hide();
                this.bookingDetails.date = '';
                this.bookingDetails.remarks = '';
            }
        },

        async fetchServices() {
            if (!this.isCustomer) return;

            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/services', {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                if (response.data) {
                    this.services = response.data;
                }
            } catch (error) {
                this.handleError(error);
            }
        },

        handleError(error) {
            if (error.response && error.response.status === 401) {
                localStorage.removeItem('jwt');
                localStorage.removeItem('role');
                this.$router.push('/');
            }
            console.error("Error:", error);
            if (error.response && error.response.data && error.response.data.error) {
                alert(error.response.data.error);
            } else {
                alert('An error occurred. Please try again.');
            }
        }
    }
}
</script>

<style scoped>
/* Add any custom styles here */
</style>
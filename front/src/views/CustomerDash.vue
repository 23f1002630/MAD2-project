<template>
    <div class="container my-5">
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
                                <label for="time" class="col-form-label">Time:</label>
                                <input type="datetime-local" class="form-control" id="time"
                                    v-model="bookingDetails.time" required>
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
            selectedprofessional: [],
            services: [],
            selectedService: {},
            selectedProfessional: {},
            bookingDetails: {
                time: ''
            },
            requestModal: null,
        }
    },

    mounted() {
        this.fetchServices();
    },

    methods: {
        async selectService(id) {
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/getprovidersbyservice/' + id, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                this.selectedprofessional = response.data;
                this.selectedService = this.services.find(service => service.id === id);
                console.log(this.selectedprofessional);
            } catch (error) {
                console.error("Error fetching professionals:", error);
            }
        },

        requestProfessional(professional) {
            this.selectedProfessional = professional;
            this.requestModal = new bootstrap.Modal('#requestModal', {
                keyboard: false
            });
            this.requestModal.show();
        },

        async sendRequest() {
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.post('http://127.0.0.1:5000/api/bookings', {
                    provider_id: this.selectedProfessional.id,
                    customer_id: "1", // Replace with actual customer ID
                    service_id: this.selectedService.id,
                    time: this.bookingDetails.time
                }, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                console.log("Booking successful:", response.data);
                this.closeModal();
            } catch (error) {
                console.error("Error sending booking request:", error);
            }
        },

        closeModal() {
            this.requestModal.hide();
            this.bookingDetails.time = '';
        },

        async fetchServices() {
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/services', {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                this.services = response.data;
                console.log(this.services);
            } catch (error) {
                console.error("Error fetching services:", error);
            }
        }
    }
}
</script>
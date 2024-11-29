<template>
    <div v-if="isCustomer" class="container my-5">
        <CustomerBar />
        <div v-if="selectedprofessional.length === 0" class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Services</h3>
            <div class="mb-3">
                <input type="text" class="form-control" placeholder="Search" v-model="searchQuery" />
            </div>
            <div class="d-flex justify-content-around flex-wrap">
                <button v-for="service in filteredServices" :key="service.id" @click="selectService(service.id)"
                    class="btn btn-outline-primary m-2">{{ service.services }}</button>
            </div>
        </div>

        <div v-else class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Professionals</h3>
            <div v-for="professional in selectedprofessional" :key="professional.id" class="card p-4">
                <h4>{{ professional.name }}</h4>
                <p>{{ professional.experience }}</p>
                <p>{{ professional.address }}</p>
                <p>{{ professional.pincode }}</p>
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
                                @click="startEditing(service.id)">
                                Edit</button>
                            <button v-if="service.status === 'pending'" class="btn btn-danger"
                                @click="deleteBooking(service.id)"> Delete</button>
                            <button v-if="service.status === 'approved'" class="btn btn-success"
                                @click="closeService(service.id)">Close</button>
                            <button v-if="service.status === 'closed'" class="btn btn-success"
                                @click="openPopover(service.id)">Rate</button>
                        </td>
                    </tr>
                </tbody>
            </table>
        </div>

        <!-- Request Modal -->
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

        <!-- Edit Booking Modal -->
        <div v-show="editBookingModal" class="modal fade" id="bookingeditModal" tabindex="-1"
            aria-labelledby="serviceModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="bookingeditModal">Update Request</h1>
                    </div>
                    <div class="modal-body">
                        <form @submit.prevent="updateBooking(bookingseditDetails)">
                            <div class="mb-3">
                                <label for="remarks-text" class="col-form-label">Remarks:</label>
                                <textarea class="form-control" id="remarks-text"
                                    v-model="bookingseditDetails.remarks"></textarea>
                            </div>
                            <div class="mb-3">
                                <label for="date" class="col-form-label">Date:</label>
                                <input type="date" class="form-control" id="date" v-model="bookingseditDetails.date"
                                    required>
                            </div>
                        </form>
                    </div>
                    <div class="modal-footer">
                        <button @click="closeEditModal" type="button" class="btn btn-secondary"
                            data-bs-dismiss="modal">Cancel</button>
                        <button @click="updateBooking(bookingseditDetails)" type="submit"
                            class="btn btn-primary">Update</button>
                    </div>
                </div>
            </div>
        </div>

        <!-- Popover Modal -->
        <div v-show="popoverModal" class="modal fade" id="popoverModal" tabindex="-1"
            aria-labelledby="popoverModalLabel" aria-hidden="true">
            <div class="modal-dialog">
                <div class="modal-content">
                    <div class="modal-header">
                        <h1 class="modal-title fs-5" id="popoverModalLabel">Rate Booking</h1>
                    </div>
                    <div class="modal-body">
                        <p>Thank you for using our service. Please rate your experience.</p>
                        <div class="mb-3">
                            <label for="rating" class="col-form-label">Rating:</label>
                            <div class="d-flex">
                                <span v-for="star in 5" :key="star" @click="setRating(star)" class="star"
                                    :class="{ 'text-warning': star <= feedbackDetails.rating, 'text-muted': star > feedbackDetails.rating }">
                                    ★
                                </span>
                            </div>
                        </div>
                        <div class="mb-3">
                            <label for="feedback" class="col-form-label">Feedback:</label>
                            <textarea class="form-control" id="feedback" v-model="feedbackDetails.feedback"></textarea>
                        </div>
                    </div>
                    <div class="modal-footer">
                        <button @click="closePopover" type="button" class="btn btn-secondary"
                            data-bs-dismiss="modal">Close</button>
                        <button @click="submitFeedback" type="button" class="btn btn-primary">Submit</button>
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
            bookings: [],
            editBookingModal: null,
            bookingseditDetails: {
                id: null,
                date: '',
                remarks: ''
            },
            bookingDetails: {
                date: '',
                remarks: ''
            },
            requestModal: null,
            popoverModal: null,
            feedbackDetails: {
                bookingId: null,
                rating: 0,
                feedback: ''
            },
            searchQuery: '',
        }
    },

    created() {
        this.checkCustomerStatus();
    },

    mounted() {
        if (this.isCustomer) {
            this.fetchServices();
            this.fetchServiceHistory();
            this.fetchTodayServices();
        }
    },

    computed: {
        filteredServices() {
            // Filter services based on search query
            return this.services.filter((service) => {
                // const nameMatch = service.name
                //     .toLowerCase()
                //     .includes(this.searchQuery.toLowerCase());
                const serviceMatch = service.services
                    .toLowerCase()
                    .includes(this.searchQuery.toLowerCase());
                // return nameMatch || serviceMatch;
                return serviceMatch;
            });
        },
    },

    methods: {
        async fetchServiceHistory() {
            try {
                const token = localStorage.getItem('jwt');
                const customerId = localStorage.getItem('userId');

                const response = await axios.get(`http://127.0.0.1:5000/api/service-history/${customerId}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    }
                });

                if (response.data && response.status === 200) {
                    this.bookings = response.data;
                }
            } catch (error) {
                this.handleError(error);
            }
        },

        updateBooking(bookingDetails) {
            let your_jwt_token = localStorage.getItem('jwt');

            if (!your_jwt_token) {
                console.error('JWT token is missing');
                this.$router.push('/login');
                return;
            }

            if (!bookingDetails.id) {
                console.error('Booking ID is missing');
                return;
            }

            axios.put(`http://127.0.0.1:5000/api/bookings/${bookingDetails.id}`, bookingDetails, {
                headers: {
                    Authorization: `Bearer ${your_jwt_token}`
                }
            })
                .then(response => {
                    this.fetchServiceHistory();
                    this.closeEditModal();
                })
                .catch(error => {
                    this.handleError(error);
                });
        },

        getBookingDetails(id) {
            let your_jwt_token = localStorage.getItem('jwt');
            axios.get(`http://127.0.0.1:5000/api/bookings/${id}`, {
                headers: {
                    Authorization: `Bearer ${your_jwt_token}`
                }
            }).then(response => {
                this.bookingseditDetails = response.data;
            })
                .catch(error => {
                    this.handleError(error);
                });
        },

        showEditModal() {
            this.editBookingModal = new bootstrap.Modal('#bookingeditModal', {
                keyboard: false
            });
            this.editBookingModal.show();
        },

        startEditing(id) {
            this.getBookingDetails(id);
            this.showEditModal();
        },

        async deleteBooking(id) {
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.delete(`http://127.0.0.1:5000/api/bookings/${id}`, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    }
                });
                this.fetchServiceHistory();
            } catch (error) {
                this.handleError(error);
            }
        },

        async closeService(serviceId) {
            if (!this.isCustomer) return;

            try {
                const token = localStorage.getItem('jwt');
                const customerId = localStorage.getItem('userId');

                const response = await axios.post(`http://127.0.0.1:5000/api/close-service/${serviceId}`, {
                    customerId: customerId
                }, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data && response.data.status === 'success') {
                    this.fetchTodayServices();
                    window.location.reload();
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

        async fetchTodayServices() {
            try {
                const token = localStorage.getItem('jwt');
                const customerId = localStorage.getItem('userId');

                const response = await axios.get(`http://127.0.0.1:5000/api/today-services/${customerId}`, {
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
                const response = await axios.get(`http://127.0.0.1:5000/api/getprovidersbyservice/${id}`, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    }
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
                    }
                });

                if (response.data) {
                    alert('Booking successful!');
                    this.closeModal();
                    this.fetchServiceHistory();
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

        closeEditModal() {
            if (this.editBookingModal) {
                this.editBookingModal.hide();
                this.bookingseditDetails = { id: null, date: '', remarks: '' };
            }
        },

        openPopover(id) {
            this.feedbackDetails.bookingId = id;
            this.popoverModal = new bootstrap.Modal('#popoverModal', {
                keyboard: false
            });
            this.popoverModal.show();
        },

        closePopover() {
            if (this.popoverModal) {
                this.popoverModal.hide();
                this.feedbackDetails = { bookingId: null, rating: 0, feedback: '' };
            }
        },

        setRating(star) {
            this.feedbackDetails.rating = star;
        },

        async submitFeedback() {
            if (!this.feedbackDetails.bookingId) return;

            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.put(`http://127.0.0.1:5000/api/bookings/${this.feedbackDetails.bookingId}/rate`, {
                    rating: this.feedbackDetails.rating,
                    feedback: this.feedbackDetails.feedback
                }, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    }
                });

                if (response.data) {
                    alert('Feedback submitted successfully!');
                    this.closePopover();
                    this.fetchServiceHistory();
                }

            } catch (error) {
                this.handleError(error);
            }
        },

        async fetchServices() {
            if (!this.isCustomer) return;

            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/services', {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    }
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
.star {
    font-size: 1.5rem;
    cursor: pointer;
}

.text-warning {
    color: #ffc107;
}

.text-muted {
    color: #6c757d;
}
</style>
<template>
    <div v-if="isCustomer" class="container mt-5">
        <CustomerBar />
        <div class="row justify-content-center mb-4 container">
            <div class="col-md-8">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search for services..." v-model="searchQuery"
                        @keyup.enter="searchServices" />
                    <button class="btn btn-primary" type="button" @click="searchServices" :disabled="loading">{{ loading
                        ? 'Searching...' : 'Search' }}</button>
                </div>
            </div>
        </div>
        <!-- Loading Spinner -->
        <div v-if="loading" class="text-center my-4">
            <div class="spinner-border text-primary" role="status">
                <span class="visually-hidden">Loading...</span>
            </div>
        </div>

        <!-- No Results Message -->
        <div v-else-if="cards.length === 0" class="text-center my-4">
            <p>No services found.</p>
        </div>

        <!-- Services Grid -->
        <div v-else class="row justify-content-center">
            <div class="col-md-3" v-for="card in cards" :key="card.id">
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Service: {{ card.service }}</h5>
                        <p class="card-text">Provider: {{ card.provider }}</p>
                        <p class="card-text">Price: {{ card.price }}</p>
                        <p class="card-text">Description: {{ card.description }}</p>
                        <button class="btn btn-primary btn-sm"
                            @click="$router.push(`/customer-dash?service=${card.id}`)">
                            Book Service
                        </button>
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
import axios from 'axios';
import CustomerBar from '../components/CustomerBar.vue';

export default {
    name: 'CustomerSearch',
    components: {
        CustomerBar
    },
    data() {
        return {
            isCustomer: false,
            searchQuery: '',
            cards: [],
            loading: false
        };
    },

    created() {
        this.checkCustomerStatus();
    },

    mounted() {
        if (this.isCustomer) {
            this.fetchServices();
        }
    },

    methods: {
        checkCustomerStatus() {
            const role = localStorage.getItem('role');
            const token = localStorage.getItem('jwt');

            if (!token || role !== 'customer') {
                this.$router.push('/');
                return;
            }

            this.isCustomer = true;
        },

        async fetchServices() {
            if (!this.isCustomer) return;

            try {
                this.loading = true;
                const token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/services/search', {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    this.cards = response.data;
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error fetching services:", error);
            } finally {
                this.loading = false;
            }
        },

        async searchServices() {
            if (!this.isCustomer || !this.searchQuery.trim()) return;

            try {
                this.loading = true;
                const token = localStorage.getItem('jwt');
                const response = await axios.get(`http://127.0.0.1:5000/api/services/search?query=${this.searchQuery}`, {
                    headers: {
                        Authorization: `Bearer ${token}`
                    },
                    withCredentials: true
                });

                if (response.data) {
                    this.cards = response.data;
                }
            } catch (error) {
                if (error.response && error.response.status === 401) {
                    localStorage.removeItem('jwt');
                    localStorage.removeItem('role');
                    this.$router.push('/');
                }
                console.error("Error searching services:", error);
            } finally {
                this.loading = false;
            }
        }
    }
};
</script>

<style scoped>
.container {
    margin-top: 50px;
}

.card {
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    transition: transform 0.2s;
}

.card:hover {
    transform: translateY(-5px);
    box-shadow: 0 4px 10px rgba(0, 0, 0, 0.15);
}

.input-group {
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
    border-radius: 5px;
}

.input-group input {
    border-right: none;
}

.input-group button {
    border-left: none;
}

.spinner-border {
    width: 3rem;
    height: 3rem;
}

.btn-primary {
    transition: all 0.3s;
}

.btn-primary:disabled {
    opacity: 0.7;
}
</style>
<template>
    <div class="container my-5">
        <CustomerBar />
        <div v-if="selectedprofessional.length === 0" class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Services</h3>
            <div class="d-flex justify-content-around flex-wrap">
                <button v-for="service in services" :key="service.id" @click="selectService(service.services)" class="btn btn-outline-primary m-2">{{ service.services }}</button>
            </div>
        </div>

        <div v-else class="card p-4 container">
            <h3 class="text-center text-primary mb-4">Our Professionals</h3>
            <div v-for="professional in selectedprofessional" :key="professional.id" class="card p-4">
                <h4>{{ professional.name }}</h4>
                <p>{{ professional.experience }}</p>
                <p>{{ professional.service }}</p>
                <p>{{ professional.phone }}</p>
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
import axios from 'axios';
export default {
    name: 'CustomerDash',
    components: {
        CustomerBar
    },
    data() {
        return {
            selectedprofessional: [],
            services: []
        }
    },

    mounted() {
        this.fetchServices();
    },

    methods: {
        async selectService(service) {
            // @app.route('/api/getprovidersbyservice/<string:service_name>', methods=['GET'])
            // @jwt_required()
            // def get_providers_by_service(service_name):
            //   professionals = Provider.query.filter_by(services=service_name).all()
            //   if not professionals:
            //       return jsonify({'error': 'Service not found'}), 404

            //   # Create a list of dictionaries for each professional
            //   providers_list = [
            //       {
            //           'id': professional.id,
            //           'name': professional.fullname,
            //           'experience': professional.experience,
            //           'service': professional.services,
            //           'phone': professional.phone
            //       }
            //       for professional in professionals
            //   ]

            //   return jsonify(providers_list), 200
            try {
                let your_jwt_token = localStorage.getItem('jwt');
                const response = await axios.get('http://127.0.0.1:5000/api/getprovidersbyservice/' + service, {
                    headers: {
                        Authorization: `Bearer ${your_jwt_token}`
                    },
                    withCredentials: true
                });
                this.selectedprofessional = response.data;
                console.log(this.selectedprofessional);
            } catch (error) {
                console.error("Error fetching professionals:", error);
            }
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
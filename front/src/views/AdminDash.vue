<template>
  <div v-if="isAdmin" class="container mt-4">
    <header>
      <AdminBar />
    </header>
    <div class="card mb-2 container">
      <div class="card-header">Services</div>
      <div class="card-body">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Services</th>
              <th>Price</th>
              <th>Description</th>
              <th>Time required</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <!-- Example row -->
            <tr v-for="service in services" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.services }}</td>
              <td>{{ service.price }}</td>
              <td>{{ service.description }}</td>
              <td>{{ service.time }} hrs</td>
              <td class="text-center">
                <button class="btn btn-primary btn-sm me-2" @click="startEditing(service.id)">Edit</button>
                <button class="btn btn-danger btn-sm" @click="deleteService(service.id)">Delete</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div class="d-flex justify-content-end mb-4">
      <button class="btn btn-success btn-sm" @click="mymodal">+ New
        Services</button>
    </div>

    <div class="card mb-4">
      <div class="card-header">Professionals</div>
      <div class="card-body">
        <div class="mb-3">
          <input type="text" class="form-control" placeholder="Search by name or service" v-model="searchQuery" />
        </div>
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Experience (Yrs)</th>
              <th>Service Name</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="professional in filteredProfessionals" :key="professional.id">
              <td>{{ professional.id }}</td>
              <td>{{ professional.name }}</td>
              <td>{{ professional.experience }}</td>
              <td>{{ professional.service_name }}</td>
              <td class="text-center">
                <p>{{ professional.status }}</p>
                <div v-if="professional.status === 'pending'">
                  <button class="btn btn-primary btn-sm me-2"
                    @click="approveProfessional(professional.id)">Approve</button>
                  <button class="btn btn-primary btn-sm me-2"
                    @click="rejectProfessional(professional.id)">Reject</button>
                  <a class="btn btn-success btn-sm" :href="'http://localhost:5000/' + professional.file"
                    target="_blank">View File</a>
                  <!--  to view the image -->
                  <!-- <img :src="'http://localhost:5000/' + professional.image" height="100px" width="100px">  -->
                </div>
                <div v-else-if="professional.isblocked">
                  <button class="btn btn-success btn-sm" @click="blockProfessional(professional.id)">Unblock</button>
                </div>
                <div v-else>
                  <button class="btn btn-danger btn-sm" @click="blockProfessional(professional.id)">Block</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-header">Customers</div>
      <div class="card-body">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Name</th>
              <th>Phone</th>
              <th>Address</th>
              <th class="text-center">Action</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="customer in customers" :key="customer.id">
              <td>{{ customer.id }}</td>
              <td>{{ customer.name }}</td>
              <td>{{ customer.phone }}</td>
              <td>{{ customer.address }}</td>
              <td class="text-center">
                <div v-if="customer.isblocked">
                  <button class="btn btn-success btn-sm" @click="blockCustomer(customer.id)">Unblock</button>
                </div>
                <div v-else>
                  <button class="btn btn-danger btn-sm" @click="blockCustomer(customer.id)">Block</button>
                </div>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <div class="card mb-4">
      <div class="card-header">Service Requests</div>
      <button @click="downloadCSV" class="btn btn-primary mb-3">Export as CSV</button>
      <div class="card-body">
        <table class="table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Assigned Professional</th>
              <th>Service Name</th>
              <th>Date</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>

            <tr v-for="service in bookings" :key="service.id">
              <td>{{ service.id }}</td>
              <td>{{ service.professional_name }}</td>
              <td>{{ service.service_name }}</td>
              <td>{{ service.date }}</td>
              <td>{{ service.status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>

    <!-- Modal -->
    <div v-show="serviceform" class="modal fade" id="serviceModal" tabindex="-1" aria-labelledby="serviceModalLabel"
      aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 @click="mymodal" class="modal-title fs-5" id="serviceModalLabel">New Service</h1>

          </div>
          <div class="modal-body">
            <form @submit.prevent="addService">
              <div class="mb-3">
                <label for="service-name" class="col-form-label">Service:</label>
                <input type="text" class="form-control" id="service-name" v-model="newService.service">
              </div>
              <div class="mb-3">
                <label for="description-text" class="col-form-label">Description:</label>
                <textarea class="form-control" id="description-text" v-model="newService.description"></textarea>
              </div>
              <div class="mb-3">
                <label for="price" class="col-form-label">Price:</label>
                <input type="text" class="form-control" id="price" v-model="newService.price">
              </div>
              <div class="mb-3">
                <label for="time" class="col-form-label">Time:</label>
                <input type="text" class="form-control" id="time" v-model="newService.time">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button @click.prevent="serviceform = false" type="button" class="btn btn-secondary"
              data-bs-dismiss="modal">Cancel</button>
            <button @click.prevent="addService" type="submit" class="btn btn-primary">Add</button>
          </div>
        </div>
      </div>
    </div>

    <!-- edit service Modal -->
    <div v-show="editServiceModal" class="modal fade" id="serviceseditModal" tabindex="-1"
      aria-labelledby="serviceModalLabel" aria-hidden="true">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h1 class="modal-title fs-5" id="serviceModalLabel">Update Service</h1>

          </div>
          <div class="modal-body">
            <form @submit.prevent="updateService(serviceseditDetails)">
              <div class="mb-3">
                <label for="service-name" class="col-form-label">Service:</label>
                <input type="text" class="form-control" id="service-name" v-model="serviceseditDetails.services">
              </div>
              <div class="mb-3">
                <label for="description-text" class="col-form-label">Description:</label>
                <textarea class="form-control" id="description-text"
                  v-model="serviceseditDetails.description"></textarea>
              </div>
              <div class="mb-3">
                <label for="price" class="col-form-label">Price:</label>
                <input type="text" class="form-control" id="price" v-model="serviceseditDetails.price">
              </div>
              <div class="mb-3">
                <label for="time" class="col-form-label">Time:</label>
                <input type="text" class="form-control" id="time" v-model="serviceseditDetails.time">
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button @click.prevent="serviceform = false" type="button" class="btn btn-secondary"
              data-bs-dismiss="modal">Cancel</button>
            <button @click="updateService(serviceseditDetails)" type="submit" class="btn btn-primary">Update</button>
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
import axios from 'axios';
import AdminBar from '../components/AdminBar.vue';

export default {
  name: 'AdminDash',
  components: {
    AdminBar
  },
  data() {
    return {
      isAdmin: false,
      professionals: [], // Initialize an empty array to store professionals
      customers: [],
      services: [],
      bookings: [],
      serviceseditDetails: {},
      myModal: null,
      serviceform: false,
      editServiceModal: null,
      newService: {
        "service": '',
        "description": '',
        "price": '',
        "time": ''
      },
      searchQuery: '',
    };
  },

  created() {
    this.checkAdminStatus();
  },
  mounted() {

    if (this.isAdmin) {
      this.fetchProfessionals();
      this.fetchServices();
      this.fetchCustomers();
      this.fetchServiceHistory();
    }

  },

  computed: {
    filteredProfessionals() {
      // Filter professionals based on search query
      return this.professionals.filter((professional) => {
        const nameMatch = professional.name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
        const serviceMatch = professional.service_name
          .toLowerCase()
          .includes(this.searchQuery.toLowerCase());
        return nameMatch || serviceMatch;
      });
    },
  },
  methods: {

    async fetchServiceHistory() {
      try {
        const token = localStorage.getItem('jwt');

        // Make a request to the modified endpoint that retrieves all bookings
        const response = await axios.get('http://127.0.0.1:5000/api/admin/service-history', {
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

    downloadCSV() {
        const token = localStorage.getItem('auth_token');  // Assuming you're storing the token in localStorage

        axios.post('http://127.0.0.1:5000/export-csv')
        .then(response => {
            console.log('Export task triggered!');
            // Optionally, wait for a few seconds for the task to complete and then allow download
            setTimeout(() => {
            window.location.href = 'http://127.0.0.1:5000/download_service_bookings';
            }, 7000);  // Adjust the delay based on the expected task completion time
        })
        .catch(error => {
            console.error('Error triggering export task:', error);
        });
    },

    checkAdminStatus() {
      const role = localStorage.getItem('role');
      const token = localStorage.getItem('jwt');

      if (!token || role !== 'admin') {
        // Redirect to login or home page if not admin
        this.$router.push('/');
        return;
      }

      this.isAdmin = true;
    },
    async fetchProfessionals() {
      if (!this.isAdmin) return;
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:5000/api/professionals', {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });

        console.log("Fetched professionals:", response); // Debugging line
        this.professionals = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/');
        }
        console.error("Error fetching professionals:", error);

      }
    },

    async fetchCustomers() {
      if (!this.isAdmin) return;
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:5000/api/customers', {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });

        console.log("Fetched customers:", response); // Debugging line
        this.customers = response.data;
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/');
        }
        console.error("Error fetching customers:", error);
      }
    },


    mymodal() {
      this.myModal = new bootstrap.Modal('#serviceModal', {
        keyboard: false
      })
      this.myModal.show()
    },
    showEditModal() {
      this.editServiceModal = new bootstrap.Modal('#serviceseditModal', {
        keyboard: false
      })
      this.editServiceModal.show()
    },
    async addService() {
      if (!this.isAdmin) return;
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.post('http://127.0.0.1:5000/api/services', this.newService, {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`,
            Accept: 'application/json'
          },
          withCredentials: true
        });
        console.log("Service added:", response.data);
        // Optionally, refresh the list of services or clear the form
        this.newService = { service: '', description: '', price: '', time: '' };
        // Close the modal
        this.myModal.hide()
        this.fetchServices();


      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/');
        }
        console.error("Error adding service:", error);
      }
    },

    async approveProfessional(id) {
      if (!this.isAdmin) return;
      const your_jwt_token = localStorage.getItem('jwt');

      if (!your_jwt_token) {
        console.error('JWT token is missing');
        return;
      }

      const response = await axios.post(`http://127.0.0.1:5000/api/approveprofessional/${id}`, {}, {
        headers: {
          Authorization: `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      })
        .then(response => {
          this.fetchProfessionals();
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error('Error approving professional:', error);
        });
    },

    async rejectProfessional(id) {

      if (!this.isAdmin) return;

      let your_jwt_token = localStorage.getItem('jwt');
      const response = await axios.post(`http://127.0.0.1:5000/api/rejectprofessional/${id}`,
        {},
        {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }).then(response => {
          this.fetchProfessionals()
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error(error);
        });
    },

    blockProfessional(id) {

      if (!this.isAdmin) return;

      let your_jwt_token = localStorage.getItem('jwt');
      const response = axios.post('http://127.0.0.1:5000/api/professionalblock/' + id,
        // passing data to server
        {},
        // passing header details
        {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }).then(response => {
          this.fetchProfessionals()
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error(error);
        });
    },

    blockCustomer(id) {

      if (!this.isAdmin) return;

      let your_jwt_token = localStorage.getItem('jwt');
      const response = axios.post('http://127.0.0.1:5000/api/customerblock/' + id,
        // passing data to server
        {},
        // passing header details
        {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }).then(response => {
          this.fetchCustomers()
        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error(error);
        });
    },


    updateService(serviceDetails) {

      if (!this.isAdmin) return;

      let your_jwt_token = localStorage.getItem('jwt');
      const response = axios.put('http://127.0.0.1:5000/api/services/' + serviceDetails.id,
        // passing data to server
        serviceDetails,
        // passing header details
        {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        }).then(response => {
          this.fetchServices()
          this.editServiceModal.hide()

        })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error(error);
        });
    },
    fetchServices() {

      if (!this.isAdmin) return;

      let your_jwt_token = localStorage.getItem('jwt');
      const response = axios.get('http://127.0.0.1:5000/api/services', {
        headers: {
          Authorization: `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      }).then(response => {
        this.services = response.data;
      })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error(error);
        });

    },



    getServiceDetails(id) {
      if (!this.isAdmin) return;

      let your_jwt_token = localStorage.getItem('jwt');
      const response = axios.get('http://127.0.0.1:5000/api/services/' + id, {
        headers: {
          Authorization: `Bearer ${your_jwt_token}`
        },
        withCredentials: true
      }).then(response => {
        this.serviceseditDetails = response.data;
      })
        .catch(error => {
          if (error.response && error.response.status === 401) {
            this.$router.push('/');
          }
          console.error(error);
        });

    },

    startEditing(id) {
      this.showEditModal()
      this.getServiceDetails(id)
    },

    async deleteService(id) {
      if (!this.isAdmin) return;

      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.delete('http://127.0.0.1:5000/api/services/' + id, {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });
        console.log("Service deleted:", response.data);
        this.fetchServices();
      } catch (error) {
        if (error.response && error.response.status === 401) {
          this.$router.push('/');
        }
        console.error("Error deleting service:", error);
      }
    }

  },
};
</script>

<style>
.container {
  max-width: 1200px;
  margin: 0 auto;
}

.text-center {
  text-align: center;
}
</style>
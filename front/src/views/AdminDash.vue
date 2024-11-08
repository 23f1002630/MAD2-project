<template>
  <div class="container mt-4">
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
            <tr v-for="professional in professionals" :key="professional.id">
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
      <div class="card-header">Service Requests</div>
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
            <!-- Example row -->
            <tr>
              <td>1</td>
              <td>John Doe</td>
              <td>Service A</td>
              <td>2023-10-30</td>
              <td>Pending</td>
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
      professionals: [], // Initialize an empty array to store professionals
      services: [],
      serviceseditDetails: {},
      myModal: null,
      serviceform: false,
      editServiceModal: null,
      newService: {
        "service": '',
        "description": '',
        "price": ''
      }
    };
  },
  mounted() {
    this.fetchProfessionals();
    this.fetchServices();
  },
  methods: {
    async fetchProfessionals() {
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
        console.error("Error fetching professionals:", error);
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
        this.newService = { service: '', description: '', price: '' };
        // Close the modal
        this.myModal.hide()
        this.fetchServices();


      } catch (error) {
        console.error("Error adding service:", error);
      }
    },

    async approveProfessional(id) {
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
          console.error('Error approving professional:', error);
        });
    },

    async rejectProfessional(id) {

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
          console.error(error);
        });
    },

    blockProfessional(id) {

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
          console.error(error);
        });
    },


    updateService(serviceDetails) {

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
          console.error(error);
        });
    },
    fetchServices() {

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
          console.error(error);
        });

    },



    getServiceDetails(id) {
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
          console.error(error);
        });
    },



    startEditing(id) {
      this.showEditModal()
      this.getServiceDetails(id)
    },

    async deleteService(id) {
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
        console.error("Error deleting service:", error);
      }
    },
    // async logout() {
    //   localStorage.removeItem('jwt');
    //   localStorage.removeItem('role');
    //   if (this.$route.path != '/') {
    //     this.$router.push('/')
    //   }
    // }
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
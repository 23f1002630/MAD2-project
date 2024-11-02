<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Admin Dashboard</h2>
      <nav>
        <a href="#" class="mx-2">Home</a>
        <a href="#" class="mx-2">Search</a>
        <a href="#" class="mx-2">Stats</a>
        <a class="mx-2" style="cursor:pointer" @click="logout">Logout</a>
      </nav>
    </div>

    <div class="card mb-2">
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
            <tr>
              <td>1</td>
              <td>Service A</td>
              <td>\$100</td>
              <td>Service A Description</td>
              <td class="text-center">
                <button class="btn btn-primary btn-sm me-2">Edit</button>
                <button class="btn btn-danger btn-sm">Delete</button>
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
                <button class="btn btn-primary btn-sm me-2">Edit</button>
                <button class="btn btn-danger btn-sm">Block</button>
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
            <h1 class="modal-title fs-5" id="serviceModalLabel">New Service</h1>
            <button @click="mymodal"></button>
          </div>
          <div class="modal-body">
            <form @submit.prevent="addService">
              <div class="mb-3">
                <label for="service-name" class="col-form-label">Service:</label>
                <select class="form-control" id="service-name" v-model="newService.service">
                  <option value="" disabled selected>Select service</option>
                  <option value="cleaningservices">Cleaning Services</option>
                  <option value="maintenanceandrepair">Maintenance and Repair</option>
                  <option value="landscapingandgardening">Landscaping and Gardening</option>
                  <option value="pestcontrol">Pest Control</option>
                  <option value="homeimprovementandrenovation">Home Improvement and Renovation</option>
                  <option value="securityandsafety">Security and Safety</option>
                  <option value="movingandstorage">Moving and Storage</option>
                  <option value="specialtyservices">Specialty Services</option>
                  <option value="organizinganddecluttering">Organizing and Decluttering</option>
                  <option value="petservices">Pet Services</option>
                </select>
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
  </div>
</template>

<script>
import bootstrap from 'bootstrap/dist/js/bootstrap.bundle.js';
import axios from 'axios';

export default {
  name: 'AdminDash',
  data() {
    return {
      professionals: [], // Initialize an empty array to store professionals
      myModal: null,
      serviceform: false,
      newService: {
        "service": '',
        "description": '',
        "price": ''
      }
    };
  },
  mounted() {
    this.fetchProfessionals();
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
    async addService() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.post('http://127.0.0.1:5000/api/services', this.newService, {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`
          },
          withCredentials: true
        });
        console.log("Service added:", response.data);
        // Optionally, refresh the list of services or clear the form
        this.newService = { service: '', description: '', price: '' };
        // Close the modal
        this.myModal.hide()
  
        
      } catch (error) {
        console.error("Error adding service:", error);
      }
    },
    async logout() {
      localStorage.removeItem('jwt');
      localStorage.removeItem('role');
      if (this.$route.path != '/') {
        this.$router.push('/')
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
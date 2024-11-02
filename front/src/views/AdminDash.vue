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
      <button class="btn btn-success btn-sm">+ New Services</button>
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
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'AdminDash',
  data() {
    return {
      professionals: [] // Initialize an empty array to store professionals
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
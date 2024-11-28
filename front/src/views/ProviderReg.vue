<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="container">
      <!-- Home Button -->
      <div class="home-button">
        <button @click="goHome" class="btn btn-outline-primary">Home</button>
      </div>
      <h2 class="text-center mb-4 text-primary">Service provider Registration</h2>
      <form @submit.prevent="register">
        <div class="row mb-3">
          <div class="col">
            <input type="email" class="form-control" placeholder="Email" v-model="emailid" />
          </div>
          <div class="col">
            <select class="form-control" v-model="selectedservice">
              <option v-for="service in services" :key="service.id" :value="service.id">{{ service.services }}</option>
            </select>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="password" class="form-control" placeholder="Password" v-model="password" />
          </div>
          <div class="col">
            <input type="text" class="form-control" placeholder="Experience in years" v-model="experience" />
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <label for="image" class="form-label">Choose image</label>
            <input type="file" class="form-control" placeholder="Image" accept="image/png, image/jpeg"
              @change="handleImageUpload" />
          </div>
          <div class="col">
            <label for="file" class="form-label">Choose file</label>
            <input type="file" class="form-control" placeholder="Attach document" accept="application/pdf"
              @change="handleFileUpload" />
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="text" class="form-control" placeholder="Phone no" v-model="phone" />
          </div>
          <div class="col">
            <input type="text" class="form-control" placeholder="Location" v-model="address" />
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="text" class="form-control" placeholder="Full name" v-model="fullname" />
          </div>
          <div class="col">
            <input type="text" class="form-control" placeholder="Pincode" v-model="pincode" />
          </div>
        </div>
        <div class="text-center">
          <button type="submit" class="btn btn-primary">Sign up</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
      services: [],
      emailid: '',
      fullname: '',
      password: '',
      address: '',
      pincode: '',
      phone: '',
      experience: '',
      services: '',
      selectedservice: null,
      file: null,
      image: null, // Add a data property for the file
    };
  },
  mounted() {
    this.fetchServices();
  },
  methods: {
    handleFileUpload(event) {
      this.file = event.target.files[0]; // Get the file from the input
    },
    handleImageUpload(event) {
      console.log('starting');
      this.image = event.target.files[0]; // Get the file from the input
      console.log('ended');
    },
    async register() {
      try {
        const formData = new FormData();
        formData.append('emailid', this.emailid);
        formData.append('fullname', this.fullname);
        formData.append('password', this.password);
        formData.append('address', this.address);
        formData.append('pincode', this.pincode);
        formData.append('phone', this.phone);
        formData.append('experience', this.experience);
        formData.append('services', this.selectedservice);
        formData.append('file', this.file); // Append the file
        formData.append('image', this.image);

        const response = await axios.post('http://127.0.0.1:5000/provider/register', formData, {
          headers: {
            'Content-Type': 'multipart/form-data', // Set the content type to multipart/form-data
          },
        });

        console.log(this.emailid, this.password, this.fullname, this.phone, this.address, this.pincode, this.experience, this.services, this.file, this.image);

        if (response.status === 201) {
          this.$router.push('/');
        } else {
          alert(response.data.error);
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    },
    async fetchServices() {
      try {
        let your_jwt_token = localStorage.getItem('jwt');
        const response = await axios.get('http://127.0.0.1:5000/api/services', {
          headers: {
            Authorization: `Bearer ${your_jwt_token}`,
          },
          withCredentials: true,
        });
        this.services = response.data;
        console.log(this.services);
      } catch (error) {
        console.error('Error fetching services:', error);
      }
    },
    goHome() {
      this.$router.push('/'); // Redirect to the home page
    },
  },
};
</script>

<style scoped>
.container {
  max-width: 600px;
  border: 1px solid #ccc;
  padding: 20px;
  border-radius: 10px;
  background-color: #f9f9f9;
}

* {
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
}

.home-button {
  position: absolute;
  top: 20px;
  right: 20px;
}
</style>
<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="container">
      <h2 class="text-center mb-4 text-primary">Service provider Registration</h2>
      <form @submit.prevent="register">
        <div class="row mb-3">
          <div class="col">
            <input type="email" class="form-control" placeholder="Email" v-model="emailid" />
          </div>
          <div class="col">
            <select class="form-control" v-model="services">
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
          <!-- <div class="col">
            <input type="password" class="form-control" placeholder="Confirm password" />
          </div> -->
          <!-- <div class="col">
            <input type="file" class="form-control" placeholder="Attach document" />
          </div> -->
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="text" class="form-control" placeholder="Phone no" v-model="phone" />
          </div>
          <div class="col">
            <input type="text" class="form-control" placeholder="Address" v-model="address" />
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
  name: 'ProviderReg',
  data() {
    return {
      emailid: "",
      fullname:"",
      password: "",
      address: "",
      pincode: "",
      phone:"",
      experience:"",
      services:""
    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/provider/register', 
        {
          "emailid": this.emailid,   // Make sure the field names match the backend expectation
          "fullname":this.fullname,
          "password": this.password,
          "address": this.address,
          "pincode": this.pincode,
          "phone":this.phone,
          "experience":this.experience,
          "services":this.services
        },
        {
          headers: {
            'Content-Type': 'application/json'  // Ensure JSON data is correctly recognized
          }
        });

        console.log(this.emailid, this.password,this.fullname,this.phone, this.address, this.pincode,this.experience,this.services);

        if (response.status === 201) {
          this.$router.push('/');
        } else {
          alert(response.data.error);
        }
      } catch (error) {
        alert('An error occurred: ' + error.message);
      }
    }
  }
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
</style>
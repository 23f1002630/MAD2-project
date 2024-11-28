<template>
  <div class="d-flex justify-content-center align-items-center vh-100">
    <div class="container">
      <h2 class="text-center mb-4 text-primary">Customer Signup</h2>
      <form  @submit.prevent="register">
        <div class="row mb-3">
          <div class="col">
            <input type="email" class="form-control" placeholder="Email"  v-model="emailid" />
          </div>
          <div class="col">
            <input type="text" class="form-control" placeholder="Full name"  v-model="fullname"/>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="password" class="form-control" placeholder="Password"  v-model="password" />
          </div>
          <div class="col">
            <input type="text" class="form-control" placeholder="Location"  v-model="address"/>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="text" class="form-control" placeholder="Pincode"  v-model="pincode"/>
          </div>
        </div>
        <div class="row mb-3">
          <div class="col">
            <input type="text" class="form-control" placeholder="Phone no"  v-model="phone"/>
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
  name: 'CustomerReg',
  data() {
    return {
      emailid: "",
      fullname:"",
      password: "",
      address: "",
      pincode: "",
      phone:"",

    };
  },
  methods: {
    async register() {
      try {
        const response = await axios.post('http://127.0.0.1:5000/customer/register', 
        {
          "emailid": this.emailid,   // Make sure the field names match the backend expectation
          "fullname":this.fullname,
          "password": this.password,
          "address": this.address,
          "pincode": this.pincode,
          "phone":this.phone
        },
        {
          headers: {
            'Content-Type': 'application/json'  // Ensure JSON data is correctly recognized
          }
        });

        console.log(this.emailid, this.password,this.fullname,this.phone, this.address, this.pincode);

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
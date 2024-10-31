<template>
  <div class="container mt-5">
    <div class="row">
      <div class="col-12 d-flex justify-content-between align-items-center mb-4 border-bottom pb-2">
        <h1 class="text-primary">Home Master</h1>
        <a href="/providerreg"><button class="btn btn-outline-primary">Want to provide service?</button></a>
      </div>
      <div class="col-md-6">
        <h2 class="text-secondary">Home services at your doorstep</h2>
        <div class="card p-3 mt-3 bg-light">
          <h5>Login to explore more</h5>
          <form @submit.prevent="login">
            <div class="form-group mb-2">
              <input v-model="email" type="email" class="form-control" placeholder="Email" />
            </div>
            <div class="form-group mb-2">
              <input v-model="password" type="password" class="form-control" placeholder="Password" />
            </div>
            <div class="form-group mb-2">
            <select v-model="role" class="form-control">
              <option value="" disabled selected>Select service</option>
                <option value="admin">Admin</option>
                <option value="customer">Customer</option>
                <option value="provider">Provider</option>
            </select>
            </div>
            <button type="submit" class="btn btn-primary">Login</button>
          </form>
          <div>
          <a href="/customerreg">
            <button class="btn btn-primary">REGISTER</button>
          </a>
          
          </div>
        </div>
        <div class="mt-4 p-3 rounded bg-white">
          <p class="text-muted custom-font-style">
            Transform your home into a sanctuary with our premier household services. Our expert team handles cleaning, organizing, and maintenance with unmatched care and reliability. Enjoy peace of mind as we treat your home like our own, allowing you to focus on what truly matters. Experience the ease of a perfectly managed home today!
          </p>
        </div>
      </div>
      <div class="col-md-6">
        <div class="row">
          <div class="col-6 mb-3">
            <div class="card">
              <img src="/home1.jpg" class="card-img-top rounded" alt="image 1" />
            </div>
          </div>
          <div class="col-6 mb-3">
            <div class="card">
              <img src="/home2.jpeg" class="card-img-top rounded" alt="image 2" />
            </div>
          </div>
          <div class="col-6">
            <div class="card">
              <img src="/home3.jpg" class="card-img-top rounded" alt="image 3" />
            </div>
          </div>
          <div class="col-6">
            <div class="card">
              <img src="/home4.jpeg" class="card-img-top rounded" alt="image 4" />
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
export default {
    name: 'HomeView',
    data() {
        return {
            email: '',
            password: '',
            role:''
        }
    },
    methods: {
        closeCard() {
            this.$router.push('/');
        },
        async login() {
          try {
            const response = await axios.post(
              'http://127.0.0.1:5000/api/login',
              {
                "email": this.email,
                "password": this.password,
                "role":this.role
              });
            if (response.status === 200) {
              if (this.role === 'admin') {
                this.$router.push('/admindash');
            } else if (this.role === 'customer') {
              this.$router.push('/cust_dashboard' ); }
              else if (this.role === 'provider') {
                this.$router.push('/providerdash');
              }
          } 
          else {
              alert(response.data.error);
              throw new Error(response.data.error);
            }}
          catch (error) {
            alert(error)
            console.error('Fetch error:', error);
            alert('Login failed. Please check your credentials and try again.');
          }
        }
    }
}
</script>

<style scoped>
.card {
  border-radius: 10px;
  overflow: hidden;
  border: 1px solid #ddd;
}
.container {
  max-width: 1200px;
}
* {
  font-family: 'Lucida Sans', 'Lucida Sans Regular', 'Lucida Grande', 'Lucida Sans Unicode', Geneva, Verdana, sans-serif;
}
.custom-font-style {
  font-style: italic; /* Change to your desired font style */
  font-weight: 700; /* Adjust font weight if needed */
}
</style>

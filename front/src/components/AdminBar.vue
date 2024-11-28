<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
      <div class="container-fluid">
        <a class="navbar-brand" href="/admindash">Admin Dashboard</a>
        <button
          class="navbar-toggler"
          type="button"
          data-bs-toggle="collapse"
          data-bs-target="#navbarNav"
          aria-controls="navbarNav"
          aria-expanded="false"
          aria-label="Toggle navigation"
        >
          <span class="navbar-toggler-icon"></span>
        </button>
        <div class="collapse navbar-collapse" id="navbarNav">
          <ul class="navbar-nav ms-auto">
            <li class="nav-item">
              <a class="nav-link" href="/admindash">Home</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" href="/adminstats">Stats</a>
            </li>
            <li class="nav-item">
              <a class="nav-link" style="cursor: pointer;" @click="logout">Logout</a>
            </li>
          </ul>
        </div>
      </div>
    </nav>
  </template>
  
  <script>
  export default {
    name: 'AdminBar',
    methods: {
      async logout() {
      localStorage.removeItem('jwt');
      localStorage.removeItem('role');
      localStorage.removeItem('userId');
      if (this.$route.path != '/') {
        this.$router.push('/')
      }
    }
  }
  };
  </script>
  
  <style>
  .navbar-brand {
    font-weight: bold;
    color: #0056b3;
  }
  
  .nav-link {
    color: #0056b3;
    font-size: 18px;
    transition: color 0.3s;
  }
  
  .nav-link:hover {
    color: #003d7a;
  }
  </style>
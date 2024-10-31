<template>
  <div class="container mt-4">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2>Admin Dashboard</h2>
      <nav>
        <a href="#" class="mx-2">Home</a>
        <a href="#" class="mx-2">Search</a>
        <a href="#" class="mx-2">Stats</a>
        <a href="#" class="mx-2">Logout</a>
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
            <!-- Example row -->
            <tr>
              <td>1</td>
              <td>John Doe</td>
              <td>5</td>
              <td>Service A</td>
              <td class="text-center">
                <button class="btn btn-primary btn-sm me-2">Edit</button>
                <button class="btn btn-danger btn-sm">Delete</button>
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
export default {
  name: 'AdminDash',
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
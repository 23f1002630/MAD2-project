<template>
    <nav class="navbar navbar-expand-lg navbar-light bg-light">
        <div class="container-fluid">
            <a class="navbar-brand" href="#">Home Master</a>
            <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav"
                aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                <span class="navbar-toggler-icon"></span>
            </button>
            <div class="collapse navbar-collapse" id="navbarNav">
                <ul class="navbar-nav ms-auto">
                    <li class="nav-item">
                        <a class="nav-link" href="/CustomerDash">Home</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Profile</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="/customersearch">Search</a>
                    </li>
                    <li class="nav-item">
                        <a class="nav-link" href="#">Stats</a>
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
    name: 'CustomerBar',
    methods: {
        async logout() {
            localStorage.removeItem('jwt');
            localStorage.removeItem('role');
            if (this.$route.path != '/') {
                this.$router.push('/')
            }
        }
    }
}
</script>

<style scoped>
.navbar {
    font-family: 'Comic Sans MS', cursive, sans-serif;
    border-radius: 8px;
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.nav-link {
    color: #1e90ff !important;
    font-size: 18px;
    transition: color 0.3s;
}

.nav-link:hover {
    color: #ff4500 !important;
}
</style>
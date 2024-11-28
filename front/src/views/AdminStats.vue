<template>
    <header>
        <AdminBar />
    </header>
    <div class="container mt-4">
        <div class="card shadow-lg">
            <div class="card-header bg-primary text-white text-center">
                <h1 class="h4 mb-0">Booking Status Bar Graph</h1>
            </div>
            <div class="card-body text-center">
                <div v-if="graphUrl">
                    <img :src="graphUrl" alt="Bar Graph" class="img-fluid rounded">
                </div>
                <div v-else>
                    <div class="spinner-border text-primary" role="status">
                        <span class="visually-hidden">Loading...</span>
                    </div>
                    <p class="mt-3 text-muted">Loading graph, please wait...</p>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import AdminBar from '../components/AdminBar.vue';
export default {
    name: 'BarGraph',
    components: {
        AdminBar
    },

    data() {
        return {
            graphUrl: null
        };
    },
    created() {
        this.fetchGraph();
    },
    methods: {
        async fetchGraph() {
            try {
                const response = await fetch('http://localhost:5000/api/status-bar-graph');
                const blob = await response.blob();
                this.graphUrl = URL.createObjectURL(blob);
            } catch (error) {
                console.error('Error fetching the graph:', error);
            }
        }
    }
}
</script>

<style scoped>
.card {
    border-radius: 10px;
    overflow: hidden;
}

.card-header {
    font-weight: bold;
    letter-spacing: 0.5px;
}

.img-fluid {
    max-height: 500px;
    object-fit: contain;
    border: 1px solid #ddd;
    padding: 5px;
    background-color: #f8f9fa;
}

.spinner-border {
    width: 3rem;
    height: 3rem;
}
</style>
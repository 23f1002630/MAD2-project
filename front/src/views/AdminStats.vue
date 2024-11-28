<template>
    <header>
        <AdminBar />
    </header>
    <div class="card mb-2 container">
        <h1>Booking Status Bar Graph</h1>
        <img v-if="graphUrl" :src="graphUrl" alt="Bar Graph">
        <p v-else>Loading...</p>
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
img {
    max-width: 100%;
    height: auto;
}
</style>
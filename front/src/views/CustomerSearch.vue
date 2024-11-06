<template>
    <div class="container mt-5">
        <CustomerBar />
        <div class="row justify-content-center mb-4 container">
            <div class="col-md-8">
                <div class="input-group">
                    <input type="text" class="form-control" placeholder="Search for services..." />
                    <button class="btn btn-primary" type="button">Search</button>
                </div>
            </div>
        </div>
        <div class="row justify-content-center">
            <div class="col-md-3" v-for="card in cards" :key="card.id">
                <div class="card mb-4">
                    <div class="card-body">
                        <h5 class="card-title">Service: {{ card.service }}</h5>
                        <p class="card-text">Provider: {{ card.provider }}</p>
                        <p class="card-text">Price: {{ card.price }}</p>
                        <p class="card-text">Description: {{ card.description }}</p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<script>
import CustomerBar from '../components/CustomerBar.vue';
export default {
    name: 'CustomerSearch',
    components: {
        CustomerBar
    },
    data() {
        return {
            cards: [
                { id: 1, service: 'Service 1', provider: 'Provider 1', price: '\$100', description: 'Description 1' },
                { id: 2, service: 'Service 2', provider: 'Provider 2', price: '\$200', description: 'Description 2' },
                { id: 3, service: 'Service 3', provider: 'Provider 3', price: '\$300', description: 'Description 3' },
            ],
        };
    },
};
</script>

<style>
.container {
    margin-top: 50px;
}

.card {
    border-radius: 10px;
    box-shadow: 0 2px 5px rgba(0, 0, 0, 0.1);
}
</style>
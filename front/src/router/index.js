import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProviderReg from '../views/ProviderReg.vue';
import CustomerReg from '../views/CustomerReg.vue';
import AdminDash from '../views/AdminDash.vue';
import ProviderDash from '../views/ProviderDash.vue';
import CustomerDash from '../views/CustomerDash.vue';
import CustomerSearch from '../views/CustomerSearch.vue';


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'home',
            component: HomeView
        },
        {
            path: '/providerreg',
            name: 'provider',
            component: ProviderReg
        },
        {
            path: '/customerreg',
            name: 'CustomerReg',
            component: CustomerReg
        },
        {
            path: '/admindash',
            name: 'AdminDash',
            component: AdminDash
        },
        {
            path: '/providerdash',
            name: 'ProviderDash',
            component: ProviderDash
        },
        {
            path: '/customerdash',
            name: 'CustomerDash',
            component: CustomerDash
        },
        {
            path: '/customersearch',
            name: 'CustomerSearch',
            component: CustomerSearch
        }

    ]
});


export default router;
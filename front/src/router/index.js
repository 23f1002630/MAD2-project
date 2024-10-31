import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProviderReg from '../views/ProviderReg.vue';
import CustomerReg from '../views/CustomerReg.vue';
import AdminDash from '../views/AdminDash.vue';


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
            path: '/register_cust',
            name: 'CustomerReg',
            component: CustomerReg
        },
        {
            path: '/admindash',
            name: 'AdminDash',
            component: AdminDash
        }

    ]
})

export default router;
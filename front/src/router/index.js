import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import ProviderReg from '../views/ProviderReg.vue';
import CustomerReg from '../views/CustomerReg.vue';
import AdminDash from '../views/AdminDash.vue';
import ProviderDash from '../views/ProviderDash.vue';
import CustomerDash from '../views/CustomerDash.vue';
import AdminStats from '../views/AdminStats.vue';


const router = createRouter({
    history: createWebHistory(),
    routes: [
        {
            path: '/',
            name: 'HomeView',
            component: HomeView
        },
        {
            path: '/providerreg',
            name: 'ProviderReg',
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
          path: '/adminstats',
          name: 'AdminStats',
          component: AdminStats
        }

    ]
});

// router.beforeEach((to, from, next) => {
//     if (to.name !== 'HomeView' && !localStorage.getItem('jwt') && 
//         to.name !== 'CustomerReg' && to.name !== 'ProviderReg') {
//       next({ name: 'HomeView' })
//     } else {
//       next()
//     }
//   })

router.beforeEach((to, from, next) => {
    const token = localStorage.getItem('jwt');
    const role = localStorage.getItem('role');
  
    // Public routes that don't require authentication
    const publicRoutes = ['HomeView', 'CustomerReg', 'ProviderReg'];
    
    // Routes that require admin access
    const adminRoutes = ['AdminDash']; // Add other admin routes as needed
    const customerRoutes = ['CustomerDash', 'CustomerSearch'];
    const providerRoutes = ['ProviderDash'];

    if (!token && !publicRoutes.includes(to.name)) {
      // If no token and trying to access protected route
      next({ name: 'HomeView' });
    } else if (adminRoutes.includes(to.name) && role !== 'admin') {
      // If trying to access admin route but not an admin
      next({ name: 'HomeView' });
    } else if (customerRoutes.includes(to.name) && role !== 'customer') {
      // If trying to access customer route but not a customer
      next({ name: 'HomeView' });
    } else if (providerRoutes.includes(to.name) && role !== 'provider') {
      // If trying to access provider route but not a provider
      next({ name: 'HomeView' });
    } else {
      next();
    }
  });

export default router;
import { createApp } from 'vue'
import { createRouter, createWebHistory } from 'vue-router'
import './style.css'
import 'flowbite';
import 'tw-elements';
import App from './App.vue';
import VueCookies from 'vue3-cookies'

const routes = [
    { path: '/', component: App },
  ]
  
  // 3. Create the router instance and pass the `routes` option
  // You can pass in additional options here, but let's
  // keep it simple for now.
  const router = createRouter({
    // 4. Provide the history implementation to use. We are using the hash history for simplicity here.
    history: createWebHistory(),
    routes, // short for `routes: routes`
  })

createApp(App)
.use(router)
.use(VueCookies, {
    expireTimes: "30d",
    path: "/",
    domain: "",
    secure: false,
    sameSite: "None"
})
.mount('#app')

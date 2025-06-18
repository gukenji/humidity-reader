import { createRouter, createWebHistory } from "vue-router";

// importa suas views
import Dashboard from "@/views/Dashboard.vue";
import RegisterPlant from "@/views/RegisterPlant.vue";
import PlantDetails from "@/views/PlantDetails.vue";

const routes = [
  {
    path: "/",
    redirect: "/dashboard",
  },
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
  },
  {
    path: "/register",
    name: "RegisterPlant",
    component: RegisterPlant,
  },
  {
    path: "/plant/:id",
    name: "PlantDetails",
    component: PlantDetails,
    props: true, // permite acessar o id como prop
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;

import MainPage from "@/pages/MainPage";
import {createRouter, createWebHistory} from "vue-router";

const routes = [
    {
        path: '/v1',
        name: "main-page",
        component: MainPage,
    },
]


const router = createRouter({
    routes,
    history: createWebHistory("/"),
    //history: createWebHistory(process.env.BASE_URL)
})

export default router;
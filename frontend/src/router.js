import { createWebHistory, createRouter } from "vue-router";
import Index from "./components/Index";
import Home from "./components/Home.vue";

const routes = [
  //一级路由
  { path: "/home", name: "Hone", component: Home },
  {
    path: "/index",
    name: "Index",
    component: Index,
    //路由嵌套
    children: [
      {
        path: "/index/menu1",
        component: () => import("./components/Main1.vue"),
      },
      {
        path: "/index/menu2",
        component: () => import("./components/Main2.vue"),
      },
      {
        path: "/index/menu3",
        component: () => import("./components/Main3.vue"),
      },
    ],
  },
];

const router = createRouter({
  history: createWebHistory(),
  routes: routes,
});

export default router;

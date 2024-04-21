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
        path: "/index/plot_opt",
        component: () => import("./components/PlotOpt.vue"),
      },
      {
        path: "/index/plot_ep",
        component: () => import("./components/PlotEP.vue"),
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

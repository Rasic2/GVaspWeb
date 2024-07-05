import { createApp } from "vue";
import App from "./App.vue";

import ElementPlus from "element-plus";
import "element-plus/dist/index.css";
import * as ElementPlusIconsVue from "@element-plus/icons-vue";

import * as echarts from "echarts";
import axios from "axios";

import router from "./router";

const app = createApp(App);
app.config.globalProperties.$echarts = echarts;
app.config.globalProperties.$axios = axios;

app.use(ElementPlus).use(router);

for (const [key, component] of Object.entries(ElementPlusIconsVue)) {
  app.component(key, component);
}

app.mount("#app");

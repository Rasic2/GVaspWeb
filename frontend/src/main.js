import { createApp } from "vue";
import App from "./App.vue";
import * as echarts from "echarts";
import axios from "axios";

const app = createApp(App);
app.config.globalProperties.$echarts = echarts;
app.config.globalProperties.$axios = axios;

app.mount("#app");

import { createApp } from "vue";
import App from "./App.vue";
import CatInput from "./components/input.vue";

createApp(App).component(CatInput.name, CatInput).mount("#app");

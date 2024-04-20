<template>
  <div id="app">
    <!-- <router-link to="/index"> Index </router-link> | -->
    <!-- <router-link to="/about"> 关于 </router-link> -->
    <!-- <Index msg="GVasp 可视化" /> -->
  </div>
  <router-view />
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
// import CatInput from "./components/input.vue";
// import SliderInput from "./components/slider-dual.vue"
// import MyEcharts from "./components/Echarts.vue";
// import MyAside from "./components/Aside.vue";
// import MyAxios from "./components/Axios.vue";
// import MyMol from "./components/3dmol.vue";
// import Index from "./components/Index.vue";

export default {
  name: 'App',
  components: {
    // HelloWorld
    // CatInput,
    // SliderInput,
    // MyEcharts,
    // MyAxios,
    // MyMol,
    // MyAside
    // Index
  },
  // data() {
  //   return {
  //     svg: require("../../static/image.svg"),
  //     uname: "",
  //     upwd: "",
  //     // 输入框v-model数据
  //     val: "",
  //     // 提示语显示与否的标志位，默认隐藏
  //     flag: false,
  //   }
  // },

  // created() {
  //   this.$nextTick(() => {
  //     this.handleMax();
  //   });
  // },

  // methods: {
  //   change(e) {
  //     const boolNum = !isNaN(parseFloat(e.target.value)) && isFinite(e.target.value);
  //     if (!boolNum) {
  //       this.flag = true;
  //     } else {
  //       this.flag = false;
  //     }
  //   },
  //   handleMax() {
  //     this.$refs["sliderData"].max = 1000
  //   }
  // }
}

</script>


<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

.cat-input {
  margin-bottom: 10px;
}

.ff-hide {
  color: red;
}
</style> -->
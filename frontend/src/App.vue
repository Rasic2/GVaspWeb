<template>
  <h1>GVasp 态密度图绘制</h1>

  <div>
    <Cat-input placeholder="请输入线宽" type="text" v-model="uname" clearable></Cat-input>
    <!-- <br /> -->
    <!-- <Cat-input placeholder="禁用的输入框" disabled></Cat-input> -->
    <!-- <br /> -->
    <!-- <Cat-input placeholder="请输入密码" v-model="upwd" show-password></Cat-input> -->
  </div>

  <div class="ff-hide">
    <input type="text" v-model="val" @input="change" maxlength="10" />
    <br />
    <span v-show="flag">格式错误</span>
  </div>

  <img :src="svg" alt />
  <!-- <embed src="../../static/image.svg" /> -->
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'
import CatInput from "./components/input.vue";

export default {
  name: 'App',
  components: {
    // HelloWorld
    CatInput
  },
  data() {
    return {
      svg: require("../../static/image.svg"),
      uname: "",
      upwd: "",
      // 输入框v-model数据
      val: "",
      // 提示语显示与否的标志位，默认隐藏
      flag: false,
    }
  },
  methods: {
    change(e) {
      const boolNum = !isNaN(parseFloat(e.target.value)) && isFinite(e.target.value);
      if (!boolNum) {
        this.flag = true;
      } else {
        this.flag = false;
      }
    },
  }
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
</style>
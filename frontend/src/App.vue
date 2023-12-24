<template>
  <h1>GVasp 态密度图绘制</h1>

  <div>
    <Cat-input placeholder="请输入用户名" type="text" v-model="uname" clearable></Cat-input>
    <br />
    <Cat-input placeholder="禁用的输入框" disabled></Cat-input>
    <br />
    <Cat-input placeholder="请输入密码" v-model="upwd" show-password></Cat-input>
  </div>

  <img :src="svg" alt />
  <!-- <embed src="../../static/image.svg" /> -->
  <!-- <img alt="Vue logo" src="./assets/logo.png"> -->
  <!-- <HelloWorld msg="Welcome to Your Vue.js App"/> -->
</template>

<script>
// import HelloWorld from './components/HelloWorld.vue'

export default {
  name: 'App',
  // components: {
  //   HelloWorld
  // }
  data() {
    return {
      svg: require("../../static/image.svg"),
      uname: "",
      upwd: "",
    }
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
</style>
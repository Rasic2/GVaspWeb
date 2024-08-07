<template>
  <el-container>
    <el-header>
      <Header></Header>
    </el-header>
    <el-container>
      <el-aside width="200px">
        <Aside></Aside>
      </el-aside>
      <el-main>
        <router-view></router-view>
      </el-main>
    </el-container>
    <el-footer>© Copyright 2024, Hui Zhou. All Rights Reserved.</el-footer>
  </el-container>
</template>

<script>
import Header from "./Header.vue"
import Aside from "./Aside.vue"

export default {
  name: 'MyIndex',
  components: {
    Aside,
    Header
  },
  props: {
    msg: String
  }
}
</script>

<style>
.el-header,
.el-footer {
  background-color: #F7FAFE;
  color: #333;
  line-height: 60px;
}

.el-footer {
  text-align: left;
}

.el-aside {
  background-color: #F7FAFE;
  color: #333;
  text-align: center;
  line-height: 200px;
}

.el-main {
  background-color: #F7FAFE;
  color: #333;
  text-align: center;
}

body>.el-container {
  width: 100%;
  height: 100%;
}
</style>

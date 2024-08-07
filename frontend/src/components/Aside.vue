<template>
  <div>
    <el-menu background-color="#F7FAFE" text-color="black" active-text-color="#5138FF" class="el-menu-vertical-demo"
      router>
      <el-menu-item index="/index/vis_traj">轨迹可视化</el-menu-item>
      <el-menu-item index="/index/plot_opt">结构优化</el-menu-item>
      <el-menu-item index="/index/plot_ep">静电势</el-menu-item>
      <el-menu-item index="/index/plot_band">能带图</el-menu-item>
      <el-menu-item index="/index/plot_dos">态密度</el-menu-item>
      <el-menu-item index="/index/plot_pes">能垒图</el-menu-item>
    </el-menu>
  </div>
</template>

<script>
export default {
  name: "MyAside"
}
</script>

<style scoped>
.el-menu-vertical-demo {
  height: 100%;
}

.el-menu .el-menu-item {
  width: 80%;
  margin-left: 10%;
}

.el-menu .el-menu-item:hover {
  background-color: #ECEEF8 !important;
  color: black !important;
  border-radius: 10px;
  width: 80%;
  margin-left: 10%;
}

.el-menu .el-menu-item.is-active {
  background-color: #5138FF !important;
  color: white !important;
  border-radius: 10px;
  width: 80%;
  margin-left: 10%;
}
</style>

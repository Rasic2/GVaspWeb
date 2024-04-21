<template>
  <div id="info">
    <el-alert
        title="info alert"
        type="success"
        description="下方是输入框"
        show-icon
    />
  </div>
  <div class="containerDisplay">
    <div id="inputXYZ">
      <el-input type="textarea" rows="20" v-model="xyzContent" :placeholder="placeHolder1"/>
      <button @click="display">display</button>
    </div>
    <div id="displayMol"></div>
  </div>
</template>

<script>

import {ref} from "vue";
import $ from "jquery";

export default {
  name: 'XyzDisplay3D',
  setup(){
    let placeHolder1=`请输入xyz格式的信息,第一行为总原子数,第二行为标题,第三行以及以后是原子三维坐标`
    let xyzContent = ref(``);
    let display = ()=>{
      // eslint-disable-next-line no-undef
      let element = $('#displayMol');
      let config = {backgroundColor: 'white'};
      // eslint-disable-next-line no-undef
      import("3dmol/build/3Dmol-min").then(($3Dmol)=>{
        const viewer1 = $3Dmol.createViewer(element, config);
        viewer1.addModel(xyzContent.value, "vasp"); // 需要去掉 Selective 行
        viewer1.setStyle({stick:{radius: 0.1},sphere:{radius:0.3}});
        viewer1.render();
        viewer1.zoomTo();
        })
    }
    return {xyzContent,placeHolder1,display}
  },


}
</script>

<style scoped>
#info{
  margin-top: 50px;
  margin-left: 25px;
  width: 500px;
}
#inputXYZ{
  width: 500px;
}
#displayMol{
  height: 430px;
  width: 800px;
  position: relative;
}
.containerDisplay{
  margin-left: 25px;
  margin-top: 50px;
  display: flex;
}
</style>
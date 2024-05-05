<template>
  <div class="containerDisplay">
    <div id="inputXYZ">
      <el-input type="textarea" rows="20" v-model="xyzContent" :placeholder="placeHolder1"/>
      <button @click="display">display</button>
    </div>
    <div id="displayMol"></div>
  </div>
  <div id="selectAtom">
    <ul>
      <li v-for="(item, index) in items" :key='index'>{{item}}</li>
    </ul>
  </div>
</template>

<script>

import {onMounted, ref} from "vue";
import $ from "jquery";

export default {
  name: 'XyzDisplay3D',
  methods: {
  },
  setup(){
    let placeHolder1=`请输入xyz格式的信息,第一行为总原子数,第二行为标题,第三行以及以后是原子三维坐标`
    let xyzContent = ref(` C  H 
 1.0000000000000000
    11.0000000000000000    0.0000000000000000    0.0000000000000000
     0.0000000000000000   12.0000000000000000    0.0000000000000000
     0.0000000000000000    0.0000000000000000   13.0000000000000000
 C   H  
   1   4
S
Cartesian
  5.1754311300009999  5.7887874483599999  7.2899531736589998 T T T
  5.5377911300030007  5.2763374483679994  6.4024631736649997 T T T
  4.0884311300030003  5.7887874483599999  7.2899531736589998 T T T
  5.5377311300080008  6.8136174483600005  7.2899531736589998 T T T
  5.5377711300009995  5.2764274483680005  8.1775131736609996 T T T
`);
let items=ref([])
    let display = ()=>{
      // eslint-disable-next-line no-undef
      let element = $('#displayMol');
      let config = {backgroundColor: 'white'};
      // eslint-disable-next-line no-undef
      import("/Users/hui_zhou/Project/3Dmol.js/build/3Dmol-min").then(($3Dmol)=>{
        const viewer1 = $3Dmol.createViewer(element, config);
        let m = viewer1.addModel(xyzContent.value, "vasp");
        viewer1.addUnitCell(m);
        viewer1.setStyle({stick:{radius: 0.1},sphere:{radius:0.3}});
        viewer1.setHoverable({},true,function(atom,viewer1) {
          if(!atom.label) {
            atom.label = viewer1.addLabel(atom.elem+` (${atom.x.toFixed(2)}, ${atom.y.toFixed(2)}, ${atom.z.toFixed(2)})`,{position: atom, backgroundColor: 'mintcream', fontColor:'black'});
          }
        },
          function(atom) {
            if(atom.label) {
              viewer1.removeLabel(atom.label);
              delete atom.label;
            }
          },
        )
        viewer1.setClickable({},true,function(atom,viewer1) {
          if(!atom.label){
            atom.label = viewer1.addLabel(atom.resn+":"+atom.atom,{position: atom, backgroundColor: 'darkgreen', backgroundOpacity: 0.8});
            // let selectAtomDiv = document.getElementById('selectAtom');
            // let selectAtomP = document.createElement("div")
            // console.log(atom.label)
            // selectAtomP.innerHTML = atom.elem
            // selectAtomDiv.appendChild(selectAtomP)
            items.value.push(atom.elem)
            console.log(items.value)
          }else{
            viewer1.removeLabel(atom.label)
            delete atom.label
            items.value.pop()
          }
      });
        viewer1.render();
        viewer1.zoomTo();
        })
    }
    onMounted(display)
    return {xyzContent,placeHolder1,display,items}
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
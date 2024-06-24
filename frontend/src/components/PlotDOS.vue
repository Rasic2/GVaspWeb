<template>
  <div class="atomSelect">
    <h1>原子/轨道选择</h1>
    <div class="singleAtom" v-for="(item, index) in items" :key="index">
      <div class="inputLDOS">
        <div class="iconLayout">
          <el-icon @click="removeItem(index)">
            <RemoveFilled />
          </el-icon>
        </div>
        <div class="singleAtomInputPlus">
          <div class="singleAtomInput">
            <el-input
              class="input"
              v-model="item.input"
              @input="inputAtom(index)"
              placeholder="Please input atom index"
            />
            <div class="iconLayout">
              <el-icon @click="showStructure(index)">
                <Management />
              </el-icon>
            </div>
            <el-radio-group v-model="item.radio" class="inputRadio">
              <el-radio value="1" size="large">LDOS</el-radio>
              <el-radio value="2" size="large">PDOS</el-radio>
            </el-radio-group>
          </div>
          <!-- 子组件访问父组件的值 -->
          <xyz-display
            :sIndex="index"
            :sItem="item"
            v-model="item.structure"
            class="structureDisplay"
            @viewer-created="handleViewerCreated"
            ref="childRef"
          ></xyz-display>
        </div>
      </div>
      <div v-if="item.radio == 2" class="inputPDOS">
        <checkbox-pdos :l-orbital="'s'" :orbitals="[]"></checkbox-pdos>
        <checkbox-pdos
          :l-orbital="'p'"
          :orbitals="['px', 'py', 'pz']"
        ></checkbox-pdos>
        <checkbox-pdos
          :l-orbital="'d'"
          :orbitals="['d1', 'd2', 'd3', 'd4', 'd5']"
        ></checkbox-pdos>
        <checkbox-pdos
          :l-orbital="'f'"
          :orbitals="['f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']"
        ></checkbox-pdos>
      </div>
    </div>
    <el-button @click="addItem" class="expand_btn">+ 添加原子</el-button>
    <el-row>
      <el-col :span="6">
        <el-checkbox v-model="checked1" label="Total DOS" />
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6" :offset="18">
        <el-button @click="plot">绘制</el-button>
      </el-col>
    </el-row>
  </div>
</template>

<script>
export default {
  name: "PlotDOS",
};
</script>

<script setup>
import { ref, provide } from "vue";
import CheckboxPdos from "@/components/CheckboxPdos.vue";
import XyzDisplay from "@/components/StructureDisplay.vue";
import $ from "jquery";

// 父组件定义变量，共享给子组件（provide，inject）
const defaultStyle = {
  stick: { radius: 0.2, colorscheme: "Jmol" },
  sphere: { scale: 0.35, colorscheme: "Jmol" },
};
const newStyle = {
  stick: { radius: 0.2, color: "yellow" },
  sphere: { scale: 0.35, color: "yellow" },
};
provide("defaultStyle", defaultStyle);
provide("newStyle", newStyle);

// 父组件通过 Ref 更新子组件的值
const childRef = ref(null);

const items = ref([]);

const addItem = () => {
  items.value.push({ radio: "1", display: "none", input: "", structure: "" });
};
const removeItem = (index) => {
  items.value.splice(index, 1);
};
const showStructure = (index) => {
  const structureDisplay = $(".structureDisplay");
  if (items.value[index]["display"] === "none") {
    $(structureDisplay[index]).show();
    $(structureDisplay[index]).css("display", "flex");
    items.value[index]["display"] = "flex";
  } else {
    $(structureDisplay[index]).css("display", "none");
    items.value[index]["display"] = "none";
  }
};

const inputAtom = (index) => {
  const inputAtomIndex = parseInt(items.value[index]["input"], 10);
  console.log(inputAtomIndex);
  let viewer = items.value[index]["structure"];
  viewer.setStyle({}, defaultStyle);
  if (inputAtomIndex) {
    viewer.setStyle({ index: inputAtomIndex }, newStyle);
    childRef.value[index].atoms = []
    childRef.value[index].atoms.push(inputAtomIndex);
    viewer.render();
  }
};
const handleViewerCreated = (index, viewer) => {
  // 父组件获得子组件创建的 Viewer
  console.log("3Dmol Viewer instance:", viewer);
  items.value[index]["structure"] = viewer;
  console.log(items.value);
};
</script>

<style scoped>
.atomSelect {
  width: 600px;
  padding-bottom: 20px;
  padding-top: 1px;
  -webkit-box-shadow: #666 0px 0px 10px;
  -moz-box-shadow: #666 0px 0px 10px;
  box-shadow: #666 0px 0px 10px;
  background: #eeff99;
  float: left;
}

.expand_btn {
  width: 80px;
  display: flex;
  margin-top: 5px;
  margin-left: 25px;
}

#info {
  margin-top: 50px;
  margin-left: 25px;
  width: 500px;
}

#inputXYZ {
  width: 500px;
}

#displayMol {
  height: 430px;
  width: 800px;
  position: relative;
}

.containerDisplay {
  margin-left: 25px;
  margin-top: 50px;
  display: flex;
}

.inputLDOS {
  display: flex;
}

.singleAtomInput {
  display: flex;
  margin-bottom: 5px;
}

.iconLayout {
  display: flex;
  align-items: center;
  height: 30px;
  padding: 0 5px;
}

.input {
  height: 30px;
  width: 200px;
}

.inputRadio {
  height: 30px;
  align-items: center;
  display: flex;
  vertical-align: middle;
  flex-wrap: nowrap;
  padding: 0 20px;
}

.structureDisplay {
  align-items: center;
  vertical-align: middle;
  flex-wrap: nowrap;
  display: none;
}
</style>
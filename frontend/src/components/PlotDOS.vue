<template>
  <div class="atomSelect">
    <h1>态密度绘制参数设置</h1>
    <el-form
        ref="ruleFormRef"
        :model="ruleForm"
        :rules="rules"
        label-width="auto"
        class="fileUpload"
        :size="formSize"
        status-icon
        label-position="left"
    >
      <el-form-item
          v-for="(item, index) in ['CONTCAR', 'DOSCAR']"
          :key="index"
          :label="item"
          prop="name"
          required
      >
        <file-upload
            :index="index"
            :limitNum="1"
            :type="4"
            :projectId="uploadItems[index].projectId"
            :fileList="uploadItems[index].fileLists"
            @uploadSuccess="handleFileLists"
            @updateFile="updateFileLists"
        ></file-upload>
      </el-form-item>
    </el-form>
    <div class="singleAtom" v-for="(item, index) in items" :key="index">
      <div class="inputLDOS">
        <div class="iconLayout">
          <el-icon @click="removeItem(index)">
            <RemoveFilled/>
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
                <Management/>
              </el-icon>
            </div>
            <el-radio-group v-model="item.radio" class="inputRadio">
              <el-radio value="1" size="large">LDOS</el-radio>
              <el-radio value="2" size="large">PDOS</el-radio>
            </el-radio-group>
          </div>
        </div>
      </div>
      <div v-if="item.radio == 2" class="inputPDOS">
        <checkbox-pdos
            :sIndex="index"
            :l-orbital="'全选'"
            :orbitals="['s']"
            @updateOrbitals="handleUpdateOrbitals"
        ></checkbox-pdos>
        <checkbox-pdos
            :sIndex="index"
            :l-orbital="'全选'"
            :orbitals="['p', 'px', 'py', 'pz']"
            @updateOrbitals="handleUpdateOrbitals"
        ></checkbox-pdos>
        <checkbox-pdos
            :sIndex="index"
            :l-orbital="'全选'"
            :orbitals="['d', 'd1', 'd2', 'd3', 'd4', 'd5']"
            @updateOrbitals="handleUpdateOrbitals"
        ></checkbox-pdos>
        <checkbox-pdos
            :sIndex="index"
            :l-orbital="'全选'"
            :orbitals="['f', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']"
            @updateOrbitals="handleUpdateOrbitals"
        ></checkbox-pdos>
      </div>
      <!-- 子组件访问父组件的值 -->
      <xyz-display
          :sIndex="index"
          :sItem="item"
          v-model="item.structure"
          class="structureDisplay"
          @viewer-created="handleViewerCreated"
      ></xyz-display>
    </div>
    <el-button @click="addItem" class="expand_btn">+ 添加原子</el-button>
    <el-row>
      <el-col :span="6">
        <el-checkbox v-model="checkedTDOS" label="Total DOS"/>
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6" :offset="18">
        <el-button @click="plot" :disabled="plotDisabled">绘制</el-button>
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
import {ref, provide, computed} from "vue";
import CheckboxPdos from "@/components/CheckboxPdos.vue";
import XyzDisplay from "@/components/StructureDisplay.vue";
import FileUpload from "@/components/upload.vue";
import $ from "jquery";

// 父组件定义变量，共享给子组件（provide，inject）
const defaultStyle = {
  stick: {radius: 0.2, colorscheme: "Jmol"},
  sphere: {scale: 0.35, colorscheme: "Jmol"},
};
const newStyle = {
  stick: {radius: 0.2, color: "yellow"},
  sphere: {scale: 0.35, color: "yellow"},
};
provide("defaultStyle", defaultStyle);
provide("newStyle", newStyle);

const atoms = ref([]);
provide("atoms", atoms);
provide("addAtoms", (newValue) => {
  atoms.value.push(newValue);
});
provide("removeAtoms", (atomItem) => {
  atoms.value = atoms.value.filter((item) => item !== atomItem);
});

const items = ref([]);
provide("items", items);
provide("updateItemsInput", (newValue, index) => {
  items.value[index]["input"] = newValue;
});

// Ref Variable
const uploadItem = {
  projectId: "",
  projectName: "",
  scene: [],
  installationSite: [],
  installationSiteOverview: "",
  fileLists: [],
  fileListsOverview: "",
}
const uploadItems = ref([uploadItem, JSON.parse(JSON.stringify(uploadItem))]);

const checkedTDOS = ref(false);

// Computed

/**
 * Whether to disable the plot button.
 *
 * 1. The number of fileLists is not equal to 2
 * 2. Each item in the items array should have a non-empty input and a non-empty orbitals array if the radio is not 1
 * 3. The items array should not be empty if checkedTDOS is false
 */
const plotDisabled = computed(() => {
  // Check if the fileLists length is not equal to 2
  let fileCount = uploadItems.value.reduce((sum, item) => sum + item.fileLists.length, 0);
  if (fileCount !== 2) {
    return true;
  }

  // Check if the items array is empty and checkedTDOS is false
  if (items.value.length === 0 && !checkedTDOS.value) {
    return true;
  }

  // Check each item in the items array
  for (const item of items.value) {
    // Check if the input is empty
    if (item.input.trim() === "") {
      return true;
    }

    // Check if the radio is not 1
    if (item.radio !== "1") {
      // Check if the orbitals array is empty
      if (item.orbitals.length === 0) {
        return true;
      }
    }
  }

  return false;
});

// Methods
const addItem = () => {
  items.value.push({
    radio: "1",
    display: "none",
    input: "",
    orbitals: [],
    structure: "",
  });
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

/**
 * Updates the style of the viewer based on the input atom index and renders the viewer.
 * If the input atom index is valid, it highlights the atom with the new style.
 * Otherwise, it renders the viewer without any highlighting.
 *
 * @param {number} index - The index of the item in the items array.
 * @return {void} This function does not return anything.
 */
const inputAtom = (index) => {
  const inputAtomIndex = parseInt(items.value[index]["input"], 10);
  let viewer = items.value[index]["structure"];
  viewer.setStyle({}, defaultStyle);
  atoms.value = [];
  if (inputAtomIndex) {
    viewer.setStyle({index: inputAtomIndex}, newStyle);
    atoms.value.push(inputAtomIndex);
    viewer.render();
  } else {
    viewer.render();
  }
  console.log(atoms.value);
};

// plot function
const plot = () => {
  console.log(checkedTDOS.value);
};

// 父组件获得子组件创建的 Viewer
const handleViewerCreated = (index, viewer) => {
  items.value[index]["structure"] = viewer;
  console.log(items.value);
};

// 处理配电房上传成功信息
const handleFileLists = (index, file) => {
  console.log("handleFileLists: file", file);
  uploadItems.value[index].fileLists.push(file);
  console.log("handleFileLists: fileLists", uploadItems.value);
};

// 更新配电房文件
const updateFileLists = (index, files) => {
  console.log("updateFileLists: files", files);
  uploadItems.value[index].fileLists = files;
};

/**
 * Handles the update of orbitals in the parent component.
 *
 * @param {String} mode - The mode of operation ('add' or 'remove').
 * @param {Number} index - The index of the item.
 * @param {Array} orbitals - The array of orbitals to be updated.
 * @return {void} This function does not return a value.
 */
const handleUpdateOrbitals = (mode, index, orbitals) => {
  if (!Array.isArray(orbitals)) {
    throw new TypeError("'orbitals' must be an array");
  }
  if (mode === "add") {
    orbitals.forEach((orbital) => {
      items.value[index]["orbitals"].push(orbital);
    });
  } else if (mode === "remove") {
    orbitals.forEach((orbital) => {
      const orbitalIndex = items.value[index]["orbitals"].indexOf(orbital);
      if (orbitalIndex !== -1) {
        items.value[index]["orbitals"].splice(orbitalIndex, 1);
      }
    });
  }
};
</script>

<style scoped>
.atomSelect {
  width: 600px;
  padding-bottom: 20px;
  padding-top: 1px;
  -webkit-box-shadow: #666 0 0 10px;
  -moz-box-shadow: #666 0 0 10px;
  box-shadow: #666 0 0 10px;
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

.fileUpload {
  margin-left: 25px;
  max-width: 600px;
}
</style>

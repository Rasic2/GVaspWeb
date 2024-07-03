<template>
  <div class="atomSelect">
    <h1>态密度绘制参数设置</h1>
    <el-form ref="ruleFormRef" :model="ruleForm" :rules="rules" label-width="auto" class="fileUpload" :size="formSize"
      status-icon label-position="left">
      <el-form-item v-for="(item, index) in ['CONTCAR', 'DOSCAR']" :key="index" :label="item" prop="name" required>
        <file-upload :index="index" :limitNum="1" :type="4" :projectId="uploadItems[index].projectId"
          :fileList="uploadItems[index].fileLists" @uploadSuccess="handleFileLists"
          @updateFile="updateFileLists"></file-upload>
      </el-form-item>
    </el-form>
    <div class="singleAtom" v-for="(item, index) in items" :key="index">
      <div class="inputLDOS">
        <div class="iconLayout">
          <el-icon @click="removeItem(index)">
            <RemoveFilled />
          </el-icon>
        </div>
        <div class="singleAtomInputPlus">
          <div class="singleAtomInput">
            <el-input class="input" v-model="item.input" @input="inputAtom(index)"
              placeholder="Please input atom index" />
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
        </div>
      </div>
      <div v-if="item.radio == 2" class="inputPDOS">
        <checkbox-pdos :sIndex="index" :l-orbital="'全选'" :orbitals="['s']"
          @updateOrbitals="handleUpdateOrbitals"></checkbox-pdos>
        <checkbox-pdos :sIndex="index" :l-orbital="'全选'" :orbitals="['p', 'px', 'py', 'pz']"
          @updateOrbitals="handleUpdateOrbitals"></checkbox-pdos>
        <checkbox-pdos :sIndex="index" :l-orbital="'全选'" :orbitals="['d', 'd1', 'd2', 'd3', 'd4', 'd5']"
          @updateOrbitals="handleUpdateOrbitals"></checkbox-pdos>
        <checkbox-pdos :sIndex="index" :l-orbital="'全选'" :orbitals="['f', 'f1', 'f2', 'f3', 'f4', 'f5', 'f6', 'f7']"
          @updateOrbitals="handleUpdateOrbitals"></checkbox-pdos>
      </div>
      <!-- 子组件访问父组件的值 -->
      <xyz-display :sIndex="index" :sItem="item" :structureFileContent="structureFileContent" v-model="item.structure"
        class="structureDisplay" @viewer-created="handleViewerCreated"></xyz-display>
    </div>
    <el-button @click="addItem" class="expand_btn" :disabled="addAtomDisabled">+ 添加原子</el-button>
    <el-row>
      <el-col :span="6">
        <el-checkbox v-model="checkedTDOS" label="Total DOS" />
      </el-col>
    </el-row>
    <el-row>
      <el-col :span="6" :offset="18">
        <el-button @click="plot" :disabled="plotDisabled">绘制</el-button>
      </el-col>
    </el-row>
  </div>
  <div id="dosEchart"></div>
</template>

<script>
export default {
  name: "PlotDOS",
};
</script>

<script setup>
import { ref, provide, computed } from "vue";
import CheckboxPdos from "@/components/CheckboxPdos.vue";
import XyzDisplay from "@/components/StructureDisplay.vue";
import FileUpload from "@/components/upload.vue";
import $ from "jquery";
import axios from "axios";
import * as echarts from "echarts";

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

const viewerSelectedAtoms = ref([]);
provide("viewerSelectedAtoms", viewerSelectedAtoms);

/**
 * Provide a function to add atoms to the atoms array.
 *
 * @param {string|number} newValue - The new atom value to add.
 * @return {void}
 */
provide("addViewerSelectedAtoms", (newValue, index) => {
  // Check if newValue exists in atoms array
  // If newValue does not exist, add newValue to atoms array
  if (!viewerSelectedAtoms.value[index].includes(Number(newValue))) {
    viewerSelectedAtoms.value[index].push(Number(newValue));
  }
});
provide("removeViewerSelectedAtoms", (atomItem, index) => {
  viewerSelectedAtoms.value[index] = viewerSelectedAtoms.value[index].filter((item) => item !== atomItem);
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
};
const uploadItems = ref([uploadItem, JSON.parse(JSON.stringify(uploadItem))]);

const checkedTDOS = ref(false);
const structureFileContent = ref("")

// Computed

const fileCount = computed(() => {
  return uploadItems.value.reduce((sum, item) => sum + item.fileLists.length, 0)
})

const addAtomDisabled = computed(() => {
  if (fileCount.value !== 2) {
    return true;
  }
  return false;
});

/**
 * Whether to disable the plot button.
 *
 * 1. The number of fileLists is not equal to 2
 * 2. Each item in the items array should have a non-empty input and a non-empty orbitals array if the radio is not 1
 * 3. The items array should not be empty if checkedTDOS is false
 */
const plotDisabled = computed(() => {
  // Check if the fileLists length is not equal to 2
  if (fileCount.value !== 2) {
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

/**
 * Adds a new item to the `items` array.
 *
 * @return {void} This function does not return anything.
 */
const addItem = () => {
  viewerSelectedAtoms.value.push([])
  items.value.push({
    radio: "1",
    display: "none",
    input: "",
    orbitals: [],
    structure: "",
  });
};

/**
 * Removes an item from the `items` array at the specified index.
 *
 * @param {number} index - The index of the item to remove.
 * @return {void} This function does not return anything.
 */
const removeItem = (index) => {
  items.value.splice(index, 1);
};

/**
 * Toggles the visibility of a structure display element based on its current state.
 *
 * @param {number} index - The index of the item in the `items` array.
 * @return {void} This function does not return anything.
 */
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
  viewerSelectedAtoms.value[index] = [];
  if (inputAtomIndex) {
    viewer.setStyle({ index: inputAtomIndex - 1 }, newStyle);
    viewerSelectedAtoms.value[index].push(inputAtomIndex);
    viewer.render();
  } else {
    viewer.render();
  }
  console.log(viewerSelectedAtoms.value);
};

/**
 * Asynchronously sends a POST request to fetch DOS data based on the provided paths.
 *
 * @return {void} This function does not return anything.
 */
const plot = async () => {
  let contcarPath = uploadItems.value[0].fileLists[0]['filePath'];
  let doscarPath = uploadItems.value[1].fileLists[0]['filePath'];
  let params = {
    contcarPath: contcarPath,
    doscarPath: doscarPath,
    checkedTDOS: checkedTDOS.value,
    atoms: items.value.map((item) => Object({ radio: item.radio, input: item.input, orbitals: item.orbitals }))
  };
  let dosEchart = echarts.init(document.getElementById("dosEchart"));
  dosEchart.clear();
  dosEchart.showLoading({ maskColor: "rgba(3,3,8,0.5)", textColor: "#fff600" });
  try {
    const res1 = await axios.post("/api/get_dos_data", params, {
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
    });
    if (res1.status == 200) {
      dosEchart.hideLoading();
      console.log(res1.data.series)
      /** @type EChartsOption */
      var dosOption = {
        tooltip: {
          trigger: 'axis',
          formatter: function (params) {
            var tooltipContent = '<div style="text-align: left;">';
            var xAxisValue = parseFloat(params[0].axisValue).toFixed(2);
            tooltipContent += `<div style="font-weight: bold; margin-bottom: 5px;">${xAxisValue}</div>`;
            tooltipContent += '<table>';
            params.forEach(function (item) {
              tooltipContent += `<tr>
                    <td style="text-align: left; padding-right: 10px;">${item.marker}${item.seriesName}</td>
                    <td style="text-align: right; font-weight: bold;">${item.value[1].toFixed(2)}</td>
                </tr>`;
            });
            tooltipContent += '</table>';
            tooltipContent += '</div>';
            return tooltipContent;
          },
        },
        legend: {
          show: true,
        },
        xAxis: [
          {
            name: "Energy (eV)",
            nameLocation: "center",
            nameGap: 25,
          },
        ],
        yAxis:
        {
          name: "Density of States (a.u.)",
          nameLocation: "center",
          nameGap: 45,
          max: function (value) {
            return Math.ceil(value.max);
          },
          min: function (value) {
            return Math.floor(value.min);
          },
        },
        dataZoom: [
          {
            type: "inside",
          },
        ],
        series: res1.data.series,
      };
      dosEchart.setOption(dosOption);
    }
  } catch (error) {
    console.log(error);
  }
};

/**
 * Assigns the viewer to the structure at the specified index in the items array.
 *
 * @param {number} index - The index of the item in the items array.
 * @param {Object} viewer - The viewer to be assigned to the structure.
 */
const handleViewerCreated = (index, viewer) => {
  items.value[index]["structure"] = viewer;
  console.log(items.value);
};

/**
 * Handles the file list for a specific index.
 *
 * @param {number} index - The index of the item in the items array.
 * @param {Object} file - The file to be added to the file list.
 */
const handleFileLists = (index, file) => {
  console.log("handleFileLists: file", file);
  if (file['fileContent']) {
    structureFileContent.value = file['fileContent'];
  }
  uploadItems.value[index].fileLists.push(file);
  console.log("handleFileLists: fileLists", uploadItems.value);
};

/**
 * Updates the file lists for a specific index.
 *
 * @param {number} index - The index of the item in the uploadItems array.
 * @param {Array} files - The new file list to be assigned to the item.
 * @return {void}
 */
const updateFileLists = (index, files) => {
  console.log("updateFileLists: files", files);
  uploadItems.value[index].fileLists = files;
  if (fileCount.value < 2) {
    items.value = []
  }
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
#dosEchart {
  width: 570px;
  height: 380px;
  display: flex;
  float: right
}

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

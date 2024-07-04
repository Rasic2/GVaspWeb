<template>
  <div class="Echarts">
    <div class="upload_plot">
      <file-upload class="upload" :index="index" :limitNum="1" :type="4" :uploadTip="'请上传 OUTCAR 文件'"
        :fileList="uploadItem.fileLists" @uploadSuccess="handleFileLists" @updateFile="updateFileLists"></file-upload>
      <el-button class="expand_btn" @click="plot" :disabled="plotDisabled">绘制</el-button>
    </div>
    <div id="optEchart"></div>
  </div>
</template>

<script>
export default {
  name: "PlotOpt",
};
</script>

<script setup>
import { ref, computed } from "vue"
import axios from "axios";
import * as echarts from "echarts";
import FileUpload from "@/components/upload.vue";

// Ref Variable
const uploadItem = ref({
  fileLists: [],
})

// Computed

const fileCount = computed(() => {
  return uploadItem.value.fileLists.length
})

/**
 * Whether to disable the plot button.
 *
 * 1. The number of fileLists is not equal to 2
 * 2. Each item in the items array should have a non-empty input and a non-empty orbitals array if the radio is not 1
 * 3. The items array should not be empty if checkedTDOS is false
 */
const plotDisabled = computed(() => {
  // Check if the fileLists length is not equal to 2
  if (fileCount.value !== 1) {
    return true;
  }
  return false;
});

// Methods
const plot = async () => {
  let outcarPath = uploadItem.value.fileLists[0]['filePath'];
  let params = {
    outcarPath: outcarPath,
  };
  let optEchart = echarts.init(document.getElementById("optEchart"));
  optEchart.clear();
  optEchart.showLoading({ maskColor: "rgba(3,3,8,0.5)", textColor: "#fff600" });
  try {
    const res = await axios.post("http://127.0.0.1:5001/api/get_opt_data", params, {
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
    });
    if (res.status == 200) {
      optEchart.hideLoading();
      console.log(res.data)
      /** @type EChartsOption */
      var OptOption = {
        title: {
          text: 'Structure Optimization',
          left: "center",
          top: "top",
        },
        xAxis: [{
          name: "Steps",
          nameLocation: "center",
          nameGap: 25,
        }],
        yAxis: [{
          name: "Energy (eV)",
          nameLocation: "center",
          nameGap: 45,
          max: function (value) {
            return Math.ceil(value.max);
          },
          min: function (value) {
            return Math.floor(value.min);
          },
        }, {
          name: "Force",
          nameLocation: "center",
          nameGap: 45,
          max: function (value) {
            return Math.ceil(value.max);
          },
          min: function (value) {
            return Math.floor(value.min);
          },
        }
        ],
        dataZoom: [{
          type: "inside"
        }],
        series: [
          {
            data: res.data['energy'],
            type: 'line',
            label: {
              show: false,
            },
            emphasis: {
              label: {
                show: true,
                formatter: '{c}',
                align: 'left',
              }
            }
          }, {
            data: res.data['force'],
            type: 'line',
            label: {
              show: false,
            },
            yAxisIndex: 1,
            emphasis: {
              label: {
                show: true,
                formatter: '{c}',
                align: 'left',
              }
            }
          }
        ]
      };
      optEchart.setOption(OptOption);
    }
  } catch (error) {
    console.log(error);
  }
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
    console.log(file['fileContent'])
    // structureFileContent.value = file['fileContent'];
  }
  uploadItem.value.fileLists.push(file);
  console.log("handleFileLists: fileLists", uploadItem.value);
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
  uploadItem.value.fileLists = files;
  // if (fileCount.value < 2) {
  //     items.value = []
  // }
};
</script>

<style>
#optEchart {
  width: 600px;
  height: 400px;
}

.upload_plot {
  display: flex;
}

.expand_btn {
  display: flex;
  float: top;
}
</style>
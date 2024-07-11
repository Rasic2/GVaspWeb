<template>
    <div class="Echarts">
        <div class="upload_plot">
            <file-upload class="upload" :index="index" :limitNum="1" :type="'EIGENVAL'" :uploadTip="'请上传 EIGENVAL 文件'"
                :fileList="uploadItem.fileLists" @uploadSuccess="handleFileLists"
                @updateFile="updateFileLists"></file-upload>
            <el-button class="expand_btn" @click="plot" :disabled="plotDisabled">绘制</el-button>
        </div>
        <div id="bandEchart"></div>
    </div>
</template>

<script>
export default {
    name: "PlotBand",
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
    let eigenvalPath = uploadItem.value.fileLists[0]['filePath'];
    let params = {
        eigenvalPath: eigenvalPath,
    };
    let bandEchart = echarts.init(document.getElementById("bandEchart"));
    bandEchart.clear();
    bandEchart.showLoading({ maskColor: "rgba(3,3,8,0.5)", textColor: "#fff600" });
    try {
        const apiUrl = process.env.VUE_APP_API_URL || '';
        const res = await axios.post(apiUrl + "/api/get_band_data", params, {
            headers: {
                "Access-Control-Allow-Origin": "*",
            },
        });
        if (res.status == 200) {
            bandEchart.hideLoading();
            console.log(res.data)
            /** @type EChartsOption */
            var bandOption = {
                title: {
                    text: 'Band Structure',
                    left: "center",
                    top: "20px",
                },
                legend: {
                    type: 'scroll', // 启用滚动
                    orient: 'vertical', // 垂直布局
                    right: -15, // 右侧位置
                    top: 50, // 距离顶部的位置
                    bottom: 20, // 距离底部的位置
                },
                xAxis: {
                    name: "",
                    nameLocation: "center",
                    nameGap: 25,
                    max: function (value) {
                        return value.max
                    }
                },
                yAxis: {
                    name: "Energy (eV)",
                    nameLocation: "center",
                    nameGap: 45,
                    max: function (value) {
                        return Math.ceil(value.max);
                    },
                    min: function (value) {
                        return Math.floor(value.min);
                    },
                },
                grid: {
                    show: true,
                    borderColor: '#000000',
                    borderWidth: 2
                },
                dataZoom: [{
                    type: "inside"
                }],
                series: res.data.series,
            };
            bandEchart.setOption(bandOption);
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
};
</script>

<style>
#bandEchart {
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
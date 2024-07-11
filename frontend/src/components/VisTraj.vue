<template>
  <div class="VisTraj">
    <div class="upload_plot">
      <file-upload class="upload" :index="index" :limitNum="1" :type="'XDATCAR'" :uploadTip="'请上传 XDATCAR 文件'"
        :fileList="uploadItem.fileLists" @uploadSuccess="handleFileLists" @updateFile="updateFileLists"></file-upload>
      <el-button class="expand_btn" @click="render" :disabled="renderDisabled">渲染</el-button>
    </div>
    <traj-display :trajData="trajData"></traj-display>
  </div>
</template>

<script>
export default {
  name: "VisTraj",
};
</script>

<script setup>
import { ref, computed } from "vue"
import fileUpload from "@/components/upload.vue";
import TrajDisplay from "@/components/TrajDisplay.vue";

// Ref Variable
const uploadItem = ref({ fileLists: [] })
const trajData = ref([])

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
const renderDisabled = computed(() => {
  // Check if the fileLists length is not equal to 2
  if (fileCount.value !== 1) {
    return true;
  }
  return false;
});

const render = () => {
  console.log(uploadItem.value.fileLists)
}

/**
 * Handles the file list for a specific index.
 *
 * @param {number} index - The index of the item in the items array.
 * @param {Object} file - The file to be added to the file list.
 */
const handleFileLists = (index, file) => {
  console.log("handleFileLists: file", file);
  if (file['fileContent']) {
    console.log("file content", file['fileContent'])
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
.upload_plot {
  display: flex;
}

.expand_btn {
  display: flex;
  float: top;
}
</style>
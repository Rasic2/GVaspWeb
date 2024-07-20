<template>
  <div class="VisTraj">
    <div class="upload_plot">
      <file-upload class="upload" :index="index" :limitNum="1" :type="'XDATCAR'" :uploadTip="'请上传 XDATCAR 文件'"
        :fileList="uploadItem.fileLists" @uploadSuccess="handleFileLists" @updateFile="updateFileLists"></file-upload>
    </div>
    <traj-display v-if="trajData.length > 0" :trajData="trajData"></traj-display>
  </div>
</template>

<script>
export default {
  name: "VisTraj",
};
</script>

<script setup>
import { ref } from "vue"
import fileUpload from "@/components/upload.vue";
import TrajDisplay from "@/components/TrajDisplay.vue";

// Ref Variable
const uploadItem = ref({ fileLists: [] })
const trajData = ref([])

/**
 * Handles the file list for a specific index.
 *
 * @param {number} index - The index of the item in the items array.
 * @param {Object} file - The file to be added to the file list.
 */
const handleFileLists = (index, file) => {
  console.log("handleFileLists: file", file);
  if (file['fileContent']) {
    trajData.value = file['fileContent']
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
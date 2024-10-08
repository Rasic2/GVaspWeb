<template>
  <el-upload v-model:file-list="waitFileList" class="upload" :on-change="onUpload" multiple :auto-upload="false"
    :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove" :limit="limitNum"
    :on-exceed="handleExceed">
    <el-button type="primary" :disabled="isDisabled">上传文件</el-button>
    <template #tip>
      <div class="el-upload__tip">{{ uploadTip }}</div>
    </template>
  </el-upload>
</template>

<script setup>
import { ref, watch, computed, defineProps, defineEmits } from "vue";
import { ElMessage, ElMessageBox, ElLoading } from "element-plus";
import axios from "axios";

const props = defineProps({
  action: {
    default: "/manager/energy/common/upload",
    type: String,
  },
  limitNum: {
    default: 5,
    type: Number,
  },
  type: {
    default: '',
    type: String,
  },
  projectId: {
    default: "",
    type: String,
  },
  fileList: {
    default: () => [],
    type: Array,
  },
  index: {
    type: Number,
    default: 0,
  },
  uploadTip: {
    type: String,
    default: ''
  }
});

let waitFileList = ref([]);
// waitFileList.value = props.fileList
watch(
  () => props.fileList,
  () => {
    // console.log("props.fileList====>", props.fileList)
    waitFileList.value = props.fileList;
  }
);

const emits = defineEmits(["uploadSuccess", "updateFile"]);
const CHUNK_SIZE = 1 * 1024 * 1024;

/**
 * Returns a computed property that indicates whether the file input should be disabled.
 *
 * @returns {boolean} - True if the file input should be disabled, false otherwise.
 */
const isDisabled = computed(() => {
  // Check if the number of files in the fileList is greater than or equal to the limitNum
  return props.fileList.length >= props.limitNum;
});

/**
 * Uploads a file.
 *
 * @param {Object} file - The file to be uploaded.
 * @param {Array} fileList - The list of files.
 * @return {Promise<boolean>} - A promise that resolves to a boolean indicating the success of the upload.
 */
const onUpload = async (file, fileList) => {
  console.log("onUpload: fileList", fileList);
  const loadingInstance = ElLoading.service({
    text: "正在上传",
    background: "rgba(0,0,0,.2)",
  });

  const totalChunks = Math.ceil(file.size / CHUNK_SIZE);
  let start = 0;
  let end = CHUNK_SIZE;
  let chunkIndex = 0;
  while (start < file.size) {
    const chunk = file.raw.slice(start, end);
    const formData = new FormData();
    formData.append('file', chunk);
    formData.append('type', props.type);
    formData.append('filename', file.name);
    formData.append('chunkIndex', chunkIndex);
    formData.append('totalChunks', totalChunks);

    try {
      const apiUrl = process.env.VUE_APP_API_URL || '';
      const res = await axios.post(apiUrl + '/api/upload', formData, {
        headers: {
          "Access-Control-Allow-Origin": "*",
          'Content-Type': 'multipart/form-data',
        }
      });
      if (res.status == 200) {
        console.log(`Chunk uploaded ${chunkIndex + 1}/${totalChunks} successfully:`, res);
        if (chunkIndex + 1 == totalChunks) {
          emits("uploadSuccess", props.index, res.data)
        }
      }
    } catch (error) {
      fileList.splice(-1, 1); //移除当前超出大小的文件
      loadingInstance.close();
      console.log(error);
      ElMessage.warning(`文件上传失败`);
      return;
    }
    start = end;
    end = start + CHUNK_SIZE;
    chunkIndex += 1;
  }

  loadingInstance.close();
  console.log(props.index, 'File uploaded successfully');
  return true;
};

/**
 * Handles the removal of a file from the upload list.
 *
 * @param {Object} file - The file object to be removed.
 * @param {Array} uploadFiles - The array of files currently being uploaded.
 * @return {void} This function does not return anything.
 */
const handleRemove = (file, uploadFiles) => {
  console.log("handleRemove: file", file);
  console.log("handleRemove: uploadFiles", uploadFiles);
  emits("updateFile", props.index, uploadFiles);
};

/**
 * A function to handle previewing an upload file.
 *
 * @param {Object} uploadFile - The file object to be previewed.
 * @return {void} This function does not return anything.
 */
const handlePreview = (uploadFile) => {
  console.log(uploadFile);
};

/**
 * Displays a warning message when the number of selected files exceeds the limit.
 *
 * @param {Array} files - The array of files that have been selected.
 * @param {Array} uploadFiles - The array of files that are currently being uploaded.
 * @return {void} This function does not return anything.
 */
const handleExceed = (files, uploadFiles) => {
  ElMessage.warning(
    `The limit is ${props.limitNum}, you selected ${files.length
    } files this time, add up to ${files.length + uploadFiles.length} totally`
  );
};

/**
 * A function that is called before a file is removed from the upload list.
 *
 * @param {Object} uploadFile - The file object that is about to be removed.
 * @return {Promise<boolean>} A promise that resolves to true if the file should be removed, or false if the removal should be cancelled.
 */
const beforeRemove = (uploadFile) => {
  return ElMessageBox.confirm(`确定移除 ${uploadFile.name}文件 ?`).then(
    () => true,
    () => false
  );
};
</script>

<script>
export default {
  name: "FileUpload",
};
</script>

<style lang="scss" scoped>
.previewDownload {
  margin-top: 80px;
  margin-left: 50px;
  display: flex;
  flex-direction: column;

  .el-link {
    height: 40px;
  }
}

.upload {
  width: 400px;
  text-align: left;
}
</style>

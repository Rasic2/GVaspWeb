<template>
  <el-upload v-model:file-list="waitFileList" class="upload-demo" :on-change="onUpload" multiple :auto-upload="false"
             :on-preview="handlePreview" :on-remove="handleRemove" :before-remove="beforeRemove" :limit="limitNum"
             :on-exceed="handleExceed">
    <el-button type="primary">上传文件</el-button>
    <template #tip>
      <div class="el-upload__tip">
        支持jpg/jpeg/png；图片大小不能超过10M；文件大小不超过20M；最多上传{{ limitNum }}个文件
      </div>
    </template>
  </el-upload>
  <!--文件预览及下载-->
  <div class="previewDownload">
    <el-link :underline="false" type="primary" style="margin-right:10px" v-for="item in fileList" :key="item.id"
             @click.prevent="downloadFile(item.url, item.name)">下载
    </el-link>
  </div>
</template>
<script setup>
import {debounce} from "lodash"
import {ref, watch, defineProps, defineEmits} from 'vue'
import {ElMessage, ElMessageBox, ElLoading} from "element-plus"
// import {uploadFileApi} from '../api/upload'

const props = defineProps({
  action: {
    default: '/manager/energy/common/upload',
    type: String,
  },
  limitNum: {
    default: 5,
    type: Number,
  },
  type: {
    default: 1,
    type: Number,
  },
  projectId: {
    default: '',
    type: String,
  },
  fileList: {
    default: () => [],
    type: Array
  }
})

let waitFileList = ref([])
// waitFileList.value = props.fileList
watch(
    () => props.fileList,
    () => {
      // console.log("props.fileList====>", props.fileList)
      waitFileList.value = props.fileList
    }
)

const emits = defineEmits(["uploadSuccess", "updateFile"])

// 上传图片
const onUpload = async (file, fileList) => {
  console.log(file)
  console.log(fileList)
  let rawFile = file.raw
  if (
      rawFile.type == "image/jpeg" && rawFile.size / 1024 / 1024 > 10 ||
      rawFile.type == "image/png" && rawFile.size / 1024 / 1024 > 10 ||
      rawFile.type == "image/jpg" && rawFile.size / 1024 / 1024 > 10
  ) {
    ElMessage.error("图片大小不能超过10MB!")
    fileList.splice(-1, 1) //移除当前超出大小的文件
    return false
  } else if (rawFile.size / 1024 / 1024 > 20) {
    ElMessage.error("文件大小不能超过20MB!")
    fileList.splice(-1, 1) //移除当前超出大小的文件
    return false
  } else {
    console.log('上传')
    const loadingInstance = ElLoading.service({
      text: "正在上传",
      background: "rgba(0,0,0,.2)",
    })

    // try {
    //   const res = await uploadFileApi(rawFile, props.projectId, props.type)
    //   console.log(res)
    //   if (res.code == 200) {
    //     loadingInstance.close()
    //     const obj = res.result
    //     emits("uploadSuccess", obj)
    //   }
    // } catch (error) {
    //   fileList.splice(-1, 1) //移除当前超出大小的文件
    //   loadingInstance.close()
    //   console.log(error)
    //   ElMessage.warning(`图片上传失败`)
    // }
  }
  return true
}


const handleRemove = (file, uploadFiles) => {
  console.log(file)
  console.log(uploadFiles)
  emits('updateFile', uploadFiles)
}

const handlePreview = (uploadFile) => {
  console.log(uploadFile)
}

const handleExceed = (files, uploadFiles) => {
  ElMessage.warning(
      `The limit is ${props.limitNum}, you selected ${files.length} files this time, add up to ${files.length + uploadFiles.length
      } totally`
  )
}

const beforeRemove = (uploadFile, uploadFiles) => {
  return ElMessageBox.confirm(
      `确定移除 ${uploadFile.name}文件 ?`
  ).then(
      () => true,
      () => false
  )
}


// 下载防抖  近一年电费详单
const downloadFile = debounce((url, fileName) => {
  // console.log(url)
  // console.log(fileName)
  const link = document.createElement('a') // 创建一个 a 标签用来模拟点击事件
  link.style.display = 'none'
  link.href = url
  // link.download = fileName
  link.setAttribute('download', fileName)
  document.body.appendChild(link)
  link.click()
  document.body.removeChild(link)
  // exportFile.getImgURLs(url, fileName)

}, 2000)
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
</style>

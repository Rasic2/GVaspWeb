<template>
    <div style="display:grid;">
        <div style="display:flex; align-items:top; grid-template-columns: 1fr; gap:45px">
            <el-form-item :label="'文件'" required></el-form-item>
            <file-upload :index="index" :limitNum="1" :type="'OUTCAR'" :uploadTip="'请上传 *.xsd 文件'"
                :fileList="uploadItem.fileLists" @uploadSuccess="handleFileLists"
                @updateFile="updateFileLists"></file-upload>
        </div>
        <el-form-item v-for="(item, index) in ['任务类型']" :key="index" :label="item" class="horizontal-align" required>
            <el-radio-group v-model="radio" class="inputRadio">
                <el-radio value=1 size="large">opt</el-radio>
                <el-radio value=2 size="large">chg</el-radio>
                <el-radio value=3 size="large">wf</el-radio>
                <el-radio value=4 size="large">dos</el-radio>
                <el-radio value=5 size="large">freq</el-radio>
                <el-radio value=6 size="large">md</el-radio>
                <el-radio value=7 size="large">stm</el-radio>
                <el-radio value=8 size="large">con-ts</el-radio>
            </el-radio-group>
        </el-form-item>
        <div v-if="radio >= 1" class="inputOptions">
            <checkbox-pdos :sIndex="index" :l-orbital="'全选'" :orbitals="checkboxOptions"
                customSelectAll="customSelectAll" customSelectSingle="customSelectSingle"
                @updateOrbitals="handleUpdateOrbitals"></checkbox-pdos>
            <div v-if="options.indexOf('potential') !== -1">
                <el-form-item label="potential" required>
                    <el-select v-model="potentialValue" clearable placeholder="Select potential" style="width: 240px">
                        <el-option v-for="item in potentialOptions" :key="item" :label="item" :value="item" />
                    </el-select>
                </el-form-item>
            </div>
            <div v-if="options.indexOf('nelect') !== -1">
                <el-form-item label="NELECT" required>
                    <el-input-number v-model="nelect" :precision="2" :step="0.1" :max="10" />
                </el-form-item>
            </div>
        </div>
    </div>
    <el-button class="expand_btn" @click="generate" :disabled="generateDisabled">生成</el-button>
</template>

<script>
export default {
    name: "CreateInput"
}
</script>

<script setup>
import { ref, computed } from "vue";
import CheckboxPdos from "@/components/CheckboxPdos.vue";
import FileUpload from "@/components/upload.vue";

// Ref Variable
const uploadItem = ref({ fileLists: [] })

const radio = ref(null)
const options = ref([])

const potentialValue = ref('PAW_PBE')
const potentialOptions = ['PAW_LDA', 'PAW_PBE', 'PAW_PW91', 'USPP_LDA', 'USPP_PW91']
const nelect = ref(0)

// Computed
const checkboxOptions = computed(() => {
    const defaultOptions = ['potential', 'vdw', 'sol', 'gamma', 'hse', 'static', 'nelect']
    if (radio.value == 1) {
        return [...defaultOptions, 'low']
    }
    return [...defaultOptions]
})

const fileCount = computed(() => {
    return uploadItem.value.fileLists.length
})

const generateDisabled = computed(() => {
    // Check if the fileLists length is not equal to 2
    if (fileCount.value !== 1) {
        return true;
    }

    if (options.value.indexOf('potential') !== -1) {
        return potentialValue.value == "" || potentialValue.value == undefined
    }

    return false;
})

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

const handleUpdateOrbitals = (mode, index, orbitals) => {
    if (!Array.isArray(orbitals)) {
        throw new TypeError("'orbitals' must be an array");
    }
    if (mode === "add") {
        orbitals.forEach((orbital) => {
            options.value.push(orbital)
        });
    } else if (mode === "remove") {
        orbitals.forEach((orbital) => {
            const orbitalIndex = options.value.indexOf(orbital);
            if (orbitalIndex !== -1) {
                options.value.splice(orbitalIndex, 1);
            }
        });
    }
    else if (mode === "substitute") {
        options.value = orbitals
    }
    console.log(options.value)
};
</script>

<style>
.horizontal-align {
    align-items: center;
}

.inputRadio {
    float: left;
    margin-left: 15px;
}

.inputOptions {
    display: grid;
    gap: 18px;
}

.customSelectAll {
    padding: 0 10px;
    width: 50px;
    margin-left: 0px;
}

.customSelectSingle {
    padding: 0 30px;
    width: 20px;
    margin-right: 20px;
}

.expand_btn {
    float: left;
    margin-top: 5px;
    margin-left: 0px;
}
</style>
<template>
    <el-form-item v-for="(item, index) in ['任务类型']" :key="index" :label="item" prop="name" class="horizontal-align"
        required>
        <el-radio-group v-model="radio" class="inputRadio">
            <el-radio value="1" size="large">opt</el-radio>
            <el-radio value="2" size="large">chg</el-radio>
            <el-radio value="3" size="large">wf</el-radio>
            <el-radio value="4" size="large">dos</el-radio>
            <el-radio value="5" size="large">freq</el-radio>
            <el-radio value="6" size="large">md</el-radio>
            <el-radio value="7" size="large">stm</el-radio>
            <el-radio value="8" size="large">ts</el-radio>
        </el-radio-group>
    </el-form-item>
    <div v-if="radio == 1" class="inputOptions">
        <checkbox-pdos :sIndex="index" :l-orbital="'全选'"
            :orbitals="['potential', 'vdw', 'sol', 'gamma', 'hse', 'static', 'nelect']"
            customSelectAll="customSelectAll" customSelectSingle="customSelectSingle"
            @updateOrbitals="handleUpdateOrbitals"></checkbox-pdos>
    </div>
</template>

<script>
export default {
    name: "CreateInput"
}
</script>

<script setup>
import { ref } from "vue";
import CheckboxPdos from "@/components/CheckboxPdos.vue";

const radio = ref(null)
const options = ref([])

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
</style>
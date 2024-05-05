<template>
  <div class="checkboxPDOS">
    <el-checkbox class="selectAll" v-model="checkAll" :indeterminate="isIndeterminate" @change="handleCheckAllChange">
      {{ lOrbital }}
    </el-checkbox>
    <el-checkbox-group v-model="checkedOrbitals" @change="handleCheckedOrbitalsChange">
      <el-checkbox class="selectSingle" v-for="orbital in orbitals" :key="orbital" :label="orbital" :value="orbital">
        {{ orbital.value }}
      </el-checkbox>
    </el-checkbox-group>
  </div>
</template>

<script setup>
import {ref} from "vue";
import {toRefs, defineProps} from 'vue';

const props = defineProps({
  lOrbital: {
    type: String,
    default: '',
  },
  orbitals: {
    type: Array,
    default: () => []
  }
})

const checkAll = ref(false)
const isIndeterminate = ref(true)
const checkedOrbitals = ref([])
const orbitals = toRefs(props.orbitals)

const handleCheckAllChange = (val) => {
  checkedOrbitals.value = val ? orbitals : []
  isIndeterminate.value = false
  console.log(checkedOrbitals.value, isIndeterminate.value)
}
const handleCheckedOrbitalsChange = (value) => {
  const checkedCount = value.length
  checkAll.value = checkedCount === orbitals.length
  isIndeterminate.value = checkedCount > 0 && checkedCount < orbitals.length
  console.log(checkAll, isIndeterminate)
}
</script>

<style>
.checkboxPDOS {
  display: flex;
}

.selectAll {
  padding: 0 10px;
  width: 30px;
  margin-left: 20px;
}

.selectSingle {
  padding: 0 10px;
  width: 30px;
  margin-right: 20px;
}
</style>
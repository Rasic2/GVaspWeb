<template>
  <div class="checkboxPDOS">
    <el-checkbox :class="['selectAll', customSelectAll]" v-model="checkAll" :indeterminate="isIndeterminate"
      @change="handleCheckAllChange">
      {{ lOrbital }}
    </el-checkbox>
    <el-checkbox-group v-model="checkedOrbitals" @change="handleCheckedOrbitalsChange">
      <el-checkbox :class="['selectSingle', customSelectSingle]" v-for="orbital in orbitals" :key="orbital"
        :label="orbital" :value="orbital">
        {{ orbital.value }}
      </el-checkbox>
    </el-checkbox-group>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { toRefs, defineProps, defineEmits } from "vue";

const props = defineProps({
  sIndex: {
    type: Number,
    default: 0,
  },
  lOrbital: {
    type: String,
    default: "",
  },
  orbitals: {
    type: Array,
    default: () => [],
  },
  customSelectAll: {
    type: String,
    default: "",
  },
  customSelectSingle: {
    type: String,
    default: "",
  },
});

const emits = defineEmits(["updateOrbitals"]);

const checkAll = ref(false);
const isIndeterminate = ref(false);
const checkedOrbitals = ref([]);
const orbitals = toRefs(props.orbitals);

const handleCheckAllChange = (val) => {
  checkedOrbitals.value = val ? orbitals : [];
  isIndeterminate.value = false;
  let updateOrbitals = orbitals.map((item) => item.value);
  if (checkAll.value) {
    emits("updateOrbitals", "add", props.sIndex, updateOrbitals);
  } else {
    emits("updateOrbitals", "remove", props.sIndex, updateOrbitals);
  }
};
const handleCheckedOrbitalsChange = (value) => {
  const checkedCount = value.length;
  checkAll.value = checkedCount === orbitals.length;
  isIndeterminate.value = checkedCount > 0 && checkedCount < orbitals.length;
  let updateOrbitals = value.map((item) => item.value);
  emits("updateOrbitals", "substitute", props.sIndex, updateOrbitals);
};
</script>

<style>
.checkboxPDOS {
  display: flex;
}

.selectAll {
  padding: 0 10px;
  width: 50px;
  margin-left: 20px;
}

.selectSingle {
  padding: 0 10px;
  width: 20px;
  margin-right: 20px;
}
</style>

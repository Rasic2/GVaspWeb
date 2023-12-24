<template>
    <d-slider :min="minValue" :max="maxValue" v-model="inputValue"></d-slider>
    <div class="flex-space-between">
      <span>{{ minValue }}</span>
      <span>{{ maxValue }}</span>
    </div>
  </template>
  `
  <script>
  import { defineComponent, ref } from 'vue';
  
  export default defineComponent({
    setup() {
      const inputValue = ref(12);
      const minValue = ref(0);
      const maxValue = ref(20);
      return {
        inputValue,
        maxValue,
        minValue,
      };
    },
  });
  </script>
  
  <style scoped>
  .flex-space-between {
    display: flex;
    justify-content: space-between;
  }
  </style>
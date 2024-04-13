<template>
    <div>{{ data }}</div>
    <button @click="loadData">点我</button>
</template>

<script>
export default {
    name: "MyAxios"
}
</script>

<script setup>
import { ref } from "vue";
import axios from "axios"

const data = ref(null)
function loadData() {
    axios.get("/data.json").then(function (res) {
        data.value = res.data
    }).catch(function (err) {
        console.log("Error", err)
    })
}
</script>

<style></style >

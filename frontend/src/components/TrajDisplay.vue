<template>
  <div id="trajViewer" class="trajViewer"></div>
  <button @click="playPause">{{ isPlaying ? '暂停' : '播放' }}</button>
  <button @click="nextFrame">下一帧</button>
</template>

<script>
export default {
  name: "TrajDisplay",
};
</script>

<script setup>
import { onMounted, defineProps } from "vue";
import $ from "jquery";

const props = defineProps({
  trajData: {
    type: Array,
    default: () => [],
  },
})

const display = () => {
  let config = { backgroundColor: "white" };
  const defaultStyle = {
    stick: { radius: 0.2, colorscheme: "Jmol" },
    sphere: { scale: 0.35, colorscheme: "Jmol" },
  };
  import("../../../../3Dmol.js/build/3Dmol-min").then(($3Dmol) => {
    const viewer = $3Dmol.createViewer($("#trajViewer"), config);
    console.log(viewer)
    let m = viewer.addModel(props.trajData[0], "vasp");
    viewer.setStyle({}, defaultStyle);
    viewer.render()
  })
};
onMounted(display);
</script>

<style>
.trajViewer {
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: 25px;
  height: 430px;
  width: 500px;
  position: relative;
}
</style>
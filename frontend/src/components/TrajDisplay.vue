<template>
  <div class="trajDisplay">
    <div class="trajControl">
      <div class="trajButton">
        <el-button @click="playPause">{{ isPlaying ? '暂停' : '播放' }}</el-button>
        <el-button @click="nextFrame">下一帧</el-button>
      </div>
      <p>{{ currentFrame }} / {{ props.trajData.length }}</p>
    </div>
    <div id="trajViewer" class="trajViewer"></div>
  </div>
</template>

<script>
export default {
  name: "TrajDisplay",
};
</script>

<script setup>
import { ref, onMounted, defineProps } from "vue";
import $ from "jquery";

const props = defineProps({
  trajData: {
    type: Array,
    default: () => [],
  },
})

const viewer = ref(null)
const isPlaying = ref(false);
const currentFrame = ref(0);
const currentView = ref(null)
let playInterval = null;

const saveView = () => {
  if (viewer.value) {
    // 保存视角信息
    currentView.value = {
      camera: viewer.value.camera.position.clone(),
      rotation: viewer.value.rotationGroup.rotation.clone(),
      center: viewer.value.rotationGroup.position.clone(),
    };
  }
};

const restoreView = () => {
  if (viewer.value && currentView.value) {
    // 恢复视角信息
    viewer.value.camera.position.copy(currentView.value.camera);
    viewer.value.rotationGroup.rotation.copy(currentView.value.rotation);
    viewer.value.rotationGroup.position.copy(currentView.value.center);
    viewer.value.render();
  }
};

const loadFrame = (frameIndex) => {
  let config = { backgroundColor: "white" };
  const defaultStyle = {
    stick: { radius: 0.2, colorscheme: "Jmol" },
    sphere: { scale: 0.35, colorscheme: "Jmol" },
  };
  import("../../../../3Dmol.js/build/3Dmol-min").then(($3Dmol) => {
    if (!viewer.value) {
      viewer.value = $3Dmol.createViewer($("#trajViewer"), config);
    }
    saveView()
    viewer.value.removeAllModels();
    let m = viewer.value.addModel(props.trajData[frameIndex], "vasp");
    viewer.value.addUnitCell(m, { alabel: 'A', blabel: 'B', clabel: 'C', astyle: { color: 'red', radius: 0.2, midpos: -1 }, bstyle: { color: 'green', radius: 0.2, midpos: -1 }, cstyle: { color: 'blue', radius: 0.2, midpos: -1 } });
    viewer.value.setStyle({}, defaultStyle);
    viewer.value.zoomTo();
    viewer.value.render()

    restoreView()
  })
};

const playPause = () => {
  if (isPlaying.value) {
    clearInterval(playInterval);
  } else {
    playInterval = setInterval(() => {
      currentFrame.value = (currentFrame.value + 1) % props.trajData.length;
      loadFrame(currentFrame.value);
    }, 1000); // 每秒播放一帧
  }
  isPlaying.value = !isPlaying.value;
};

const nextFrame = () => {
  if (!isPlaying.value) {
    currentFrame.value = (currentFrame.value + 1) % props.trajData.length;
    loadFrame(currentFrame.value);
  }
};

onMounted(() => {
  loadFrame(currentFrame.value);
});
</script>

<style>
.trajViewer {
  display: flex;
}

.trajButton {
  margin-right: 10px;
}

.trajControl {
  float: top;
  display: flex;
  align-items: center;
}

.trajViewer {
  margin-top: 10px;
  margin-bottom: 10px;
  height: 430px;
  width: 500px;
  position: relative;
  float: left
}
</style>
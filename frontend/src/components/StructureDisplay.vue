<template>
  <div>
    <div :id="'displayMol' + sIndex" class="structureView"></div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, inject } from "vue";
import $ from "jquery";

const viewerSelectedAtoms = inject("viewerSelectedAtoms");
const addViewerSelectedAtoms = inject("addViewerSelectedAtoms");
const removeViewerSelectedAtoms = inject("removeViewerSelectedAtoms");

// const items = inject("items")
const updateItemsInput = inject("updateItemsInput")

// 子组件访问父组件的值
const props = defineProps({
  sIndex: {
    type: Number,
    default: 0,
  },
  sItem: {
    type: Object,
    default: () => {
    },
  },
  structureFileContent: {
    type: String,
    default: ""
  }
});

// 父组件获得子组件创建的 Viewer，子组件通过 emit 来定义
const emit = defineEmits(["viewer-created"]);

const display = () => {
  // eslint-disable-next-line no-undef
  let element = $("#displayMol" + props.sIndex);
  console.log(element);
  console.log(props.sItem["input"]);
  let config = { backgroundColor: "white" };
  const newStyle = inject("newStyle");
  const defaultStyle = inject("defaultStyle");
  // eslint-disable-next-line no-undef
  import("../../../../3Dmol.js/build/3Dmol-min").then(($3Dmol) => {
    const viewer = $3Dmol.createViewer(element, config);
    console.log("structureFileContent in display", props.structureFileContent);
    let m = viewer.addModel(props.structureFileContent, "vasp"); // 需要去掉 Selective 行
    viewer.addUnitCell(m, { alabel: 'A', blabel: 'B', clabel: 'C', astyle: { color: 'red', radius: 0.2, midpos: -1 }, bstyle: { color: 'green', radius: 0.2, midpos: -1 }, cstyle: { color: 'blue', radius: 0.2, midpos: -1 } });
    viewer.setStyle({}, defaultStyle);

    const handleMouseClick = (event) => {
      if (event.altKey && event.button === 0) { // Alt + 左键点击
        const x = viewer.getX(event);
        const y = viewer.getY(event);
        const mouse = viewer.mouseXY(x, y)

        // 使用 targetedObjects 方法获取点击位置的原子
        const intersects = viewer.targetedObjects(mouse.x, mouse.y, viewer.selectedAtoms({}));
        if (intersects.length) {
          let selectedAtom = intersects[0].clickable
          let selectedAtomElement = selectedAtom.elem
          let selectedAtomIndex = selectedAtom.index + 1
          let atomIndexes = []
          for (let index in viewer.selectedAtoms({})) {
            if (viewer.selectedAtoms({})[index].elem === selectedAtomElement) {
              atomIndexes.push(Number(index) + 1)
            }
          }
          console.log(atomIndexes)
          if (viewerSelectedAtoms.value[props.sIndex].includes(selectedAtomIndex)) {
            viewer.setStyle({ index: atomIndexes.map((index) => index - 1) }, newStyle)
            atomIndexes.forEach((index) => { addViewerSelectedAtoms(index, props.sIndex) })
            viewer.render();
            console.log("atoms after add", viewerSelectedAtoms.value, props.sIndex)
            updateItemsInput(viewerSelectedAtoms.value[props.sIndex].join(","), props.sIndex)
          } else {
            viewer.setStyle({ index: atomIndexes.map((index) => index - 1) }, defaultStyle)
            atomIndexes.forEach((index) => { removeViewerSelectedAtoms(index, props.sIndex) })
            viewer.render();
            console.log("atoms after add", viewerSelectedAtoms.value, props.Index)
            updateItemsInput(viewerSelectedAtoms.value[props.sIndex].join(","), props.sIndex)
          }
        }
      }
    }
    // 添加鼠标点击事件监听器
    window.addEventListener('click', handleMouseClick);

    /**
     * Handles keydown events and performs specific actions based on the pressed key.
     *
     * @param {KeyboardEvent} event - The keyboard event object.
     * @return {void} This function does not return anything.
     */
    const handleKeydown = (event) => {
      switch (event.key) {
        case 'r':
          viewer.rotate(90, 'y');
          viewer.render();
          break;
        case 'z':
          viewer.zoomTo();
          viewer.render();
          break;
        // Add more cases here for additional shortcuts
        default:
          break;
      }
    };
    document.addEventListener('keydown', handleKeydown);

    viewer.setHoverable(
      {},
      true,
      function (atom, viewer1) {
        if (!atom.label) {
          atom.label = viewer1.addLabel(
            atom.elem + `${atom.index + 1}` +
            ` (${atom.x.toFixed(2)}, ${atom.y.toFixed(2)}, ${atom.z.toFixed(
              2
            )})`,
            {
              position: atom,
              backgroundColor: "mintcream",
              fontColor: "black",
            }
          );
        }
      },
      function (atom) {
        if (atom.label) {
          viewer.removeLabel(atom.label);
          delete atom.label;
        }
      }
    );
    viewer.setClickable({}, true, function (atom, viewer1) {
      let atomItem = atom.index + 1;
      if (!viewerSelectedAtoms.value[props.sIndex].includes(atomItem)) {
        viewer1.setStyle({ index: atom.index }, newStyle);
        addViewerSelectedAtoms(atom.index + 1, props.sIndex);
        console.log("atoms after add", viewerSelectedAtoms.value)
        viewer1.render();
        updateItemsInput(viewerSelectedAtoms.value[props.sIndex].join(","), props.sIndex)
      } else {
        viewer1.setStyle({ index: atom.index }, defaultStyle);
        removeViewerSelectedAtoms(atomItem, props.sIndex);
        console.log("atoms after remove", viewerSelectedAtoms.value)
        updateItemsInput(viewerSelectedAtoms.value[props.sIndex].join(","), props.sIndex)
        viewer1.render();
      }
    });
    // viewer1.render();
    viewer.zoomTo();

    // 父组件获得子组件创建的 Viewer，子组件通过 emit 来定义
    emit("viewer-created", props.sIndex, viewer);
  });
};
onMounted(display);
// onBeforeUnmount(() => {
//   // Clean up event listener
//   document.removeEventListener('keydown', handleKeydown);
// });
</script>

<script>
export default {
  name: "XyzDisplay",
};
</script>

<style scoped>
.structureView {
  margin-top: 10px;
  margin-bottom: 10px;
  margin-left: 25px;
  height: 430px;
  width: 500px;
  position: relative;
}

.containerDisplay {
  margin-left: 25px;
  margin-top: 50px;
  display: flex;
}
</style>

<template>
  <div>
    <div :id="'displayMol' + sIndex" class="structureView"></div>
  </div>
</template>

<script setup>
import { defineProps, defineEmits, onMounted, inject } from "vue";
import $ from "jquery";

const atoms = inject("atoms");
const addAtoms = inject("addAtoms");
const removeAtoms = inject("removeAtoms");

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
  import("/Users/hui_zhou/Project/3Dmol.js/build/3Dmol-min").then(($3Dmol) => {
    const viewer = $3Dmol.createViewer(element, config);
    console.log("structureFileContent in display", props.structureFileContent);
    let m = viewer.addModel(props.structureFileContent, "vasp"); // 需要去掉 Selective 行
    viewer.addUnitCell(m, { alabel: 'A', blabel: 'B', clabel: 'C', astyle: { color: 'red', radius: 0.2, midpos: -1 }, bstyle: { color: 'green', radius: 0.2, midpos: -1 }, cstyle: { color: 'blue', radius: 0.2, midpos: -1 } });
    viewer.setStyle({}, defaultStyle);

    viewer.setHoverable(
      {},
      true,
      function (atom, viewer1) {
        if (!atom.label) {
          atom.label = viewer1.addLabel(
            atom.elem +
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
      if (!atoms.value.includes(atomItem)) {
        viewer1.setStyle({ index: atom.index }, newStyle);
        addAtoms(atom.index + 1);
        console.log("atoms after add", atoms.value)
        viewer1.render();
        updateItemsInput(atoms.value.join(","), props.sIndex)
      } else {
        viewer1.setStyle({ index: atom.index }, defaultStyle);
        removeAtoms(atomItem);
        console.log("atoms after remove", atoms.value)
        updateItemsInput(atoms.value.join(","), props.sIndex)
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

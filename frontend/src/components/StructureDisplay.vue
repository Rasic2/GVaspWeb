<template>
  <div>
    <div :id="'displayMol' + sIndex" class="structureView"></div>
    <!-- <div id="selectAtom">
      <ul>
        <li v-for="(item, index) in atoms" :key="index">{{ item }}</li>
      </ul>
    </div> -->
  </div>
</template>

<script setup>
import {defineProps, defineEmits, onMounted, ref, inject} from "vue";
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
});

// 父组件获得子组件创建的 Viewer，子组件通过 emit 来定义
const emit = defineEmits(["viewer-created"]);

// 父组件通过 Ref 更新子组件的值（子组件的变量定义）
// let atoms = ref([]);
// defineExpose({
//   atoms,
// });

let xyzContent = ref(`# generated using pymatgen
data_CeO3
_symmetry_space_group_name_H-M   'P 1'
_cell_length_a   6.06488433
_cell_length_b   6.06488433
_cell_length_c   3.64122000
_cell_angle_alpha   90.00000000
_cell_angle_beta   90.00000000
_cell_angle_gamma   120.00000364
_symmetry_Int_Tables_number   1
_chemical_formula_structural   CeO3
_chemical_formula_sum   'Ce2 O6'
_cell_volume   115.99054273
_cell_formula_units_Z   2
loop_
_symmetry_equiv_pos_site_id
_symmetry_equiv_pos_as_xyz
1  'x, y, z'
loop_
_atom_site_type_symbol
_atom_site_label
_atom_site_symmetry_multiplicity
_atom_site_fract_x
_atom_site_fract_y
_atom_site_fract_z
_atom_site_occupancy
Ce  Ce0  1  0.33333300  0.66666700  0.75000000  1
Ce  Ce1  1  0.66666700  0.33333300  0.25000000  1
O  O2  1  0.91327400  0.58959600  0.75000000  1
O  O3  1  0.08672600  0.41040400  0.25000000  1
O  O4  1  0.67632100  0.08672600  0.75000000  1
O  O5  1  0.32367900  0.91327400  0.25000000  1
O  O6  1  0.41040400  0.32367900  0.75000000  1
O  O7  1  0.58959600  0.67632100  0.25000000  1
`);

const display = () => {
  // eslint-disable-next-line no-undef
  let element = $("#displayMol" + props.sIndex);
  console.log(element);
  console.log(props.sItem["input"]);
  let config = {backgroundColor: "white"};
  const newStyle = inject("newStyle");
  const defaultStyle = inject("defaultStyle");
  // eslint-disable-next-line no-undef
  import("/Users/hui_zhou/Project/3Dmol.js/build/3Dmol-min").then(($3Dmol) => {
    const viewer1 = $3Dmol.createViewer(element, config);
    let m = viewer1.addModel(xyzContent.value, "cif"); // 需要去掉 Selective 行
    viewer1.addUnitCell(m);
    viewer1.setStyle({}, defaultStyle);

    viewer1.setHoverable(
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
            viewer1.removeLabel(atom.label);
            delete atom.label;
          }
        }
    );
    viewer1.setClickable({}, true, function (atom, viewer1) {
      let atomItem = atom.index + 1;
      if (!atoms.value.includes(atomItem)) {
        viewer1.setStyle({index: atom.index}, newStyle);
        addAtoms(atom.index + 1);
        console.log("atoms after add", atoms.value)
        viewer1.render();
        updateItemsInput(atoms.value.join(","), props.sIndex)
      } else {
        viewer1.setStyle({index: atom.index}, defaultStyle);
        removeAtoms(atomItem);
        console.log("atoms after remove", atoms.value)
        updateItemsInput(atoms.value.join(","), props.sIndex)
        viewer1.render();
      }
    });
    // viewer1.render();
    viewer1.zoomTo();

    // 父组件获得子组件创建的 Viewer，子组件通过 emit 来定义
    emit("viewer-created", props.sIndex, viewer1);
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

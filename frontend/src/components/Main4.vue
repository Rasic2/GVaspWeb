<template>
  <div>
    <div id="info">
      <el-alert
          title="info alert"
          type="success"
          description="下方是输入框"
          show-icon
      />
    </div>
    <div class="containerDisplay">
      <div id="inputXYZ">
        <el-input type="textarea" rows="20" v-model="xyzContent" :placeholder="placeHolder1"/>
        <button @click="display">display</button>
      </div>
      <div id="displayMol"></div>
    </div>
  </div>
</template>

<script>
import {onMounted, ref} from "vue";
import $ from "jquery";

export default {
  name: 'XyzDisplay',
  setup() {
    let placeHolder1 = `请输入xyz格式的信息,第一行为总原子数,第二行为标题,第三行以及以后是原子三维坐标`
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
    let display = () => {
// eslint-disable-next-line no-undef
      let element = $('#displayMol');
      let config = {backgroundColor: 'white'};
// eslint-disable-next-line no-undef
      import("../../../../3Dmol.js/build/3Dmol-min").then(($3Dmol) => {
        const viewer1 = $3Dmol.createViewer(element, config);
        let m = viewer1.addModel(xyzContent.value, "cif"); // 需要去掉 Selective 行
        viewer1.addUnitCell(m);
        viewer1.setStyle({stick: {radius: 0.1}, sphere: {radius: 0.3}});
        viewer1.render();
        viewer1.zoomTo();
      })
    }
    onMounted(display)
    return {xyzContent, placeHolder1, display}
  },

}
</script>

<style scoped>
#info {
  margin-top: 50px;
  margin-left: 25px;
  width: 500px;
}

#inputXYZ {
  width: 500px;
}

#displayMol {
  height: 430px;
  width: 800px;
  position: relative;
}

.containerDisplay {
  margin-left: 25px;
  margin-top: 50px;
  display: flex;
}
</style>
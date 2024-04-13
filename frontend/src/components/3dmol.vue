<template>
    <div id="container-01" class="mol-container"></div>
    <button @click="AddSphere">Click</button>
</template>

<script>
export default {
    name: 'MyMol'
}
</script >

<script setup>
import $ from "jquery"

function AddSphere() {
    const element = $('#container-01');
    const config = { backgroundColor: 'orange' };
    import("3dmol/build/3Dmol-min").then(($3Dmol) => {
        console.log($3Dmol);
        $(function () {
            const viewer = $3Dmol.createViewer(element, config);
            viewer.addSphere({ center: { x: 0, y: 0, z: 0 }, radius: 10.0, color: 'green' });
            viewer.zoomTo();
            viewer.render();
            viewer.zoom(0.8, 2000);
        })
    })
}


</script>



<style>
.mol-container {
    width: 60%;
    height: 400px;
    position: relative;
}
</style>
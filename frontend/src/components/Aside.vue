<template>
    <div>
        <el-menu background-color="#545c64" text-color="#ffffff" active-text-color="#ffd04b" 
            class="el-menu-vertical-demo" router>
            <el-menu-item index="/index/plot_opt">结构优化</el-menu-item>
            <el-menu-item index="/index/plot_ep">静电势</el-menu-item>
            <el-menu-item index="/index/structure">结构渲染</el-menu-item>
            <!-- <el-menu-item index="/index/menu4">CIF测试</el-menu-item> -->
        </el-menu>
    </div>
</template>

<script>
export default {
    name: "MyAside"
}
</script>

<style scoped>
.el-menu-vertical-demo {
    height: 100%;
}
</style>

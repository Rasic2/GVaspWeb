<template>
    <div class="Echarts">
        <div id="energy_opt" style="width: 600px;height:400px;float:left;"></div>
        <div id="force_opt" style="width: 600px;height:400px;float:right;"></div>
    </div>
</template>
  
<script>
import { ref } from "vue";
const data = ref(null)

export default {
    name: 'MyEcharts',
    mounted() {
        this.EnergyEChart = this.$echarts.init(document.getElementById('energy_opt'));
        this.ForceEChart = this.$echarts.init(document.getElementById('force_opt'));
        // this.loading
        this.initDrawEChart();
    },
    methods: {
        initDrawEChart() {
            this.EnergyEChart.showLoading({
                maskColor: 'rgba(3,3,8,0.5)',
                textColor: '#fff600'
            });
            this.ForceEChart.showLoading({
                maskColor: 'rgba(3,3,8,0.5)',
                textColor: '#fff600'
            });

            this.$axios.get("http://127.0.0.1:5000/api/getdata", {
                headers: {
                    "Access-Control-Allow-Origin": "*"
                }
            }).then((res) => {
                this.EnergyEChart.hideLoading();
                this.ForceEChart.hideLoading();
                // console.log(res)
                data.value = res.data;
                // console.log(data.value);
                // console.log(this);
                var EnergyOption = {
                    title: {
                        text: 'Structure Optimization',
                        left: "center",
                        top: "top",
                    },
                    xAxis: [{
                        name: "Steps",
                        nameLocation: "center",
                        nameGap: 25,
                    }],
                    yAxis: [{
                        name: "Energy (eV)",
                        nameLocation: "center",
                        nameGap: 45,
                        max: function (value) {
                            return Math.ceil(value.max);
                        },
                        min: function (value) {
                            return Math.floor(value.min);
                        },
                    }],
                    dataZoom: [{
                        type: "inside"
                    }],
                    // toolbox: {
                    // 区域缩放
                    //     show: true,
                    //     feature: {
                    //         dataZoom: {
                    //             yAxisIndex: "none"
                    //         }
                    //     }
                    // },
                    series: [
                        {
                            data: data.value['energy'],
                            type: 'line',
                            label: {
                                show: false,
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    formatter: '{c}',
                                    align: 'left',
                                }
                            }
                        }
                    ]
                };
                var ForceOption = {
                    title: {
                        text: 'Structure Optimization',
                        left: "center",
                        top: "top",
                    },
                    xAxis: [{
                        name: "Steps",
                        nameLocation: "center",
                        nameGap: 25,
                    }],
                    yAxis: [{
                        name: "Force",
                        nameLocation: "center",
                        nameGap: 45,
                        max: function (value) {
                            return Math.ceil(value.max);
                        },
                        min: function (value) {
                            return Math.floor(value.min);
                        },
                    }],
                    dataZoom: [{
                        type: "inside"
                    }],
                    series: [
                        {
                            data: data.value['force'],
                            type: 'line',
                            label: {
                                show: false,
                            },
                            emphasis: {
                                label: {
                                    show: true,
                                    formatter: '{c}',
                                    align: 'left',
                                }
                            }
                        }
                    ]
                };
                this.EnergyEChart.setOption(EnergyOption);
                this.ForceEChart.setOption(ForceOption);
            }).catch(function (err) {
                console.log("Error", err)
            })
        },
    },
}
</script>
  
<style></style>
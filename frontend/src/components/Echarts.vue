<template>
    <div class="Echarts">
        <div id="main" style="width: 600px;height:400px;"></div>
    </div>
</template>
  
<script>
import { ref } from "vue";
const data = ref(null)

export default {
    name: 'MyEcharts',
    mounted() {
        this.myEChart = this.$echarts.init(document.getElementById('main'));
        this.loading
        this.initDrawEChart();
    },
    methods: {
        initDrawEChart() {
            this.myEChart.showLoading({
                maskColor: 'rgba(3,3,8,0.5)',
                textColor: '#fff600'
            });

            this.$axios.get("http://127.0.0.1:5000/api/getdata", {
                headers: {
                    "Access-Control-Allow-Origin": "*"
                }
            }).then((res) => {
                this.myEChart.hideLoading();
                // console.log(res)
                data.value = res.data;
                // console.log(data.value);
                // console.log(this);
                var option = {
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
                            data: data.value['data'],
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
                this.myEChart.setOption(option);
            }).catch(function (err) {
                console.log("Error", err)
            })
        },
    },
}
</script>
  
<style></style>
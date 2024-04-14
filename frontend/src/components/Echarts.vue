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
    methods: {
        myEcharts() {
            // 基于准备好的dom，初始化echarts实例
            var myChart = this.$echarts.init(document.getElementById('main'));

            // 指定图表的配置项和数据
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

            // 使用刚指定的配置项和数据显示图表。
            myChart.setOption(option);
        },

    },
    created() {
        this.$axios.get("http://127.0.0.1:5000/api/getdata", { headers: { "Access-Control-Allow-Origin": "*" } }).then((res) => {
            console.log(res)
            data.value = res.data;
            console.log(data.value);
            console.log(this);
            this.myEcharts();
        }).catch(function (err) {
            console.log("Error", err)
        })
    },
    // mounted() {
    //     this.myEcharts();
    // }
}
</script>
  
<style></style>
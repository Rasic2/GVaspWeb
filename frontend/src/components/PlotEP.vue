<template>
    <div class="Echarts">
        <div id="plot_ep" style="width: 600px;height:400px"></div>
    </div>
</template>
  
<script>
import { ref } from "vue";
const data = ref(null)

export default {
    name: 'MyEcharts',
    mounted() {
        this.EPEChart = this.$echarts.init(document.getElementById('plot_ep'));
        this.initDrawEChart();
    },
    methods: {
        initDrawEChart() {
            this.EPEChart.showLoading({
                maskColor: 'rgba(3,3,8,0.5)',
                textColor: '#fff600'
            });

            this.$axios.get("/api/get_ep_data", {
                headers: {
                    "Access-Control-Allow-Origin": "*"
                }
            }).then((res) => {
                this.EPEChart.hideLoading();
                // console.log(res)
                data.value = res.data;
                // console.log(data.value);
                // console.log(this);
                var EPOption = {
                    title: {
                        text: 'Local Potential',
                        left: "center",
                        top: "top",
                    },
                    xAxis: [{
                        name: "Position (Å)",
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
                    series: [
                        {
                            data: data.value['locpot'],
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
                this.EPEChart.setOption(EPOption);
            }).catch(function (err) {
                console.log("Error", err)
            })
        },
    },
}
</script>
  
<style></style>
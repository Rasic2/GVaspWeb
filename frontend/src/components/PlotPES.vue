<template>
  <div>
    <div class="paramSetting">
      <h1>能垒图绘制参数设置</h1>
      <div class="singleRoute" v-for="(item, index) in routes" :key="index">
        <el-icon class="iconLayout" @click="removeRoute(index)">
          <RemoveFilled />
        </el-icon>
        <el-input class="input" v-model="item.input" @input="inputRoute(index)" placeholder="请输入能量，逗号分隔" />
      </div>
      <el-button @click="addRoute" class="expand_btn" :disabled="addAtomDisabled">+ 添加反应路径</el-button>
    </div>
    <div id="pesEchart"></div>
  </div>
</template>

<script>
export default {
  name: "PlotPES",
};
</script>

<script setup>
import { ref, watch } from "vue";
import axios from "axios";
import * as echarts from "echarts";

const apiUrl = process.env.VUE_APP_API_URL || '';

// Ref variables

const routes = ref([])
const plotData = ref([])

watch(plotData, (newValue, oldValue) => {
  plot();
});

// Methods

/**
 * Adds a new route to the `routes` array.
 *
 * @return {void} This function does not return anything.
 */
const addRoute = () => {
  routes.value.push({
    input: ""
  });
};

/**
 * Removes a route from the `routes` array at the specified index.
 *
 * @param {number} index - The index of the route to remove.
 * @return {void} This function does not return anything.
 */
const removeRoute = (index) => {
  routes.value.splice(index, 1);
  plotData.value = plotData.value.filter((item) => item.name != `L${index}`);
};

const inputRoute = async (index) => {
  let inputs = []
  routes.value.forEach((item) => {
    inputs.push(item['input'].split(",").map((item) => parseFloat(item)));
  })
  let params = { "data": inputs }
  try {
    const res = await axios.post(apiUrl + "/api/get_pes_data", params, {
      headers: {
        "Access-Control-Allow-Origin": "*",
      },
    });
    if (res.status == 200) {
      console.log("Server Response", res.data)
      plotData.value = res.data
    }
  } catch (error) {
    console.error(error);
  }
};

const plot = () => {
  let pesEchart = echarts.init(document.getElementById("pesEchart"));
  pesEchart.clear();

  /** @type EChartsOption */
  var pesOption = {
    title: {
      text: '能量势垒图'
    },
    legend: {},
    tooltip: {
      trigger: 'axis',
      axisPointer: {
        type: 'none' // 移除垂直竖线
      },
      formatter: function (params) {
        let dashedCount = params.filter((item) => pesOption.series[item.seriesIndex].lineStyle.type == 'dashed').length
        if (dashedCount > 0) {
          var tooltipContent = '<div style="text-align: left;">';
          tooltipContent += '<table>';
          params.forEach((item) => {
            var line = pesOption.series[item.seriesIndex]
            var lineStyle = line.lineStyle
            if (lineStyle.type != 'solid') {
              tooltipContent += `<tr>
                    <td style="text-align: left; padding-right: 10px; color: red;">${item.marker}${item.seriesName}(能垒)</td>
                    <td style="text-align: right; font-weight: bold; color: red;">${(line.data[1][1] - line.data[0][1]).toFixed(2)} eV</td>
                </tr>`
            }
          })
          tooltipContent += '</table>';
          tooltipContent += '</div>';
          return tooltipContent
        }
      }
    },
    xAxis: {
      type: 'value',
      name: 'Reaction Coordinates',
      nameLocation: 'center',
      nameGap: 15,
      axisTick: { show: false },
      axisLabel: {
        show: false,
      },
    },
    yAxis: {
      type: 'value',
      name: "Energy (eV)",
      nameLocation: "center",
      nameGap: 45,
    },
    series: plotData.value
  };
  pesEchart.setOption(pesOption);
  pesEchart.on('mouseover', function (params) {
    console.log(params)
  })
}

</script>

<style>
#pesEchart {
  width: 570px;
  height: 380px;
  display: flex;
  float: right
}

.singleRoute {
  display: flex;
  margin-bottom: 5px;
}

.iconLayout {
  display: flex;
  align-items: center;
  height: 30px;
  padding: 0 5px;
}

.input {
  height: 30px;
  width: 200px;
}

.expand_btn {
  width: 120px;
  display: flex;
  margin-top: 5px;
  margin-left: 25px;
}

.paramSetting {
  width: 600px;
  padding-bottom: 20px;
  padding-top: 1px;
  -webkit-box-shadow: #999 0 0 5px;
  -moz-box-shadow: #999 0 0 5px;
  box-shadow: #999 0 0 5px;
  background: white;
  border-radius: 10px;
  float: left;
}
</style>
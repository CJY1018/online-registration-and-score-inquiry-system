<template>
  <el-main style="background: white;padding: 20px;height: 100%">
    <!--  搜索  -->
    <div class="search">
      考试名称 / 场次：
      <el-cascader
          v-model="select_exam"
          :options="exam_names_turns"
          placeholder="请选择考试名称和场次"
          style="width: 200px"
          clearable
      />
      <el-button type="primary" @click="handleSearch" style="margin-left: 50px">搜索</el-button>
      <el-button @click="handleReset" style="margin-left: 20px">重置</el-button>
    </div>
    <div id="main" style="width: 600px;height:400px;margin: 20px auto;
    border: 1px solid #ccc;border-radius: 10px;box-shadow: 0 0 5px #ccc;padding: 10px"/>
    <div style="width: 600px;margin: 20px auto;">
      <ul>
        <li>
          <el-descriptions style="margin: 20px auto;width: 150px" border>
            <el-descriptions-item label="平均分：">{{ average }}</el-descriptions-item>
          </el-descriptions>
        </li>
        <li>
          <el-descriptions style="margin: 20px auto; width: 150px" border>
            <el-descriptions-item label="中位分：">{{ median }}</el-descriptions-item>
          </el-descriptions>
        </li>
      </ul>
    </div>
  </el-main>
</template>

<script>
import axios from "axios";
import {ElNotification} from "element-plus";
import {markRaw} from 'vue'
import 'element-plus/dist/index.css'

// 引入 echarts 核心模块，核心模块提供了 echarts 使用必须要的接口。
import * as echarts from 'echarts/core';
// 引入柱状图图表，图表后缀都为 Chart
import {BarChart, LineChart} from 'echarts/charts';
// 引入提示框，标题，直角坐标系，数据集，内置数据转换器组件，组件后缀都为 Component
import {
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  DataZoomComponent,
  ToolboxComponent,
  MarkLineComponent
} from 'echarts/components';
// 标签自动布局、全局过渡动画等特性
import {LabelLayout, UniversalTransition} from 'echarts/features';
// 引入 Canvas 渲染器，注意引入 CanvasRenderer 或者 SVGRenderer 是必须的一步
import {CanvasRenderer} from 'echarts/renderers';
import "echarts/lib/component/dataZoom";

// 注册必须的组件
echarts.use([
  TitleComponent,
  TooltipComponent,
  GridComponent,
  DatasetComponent,
  TransformComponent,
  DataZoomComponent,
  ToolboxComponent,
  MarkLineComponent,
  BarChart,
  LineChart,
  LabelLayout,
  UniversalTransition,
  CanvasRenderer,
]);

export default {
  email: 'ScoreAnalysis',
  data() {
    return {
      filterTableData: [],
      myChart: null,
      grades: [],
      select_exam: [],
      exam_names_turns: [],
      average: 0.0,
      median: 0.0,
    }
  },
  methods: {
    handleSearch() {
      if (!this.select_exam || this.select_exam.length === 0) {
        ElNotification({
          title: '警告',
          message: '请选择考试名称和场次',
          type: 'warning'
        })
        return
      }
      axios.get("http://localhost:8000/administrator/score_analysis/grades/" + this.select_exam[0] + "/" + this.select_exam[1])
          .then(res => {
            if (res.data.status === 'failed') {
              ElNotification({
                title: '警告',
                message: '没有该考试信息',
                type: 'warning'
              })
              this.myChart.clear()
              this.myChart.showLoading({
                text: '没有该考试信息',
                fontSize: 18,
                color: 'transparent', // loading颜色，设置成透明或白色，不然会显示loading状态
                textColor: '#ccc',// 文字颜色
                maskColor: 'rgba(255, 255, 255, 0.2)' // 背景色
              })
              return
            }
            this.grades = res.data.data
            this.average = res.data.average
            this.median = res.data.median
            this.paint()
          })
          .catch(e => {
            console.log(e)
          })
    },
    paint() {
      this.myChart.hideLoading()
      // 绘制图表
      this.myChart.setOption({
        title: {
          text: '分数分布'
        },
        toolbox: {
          show: true,
          feature: {
            mark: {show: true},
            // 以表格方式展示数据
            dataView: {
              show: true, title: '一分一段表', optionToContent: function (opt) {
                var axisData = opt.xAxis[0].data;
                var series = opt.series;
                var table = '<table style="width:90%;text-align:center;border-collapse:collapse;border: 1px solid #EBEEF5">'
                    + '<thead style="background-color: #F4F5F7"><tr>'
                    + '<th>分数</th>'
                    + '<th>人数</th>'
                    + '</tr></thead><tbody>';
                for (var i = 0, l = axisData.length; i < l; i++) {
                  // 条纹
                  table += '<tr style="background-color: ' + (i % 2 ? '#FAFAFA' : '#fff') + ';border: 1px solid #EBEEF5">'
                      + '<td>' + axisData[i] + '</td>'
                      + '<td>' + series[0].data[i] + '</td>'
                      + '</tr>';
                }
                table += '</tbody></table>';
                return table;
              }, lang: ['一分一段表', '关闭', '刷新'], readOnly: true,
            },
            magicType: {show: true, type: ['line', 'bar']},
            restore: {show: true},
            saveAsImage: {show: true}
          }
        },
        tooltip: {},
        dataZoom: [
          {
            type: 'inside'
          },
          {
            type: 'slider'
          },
        ],
        xAxis: {
          name: '分数',
          data: this.grades.map(item => item.grade),
        },
        yAxis: {
          name: '数量',
        },
        series: [
          {
            name: '一分一段',
            type: 'bar',
            barWidth: '99.3%',
            precision: 2,
            data: this.grades.map(item => item.count),
            // 在分数为425的地方画一条线
            markLine: {
              symbol: ['none', 'none'],
              precision: 2,
              data: [
                {xAxis: 425, name: '及格线', lineStyle: {color: '#ee6666'}},
                {xAxis: this.average, name: '平均分', lineStyle: {color: '#fac858'}},
                {xAxis: this.median, name: '中位分', lineStyle: {color: '#91cc75'}}
              ]
            }
          }
        ]
      });
    },
    handleReset() {
      this.select_exam = []
    }
  },
  mounted() {
    axios.get("http://localhost:8000/administrator/score_analysis")
        .then(res => {
          this.filterTableData = res.data.data
          // 将考试名称和考试轮次按树形结构组织
          let exam_tree = {}
          this.filterTableData.forEach(item => {
            if (!exam_tree[item.exam_name]) {
              exam_tree[item.exam_name] = []
              exam_tree[item.exam_name].push(item.exam_turn)
            } else if (!exam_tree[item.exam_name].includes(item.exam_turn)) {
              exam_tree[item.exam_name].push(item.exam_turn)
            }
          })

          for (let key in exam_tree) {
            this.exam_names_turns.push({
              value: key,
              label: key,
              children: exam_tree[key].map(turn => {
                return {
                  value: turn,
                  label: turn
                }
              })
            })
          }
        })
        .catch(e => {
          console.log(e)
        })

    // 基于准备好的dom，初始化echarts实例
    this.myChart = markRaw(echarts.init(document.getElementById('main')));
    this.myChart.showLoading({
      text: '请先选择考试名称和场次',
      fontSize: 18,
      color: 'transparent', // loading颜色，设置成透明或白色，不然会显示loading状态
      textColor: '#ccc',// 文字颜色
      maskColor: 'rgba(255, 255, 255, 0.2)' // 背景色
    })
  }
}

</script>

<style scoped>
ul {
  display: flex;
  justify-content: space-around;
  list-style: none;
  padding: 0;
}


</style>
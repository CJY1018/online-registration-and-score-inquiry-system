<template>
  <div>
    <div class="block-border">
      <p style="font-size: 20px; margin: 0 0 40px 0;" class="search">考试成绩查询</p>
      <!--  搜索  -->
      <div>
        考试名称：
        <el-select v-model="select_exam" placeholder="请选择考试名称" style="width: 200px">
          <el-option
              v-for="item in exam_names"
              :key="item"
              :label="item"
              :value="item">
          </el-option>
        </el-select>
        <el-button type="primary" @click="handleSearch" style="margin-left: 50px">搜索</el-button>
        <el-button @click="handleReset" style="margin-left: 20px">重置</el-button>
      </div>

      <!--  成绩列表  -->
      <div style="width: 80%;margin: 40px auto">
        <p style="font-size: 20px; margin: 0 0 40px 0;color: #3083C7">{{ exam_title }}</p>
        <p style="text-align: left">
          姓名: {{ stu_name }}&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
          身份证号: {{ id_no }}
        </p>
        <el-table
            :data="tableData"
            style="width: 100%"
            stripe
            border
            header-row-class-name="table-header"
            table-layout="auto"
        >
          <el-table-column prop="exam_turn" label="考试轮次"></el-table-column>
          <el-table-column prop="stu_school" label="学校"></el-table-column>
          <el-table-column prop="exam_grades" label="分数"></el-table-column>
          <el-table-column prop="rank" label="排名"></el-table-column>
          <el-table-column prop="school_rank" label="本校排名"></el-table-column>
        </el-table>

      </div>
    </div>

    <!--  一分一段  -->
    <div class="block-border">
      <p style="font-size: 20px;margin:0 0 20px 0;" class="search">“一分一段”&nbsp;&nbsp;&nbsp;&nbsp;查询图表</p>
      <ScoreAnalysis></ScoreAnalysis>
    </div>

  </div>
</template>

<script>
import axios from "axios";
import {ElNotification} from "element-plus";
import 'element-plus/dist/index.css'
import ScoreAnalysis from "@/components/administrator_console_page/menu/ScoreAnalysis.vue";

export default {
  components: {ScoreAnalysis},
  email: 'ScoreAnalysis',
  data() {
    return {
      select_exam: [],
      exam_names: [],
      tableData: [],
      exam_title: '成绩列表',
      stu_name: '',
      id_no: ''
    }
  },
  methods: {
    handleSearch() {
      if (this.select_exam.length === 0) {
        ElNotification({
          title: '提示',
          message: '请先选择考试名称',
          type: 'error'
        });
        return;
      }
      axios.get('http://localhost:8000/score_inquiry/exams/' + this.select_exam, {
        headers: {
          // 从Cookie中获取名为access_token的值
          'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
        }
      }).then(res => {
        this.tableData = res.data.data;
        console.log(res.data.data)
        this.exam_title = res.data.exam_title;
      }).catch(err => {
        console.log(err);
      })
    },
    handleReset() {
      this.select_exam = '';
      this.tableData = [];
      this.exam_title = '成绩列表';
    }
  },
  mounted() {
    axios.get('http://localhost:8000/score_inquiry', {
      headers: {
        // 从Cookie中获取名为access_token的值
        'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
      }
    }).then(res => {
      this.exam_names = res.data.exam_names.sort()
      this.stu_name = res.data.stu_name;
      this.id_no = res.data.id_no;
    }).catch(err => {
      console.log(err);
    })
  }
}


</script>

<style scoped>
/deep/ .table-header th {
  background-color: #0DA3E2;
  color: #fff;
}

.block-border {
  border: 1px solid #DCDFE6;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 35px;
  margin: 40px 160px 60px 160px;
  padding: 0;
  background-color: white;
}

.search {
  background-color: #DDE7FF;
  padding: 20px;
  border-radius: 35px 35px 0 0;
}

</style>
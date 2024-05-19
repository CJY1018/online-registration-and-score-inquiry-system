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

    <el-table
        :data="filterTableData"
        style="width: 100%;"
        height="520px"
        :header-cell-style="{background: '#F4F5F7'}"
        table-layout="auto"
        ref="table"
        stripe
        border
        :cell-class-name="cellClassName"
        @cell-dblclick="dblclick">
      <el-table-column
          prop="id_no"
          label="身份证号"
          sortable>
        <template #default="scope">
          <span>{{ scope.row.id_no }}</span>
        </template>
      </el-table-column>
      <el-table-column
          v-for="item in items"
          :key="item.prop"
          :prop="item.prop"
          :label="item.label"
          :sortable="item.sortable">
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row[item.prop]"
                    @blur="handleAlter" ref="fo_input"/>
          <span v-else>{{ scope.row[item.prop] }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-pagination
        @size-change="handleSizeChange"
        @current-change="handleCurrentChange"
        :current-page="currentPage"
        :page-sizes="[10, 20, 30, 40]"
        :page-size="perPage"
        layout="total, sizes, prev, pager, next, jumper"
        :total="total">
    </el-pagination>
    <el-button class="mt-4" type="success" plain style="width: 100%;margin: 0" @click="handleSave">
      保存
    </el-button>
    <el-button class="mt-4" type="warning" plain style="width: 100%;margin: 0" @click="handleRandom">
      随机分配
    </el-button>
  </el-main>

</template>

<script>
import axios from "axios";

import 'element-plus/dist/index.css'
import {nextTick} from "vue";
import {ElNotification} from "element-plus";

const items = [
  {prop: 'invigilator_no', label: '监考员编号', sortable: true},
  {prop: 'exam_venue', label: '考试地点', sortable: true},
  {prop: 'exam_venue_no', label: '考试地点编号', sortable: true},
]


export default {
  email: '',
  data() {
    return {
      filterTableData: [],
      copyTableData: [],
      items,
      editRow: -1,
      editCol: -1,
      invigilator_no: [],
      select_exam: [],
      exam_names_turns: [],
      currentPage: 1,
      perPage: 20,
      total: 0
    }
  },
  methods: {
    cellClassName({row, column, rowIndex, columnIndex}) {
      row.index = rowIndex;
      column.index = columnIndex;
    },
    dblclick(row, col) {
      this.editRow = row.index
      this.editCol = col.index
      nextTick(() => {
        if (this.$refs.fo_input && this.$refs.fo_input.length > 0)
          this.$refs.fo_input[0].focus()
      })
      console.log(row.index, col.index)
    },
    handleAlter() {
      this.editRow = -1
      this.editCol = -1
    },
    handleSearch() {
      if (!this.select_exam || this.select_exam.length === 0) {
        this.filterTableData = JSON.parse(JSON.stringify(this.copyTableData))
        return
      }
      let exam_name = this.select_exam[0]
      let exam_turn = this.select_exam[1]
      // this.filterTableData = this.copyTableData.filter(item => {
      //   return item.exam_name === exam_name && item.exam_turn === exam_turn
      // })
      axios.get("http://localhost:8000/administrator/exam_arrangement", {
        params: {
          exam_name,
          exam_turn,
          page: this.currentPage,
          per_page: this.perPage
        }
      }).then(res => {
        this.filterTableData = res.data.items
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        this.total = res.data.total
      }).catch(e => {
        console.log(e)
      })
    },
    handleReset() {
      this.select_exam = []
      axios.get("http://localhost:8000/administrator/exam_arrangement", {
        params: {
          page: 1,
          per_page: 20
        }
      }).then(res => {
        this.filterTableData = res.data.items
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        this.total = res.data.total
      }).catch(e => {
        console.log(e)
      })
    },
    handleSave() {
      axios.post('http://localhost:8000/administrator/exam_arrangement', {
        exams: this.filterTableData,
        page: this.currentPage,
        per_page: this.perPage
      }).then(res => {
        if (res.data.status === 'success') {
          ElNotification({
            title: '成功',
            message: '保存成功',
            type: 'success'
          })
          // 保存成功，更新原数据
          this.copyTableData = res.data.data.items
        } else {
          ElNotification({
            title: '失败',
            message: '保存失败，' + res.data.message,
            type: 'error'
          })
          // 保存失败，恢复原数据
          this.filterTableData = JSON.parse(JSON.stringify(this.copyTableData))
        }
      }).catch(() => {
        ElNotification({
          title: '失败',
          message: '保存失败',
          type: 'error'
        })
        // 保存失败，恢复原数据
        this.filterTableData = JSON.parse(JSON.stringify(this.copyTableData))
      })
    },
    handleRandom() {
      console.log(this.invigilator_no)
      this.filterTableData.forEach(item => {
        item.invigilator_no = this.invigilator_no[Math.floor(Math.random() * this.invigilator_no.length)]
        item.exam_venue = '考试地点' + Math.floor(Math.random() * 1000)
        item.exam_venue_no = Math.floor(Math.random() * 1000)
      })
    },
    handleSizeChange(val) {
      this.perPage = val
      let exam_name = this.select_exam[0]
      let exam_turn = this.select_exam[1]
      axios.get("http://localhost:8000/administrator/exam_arrangement", {
        params: {
          exam_name,
          exam_turn,
          page: this.currentPage,
          per_page: val
        }
      }).then(res => {
        this.filterTableData = res.data.items
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        this.total = res.data.total
      }).catch(e => {
        console.log(e)
      })
    },
    handleCurrentChange(val) {
      this.currentPage = val
      let exam_name = this.select_exam[0]
      let exam_turn = this.select_exam[1]
      axios.get("http://localhost:8000/administrator/exam_arrangement", {
        params: {
          exam_name,
          exam_turn,
          page: val,
          per_page: this.perPage
        }
      }).then(res => {
        this.filterTableData = res.data.items
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        this.total = res.data.total
      }).catch(e => {
        console.log(e)
      })
    }
  },
  mounted() {
    axios.get("http://localhost:8000/administrator/exam_arrangement", {
      params: {
        page: 1,
        per_page: 20
      }
    }).then(res => {
      this.filterTableData = res.data.items
      this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
      this.total = res.data.total

      // 获取考试名称和场次
      axios.get("http://localhost:8000/administrator/exam_arrangement/exam_name_turn")
          .then(res => {
            const exam_tree = res.data.data
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


      // 获取监考员编号
      axios.get("http://localhost:8000/administrator/exam_arrangement/invigilator_no")
          .then(res => {
            this.invigilator_no = res.data.data.map(item => item.invigilator_no)
          })
          .catch(e => {
            console.log(e)
          })
    }).catch(e => {
      console.log(e)
    })
  },
}

</script>

<style scoped>

</style>
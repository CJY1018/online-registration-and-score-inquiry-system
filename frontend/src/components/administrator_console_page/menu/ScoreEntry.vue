<template>
  <el-main style="background: white;padding: 20px;height: 100%">
    <el-table
        :data="filterTableData"
        style="width: 100%;"
        height="600px"
        :header-cell-style="{background: '#F4F5F7'}"
        table-layout="auto"
        ref="table"
        stripe
        border
        :cell-class-name="cellClassName"
        @cell-dblclick="dblclick">
      <el-table-column
          v-for="item in items"
          :key="item.prop"
          :prop="item.prop"
          :label="item.label"
          :sortable="item.sortable">
        <template #default="scope">
          <span>{{ scope.row[item.prop] }}</span>
        </template>
      </el-table-column>
      <el-table-column
          prop="exam_grades"
          label="考试成绩"
          sortable>
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row.exam_grades"
                    @blur="handleAlter" ref="fo_input2"/>
          <span v-else>{{ scope.row.exam_grades }}</span>
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
      Save
    </el-button>
  </el-main>
</template>

<script>
import axios from "axios";
import {nextTick} from "vue";

import 'element-plus/dist/index.css'
import {ElNotification} from "element-plus";


const items = [
  {prop: 'exam_name', label: '考试名', sortable: true},
  {prop: 'exam_turn', label: '考试场次', sortable: true},
  {prop: 'id_no', label: '身份证号', sortable: true},
  {prop: 'stu_name', label: '学生姓名', sortable: true},
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
      perPage: 20,
      currentPage: 1,
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
      console.log(row.index, col.index)
      nextTick(() => {
        if (this.$refs.fo_input2)
          this.$refs.fo_input2.focus()

      })
    },
    handleAlter() {
      this.editRow = -1
      this.editCol = -1
    },
    handleSave() {
      axios.post('http://localhost:8000/administrator/score_entry', {
        examinees: this.filterTableData
      }).then(() => {
        ElNotification({
          title: '成功',
          message: '保存成功',
          type: 'success'
        })
        // 保存成功，更新原数据
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
      }).catch(err => {
        console.log(err)
        ElNotification({
          title: '失败',
          message: '保存失败',
          type: 'error'
        })
        // 保存失败，恢复原数据
        this.filterTableData = JSON.parse(JSON.stringify(this.copyTableData))
      })
    },
    handleSizeChange(val) {
      this.perPage = val;
      axios.get('http://localhost:8000/administrator/score_entry', {
        params: {
          page: this.currentPage,
          per_page: val
        }
      }).then(res => {
        this.filterTableData = res.data.items;
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        this.total = res.data.total;
      }).catch(err => {
        console.log(err);
      });
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      axios.get('http://localhost:8000/administrator/score_entry', {
        params: {
          page: val,
          per_page: this.perPage
        }
      }).then(res => {
        this.filterTableData = res.data.items;
        this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        this.total = res.data.total;
      }).catch(err => {
        console.log(err);
      });
    }
  },
  mounted() {
    axios.get('http://localhost:8000/administrator/score_entry', {
      params: {
        page: 1,
        per_page: 20
      }
    }).then(res => {
      this.filterTableData = res.data.items;
      this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
      this.total = res.data.total;
    }).catch(err => {
      console.log(err);
    });
  }
}

</script>


<style scoped>

</style>
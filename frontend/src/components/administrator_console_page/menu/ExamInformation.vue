<template>
  <el-main style="background: white;padding: 20px;height: 100%">
    <el-table
        :data="filterTableData"
        style="width: 100%;"
        height="500px"
        :header-cell-style="{background: '#F4F5F7'}"
        table-layout="auto"
        ref="table"
        stripe
        border
        :cell-class-name="cellClassName"
        @cell-dblclick="dblclick"
        @selection-change="handleSelectionChange">
      <el-table-column type="selection" width="55"/>
      <el-table-column
          prop="exam_no"
          label="考试编号"
          sortable>
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row.exam_no"
                    @blur="handleAlter" ref="fo_input"/>
          <span v-else>{{ scope.row.exam_no }}</span>
        </template>
      </el-table-column>
      <el-table-column
          prop="exam_turn"
          label="考试场次"
          sortable>
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row.exam_turn"
                    @blur="handleAlter" ref="fo_input"/>
          <span v-else>{{ scope.row.exam_turn }}</span>
        </template>
      </el-table-column>
      <el-table-column
          prop="exam_name"
          label="考试名"
          sortable>
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row.exam_name"
                    @blur="handleAlter" ref="fo_input"/>
          <span v-else>{{ scope.row.exam_name }}</span>
        </template>
      </el-table-column>
      <el-table-column
          prop="exam_time"
          label="考试时间"
          sortable>
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row.exam_time"
                    @blur="handleAlter" ref="fo_input"/>
          <span v-else>{{ time_format(scope.row) }}</span>
        </template>
      </el-table-column>
      <el-table-column
          prop="exam_info"
          label="考试信息"
          show-overflow-tooltip>
        <template #default="scope">
          <el-input v-if="scope.row.index === editRow && scope.column.index === editCol" v-model="scope.row.exam_info"
                    @blur="handleAlter" ref="fo_input"/>
          <span v-else>{{ scope.row.exam_info }}</span>
        </template>
      </el-table-column>
    </el-table>
    <el-button class="mt-4" type="primary" plain style="width: 100%" @click="handleAdd">
      Add Item
    </el-button>
    <el-button class="mt-4" type="danger" plain style="width: 100%;margin: 0" @click="handleDelete">
      Delete
    </el-button>
    <el-button class="mt-4" type="success" plain style="width: 100%;margin: 0" @click="handleSave">
      Save
    </el-button>
  </el-main>
</template>

<script>
import {nextTick} from "vue";
import axios from "axios";
import {dayjs, ElMessageBox, ElNotification} from "element-plus";
import 'element-plus/dist/index.css'


export default {
  email: "ExamInformation",
  data() {
    return {
      filterTableData: [],
      copyTableData: [],
      multipleTableRef: null,
      editIndex: -1,
      editRow: -1,
      editCol: -1
    }
  },
  computed: {
    time_format() {
      return (row) => {
        return dayjs(row.exam_time).format('YYYY-MM-DD HH:mm:ss')
      }
    }
  },
  methods: {
    handleAdd() {
      this.filterTableData.push({
        exam_no: '',
        exam_turn: '',
        exam_name: '',
        exam_time: dayjs(new Date()).format('YYYY-MM-DDTHH:mm:ss'),
        exam_info: '',
      })
    },
    handleEdit(index) {
      this.editIndex = index
    },
    handleDelete() {
      if (this.multipleTableRef && this.multipleTableRef.length > 0) {
        ElMessageBox.confirm('确认删除勾选行吗？', '警告', {
          confirmButtonText: '删除',
          cancelButtonText: '取消',
          type: 'error'
        }).then(() => {
          this.multipleTableRef.forEach(item => {
            const index = this.filterTableData.indexOf(item)
            this.filterTableData.splice(index, 1)
          })
        }).catch(() => {
          console.log('cancel')
        })
      }
    },
    handleSave() {
      let diffTableData = JSON.parse(JSON.stringify(this.filterTableData))
      let hasEmpty = false

      // 删除index属性
      diffTableData.forEach(item => {
        if (item.index !== undefined)
          delete item.index
        if (item.exam_no === '' || item.exam_turn === '' || item.exam_name === '' || item.exam_time === '') {
          hasEmpty = true
        }
      })
      // 比较两个数组是否相等
      let diff = JSON.stringify(diffTableData) === JSON.stringify(this.copyTableData)
      if (diff) {
        ElMessageBox.alert('没有修改', '提示', {
          confirmButtonText: '确定',
          type: 'info'
        })
      } else if (hasEmpty) {
        ElMessageBox.alert('请填写完整信息', '提示', {
          confirmButtonText: '确定',
          type: 'error'
        })
      } else {
        // 保存修改
        ElMessageBox.confirm(`确认保存修改吗？`, '警告', {
          confirmButtonText: '保存',
          cancelButtonText: '取消',
          type: 'warning'
        }).then(() => {
          axios.post('http://localhost:8000/administrator/exam_information', {
            exams: this.filterTableData
          }).then(res => {
            if (res.data.status === 'success') {
              ElNotification({
                title: '成功',
                message: '保存成功',
                type: 'success'
              })
              // 保存成功，更新原数据
              this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
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
        }).catch(() => {
          console.log('cancel')
        })
      }
    },
    cellClassName({row, column, rowIndex, columnIndex}) {
      row.index = rowIndex;
      column.index = columnIndex;
    },
    dblclick(row, col) {
      this.editRow = row.index
      this.editCol = col.index
      nextTick(() => {
        if (this.$refs.fo_input)
          this.$refs.fo_input.focus()
      })
      console.log(row.index, col.index)
    },
    handleAlter() {
      this.editRow = -1
      this.editCol = -1
    },
    handleSelectionChange(val) {
      this.multipleTableRef = val
    },
  },
  mounted() {
    axios.get("http://localhost:8000/administrator/exam_information")
        .then(res => {
          this.filterTableData = res.data.data
          this.copyTableData = JSON.parse(JSON.stringify(this.filterTableData))
        })
        .catch(e => {
          console.log(e)
        })
  }
}

</script>

<style scoped>


</style>
<template>
  <el-main style="background: white;padding: 20px">
    <!--  搜索  -->
    <div class="search-input">
      <ul>
        <li style="min-width: 285px">
          身份证号：
          <el-input
              placeholder="请输入搜索内容"
              v-model="search_id_no"
              clearable
              style="width: 200px">
          </el-input>
        </li>

        <li style="min-width: 285px">
          用户姓名：
          <el-input
              placeholder="请输入搜索内容"
              v-model="search_stu_name"
              clearable
              style="width: 200px">
          </el-input>
        </li>

        <li style="min-width: 285px">
          用户学校：
          <el-input
              placeholder="请输入搜索内容"
              v-model="search_stu_school"
              clearable
              style="width: 200px">
          </el-input>
        </li>

        <li style="flex: 1"/>

        <li>
          <el-button type="primary" :icon="Search" @click="search">搜索</el-button>
        </li>
        <li>
          <el-button :icon="RefreshRight" @click="reset">重置</el-button>
        </li>

      </ul>
    </div>

    <!--  表格  -->
    <el-table
        :data="filterTableData"
        style="width: 100%;"
        max-height="540"
        :header-cell-style="{background: '#F4F5F7'}"
        table-layout="auto"
        stripe
        border>
      <el-table-column
          prop="id_no"
          width="200"
          label="身份证号码"
          sortable>
      </el-table-column>
      <el-table-column
          prop="stu_name"
          label="姓名"
          sortable>
      </el-table-column>
      <el-table-column
          prop="stu_no"
          label="学号">
      </el-table-column>
      <el-table-column
          prop="stu_school"
          label="学校"
          sortable>
      </el-table-column>
      <el-table-column
          prop="stu_department"
          label="院系">
      </el-table-column>
      <el-table-column
          prop="stu_major"
          label="专业">
      </el-table-column>
      <el-table-column
          prop="stu_cls"
          label="班级">
      </el-table-column>
      <el-table-column
          prop="confirm"
          label="报名状态"
          :filters="[{text: '未确认', value: '0'}, {text: '已确认', value: '1'}]"
          :filter-method="filterConfirm"
          filter-placement="bottom-end">
        <template #default="scope">
          <el-tag :type="scope.row.confirm === '0' ? 'danger' : 'success'" disable-transitions>
            {{ scope.row.confirm === '0' ? '未确认' : '已确认' }}
          </el-tag>
        </template>
      </el-table-column>
      <el-table-column
          prop="pay_status"
          label="支付状态"
          :filters="[{text: '未支付', value: '0'}, {text: '已支付', value: '1'}]"
          :filter-method="filterPayStatus"
          filter-placement="bottom-end">
        <template #default="scope">
          <el-tag :type="scope.row.pay_status === '0' ? 'danger' : 'success'" disable-transitions>
            {{ scope.row.pay_status === '0' ? '未支付' : '已支付' }}
          </el-tag>
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
  </el-main>
</template>

<script>
import axios from "axios";
import {nextTick} from "vue";
import {RefreshRight, Search} from "@element-plus/icons-vue";


export default {
  email: "RegistrationInformation",
  computed: {
    RefreshRight() {
      return RefreshRight
    },
    Search() {
      return Search
    }
  },
  data() {
    return {
      search_id_no: '',
      search_stu_name: '',
      search_stu_school: '',
      tableData: [],
      filterTableData: [],
      perPage: 20,
      currentPage: 1,
      total: 0
    }
  },
  methods: {
    filterConfirm(value, row) {
      return row.confirm === value;
    },
    filterPayStatus(value, row) {
      return row.pay_status === value;
    },
    search() {
      axios.get('http://localhost:8000/administrator/registration_information/search', {
        params: {
          id_no: this.search_id_no,
          stu_name: this.search_stu_name,
          stu_school: this.search_stu_school,
          page: 1,
          per_page: 20
        }
      }).then(res => {
        this.tableData = res.data.items;
        this.filterTableData = res.data.items;
        this.total = res.data.total;
        nextTick(() => {
          this.currentPage = 1;
        });
      }).catch(error => {
        console.log(error);
      });
    },
    reset() {
      this.search_id_no = '';
      this.search_stu_name = '';
      this.search_stu_school = '';
      axios.get('http://localhost:8000/administrator/registration_information', {
        params: {
          page: 1,
          per_page: 20
        }
      }).then(res => {
        this.tableData = res.data.items;
        this.filterTableData = res.data.items;
        this.total = res.data.total;
        nextTick(() => {
          this.currentPage = 1;
        });
      }).catch(error => {
        console.log(error);
      });
    },
    handleSizeChange(val) {
      this.perPage = val;
      axios.get('http://localhost:8000/administrator/registration_information/search', {
        params: {
          id_no: this.search_id_no,
          stu_name: this.search_stu_name,
          stu_school: this.search_stu_school,
          page: 1,
          per_page: val
        }
      }).then(res => {
        this.tableData = res.data.items;
        this.filterTableData = res.data.items;
        this.total = res.data.total;
      }).catch(error => {
        console.log(error);
      });
    },
    handleCurrentChange(val) {
      this.currentPage = val;
      axios.get('http://localhost:8000/administrator/registration_information/search', {
        params: {
          id_no: this.search_id_no,
          stu_name: this.search_stu_name,
          stu_school: this.search_stu_school,
          page: val,
          per_page: this.perPage
        }
      }).then(res => {
        this.tableData = res.data.items;
        this.filterTableData = res.data.items;
        this.total = res.data.total;
      }).catch(error => {
        console.log(error);
      });
    },
  },
  mounted() {
    axios.get('http://localhost:8000/administrator/registration_information', {
      params: {
        page: 1,
        per_page: 20
      }
    }).then(res => {
      this.tableData = res.data.items;
      this.filterTableData = res.data.items;
      this.total = res.data.total;

    }).catch(error => {
      console.log(error);
    });
  },
}

</script>

<style scoped>
.search-input {
  background: #F4F5F7;
  border: 1px solid #E4E7ED;
  border-radius: 4px;
  padding: 5px;
  margin-bottom: 20px;
}

ul {
  display: flex;
  padding: 0 20px;
  margin: 0;
}

ul li {
  display: flex;
  align-items: center;
  margin-right: 20px;
}


@media screen and (max-width: 1444px) {
  ul {
    flex-direction: column;
  }

  ul li {
    margin: auto auto 10px;
  }
}

</style>
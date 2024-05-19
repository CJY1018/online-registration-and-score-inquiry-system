<template>
  <el-container>
    <el-aside style="width: 240px;">
      <el-menu
          default-active="2"
          class="el-menu-vertical-demo"
          :router='true'
          @open="handleOpen"
          @close="handleClose"
      >
        <el-menu-item index="/administrator_console/registration_information">
          <template #title>
            <el-icon>
              <user/>
            </el-icon>
            <span>报名信息</span>
          </template>
        </el-menu-item>
        <el-menu-item index="/administrator_console/exam_information">
          <el-icon>
            <Tickets/>
          </el-icon>
          <span>考试信息</span>
        </el-menu-item>
        <el-menu-item index="/administrator_console/exam_arrangement">
          <el-icon>
            <EditPen/>
          </el-icon>
          <span>考试安排</span>
        </el-menu-item>
        <el-menu-item index="/administrator_console/score_entry">
          <el-icon>
            <Upload/>
          </el-icon>
          <span>成绩录入</span>
        </el-menu-item>
        <el-menu-item index="/administrator_console/score_analysis">
          <el-icon>
            <DataLine/>
          </el-icon>
          <span>成绩分析</span>
        </el-menu-item>
        <el-menu-item index="/administrator_console/other_operations">
          <el-icon>
            <setting/>
          </el-icon>
          <span>其他操作</span>
        </el-menu-item>
      </el-menu>
    </el-aside>

    <router-view></router-view>


  </el-container>
</template>

<script>

import {Setting, User, DataLine, Upload, Tickets, EditPen} from "@element-plus/icons-vue";

export default {
  components: {
    EditPen,
    Tickets,
    Upload,
    DataLine,
    User,
    Setting,
  },
  methods: {
    handleOpen(key, keyPath) {
      console.log(key, keyPath);
    },
    handleClose(key, keyPath) {
      console.log(key, keyPath);
    }
  }
}
</script>

<style scoped>
.tac {
  text-align: center;
}

.el-menu-vertical-demo {
  height: 100%;
}

</style>
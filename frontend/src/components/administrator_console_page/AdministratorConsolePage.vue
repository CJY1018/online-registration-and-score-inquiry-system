<template>
  <div class="common-layout">
    <el-container>
      <!--   顶栏   -->
      <el-header>
        <PageHeader></PageHeader>
      </el-header>
      <!--   主体   -->
      <el-main>
        <AdministratorConsolePageMain></AdministratorConsolePageMain>
      </el-main>
      <!--   底栏   -->
    </el-container>
  </div>
</template>

<script setup>
import PageHeader from "@/components/common/header/PageHeader.vue";
import AdministratorConsolePageMain
  from "@/components/administrator_console_page/main/AdministratorConsolePageMain.vue";
</script>



<style scoped>
.common-layout {
  height: 100vh;
  width: 100%;
  margin: 0;
}

.el-container {
  height: 100%;
  width: 100%;
  padding: 0;
  background: url("../../../static/imgs/bg.png") no-repeat;
  background-size: 100% 100%;
}

.el-main {
  color: #333;
  text-align: center;
  line-height: 55px;
  padding: 0;
}
</style>
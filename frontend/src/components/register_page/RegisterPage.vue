<template>
  <div class="common-layout">
    <el-container>
      <!--   顶栏   -->
      <el-header>
        <PageHeader></PageHeader>
      </el-header>

      <el-main>
        <!--   主体   -->
        <RegisterPageMain></RegisterPageMain>
        <!--   底栏   -->
        <PageFooter></PageFooter>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import PageFooter from "@/components/common/footer/PageFooter.vue";
import PageHeader from "@/components/common/header/PageHeader.vue";
import RegisterPageMain from "@/components/register_page/main/RegisterPageMain.vue";
</script>


<style scoped>
.common-layout {
  height: 100vh;
  width: 100%;
}

.el-container {
  height: 100%;
  width: 100%;
  padding: 0;
  background: url("../../../static/imgs/bg.png") no-repeat;
  background-size: 100% 100%;
}

.el-header {
  background-color: #B3C0D1;
  color: #333;
  text-align: center;
  line-height: 60px;
}

.el-main {
  color: #333;
  text-align: center;
  line-height: 55px;
  padding: 0;
}

section {
  height: 100%;
}
</style>
<template>
  <div class="common-layout">
    <el-container>
      <!--   顶栏   -->
      <el-header>
        <PageHeader></PageHeader>
      </el-header>
      <!--   主体   -->
      <el-main>
        <LoginPageMain></LoginPageMain>
        <PageFooter></PageFooter>
      </el-main>
      <!--   底栏   -->
    </el-container>
  </div>
</template>

<script>
import PageHeader from "@/components/common/header/PageHeader.vue";
import PageFooter from "@/components/common/footer/PageFooter.vue";
import LoginPageMain from "@/components/login_page/main/LoginPageMain.vue";

import 'element-plus/es/components/container/style/css';

export default {
  email: "LoginPage",
  components: {
    PageFooter,
    LoginPageMain,
    PageHeader,
  },
}


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
</style>
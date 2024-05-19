<template>
  <el-container class="reset-password-container">
    <!--   顶栏   -->
    <el-header>
      <PageHeader></PageHeader>
    </el-header>

    <el-main>
      <!--   主体   -->
      <ResetPasswordPageMain></ResetPasswordPageMain>

    </el-main>
    <PageFooter></PageFooter>
  </el-container>
</template>

<script>
import PageHeader from "@/components/common/header/PageHeader.vue";
import ResetPasswordPageMain from "@/components/reset_pasword_page/main/ResetPasswordPageMain.vue";
import PageFooter from "@/components/common/footer/PageFooter.vue";

export default {
  components: {PageFooter, ResetPasswordPageMain, PageHeader},
  data() {
    return {}
  },
}
</script>


<style scoped>
.reset-password-container {
  height: 100vh;
  width: 100%;
}

</style>
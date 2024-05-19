<template>
  <div class="common-layout">
    <el-container>
      <!--   顶栏   -->
      <el-header>
        <PageHeader></PageHeader>
      </el-header>

      <el-main>
        <!--   主体   -->
        <SignUpPageMain></SignUpPageMain>
      </el-main>
    </el-container>
  </div>
</template>

<script>
import PageHeader from "@/components/common/header/PageHeader.vue";
import SignUpPageMain from "@/components/sign_up_page/main/SignUpPageMain.vue";

export default {
  components: {SignUpPageMain, PageHeader},
  data() {
    return {}
  },
}
</script>


<style scoped>

</style>
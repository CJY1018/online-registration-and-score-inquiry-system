<template>
  <div class="common-layout">
    <el-container>
      <!--   顶栏   -->
      <el-header>
        <PageHeader></PageHeader>
      </el-header>
      <!--   主体   -->
      <el-main class="main-bg">
        <ScoreInquiryPageMain></ScoreInquiryPageMain>
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import PageHeader from "@/components/common/header/PageHeader.vue";
import ScoreInquiryPageMain from "@/components/score_inquiry_page/ScoreInquiryPageMain/ScoreInquiryPageMain.vue";

</script>

<style scoped>
.main-bg {
  background: url("../../../static/imgs/bg.png") no-repeat;
  background-size: 400% 100%;
}

</style>
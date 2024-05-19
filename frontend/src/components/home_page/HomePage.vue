<template>
  <el-container>
    <el-header>
      <PageHeader></PageHeader>
    </el-header>

    <el-main>
      <div style="width: 50%;text-align: left;margin: 0 auto;line-height: 40px;border: 1px solid #ebeef5;padding: 30px">
        <h3 style="text-align: center;margin-top: 0">
          报名须知
        </h3>
        <p>
          1、您好，<span style="color: #62AAF2">{{ stu_name }}</span>！开始报名前，请仔细阅读常见问题以及各单位网报公告，提前准备好-需要填写的信息。报名过程中，请考生<span style="color: #fc9956">仔细阅读网报页面提示文字</span>，并认真填写选择，<span style="color: #fc9956">避免造成无效报名</span>。
        </p>
        <p>
          2、网上报名时间：报名时间:<span style="color: #62AAF2">3月22日14：00至3月29日17：00；9月14日14:00至9月26日17:00</span>。
        </p>
        <p>
          3、网上报名期间，考生可自行填报、修改或重新填报报名信息，但一位考生只能保留一条有效报名信息。如需重新填报报名信息(新增报名)，须取消已有的报名，已取消的报名信息不可用于网上确认.报名过程中如需修改信息，建议退出网上报名系统，重新登录修改.网上确认前，考生可查看及下载网上报名信息
        </p>
        <p>
          4、<span style="color: #62AAF2">请考生牢记的用户名和密码</span>（为避免个人信息泄露，请设置复杂密码并定期修改)，再次报名还需使用。
        </p>
        <p>
          5、<span style="color: #fc9956">一位考生只能保留一条有效报名信息</span>。
        </p>
      </div>
      <p style="text-align: center;font-size: 20px;margin-top: 30px">你可以选择以下操作:</p>
      <el-button type="primary" @click="this.$router.push('/signup')" style="margin-right: 50px">报名</el-button>
      <el-button type="success" @click="this.$router.push('/score_inquiry')">查分</el-button>
    </el-main>
  </el-container>
</template>

<script>
import axios from "axios";
import PageHeader from "@/components/common/header/PageHeader.vue";

export default {
  components: {PageHeader},
  email: 'HomePage',
  data() {
    return {
      stu_name: '',
    }
  },
  mounted() {
    axios.get('http://localhost:8000/signup_info', {
      headers: {
        // 从Cookie中获取名为access_token的值
        'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
      }
    }).then(res => {
      this.stu_name = res.data.stu_name
    }).catch(err => {
      console.log(err)
      if (err.response.status === 403) {
        this.$router.push('/login')
      }
    })
  }
}

</script>


<style scoped>

</style>
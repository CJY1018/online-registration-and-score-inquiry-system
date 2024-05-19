<template>
  <div>
    <p>hello</p>
    <p>用户名: {{ username }}</p>
    <p>密码: {{ password }}</p>
  </div>
</template>

<script>
import axios from "axios";

export default {
  email: 'MePage',
  data() {
    return {
      username: '',
      password: ''
    }
  },
  mounted() {
    let _this = this
    axios.get('http://localhost:8000/me/', {
      headers: {
        // 从Cookie中获取名为access_token的值
        'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
      }
    }).then(res => {
      _this.username = res.data.id_no
      _this.password = res.data.password
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
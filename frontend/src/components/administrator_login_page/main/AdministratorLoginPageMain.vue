<template>
  <div class="form-container">
    <el-aside class="form">
      <el-form ref="ruleFormRef"
               style="max-width: 600px; width: 80%;"
               :model="ruleForm"
               :rules="rules"
               label-width="auto"
               label-position="top"
               class="demo-ruleForm"
               status-icon>
        <h2 style="letter-spacing: 1px; font-size: 22px; font-weight: 600; text-align: left; margin: 0;line-height: 25px">
          <span style="color: #5cb85c">CET超级管理员 </span>登录
        </h2>
        <hr style="margin-bottom: 20px;border: 0;border-top: 1px solid rgba(162,169,182,0.25)"/>
        <el-form-item label="身份证号：" prop="username">
          <el-input v-model="ruleForm.username" size="large" :prefix-icon="User" placeholder="请输入身份证号"
                    maxlength="18"/>
        </el-form-item>
        <el-form-item label="密码：" prop="password">
          <el-input v-model="ruleForm.password" type="password" size="large" :prefix-icon="Lock"
                    placeholder="请输入密码" show-password maxlength="20"/>
        </el-form-item>
        <!--   验证码   -->
        <el-form-item label="验证码：" prop="code">
          <el-input v-model="ruleForm.code" size="large" :prefix-icon="CircleCheck" placeholder="验证码" maxlength="6">
            <template #append>
              <el-image :src="img_url"
                        style="width: 120px;height: 40px"
                        @click="changeCaptchaImg"
                        :v-loading="true"/>
            </template>
          </el-input>
        </el-form-item>
        <!--    登录    -->
        <el-form-item style="margin-top: 15%">
          <el-button @click="checkCaptcha('ruleFormRef')" round size="large"
                     style="width: 70%; margin: auto" color="#007bff">
            登录
          </el-button>
        </el-form-item>
      </el-form>
    </el-aside>

    <el-main class="form-extra">
      <ul style="width: 100%; margin-bottom: 30%">
        <li style="text-align: left">
          <span>&nbsp;&nbsp;&nbsp;&nbsp;忘记密码?</span>
        </li>
        <li>
          <el-button @click="toResetPasswordPage" round style="width: 90%;margin-bottom: 20px" size="large">
            重置密码
          </el-button>
        </li>
        <li style="text-align: left;line-height: 30px">
          <div class="col-md-12 mt-5 p-4"
               style="background: rgb(252, 252, 245);padding: 13px; border-radius: 10px; border: 1px solid #e4d08f; color:rgb(113, 128, 150) ;">
            <div class="px-md-1" style="color: #222;font-size: 16px;margin-bottom:1em;">
              什么是CET超级管理员？
            </div>
            <div class="px-md-1" style="color: rgb(248, 64, 8);margin-bottom:1em;font-size:14px;font-weight:600">
              “CET超级管理员”可管理报名系统与查分系统
            </div>
            <p style="text-indent: 2em;">
              本页面仅用于超级管理员登录，如果您不是超级管理员，请移步至
              <a @click="toLoginPage">普通用户登录</a>
              ，或点击下方按钮联系客服申请管理员权限。
            </p>
          </div>
        </li>
        <li style="text-align: left">
          <span>&nbsp;&nbsp;&nbsp;&nbsp;遇到问题?</span>
        </li>
        <li>
          <a href="http://172.18.105.4:3000/">
            <el-button round style="width: 90%" color="#007bff" size="large">
              联系客服
            </el-button>
          </a>
        </li>
      </ul>
    </el-main>
  </div>
</template>

<script src="">
import axios from 'axios';
import 'element-plus/es/components/message-box/style/css';
import {v4 as uuidv4} from 'uuid';
import {reactive} from 'vue'
import {CircleCheck, Lock, User} from "@element-plus/icons-vue";
import {ElMessageBox} from "element-plus";

axios.defaults.withCredentials = true
// do not use same name with ref
const ruleForm = reactive({
  username: '',
  password: '',
  code: ''
})

const rules = {
  username: [
    {required: true, message: '请输入身份证号', trigger: 'blur'},
    {min: 18, max: 18, message: '长度在 18 个字符', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur'}
  ],
  code: [
    {required: true, message: '请输入验证码', trigger: 'blur'},
    {min: 4, max: 4, message: '长度在 4 个字符', trigger: 'blur'}
  ]
}

let checkNum = '获取验证码'

export default {
  email: 'AdministratorLoginPageMain',
  computed: {
    CircleCheck() {
      return CircleCheck
    },
    User() {
      return User
    },
    Lock() {
      return Lock
    },
  },
  data() {
    return {
      ruleForm,
      rules,
      checkNum,
      img_url: ''
    }
  },
  methods: {
    submitForm(formName) {
      // 发送axios请求
      axios.post('http://localhost:8000/jwt/token/admin', {
        username: this.ruleForm.username,
        password: this.ruleForm.password,
      }).then(res => {
        this.$refs[formName].resetFields()
        if (res.status === 200) {
          this.$router.push('/administrator_console')
        }
      }).catch(err => {
        this.$refs[formName].resetFields()
        console.log(err)
        ElMessageBox.alert('用户名或密码错误!', '提示', {
          confirmButtonText: '确定',
          type: 'error',
          callback: () => {
            console.error('error: ', '用户名或密码错误!')
          }
        })
      })
    },
    changeCaptchaImg() {
      // 设置cookie为uuid
      let captcha_id = uuidv4();
      document.cookie = 'captcha_id=' + captcha_id;
      this.img_url = 'http://localhost:8000/captcha/get?captcha_id=' + captcha_id
    },
    toLoginPage() {
      this.$router.push('/login')
    },
    toResetPasswordPage() {
      this.$router.push('/reset_password')
    },
    // 验证code是否正确
    checkCaptcha(formName) {
      let captcha_id = document.cookie.split(';').find(item => item.trim().startsWith('captcha_id=')).split('=')[1]
      this.$refs[formName].validate((valid) => {
        if (valid) {
          axios.get('http://localhost:8000/captcha/check?captcha_id=' + captcha_id + '&captcha_code=' + this.ruleForm.code).then(res => {
            if (res.data.status === 'success') {
              console.log('验证码正确')
              this.submitForm(formName)
            } else {
              ElMessageBox.alert('验证码错误!', '提示', {
                confirmButtonText: '确定',
                type: 'error',
                callback: () => {
                  this.changeCaptchaImg()
                  console.error('error: ', '验证码错误或过期!')
                }
              })
            }
          }).catch(err => {
            console.log(err)
            ElMessageBox.alert('网络错误!', '提示', {
              confirmButtonText: '确定',
              type: 'error',
              callback: () => {
                this.changeCaptchaImg()
                console.error('error: ', '网络发生故障!')
              }
            })
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    }
  },
  mounted() {
    // 获取验证码
    this.changeCaptchaImg()
  }
}

</script>


<style scoped>
.form-container {
  display: flex;
  height: 90%;
  width: 71%;
  margin: 2% auto 4% auto;

  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  background: #fff url(object_con3_bg.png) no-repeat bottom left;
}

.form {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 61.8%;
}

.form-extra {
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #DDE7FF;
}

.el-button {
  font-size: 16px;
  font-weight: bold;
}

/*ul li去点*/
ul {
  list-style: none;
  padding: 0;
}

/deep/ .el-input-group__append {
  padding: 0;
}

a:hover {
  color: #0056b3;
  text-decoration: underline;
}

a {
  color: #007bff;
  text-decoration: none;
  background-color: transparent;
}
</style>
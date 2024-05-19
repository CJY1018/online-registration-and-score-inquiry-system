<template>
  <el-container class="form-container">
    <!--  第一步: 验证邮箱  -->
    <div v-if="step===0" style="margin: 40px auto;width: 100%">
      <!--  第一步: 输入待修改密码账号的邮箱  -->
      <el-form :model="ruleForm" :rules="rules" ref="ruleForm" label-width="80px"
               style="width: 80%;margin: 10px auto" label-position="top">
        <el-form-item label="邮箱" prop="email" ref="email">
          <el-input v-model="ruleForm.email" :prefix-icon="Message" placeholder="请输入邮箱" size="large"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="captcha" style="margin-top: 40px">
          <el-input v-model="ruleForm.captcha" :prefix-icon="CircleCheck" placeholder="请输入验证码" size="large">
            <template #append>
              <el-button @click="getCaptcha" :disabled="checkNum !== '获取验证码'">{{ checkNum }}</el-button>
            </template>
          </el-input>
        </el-form-item>
      </el-form>

      <el-button type="primary" @click="nextStep" style="margin: 40px auto">
        下一步
      </el-button>
    </div>

    <!--  第二步: 重置密码  -->
    <div v-if="step===1" style="margin: 40px auto;width: 100%">
      <!--  第二步: 输入新密码  -->
      <el-form :model="ruleForm2" :rules="rules2" ref="ruleForm2" label-width="80px"
               style="width: 80%;margin: 10px auto" label-position="top">
        <el-form-item label="身份证号" prop="id_no">
          <el-input v-model="ruleForm2.id_no" :prefix-icon="User" placeholder="请输入身份证号"
                    size="large"></el-input>
        </el-form-item>
        <el-form-item label="新密码" prop="password">
          <el-input v-model="ruleForm2.password" :prefix-icon="Lock" placeholder="请输入新密码" size="large"
                    type="password"></el-input>
        </el-form-item>
        <el-form-item label="确认密码" prop="confirmPassword">
          <el-input v-model="ruleForm2.confirmPassword" :prefix-icon="Lock" placeholder="请再次输入新密码"
                    size="large"
                    type="password"></el-input>
        </el-form-item>
      </el-form>

      <el-button type="primary" @click="resetPassword" style="margin: 20px auto">
        重置密码
      </el-button>
    </div>

    <!--  第三步: 重置成功  -->
    <div v-if="step===2" style="margin: 40px auto;width: 100%">
      <el-result
          icon="success"
          status="success"
          title="重置密码成功"
          :sub-title="`将在 ${jumpTime} 秒后自动跳转到登录页面`"
      >
        <template #extra>
          <el-button type="primary" @click="$router.push('/login')">重新登录</el-button>
        </template>
      </el-result>
    </div>

    <!--  步骤条  -->
    <el-steps
        class="mb-4"
        style="margin-bottom: 20px"
        :active="step"
        simple
        finish-status="success"
    >
      <el-step title="验证邮箱"/>
      <el-step title="输入新密码"/>
      <el-step title="修改成功"/>
    </el-steps>
    <p style="text-align: left;padding:0 20px">{{ step === 0 ? tips1 : tips2 }}</p>

  </el-container>
</template>

<script>
import axios from "axios";
import {reactive} from 'vue'
import {Message, CircleCheck, User, Lock} from "@element-plus/icons-vue";
import {ElNotification} from "element-plus";
import 'element-plus/dist/index.css'

const rules = {
  email: [
    {required: true, message: "请输入邮箱", trigger: "blur"},
    {type: "email", message: "邮箱格式不正确", trigger: "blur"}
  ],
  captcha: [
    {required: true, message: "请输入验证码", trigger: "blur"}
  ]
}

const ruleForm2 = reactive({
  id_no: "",
  password: "",
  confirmPassword: ""
})

const rules2 = {
  id_no: [
    {required: true, message: "请输入身份证号", trigger: "blur"},
    {pattern: /^[0-9]{17}[0-9X]$/, message: "身份证号格式不正确", trigger: "blur"}
  ],
  password: [
    {required: true, message: "请输入密码", trigger: "blur"},
    {min: 6, message: "密码长度不能小于6位", trigger: "blur"}
  ],
  confirmPassword: [
    {required: true, message: "请再次输入密码", trigger: "blur"},
    {
      validator: (rule, value, callback) => {
        if (value !== ruleForm2.password) {
          callback(new Error("两次输入密码不一致"))
        } else {
          callback()
        }
      }, trigger: "blur"
    }
  ]
}

export default {
  email: "ResetPasswordPageMain",
  data() {
    return {
      step: 0,
      checkNum: "获取验证码",
      ruleForm: {
        email: "",
        captcha: "",
      },
      ruleForm2,
      rules,
      rules2,
      jumpTime: 0,
    }
  },
  computed: {
    Message() {
      return Message
    },
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
  methods: {
    getCaptcha() {
      delete this.rules.captcha
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          axios.post("http://localhost:8000/reset_password/send_email", {email: this.ruleForm.email}).then(res => {
            if (res.data.status === 'success') {
              ElNotification({
                title: "验证码发送成功",
                message: "请查看邮箱",
                type: "success"
              })
              this.checkNum = 60
              let timer = setInterval(() => {
                this.checkNum--
                if (this.checkNum === 0) {
                  clearInterval(timer)
                  this.checkNum = "获取验证码"
                }
              }, 1000)
            } else {
              ElNotification({
                title: "验证码发送失败",
                message: "请检查邮箱是否正确",
                type: "error"
              })
            }
          })
        }
      })
    },
    nextStep() {
      this.rules.captcha = [
        {required: true, message: "请输入验证码", trigger: "blur"},
      ]
      this.$refs.ruleForm.validate(valid => {
        if (valid) {
          axios.post("http://localhost:8000/reset_password/check_captcha", {
            email: this.ruleForm.email,
            captcha: this.ruleForm.captcha
          }).then(res => {
            if (res.data.status === 'success') {
              this.step = 1
            } else {
              ElNotification({
                title: "验证码错误",
                message: "请检查验证码是否正确",
                type: "error"
              })
            }
          })
        }
      })
    },
    resetPassword() {
      this.$refs.ruleForm2.validate(valid => {
        if (valid) {
          axios.post("http://localhost:8000/reset_password", {
            email: this.ruleForm.email,
            id_no: this.ruleForm2.id_no,
            password: this.ruleForm2.password
          }).then(res => {
            if (res.data.status === 'success') {
              this.step = 2
              // 重置成功，自动跳转到登录页面
              this.jumpTime = 5
              let timer = setInterval(() => {
                this.jumpTime--
                if (this.jumpTime === 0) {
                  clearInterval(timer)
                  this.$router.push('/login')
                }
              }, 1000)
            } else {
              ElNotification({
                title: "重置密码失败",
                message: res.data.message,
                type: "error"
              })
            }
          })
        }
      })
    }
  },
  mounted() {
  }
}


</script>


<style scoped>
.form-container {
  width: 38.2%;
  margin: 3% auto 4% auto;
  flex-direction: column;

  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
  border-radius: 28px;
  background: #fff;
}

</style>
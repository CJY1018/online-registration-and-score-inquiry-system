<template>
  <div class="form-container">
    <el-aside class="form">
      <el-form ref="ruleFormRef"
               style="max-width: 600px; width: 80%"
               :model="ruleForm"
               :rules="rules"
               label-width="auto"
               label-position="top"
               class="demo-ruleForm"
               status-icon>
        <h2 style="letter-spacing: 1px; font-size: 22px; font-weight: 600; text-align: left; margin: 0;line-height: 25px">
          注册<span style="color: #5cb85c">ETEST</span>通行证
        </h2>
        <hr style="margin-bottom: 20px;border: 0;border-top: 1px solid rgba(162,169,182,0.25)"/>
        <el-form-item label="电子邮箱：" prop="email">
          <el-input v-model="ruleForm.email" size="large" :prefix-icon="Message" placeholder="电子邮箱"/>
        </el-form-item>
        <el-form-item label="手机号：" prop="tel">
          <el-input v-model="ruleForm.tel" size="large" :prefix-icon="Phone" placeholder="手机号"/>
        </el-form-item>
        <el-form-item label="密码：" prop="password">
          <el-input v-model="ruleForm.password" type="password" autocomplete="off" show-password size="large"
                    :prefix-icon="Lock" placeholder="密码"/>
        </el-form-item>
        <el-form-item label="确认密码：" prop="confirm_password">
          <el-input v-model="ruleForm.confirm_password" type="password" autocomplete="off" show-password size="large"
                    :prefix-icon="Lock" placeholder="确认密码"/>
        </el-form-item>
        <el-form-item label="证件类型：" prop="id_type">
          <el-select
              v-model="ruleForm.id_type"
              placeholder="--请选择证件类型--"
              size="large">
            <el-option
                v-for="item in options"
                :key="item.value"
                :label="item.label"
                :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="证件号码：" prop="id_no">
          <el-input v-model="ruleForm.id_no" size="large" :prefix-icon="Postcard" placeholder="证件号码"/>
        </el-form-item>
        <el-form-item label="姓名：" prop="stu_name">
          <el-input v-model="ruleForm.stu_name" size="large" :prefix-icon="User" placeholder="姓名"/>
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
        <el-form-item prop="agree">
          <el-checkbox-group v-model="ruleForm.agree">
            <el-checkbox>已仔细阅读并同意</el-checkbox>
          </el-checkbox-group>
          《<a href="https://resource.neea.edu.cn/project/Passport/PublicInfo/CETNCREPETSServicesAgreement.pdf"
              target="_blank">用户服务协议</a>》
          《<a href="https://resource.neea.edu.cn/project/Passport/PublicInfo/CETNCREPETSPrivacyPolicy.pdf"
              target="_blank">用户隐私政策</a>》
        </el-form-item>
        <!--    注册    -->
        <el-form-item style="margin-top: 7%">
          <el-button @click="submitForm('ruleFormRef')" round size="large"
                     style="width: 70%; margin: auto" color="#007bff">
            注册
          </el-button>
        </el-form-item>
      </el-form>
    </el-aside>

    <el-main class="form-extra">
      <ul style="width: 100%;margin-bottom: 70%">
        <li style="text-align: left;line-height: 40px">
          <span style="color: #26337A;margin-left: 5%">已有ETEST通行证账号？</span>
        </li>
        <li>
          <el-button @click="toLoinPage" round style="width: 90%" color="#007bff" size="large">
            登录
          </el-button>
          <p style="font-size: 12px;line-height: 15px;text-align: left;padding-left: 5%">
            <span style="color: #a0aec0">
              忘记密码?
              <a @click="toResetPasswordPage">重置密码</a>
            </span>
          </p>
          <hr style="margin-bottom: 20px;border: 0;border-top: 1px solid rgba(162,169,182,0.25)"/>
        </li>
        <li style="text-align: left;line-height: 30px">
          <div class="col-md-12 mt-5 p-4"
               style="background: rgb(252, 252, 245);padding: 13px; border-radius: 10px; border: 1px solid #e4d08f; color:rgb(113, 128, 150) ;">
            <div class="px-md-1" style="color: #222;font-size: 16px;margin-bottom:1em;">
              什么是ETEST通行证？
            </div>
            <div class="px-md-1" style="color: rgb(248, 64, 8);margin-bottom:1em;font-size:14px;font-weight:600">
              “ETEST通行证”可用于登录报名系统
            </div>
            <p style="text-indent: 2em;">
              支持的平台有：全国大学英语四、六级考试（CET）报名系统、全国计算机等级考试（NCRE）报名系统、全国英语等级考试（PETS）报名系统。
            </p>
            <p style="text-indent: 2em;">
              如果您在使用这些服务时注册过账号，则可凭此账号使用其他服务，例如：如果您报名过CET，则可凭此账号报名NCRE、PETS等，而无需再次注册账号。
            </p>
          </div>
        </li>
        <li style="text-align: left">
          <span style="margin-left: 5%">信息被占用？</span>
        </li>
        <li>
          <el-button @click="submitForm('ruleFormRef')" round style="width: 90%" color="#dc3545" size="large">
            信息占用申诉
          </el-button>
        </li>
      </ul>
    </el-main>
  </div>
</template>

<script src="">
import {reactive} from 'vue'
import {CircleCheck, Lock, Message, Phone, Postcard, User} from "@element-plus/icons-vue";
import axios from "axios";
import {ElMessageBox} from "element-plus";
import {v4 as uuidv4} from "uuid";

// 表单项
const ruleForm = reactive({
  email: '',
  tel: '',
  password: '',
  id_type: '',
  id_no: '',
  stu_name: '',
})

class RuleFormOutput {
  constructor(email, tel, password, id_type, id_no, stu_name) {
    this.email = email
    this.tel = tel
    this.password = password
    this.id_type = id_type
    this.id_no = id_no
    this.stu_name = stu_name
  }
}

// 校验密码
const validatePass2 = (rule, value, callback) => {
  if (value === '') {
    callback(new Error('请再次输入密码'))
  } else if (value !== ruleForm.password) {
    callback(new Error("两次输入密码不一致"))
  } else {
    callback()
  }
}

// 校验规则
const rules = {
  email: [
    {required: true, message: '请输入电子邮箱', trigger: 'blur'},
    {type: 'email', message: '请输入正确的邮箱地址', trigger: 'blur'}
  ],
  tel: [
    {required: true, message: '请输入手机号', trigger: 'blur'},
    {pattern: /^1[3456789]\d{9}$/, message: '请输入正确的手机号', trigger: 'blur'}
  ],
  stu_name: [
    {required: true, message: '请输入账号', trigger: 'blur'},
    {min: 0, max: 10, message: '长度在 10 个字符', trigger: 'blur'}
  ],
  password: [
    {required: true, message: '请输入密码', trigger: 'blur'},
    {min: 6, max: 20, message: '长度在 6 到 20 个字符', trigger: 'blur'}
  ],
  confirm_password: [
    {required: true, message: '请再次输入密码', trigger: 'blur'},
    {validator: validatePass2, trigger: 'blur'}
  ],
  id_type: [
    {required: true, message: '请选择证件类型', trigger: 'change'}
  ],
  id_no: [
    {required: true, message: '请输入证件号码', trigger: 'blur'},
    {min: 18, max: 18, message: '长度在 18 个字符', trigger: 'blur'}
  ],
  code: [
    {required: true, message: '请输入验证码', trigger: 'blur'},
    {min: 4, max: 4, message: '长度在 6 个字符', trigger: 'blur'}
  ],
  agree: [
    {required: true, message: '请同意用户服务协议和用户隐私政策', trigger: 'change'}
  ],
}

// 证件类型
const options = [
  {
    value: '0',
    label: '中华人民共和国居民身份证',
  },
  {
    value: '1',
    label: '台湾居民来往大陆通行证',
  },
  {
    value: '2',
    label: '港澳居民来往内地通行证',
  },
  {
    value: '3',
    label: '护照',
  },
  {
    value: '4',
    label: '香港身份证',
  },
  {
    value: '5',
    label: '澳门身份证',
  },
  {
    value: '6',
    label: '中华人民共和国外国人永久居留身份证',
  },
  {
    value: '7',
    label: '港澳居民居住证',
  },
  {
    value: '8',
    label: '台湾居民居住证',
  },
]

export default {
  email: 'LoginPageMain',
  computed: {
    Postcard() {
      return Postcard
    },
    Phone() {
      return Phone
    },
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
  data() {
    return {
      ruleForm,
      rules,
      options,
      img_url: '',
      checkNum: '获取验证码',
      checkDisabled: false,
    }
  },
  methods: {
    submitForm(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          alert('submit!')
          let ruleFormOutput = new RuleFormOutput(
              this.ruleForm.email,
              this.ruleForm.tel,
              this.ruleForm.password,
              this.ruleForm.id_type,
              this.ruleForm.id_no,
              this.ruleForm.stu_name
          )
          // 提交表单
          axios.post('http://localhost:8000/register', ruleFormOutput
          ).then(res => {
            if (res.data.status === 'success') {
              this.$router.push('/login')
            } else {
              ElMessageBox.alert('该身份证已注册，请直接登录或信息占用申诉', '提示', {
                confirmButtonText: '确定',
                type: 'error',
                callback: () => {
                  console.error('error: ', '注册失败!')
                }
              })
            }
          }).catch(err => {
            console.log(err)
            ElMessageBox.alert('注册失败!', '提示', {
              confirmButtonText: '确定',
              type: 'error',
              callback: () => {
                console.error('error: ', '注册失败!')
              }
            })
          })
        } else {
          console.log('error submit!!')
          return false
        }
      })
    },
    changeCaptchaImg() {
      // 设置cookie为uuid
      let captcha_id = uuidv4();
      document.cookie = 'captcha_id=' + captcha_id;
      this.img_url = 'http://localhost:8000/captcha/get?captcha_id=' + captcha_id
    },
    toLoinPage() {
      this.$router.push({path: '/login'})
    },
    toResetPasswordPage() {
      this.$router.push({path: '/reset_password'})
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
  width: 71%;
  margin: 2% auto 4% auto;

  background: #fff;
  box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1);
}

.form {
  display: flex;
  align-items: center;
  justify-content: center;
  height: 100%;
  width: 65%;
  padding-top: 50px;
  padding-bottom: 10px;
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

a:hover {
  color: #0056b3;
  text-decoration: underline;
}

a {
  color: #007bff;
  text-decoration: none;
  background-color: transparent;
}

/deep/ .el-input-group__append {
  padding: 0;
}
</style>
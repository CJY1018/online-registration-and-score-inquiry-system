<template>
  <!-- 第一步 -->
  <div v-show="step_active===0">
    <el-form :model="form" :rules="rules" ref="form" label-width="50px"
             style="width: 400px; margin: 0 auto;">
      <el-form-item label="学校" prop="stu_school">
        <el-select-v2 v-model="form.stu_school"
                      placeholder="请选择学校"
                      value-key="name"
                      clearable
                      filterable
                      remote
                      reserve-keyword
                      :remote-method="remoteMethod"
                      :loading="loading"
                      :options="schools"
                      @change="remoteMethod2"/>
        <!--                    <el-option v-for="item in schools" :key="item.label" :label="item.label"-->
        <!--                               :value="item.school_id" @click="remoteMethod2(item)"></el-option>-->
      </el-form-item>
      <el-form-item label="院系" prop="stu_department">
        <!--        <el-select v-model="form.stu_department"-->
        <!--                   placeholder="请选择院系"-->
        <!--                   :disabled="departments.length === 0"-->
        <!--                   clearable-->
        <!--                   reserve-keyword-->
        <!--                   :loading="loading">-->
        <!--          <el-option v-for="item in departments" :key="item.label" :label="item.label"-->
        <!--                     :value="item.special_id"></el-option>-->
        <!--        </el-select>-->
        <el-cascader v-model="form.stu_department"
                     style="width: 400px"
                     clearable
                     filterable
                     :disabled="departments.length === 0"
                     :options="departments"
                     :show-all-levels="false"
                     placeholder="请选择院系">
        </el-cascader>
      </el-form-item>
      <el-form-item label="专业" prop="stu_major">
        <el-cascader v-model="form.stu_major"
                     style="width: 400px"
                     clearable
                     filterable
                     :disabled="options.length === 0"
                     :options="options"
                     :show-all-levels="false"
                     placeholder="请选择专业">
        </el-cascader>
      </el-form-item>
      <el-form-item label="班级" prop="stu_cls">
        <el-input v-model="form.stu_cls"></el-input>
      </el-form-item>
      <el-form-item label="学号" prop="stu_no">
        <el-input v-model="form.stu_no"></el-input>
      </el-form-item>
      <el-form-item label="头像" prop="avatar">
        <el-upload
            action="http://127.0.0.1:8000/upload_picture"
            :headers="headers"
            with-credentials
            drag
            style="height: 160px;width: 120px"
            :on-success="handleAvatarSuccess"
            :before-upload="beforeAvatarUpload"
            :show-file-list="false"
            v-model="form.avatar"
        >
          <el-image v-if="upload_url" :src="upload_url" class="avatar" alt="avatar"/>
          <el-icon v-else>
            <Plus/>
          </el-icon>
        </el-upload>
        <span style="width: 200px;color: #8c939d;margin-left: 10px">请上传头像，格式为：jpg/jpeg/png，大小不超过2M</span>
      </el-form-item>
      <el-form-item label="备注">
        <el-input v-model="form.stu_info" type="textarea"></el-input>
      </el-form-item>
    </el-form>
  </div>
  <!-- 第二步 -->
  <div v-show="step_active===1 || step_active===2">
    <!-- 头像信息 -->
    <table style="width: 925px; margin: 0 auto;padding: 2px;border: #bae1ff solid 1px">
      <tr>
        <td style="width: 120px;padding: 0">
          <!--          <el-image :src="require('./Show.jpg')" style="width: 120px;height: 160px;transform: rotate(90deg);"-->
          <!--                    :style="{transform:'rotate('+deg+'deg)'}"></el-image>-->
          <el-image v-if="imageUrl" :src="imageUrl" class="avatar" alt="avatar"/>
          <!--          <el-upload
                        action="http://127.0.0.1:8000/upload_picture"
                        :headers="headers"
                        with-credentials
                        drag
                        style="height: 160px;width: 120px"
                        :on-success="handleAvatarSuccess"
                        :before-upload="beforeAvatarUpload"
                    >
                      <img v-if="imageUrl" :src="imageUrl" class="avatar" alt="avatar"/>
                      <el-icon v-else>
                        <Plus/>
                      </el-icon>
                    </el-upload>-->
        </td>
        <td>
          <table>
            <tr style="height: 30px;">
              <td class="lz_td1"><span>姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名：</span></td>
              <td class="lz_td2"><span>{{ name }}</span></td>
            </tr>
            <tr style="height: 30px;">
              <td class="lz_td1"><span>性&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;别：</span></td>
              <td class="lz_td2"><span>{{ sex }}</span></td>
            </tr>
            <tr style="height: 30px;">
              <td class="lz_td1"><span>证件类型：</span></td>
              <td class="lz_td2"><span>{{ id_type }}</span></td>
            </tr>
            <tr style="height: 30px;">
              <td class="lz_td1"><span>证件号码：</span></td>
              <td class="lz_td2"><span>{{ id_no }}</span></td>
            </tr>
            <tr style="height: 30px;">
              <td class="lz_td1"><span>笔试报名学校校区：</span></td>
              <td class="lz_td2"><span>	{{ form.stu_school.name || this.stu_school }}</span></td>
            </tr>
          </table>
        </td>
      </tr>
    </table>

    <!-- 详细信息 -->
    <el-descriptions
        class="margin-top"
        :column="2"
        size='default'
        border
        style="width: 925px; margin: 20px auto;padding: 5px;border: #bae1ff solid 1px;"
    >
      <template #title>
        <div class="title">报名个人信息</div>
      </template>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            姓&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;名：
          </div>
        </template>
        <span class="cell-context">{{ name }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            性&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;别：
          </div>
        </template>
        <span class="cell-context">{{ sex }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            证件类型：
          </div>
        </template>
        <span class="cell-context">{{ id_type }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            证件号码：
          </div>
        </template>
        <span class="cell-context">{{ id_no }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            邮&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;箱：
          </div>
        </template>
        <span class="cell-context">{{ email }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            手机号码：
          </div>
        </template>
        <span class="cell-context">{{ tel }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            年&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;龄：
          </div>
        </template>
        <span class="cell-context">{{ stu_age }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            学&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;校：
          </div>
        </template>
        <span class="cell-context">{{ form.stu_school.name || this.stu_school }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            院&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;系：
          </div>
        </template>
        <span class="cell-context">{{ form.stu_department ? form.stu_department[0] : this.stu_department }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            专&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;业：
          </div>
        </template>
        <span class="cell-context">{{
            form.stu_major ? form.stu_major[form.stu_major.length - 1] : this.stu_major
          }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            班&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;级：
          </div>
        </template>
        <span class="cell-context">{{ form.stu_cls || this.stu_cls }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            学&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;号：
          </div>
        </template>
        <span class="cell-context">{{ form.stu_no || this.stu_no }}</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            备&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;注：
          </div>
        </template>
        <span class="cell-context">{{ form.stu_info || this.stu_info }}</span>
      </el-descriptions-item>
    </el-descriptions>

    <!--  检查报名信息  -->
    <el-alert title="请仔细检测上述信息是否正确！" style="width: 400px;margin: 10px auto" type="warning"
              :closable="false"
              v-show="step_active===1"
              center show-icon/>
  </div>
  <!-- 第三步 -->
  <div v-show="step_active===2">
    <div style="width: 925px; margin: 20px auto;border: #bae1ff solid 1px;" v-if="!pay_status">
      <p>请扫描下方二维码或点击按钮进行报名付费</p>
      <table style="margin:auto;text-align: center">
        <tr>
          <td>
            <el-image :src="require('./报名二维码.png')" style="vertical-align: middle;width: 160px" @click="large"/>
          </td>
          <td>
            <a href="https://afdian.net/item/e7b84b58f6de11eeaf4e52540025c377" target="_blank">
              <el-button style="width: 348px;height: 128px" class="afd"></el-button>
            </a>
          </td>
        </tr>
      </table>
      <p>
        <span>支付状态: </span>
        <el-tag type="danger" v-if="!pay_status">未支付</el-tag>
        <el-tag type="success" v-else>已支付</el-tag>
        <span style="margin-left: 50px">刷新: </span>
        <el-button plain :icon="Refresh" circle @click="refresh_status"></el-button>
      </p>
    </div>
    <!--   考试信息   -->
    <el-descriptions
        class="margin-top"
        :column="2"
        size='default'
        border
        v-else
        style="width: 925px; margin: 20px auto;padding: 5px;border: #bae1ff solid 1px;"
    >
      <template #title>
        <div class="title">考试信息</div>
      </template>
      <template #extra>
        <div style="margin-right:  20px;">
          <span style="height: 20px;font-size: 14px">支付状态： </span>
          <el-tag type="success">已支付</el-tag>
        </div>
      </template>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            考试科目：
          </div>
        </template>
        <span class="cell-context" v-if="exam.exam_name">{{ exam.exam_name }}</span>
        <span class="default-cell-context" v-else>(准考证打印开始后显示)</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            支付费用：
          </div>
        </template>
        <span class="cell-context" v-if="exam.exam_name">{{ exam.exam_price }} 元</span>
        <span class="default-cell-context" v-else>(准考证打印开始后显示)</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            考试学校：
          </div>
        </template>
        <span class="cell-context" v-if="exam.exam_name">{{ exam.exam_venue }}</span>
        <span class="default-cell-context" v-else>(准考证打印开始后显示)</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            考场编号：
          </div>
        </template>
        <span class="cell-context" v-if="exam.exam_name">{{ exam.exam_venue_no }}</span>
        <span class="default-cell-context" v-else>(准考证打印开始后显示)</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            考试时间：
          </div>
        </template>
        <span class="cell-context" v-if="exam.exam_name">{{ time_format(exam.exam_time) }}</span>
        <span class="default-cell-context" v-else>(准考证打印开始后显示)</span>
      </el-descriptions-item>
      <el-descriptions-item :label-align="label_align">
        <template #label>
          <div class="cell-item">
            考试说明：
          </div>
        </template>
        <span class="cell-context" v-if="exam.exam_name">{{ exam.exam_info }}</span>
        <span class="default-cell-context" v-else>(准考证打印开始后显示)</span>
      </el-descriptions-item>
    </el-descriptions>
  </div>

  <!-- 进入上一步 -->
  <el-button @click="changeStep(step_active-1)" v-if="step_active===1 && !pay_status">
    上一步
  </el-button>
  <!-- 进入下一步 -->
  <el-button @click="changeStep(step_active+1)" v-if="step_active<2 && !pay_status">
    下一步
  </el-button>


  <!-- 步骤条 -->
  <el-steps style="max-width: 600px;margin:30px auto" :active="step_active" finish-status="success" align-center
            ref="steps" v-if="step_active<3 && !pay_status">
    <el-step title="填写信息">
      <!--      <template #title>-->
      <!--        <el-button :type="step_active>0?'success':''" :disabled="max_step<0" link @click="changeStep(0)">-->
      <!--          Step 1-->
      <!--        </el-button>-->
      <!--      </template>-->
    </el-step>
    <el-step title="确认信息">
      <!--      <template #title>-->
      <!--        <el-button :type="step_active>1?'success':''" :disabled="max_step<1" link @click="changeStep(1)">-->
      <!--          Step 2-->
      <!--        </el-button>-->
      <!--      </template>-->
    </el-step>
    <el-step title="考试缴费">
      <!--      <template #title>-->
      <!--        <el-button :type="step_active>2?'success':''" :disabled="max_step<2" link @click="changeStep(2)">-->
      <!--          Step 3-->
      <!--        </el-button>-->
      <!--      </template>-->
    </el-step>
  </el-steps>
</template>

<script>

import axios from "axios";
import {nextTick} from "vue";
import {Plus, Refresh} from "@element-plus/icons-vue";
import {dayjs, ElMessageBox, ElNotification} from 'element-plus'
import 'element-plus/dist/index.css'
import {h} from 'vue'

const form = {
  stu_school: '',
  stu_department: '',
  stu_major: '',
  stu_cls: '',
  stu_no: '',
  stu_info: '',
  avatar: ''
}


const rules = {
  stu_school: [
    {required: true, message: '请选择学校', trigger: 'change'}
  ],
  stu_department: [
    {required: true, message: '请选择院系', trigger: 'change'}
  ],
  stu_major: [
    {required: true, message: '请选择专业', trigger: 'change'}
  ],
  stu_cls: [
    {required: true, message: '请输入班级', trigger: 'blur'}
  ],
  stu_no: [
    {required: true, message: '请输入学号', trigger: 'blur'}
  ],
  avatar: [
    {
      required: true, message: '请上传头像', trigger: 'change', validator: (rule, value, callback) => {
        if (!form.avatar) {
          callback(new Error('请上传头像'))
        } else {
          callback()
        }
      }
    }
  ],
}


const label_align = 'right'

const id_type_map = {
  '0': '中华人民共和国居民身份证',
  '1': '台湾居民来往大陆通行证',
  '2': '港澳居民来往内地通行证',
  '3': '护照',
  '4': '香港身份证',
  '5': '澳门身份证',
  '6': '中华人民共和国外国人永久居留身份证',
  '7': '港澳居民居住证',
  '8': '台湾居民居住证'
}

const exam = {
  exam_name: '',
  exam_price: '',
  exam_venue: '',
  exam_time: '',
  exam_info: ''
}

export default {
  components: {Plus},
  email: 'SignUpPageMain',
  data() {
    return {
      label_align,
      name: '',
      sex: '',
      id_type: '',
      id_no: '',
      email: '',
      tel: '',
      stu_school: '',
      stu_department: '',
      stu_major: '',
      stu_age: '',
      stu_cls: '',
      stu_no: '',
      stu_info: '',
      step_active: -1,
      max_step: 0,
      form,
      loading: false,
      schools: [],
      departments: [],
      options: [],
      rules,
      ref_form: 'form',
      confirm: false,
      pay_status: false,
      exam,
      upload_url: '',
      imageUrl: '',
      headers: {
        Authorization: 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
      },
    }
  },
  computed: {
    Refresh() {
      return Refresh
    },
    Plus() {
      return Plus
    },
    time_format() {
      return (row) => {
        return dayjs(row).format('YYYY-MM-DD HH:mm:ss')
      }
    }
  },
  methods: {
    changeStep(step) {
      rules.stu_department[0].required = this.departments.length !== 0;
      rules.stu_major[0].required = this.options.length !== 0;
      console.log('step' + step)

      this.$refs.form.validate((valid) => {
        if (valid) {
          console.log('学校：' + this.form.stu_school.name + ' 院系：' + this.form.stu_department + ' 专业：' + this.form.stu_major + ' 班级：' + this.form.stu_cls + ' 学号：' + this.form.stu_no)
          this.get_avatar()
          if (step !== 2) {
            if (this.max_step < step)
              this.max_step = step
            this.step_active = step
          } else {
            ElMessageBox.confirm('请仔细确认上述信息是否正确！', '提示', {
              confirmButtonText: '确认正确',
              cancelButtonText: '取消',
              type: 'warning'
            }).then(() => {
              axios.post('http://localhost:8000/signup', {
                stu_school: this.form.stu_school.name,
                stu_department: this.form.stu_department[0],
                stu_major: this.form.stu_major[this.form.stu_major.length - 1],
                stu_cls: this.form.stu_cls,
                stu_no: this.form.stu_no,
                stu_info: this.form.stu_info,
                confirm: '1'
              }, {
                headers: {
                  // 从Cookie中获取名为access_token的值
                  'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
                }
              }).then(res => {
                console.log(res)
                if (this.max_step < ++this.step_active)
                  this.max_step = this.step_active
              }).catch(err => {
                console.log(err)
              })
            }).catch(e => {
              console.log(e)
            })
          }
        }
      })
    },
    remoteMethod(query) {
      if (query !== '') {
        // 如果学校名字发生变化, 清空院系和专业
        if (this.form.stu_school.name && query !== this.form.stu_school.name) {
          console.log('query:' + query + ' stu_school:' + this.form.stu_school.name)
          this.form.stu_department = ''
          this.form.stu_major = ''
        }

        this.loading = true
        setTimeout(() => {
          this.loading = false
          // 匹配学校
          this.schools = this.all_schools.filter(item => item.label.indexOf(query) > -1)
          // 按照学校名字排序, 优先匹配前缀, 然后按照字母顺序排序
          this.schools.sort((a, b) => {
            let index_a = a.label.indexOf(query)
            let index_b = b.label.indexOf(query)
            // 获取最后两个字符
            // let last_a = a.label.slice(-2)
            // let last_b = b.label.slice(-2)
            // 是否为大学
            let is_university_a = a.label.indexOf('大学') > -1
            let is_university_b = b.label.indexOf('大学') > -1
            if (index_a === index_b) {
              // 如果前缀相同, 比较最后两个字符
              if (is_university_a && is_university_b) {
                // 如果最后两个字符相同, 按照拼音排序
                return a.label.localeCompare(b.label)
              } else {
                return is_university_b - is_university_a
              }
            } else {
              return index_a - index_b
            }
          })
          // let turns = 0
          // // 获取学校列表
          // axios.get('/web/api/?keyword=' + query + '&page=1&province_id=&ranktype=&request_type=1&size=30&type=&uri=apidata/api/gkv3/school/lists&signsafe=8be0023a2a61cf35f72d17dad1c12534').then(res => {
          //   turns = res.data.data.numFound
          //   this.schools = res.data.data.item.map(item => {
          //     return {
          //       label: item.name,
          //       school_id: item.school_id
          //     }
          //   })
          //   for (let i = 2; i <= Math.ceil(turns / 30); i++) {
          //     axios.get('/web/api/?keyword=' + query + '&page=' + i + '&province_id=&ranktype=&request_type=1&size=30&type=&uri=apidata/api/gkv3/school/lists&signsafe=8be0023a2a61cf35f72d17dad1c12534').then(res => {
          //       this.schools = this.schools.concat(res.data.data.item.map(item => {
          //         return {
          //           label: item.name,
          //           school_id: item.school_id
          //         }
          //       }))
          //     }).catch(err => {
          //       console.log(err)
          //     })
          //   }
          // }).catch(err => {
          //   console.log(err)
          // })
        }, 200)
      } else {
        this.schools = []
      }
    },
    remoteMethod2(data) {
      if (data) {
        // 获取院系和专业
        axios.get('/static-data/www/2.0/school/' + data.school_id + '/pc_special.json').then(res => {
          console.log(data)
          // 获取院系
          if (res.data.data.special_detail['3']) {
            this.departments = res.data.data.special_detail['3'].map(item => {
              return {
                value: item.name,
                label: item.name,
              }
            })
          } else {
            this.departments = []
          }
          console.log(this.departments)
          // 将专业按树形结构组织
          let special_tree = {}
          res.data.data.special_detail['1'].forEach(item => {
            if (!special_tree[item.level2_name]) {
              special_tree[item.level2_name] = {}
              special_tree[item.level2_name][item.level3_name] = [item.special_name]
            } else {
              if (!special_tree[item.level2_name][item.level3_name]) {
                special_tree[item.level2_name][item.level3_name] = [item.special_name]
              } else {
                special_tree[item.level2_name][item.level3_name].push(item.special_name)
              }
            }
          })
          console.log(special_tree)
          // 获取专业
          this.options = Object.keys(special_tree).map(level2_name => {
            return {
              value: level2_name,
              label: level2_name,
              children: Object.keys(special_tree[level2_name]).map(level3_name => {
                return {
                  value: level3_name,
                  label: level3_name,
                  children: special_tree[level2_name][level3_name].map(special_name => {
                    return {
                      value: special_name,
                      label: special_name
                    }
                  })
                }
              })
            }
          })
        }).catch(err => {
          console.log(err)
        })
      }
    },
    large() {
      ElMessageBox.alert('请扫描下方二维码或点击按钮进行报名付费', '', {
        closeOnClickModal: true,
        closeOnPressEscape: true,
        showConfirmButton: false,
        message: () => h(
            'img',
            {
              src: require('./报名二维码.png'),
              style: {
                width: '400px'
              }
            }
        ),
        callback: () => {
        }
      })
    },
    refresh_status() {
      axios.get('http://localhost:8000/pay', {
        headers: {
          // 从Cookie中获取名为access_token的值
          'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
        }
      }).then(res => {
        if (res.data.status === 'failed')
          return

        this.pay_status = true
        this.exam.exam_name = res.data.data.exam_name
        this.exam.exam_price = res.data.data.exam_price
        this.exam.exam_venue = res.data.data.exam_venue
        this.exam.exam_venue_no = res.data.data.exam_venue_no
        this.exam.exam_time = res.data.data.exam_time
        this.exam.exam_info = res.data.data.exam_info

      }).catch(err => {
        console.log(err)
      })
    },
    handleAvatarSuccess(res, file) {
      this.upload_url = URL.createObjectURL(file.raw)
      this.form.avatar = true
    },
    beforeAvatarUpload(file) {
      // 限制图片格式为jpg, jpeg, png, webp
      const isImage = file.type === 'image/jpeg' || file.type === 'image/png' || file.type === 'image/webp'
      if (!isImage) {
        ElNotification({
          title: '提示',
          message: '上传头像图片只能是 jpg/jpeg/png/webp 格式!',
          type: 'error'
        })
        return false
      }

      const isLt2M = file.size / 1024 / 1024 < 2
      if (!isLt2M) {
        ElNotification({
          title: '提示',
          message: '上传头像图片大小不能超过 2MB!',
          type: 'error'
        })
      }
      return isLt2M
    },
    get_avatar() {
      axios.get('http://localhost:8000/get_picture', {
        headers: {
          // 从Cookie中获取名为access_token的值
          'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
        },
        responseType: 'blob',
      }).then(res => {
        // 处理 base64 图片\
        let _this = this
        let reader = new FileReader()
        reader.readAsDataURL(res.data)
        console.log(res.data)
        nextTick(() => {
          reader.onload = function () {
            _this.imageUrl = reader.result
          }
        })
      }).catch(err => {
        console.log(err)
      })
    }
  },
  mounted() {
    let _this = this
    this.refresh_status()

    axios.get('http://localhost:8000/signup_info', {
      headers: {
        // 从Cookie中获取名为access_token的值
        'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
      }
    }).then(res => {
      _this.name = res.data.stu_name
      _this.sex = res.data.id_no[-2] % 2 === 0 ? '女' : '男'
      _this.id_type = id_type_map[res.data.id_type]
      _this.id_no = res.data.id_no
      _this.email = res.data.email
      _this.tel = res.data.tel
      _this.stu_school = res.data.stu_school
      _this.stu_department = res.data.stu_department
      _this.stu_major = res.data.stu_major
      _this.stu_age = new Date().getFullYear() - res.data.id_no.slice(6, 10)
      _this.stu_cls = res.data.stu_cls
      _this.stu_no = res.data.stu_no
      _this.stu_info = res.data.stu_info
      _this.confirm = res.data.confirm
      _this.step_active = res.data.confirm === '0' ? 0 : 2
      _this.max_step = res.data.confirm === '0' ? 0 : 3
      _this.pay_status = res.data.pay_status !== '0'


      if (_this.step_active === 0) {
        // 获取学校列表
        axios.get('/static-data/www/2.0/school/name.json').then(res => {
          this.all_schools = res.data.data.map(item => {
            return {
              value: {'name': item.name, 'school_id': item.school_id},
              label: item.name,
            }
          })
        }).catch(err => {
          console.log(err)
        })
      } else {
        // 获取头像
        axios.get('http://localhost:8000/get_picture', {
          headers: {
            // 从Cookie中获取名为access_token的值
            'Authorization': 'Bearer ' + document.cookie.split(';').find(item => item.trim().startsWith('access_token=')).split('=')[1]
          },
          responseType: 'blob',
        }).then(res => {
          // 处理 base64 图片
          let reader = new FileReader()
          reader.readAsDataURL(res.data)
          console.log(res.data)
          reader.onload = function () {
            _this.imageUrl = reader.result
          }
        }).catch(err => {
          console.log(err)
        })
      }
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
.lz_td1 {
  width: 30%;
  text-align: right;
  font: 14px "微软雅黑";
  color: #999999;
}

.lz_td2 {
  width: 70%;
  text-align: left;
  font: 14px "微软雅黑";
  color: #212963;
}

.margin-top {
  display: block;
  background: url(./zc_top_bg0.png) no-repeat 0 0;
  border-top-left-radius: 16px;
}

.cell-item {
  font-size: 14px;
  color: #999999;
}

.cell-context {
  font-size: 14px;
  color: #212963;
}

.default-cell-context {
  font-size: 14px;
  color: #ccc;
}

.title {
  font-size: 18px;
  font-weight: normal;
  margin: 6px 0 0 34px;
  color: #ffffff;
}

.img {
  transform: rotate(90deg);
}

.afd {
  background-image: url('./support me on afd-白底.png');
  background-size: 100% 100%;
}

.afd:hover {
  background-image: url('./support me on afd-发电紫.png');
}

/deep/ .el-upload {
  height: 160px;
}

/deep/ .el-upload-dragger {
  height: 100%;
  padding: 0;

  .el-icon {
    margin-top: 50px;
    font-size: 60px;
    color: #8c939d;
  }
}

.avatar {
  width: 120px;
  height: 160px;
}

</style>
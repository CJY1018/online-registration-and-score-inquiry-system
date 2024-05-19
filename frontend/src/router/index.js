import {createRouter, createWebHistory} from 'vue-router'
import HelloWorldView from '../views/HelloWorldView.vue'
import LoginView from "@/views/LoginView.vue";
import RegisterView from "@/views/RegisterView.vue";
import ResetPasswordView from "@/views/ResetPasswordView.vue";
import MeView from "@/views/MeView.vue";
import HomeView from "@/views/HomeView.vue";
import ScoreInquiryView from "@/views/ScoreInquiryView.vue";
import SignUpView from "@/views/SignUpView.vue";
import AdministratorLoginView from "@/views/AdministratorLoginView.vue";
import AdministratorConsoleView from "@/views/AdministratorConsoleView.vue";
import {
    RegistrationInformation,
    ExamInformation,
    ExamArrangement,
    ScoreEntry,
    ScoreAnalysis,
    OtherOperations
} from "@/components/administrator_console_page/menu/menu.js";

import axios from "axios";


const routes = [
    {
        path: '/',
        name: 'hello_world',
        component: HelloWorldView
    },
    {
        path: '/about',
        name: 'about',
        // route level code-splitting
        // this generates a separate chunk (about.[hash].js) for this route
        // which is lazy-loaded when the route is visited.
        component: () => import(/* webpackChunkName: "about" */ '../views/AboutView.vue')
    },
    {
        path: '/login',
        name: 'login',
        component: LoginView
    },
    {
        path: '/register',
        name: 'register',
        component: RegisterView
    },
    {
        path: '/reset_password',
        name: 'reset_password',
        component: ResetPasswordView
    },
    {
        path: '/me',
        name: 'me',
        component: MeView,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/home',
        name: 'home',
        component: HomeView,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/score_inquiry',
        name: 'score_inquiry',
        component: ScoreInquiryView,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/signup',
        name: 'signup',
        component: SignUpView,
        meta: {
            requiresAuth: true
        }
    },
    {
        path: '/administrator_login',
        name: 'administrator_login',
        component: AdministratorLoginView
    },
    {
        path: '/administrator_console',
        name: 'administrator_console',
        component: AdministratorConsoleView,
        meta: {
            requiresAdmin: true
        },
        children: [
            {
                path: 'registration_information',
                name: 'registration_information',
                component: RegistrationInformation
            },
            {
                path: 'exam_information',
                name: 'exam_information',
                component: ExamInformation
            },
            {
                path: 'exam_arrangement',
                name: 'exam_arrangement',
                component: ExamArrangement
            },
            {
                path: 'score_entry',
                name: 'score_entry',
                component: ScoreEntry
            },
            {
                path: 'score_analysis',
                name: 'score_analysis',
                component: ScoreAnalysis
            },
            {
                path: 'other_operations',
                name: 'other_operations',
                component: OtherOperations
            }
        ]
    }
]

const router = createRouter({
    history: createWebHistory(),
    routes
})

router.beforeEach((to, from, next) => {
    if (to.matched.some(record => record.meta.requiresAuth)) {
        if (!document.cookie.includes('access_token')) {
            // 未登录
            next({
                path: '/login',
                query: {redirect: to.fullPath, message: '请先登录'}
            })
        } else {
            const access_token = document.cookie.split('; ').find(row => row.startsWith('access_token')).split('=')[1]
            // 验证 access_token 是否有效
            axios.get('http://localhost:8000/signup_info', {
                headers: {'Authorization': 'Bearer ' + access_token}
            }).then(() => {
                // 验证通过
                next()
            }).catch(err => {
                // 验证失败
                console.log(err)
                if (err.response.status === 403) {
                    next({
                        path: '/login',
                        query: {redirect: to.fullPath, message: '验证失败'}
                    })
                }
            })
        }
    } else if (to.matched.some(record => record.meta.requiresAdmin)) {
        if (!document.cookie.includes('admin_token')) {
            // 未登录
            next({
                path: '/administrator_login',
                query: {redirect: to.fullPath, message: '请先登录'}
            })
        } else {
            const admin_token = document.cookie.split('; ').find(row => row.startsWith('admin_token')).split('=')[1]
            // 验证 admin_token 是否有效
            axios.get('http://localhost:8000/administrator_info', {
                headers: {'Authorization': 'Bearer ' + admin_token}
            }).then(() => {
                // 验证通过
                next()
            }).catch(err => {
                // 验证失败
                console.log(err)
                if (err.response.status === 403) {
                    next({
                        path: '/administrator_login',
                        query: {redirect: to.fullPath, message: '验证失败'}
                    })
                }
            })
        }
    } else {
        next()
    }
})

export default router

import {createApp} from 'vue'
import App from './App.vue'
import router from './router'

createApp(App).use(router).use(router).mount('#app')


const debounce = (fn, delay) => {
    let timer
    return (...args) => {
        if (timer) {
            clearTimeout(timer)
        }
        timer = setTimeout(() => {
            fn(...args)
        }, delay)
    }
}

const _ResizeObserver = window.ResizeObserver;
window.ResizeObserver = class ResizeObserver extends _ResizeObserver {
    constructor(callback) {
        callback = debounce(callback, 20);
        super(callback);
    }
}
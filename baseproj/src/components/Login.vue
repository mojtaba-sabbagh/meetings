<template>
  <div>
    <form @submit.prevent="submit">
      <div class="mt-10">
        <label class="font-farsi mb-2 text-sm ml-4">نام کاربری</label>
        <input type="text" v-model="username" class="font-farsi ltr-grid border text-sm rounded-lg p-2
           bg-white-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400"/>
      </div>
      <div class="mt-4">
        <label class="font-farsi text-sm ml-4">کلمه عبور</label>
        <input type="password" v-model="password"
           class="font-farsi ltr-grid border text-sm rounded-lg p-2
           bg-white-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400"
          />
      </div>
      <div>
        <button type="submit" class="mr-12 mt-4 border border-gray-500 px-8 py-1 hover:bg-red-100">ورود</button>
      </div>
    </form>
    <div class="my-10">
        {{ message }}
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import { serverUrl } from '../../settings';

export default {
  data() {
    return {
      username: "",
      password: "",
      message: "",
      toast: null,
    }
  },
  mounted() {

  },
  methods: {
    async submit() {
      const this_ = this;
      if (this.username === '' || this.password === '') {
        this.message = 'نام کاربری و پسورد را وارد کنید'
      } else
          
          axios({
            method: 'post',
            url: serverUrl+'api/login/',
            headers: {
              'Accept': '*/*',
              'Content-Type': 'application/json',
            },
            data: {
              username: this.username,
              password: this.password,
            },
            withCredentials: true,
            })
            .then(response => {
                console.log(response);
                this.$emit('onLogin');
            })
            .catch(error => {
                this.message = error; //'نام کاربری یا پسورد اشتباه است'; 
            });
      }
    }
}
</script>

<style scoped>
.parent {
  height: 100vh;
}
.ltr-grid {
  direction: ltr;
}
</style>
<script>
// This starter template is using Vue 3 <script setup> SFCs
// Check out https://vuejs.org/api/sfc-script-setup.html#script-setup
  import Base from './components/Base.vue';
  import Meeting from './components/Meeting.vue';
  import Proceeding from './components/Proceeding.vue';
  import Resolution from './components/Resolution.vue';
  import Search from './components/Search.vue';
  import Login from './components/Login.vue';
  import axios from 'axios';
  import { serverUrl } from '../settings';

  const defatUser = {
          first_name: 'نام',
          last_name: 'کاربر',
          email: '',
          username: '',
          is_staff: false,
        };
  export default {
    data() {
      return {
        activeSec: 5,
        loggedIn: false,
        user: defatUser,
      }
    },
    components: {
      Base,
      Meeting,
      Proceeding,
      Resolution,
      Search,
      Login,
    },
    computed:{
      fullname() {
        return `${this.user.first_name} ${this.user.last_name}`;
      }
    },
    methods: {
    // We can add our functions here
      async fetchUser() {
        //axios.defaults.headers.post['Access-Control-Allow-Origin'] = '*';
        await axios({
            method: 'get',
            url: serverUrl+'api/profile/',
            headers: {
              'Accept': '*/*',
              'Content-Type': 'application/json',
            },
            withCredentials: true,
            })
            .then(response => {
              this.user = response.data;
              this.loggedIn = true;
              this.activeSec = 0;
            })
            .catch(error => {
                this.message = error; //'خطایی در ثبت اطلاعات کاربر رخ داد'; 
                this.loggedIn = false;
                this.activeSec = 5;
            });
      },

      loggingIn(){
        this.loggedIn = true;
        this.activeSec = 0;
        this.fetchUser();
      },
      loggingOut(){
        this.loggedIn = false;
        this.activeSec = 5;
        this.user = defatUser;
        axios({
        method: 'post',
        url: serverUrl+'api/logout/',
        withCredentials: true,
        })
        .then(response => {
            this.$cookies.remove('XSRF-TOKEN');
            this.$cookies.remove('sessionid');
        })
        .catch(error => {
            this.message = error; //'خطایی در ثبت اطلاعات کاربر رخ داد'; 
        });
      },
    },
    created(){
       this.fetchUser();
    },
  }
</script>

<template>
  <!--div class="grid grid-cols-5 gap-3 w-full">
    <div class="bg-blue-100">1st col</div>
    <div class="bg-red-100 col-span-4">2nd col</div>
  </div-->
  <div class="flex flex-col font-farsi m-5">
    <div class="flex justify-between mb-5 p-5 border-2 text-sm font-bold bg-red-50"> 
      <div class="grid justify-items-center p-2"> 
        <img class="w-1/6" src="images/logo.png"/>
        <span class="mt-2 hover:text-blue-500"> دانشگاه ولی عصر(عج) رفسنجان  </span>
      </div>
      <span class="text-3xl pt-4 hover:text-blue-500"> سامانه مصوبات </span>
      <div class="flex text-sm"> 
        <div class="grid justify-items-center hover:text-blue-500 p-2"> 
            <img class="" src="images/user-24.png"/>
            <span lass="mt-0"> {{ fullname }} </span>
        </div>
        <a v-if="loggedIn" href="#" @click="loggingOut" class="block mr-10"> 
          <div class="grid justify-items-center hover:bg-red-100 p-2"> 
            <img class="w-1/2" src="images/logout-48.png"/>
            <span class="mt-2"> خروج </span>
          </div>
        </a>
      </div>
    </div>


    <div class="flex flex-row gap-0.5">
      <div class="bg-red-50 border-2 basis-1/12">  
        
        <a href="#" class="block  hover:bg-red-100" @click="activeSec=0"> 
            <div class="border-b-4 py-5"> ابزارها </div> 
        </a>

        <a v-if="loggedIn && user.is_staff" class="block mt-5  py-2  hover:bg-red-100" @click="activeSec=1">
          <div class="grid justify-items-center">
             <img class="w-12" src="images/network.png"/> 
            <span class="text-sm"> مدیریت جلسات </span>
          </div>
        </a>
       
        <a v-if="loggedIn && user.is_staff" class="block mt-5 py-2  hover:bg-red-100" href="#" @click="activeSec=2">
          <div class="grid justify-items-center">
             <img class="w-12" src="images/document.png"/> 
            <span class="text-sm"> مدیریت صورتجلسه </span>
          </div>
        </a>

        <a v-if="loggedIn && user.is_staff" class="block mt-5 py-2  hover:bg-red-100" href="#" @click="activeSec=3">
          <div class="grid justify-items-center">
             <img class="w-12" src="images/justice.png"/> 
            <span class="text-sm"> مدیریت مصوبات </span>
          </div>
        </a>

        <a v-if="loggedIn" class="block mt-5 py-2  hover:bg-red-100" href="#" @click="activeSec=4">
          <div class="grid justify-items-center">
             <img class="w-12" src="images/report.png"/> 
            <span class="text-sm"> جستجوی مصوبات </span>
          </div>
        </a>
      
      </div>
      <div class="border-2 basis-11/12">  
        <Base v-if="activeSec == 0" />
        <Meeting v-if="activeSec == 1" />
        <Proceeding v-if="activeSec == 2" />
        <Resolution v-if="activeSec == 3" />
        <Search v-if="activeSec == 4" />
        <Login v-if="activeSec == 5" @onLogin="loggingIn"/>
      </div>
    </div>
  </div>
</template>

<style scoped>
  
</style>

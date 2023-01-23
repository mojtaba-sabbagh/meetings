<script>
    import DropDown from './elements/DropDown.vue';
    import InputText from './elements/InputText.vue';
    import axios from 'axios';
    import { serverUrl } from '../../settings';
    export default {
        data() {
          return {
            meetingNamesOptions: Object,
            meetingData: Object,
            employeeOptions: {},
            members: [],
            meetingId: 0,
            meetingName: '',
            meetingPeriod: '0',
            manipulationMode: 0,
            showForm: false,
            showAlert: false,
            message: '',
            buttonLabel: 'تایید',
            periodOptions: [
                { "ID": "روزانه",
                  "text":"روزانه"
                },
                {"ID": "روزانه",
                  "text":"هفتگی"
                },
                {"ID": "دوهفتگی",
                  "text":"دوهفتگی"
                },
                {"ID": "ماهیانه",
                  "text":"ماهیانه"
                },
                {"ID": "غیرمشخص",
                  "text":"غیرمشخص"
                }
            ],
            roleOptions: [
                {"ID":"عضو", "text":"عضو"},
                {"ID":"دبیر", "text":"دبیر"},
            ],
            errorMessage: '',
          }
        },
        components: {
            DropDown,
            InputText,
        },
        methods: {
            meetingsName(){
             axios.defaults.withCredentials = true;
             axios({
                    method: 'get',
                    url: serverUrl+'api/meetings/',
                    withCredentials: true,
                    }
                    )
                .then(response => {
                    this.meetingNamesOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          employeesName(){
             axios({
                    method: 'get',
                    url: serverUrl+'api/employees/',
                    headers: {
                        'Accept': '*/*',
                        'Content-Type': 'application/json',},
                    })
                .then(response => {
                    this.employeeOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          getMeetingAPI(meetingId){
             axios({
                    method: 'get',
                    url: serverUrl+'api/meetings/'+meetingId+'/',
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.fillMeetingForm(response.data);
                })
                .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          addMeetingAPI(){
            if (this.manipulationMode == 0){
                axios.post(serverUrl+'api/meetings/', {'meeting_name':this.meetingName, 'period':this.meetingPeriod})
                    .then(response => {
                        this.blankForm();
                        this.meetingsName();
                        this.$toast.success('جلسه با موفقیت ذخیره گردید.');
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در ذخیره اطلاعات رخ داد.');
                    });
            }
            else {
                axios.put(serverUrl+'api/meetings/'+this.meetingId+'/', {'meeting_name':this.meetingName, 'period':this.meetingPeriod})
                    .then(response => {
                        this.meetingsName();
                        this.$toast.success('جلسه با موفقیت ذخیره گردید.');
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در ذخیره اطلاعات رخ داد.');
                    });   
            }
          },
          getMeeting(newValue){
            if (newValue && newValue != 0){
                this.meetingId = newValue;
                this.getMeetingAPI(newValue);
                this.buttonLabel = 'بروزرسانی جلسه';
                this.manipulationMode = 1;
                this.showForm = true;
            }
            else {
              this.meetingId = 0;
              this.blankForm();
            }
          },
          fillMeetingForm(meetingData){
            this.meetingName = meetingData.meeting_name;
            this.meetingPeriod = meetingData.period;
            this.members = meetingData.members;
          },
          updateName(newValue){
           this.meetingName = newValue; 
          },
          updatePeriod(newValue){
           this.meetingPeriod = newValue; 
          },
          updateRole(newValue, row){
            this.members[row].role = newValue;
          },
          updateMember(newValue, row){
            this.members[row].employee_id = newValue;
          },
          blankForm(){
            this.members = [];
            this.meetingName = '';
            this.meetingPeriod = '0';
            this.buttonLabel = 'ایجاد جلسه';
            this.manipulationMode = 0;
            this.showForm = true;
            this.meetingId = 0;
          },
          deleteMeeting(){
            axios.delete(serverUrl+'api/meetings/'+this.meetingId+'/')
            .then(response => {
                    this.meetingsName();
                    this.blankForm();
                    this.$toast.success('جلسه حذف گردید.');
                })
            .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                });
          },
          addMember(){
            this.members.push({"role": "0", "employee_id":"0", "id":0});
          },
          deleteMember(event){
            let row = parseInt(event.currentTarget.getAttribute('row'));
            let memId = this.members[row].id;
            if (memId !=0 ){
                axios.delete(serverUrl+'api/members/'+memId+'/')
                .then(response => {
                    this.members.splice(row, 1);
                    this.$toast.success('عضو حذف گردید.');
                    })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                    });
                }
          },
          showAlertFunc(message){
            this.message = message;
            this.showAlert = true;
            let delayInMilliseconds=2000;
            setTimeout(() => {
                this.showAlert = false;
            }, delayInMilliseconds);
          },
          saveAPI(memId, row) {
            // call apis
            if (memId !=0 ){
                axios.put(serverUrl+'api/members/'+memId+'/', {'employee':this.members[row].employee_id, 
                                                        'role':this.members[row].role, 'meeting':this.meetingId})
                .then(response => {
                    this.$toast.success('تغییرات ذخیره شد.');
                    })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                    console.log(memId, row);
                    });
                }
            else {
                axios.post(serverUrl+'api/members/', {'employee':this.members[row].employee_id, 
                                                        'role':this.members[row].role, 'meeting':this.meetingId})
                    .then(response => {
                        this.$toast.success('تغییرات ذخیره شد.');
                    })
                    .catch(error => {
                        this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در برقرار ارتباط با سامانه رخ داد.');
                    });
            }
          },
          saveMember(event){
            let row = parseInt(event.currentTarget.getAttribute('row'));
            let memId = this.members[row].id;
            this.saveAPI(memId, row);
          },
          saveAllMembers(){
           // this.members.forEach(function (member, row) {
           //     this.saveAPI(member.id, row);
           // });
            for (const [row, member] of this.members.entries()) {
                this.saveAPI(member.id, row);
                };
            },
        },
        created(){
          this.meetingsName();
          this.employeesName();
        },
        computed: {
            isDisabled() {
                // evaluate whatever you need to determine disabled here...
                if (this.meetingName == '' || this.meetingPeriod == '0')
                    return true;
                return false;
             },
        }
    }
</script>

<template>
    <div> 
        <span class="block-inline text-lg hover:text-blue-500 p-2 border-2 bg-red-100"> مدیریت جلسه </span>
        <div class="flex flex-col font-farsi items-stretch items-center">
            <div class="flex items-end">
                <DropDown class="mt-10 mx-5 w-4/5 md:w-1/2" label_title="جلسات موجود"  @onChangeValue="getMeeting"
                    :options="meetingNamesOptions" :order=1 :itemSelected="meetingId"/>
                    <button class="block-inline flex items-end justify-right" @click="blankForm">
                        <img class="opacity-60 hover:bg-red-100 w-8 p-1 mb-1" title="اضافه کردن جلسه" src="images/plus.png"/>
                    </button>
                    <button class="block-inline flex justify-center hover:bg-red-100 p-1 mb-1" @click="deleteMeeting" :disabled="meetingId == 0">
                        <img class="w-6 opacity-60" title="حذف جلسه" src="images/minus.png"/>
                    </button>
            </div>
            <div v-if="showForm">
                <div class="border border-gray-500 mt-5 pb-5 mx-5">
                    <form v-on:submit.prevent="addMeetingAPI">
                        <div class="md:flex md:flex-row gap-4 mt-5 items-center">
                            <InputText  class="w-5/6 md:w-2/3 mx-4" v-model:value="meetingName"
                                @onChangeValue="updateName" label_title="نام جلسه" input_placeholder="نام جلسه" />
                            <DropDown class="w-5/6 md:w-1/3 mx-4" label_title="دوره"  v-model:itemSelected="meetingPeriod" 
                                :options="periodOptions" @onChangeValue="updatePeriod" :order=2 />
                        </div>
                        <button class="hover:bg-red-100 mt-14 w-1/2 appearance-none border text-sm text-center rounded-lg p-2.5
                            bg-red-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 
                            focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400 disabled:bg-slate-50 disabled:text-slate-300" :disabled="isDisabled"> 
                            <span> {{ buttonLabel }} </span>
                        </button>
                    </form>
                    <p class="text-red-500 mt-2"> {{ errorMessage }} </p>
                </div>
                <div class="mt-10">
                    <div class="flex items-center">
                        <span class="block-inline float-right text-green-800 text-lg hover:text-blue-500 p-2">اعضاء جلسه: </span>
                        <button class="block-inline flex justify-center hover:bg-red-100 hover:border hover:border-1 p-1"
                                title="ذخیره همه اعضا" @click="saveAllMembers">
                            <img class="w-7 opacity-60" src="images/ok.png"/>
                        </button>
                    </div>
                    <div class="flex flex-col items-center pb-5 mx-5 border border-gray-500">
                        <div class="w-full md:flex md:gap-6 justify-center mt-2 px-2" v-for="(member, i) in members">
                            <DropDown class="w-full md:w-2/5 md:float-right" label_title="نام عضو"  v-model:itemSelected="members[i].employee_id" 
                                    :options="employeeOptions" @onChangeValue="updateMember" :row="i" :order=3 />
                            <DropDown class="w-full mt-1 md:w-2/5 md:mt-0 md:float-right" label_title="نقش"  v-model:itemSelected="members[i].role" :options="roleOptions"
                                    @onChangeValue="updateRole" :row="i" :order=4 />
                            <div class="flex flex-row items-end justify-center w-full md:w-1/4">  
                                <button class="block-inline flex justify-center hover:bg-red-100 p-1" title="حذف عضو" 
                                    :row="i" :name="members[i].id" @click="deleteMember">
                                    <img class="w-7 opacity-60" src="images/minus.png"/>
                                </button>
                                <button class="block-inline flex justify-center hover:bg-red-100 hover:border hover:border-1 p-1"
                                    title="ذخیره عضو" :row="i" :name="members[i].id" @click="saveMember">
                                    <img class="w-7 opacity-60" src="images/ok.png"/>
                                </button>
                            </div>
                        </div>
                    </div>
                    <div class="flex flex-col items-center mt-5">
                        <button class="block-inline flex items-end justify-right" title="افزودن عضو" @click="addMember">
                            <img class="opacity-60 hover:bg-red-100 w-8 p-1" src="images/plus.png"/>
                        </button>
                    </div>
                </div>
                <div class="flex justify-center">
                    <div  class="flex items-center justify-center md:w-1/4 my-5 text-black font-farsi text-sm font-bold px-4 py-3" role="alert">
                        <p v-if="showAlert" class=""> {{ message }} </p>
                    </div>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
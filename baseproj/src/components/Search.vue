<script>
    import DropDown from './elements/DropDown.vue';
    import InputText from './elements/InputText.vue';
    import DateInput from './elements/DateInput.vue';
    import Radio from './elements/Radio.vue';
    import TableResults from './elements/TableResults.vue';
    import axios from 'axios';
    import { serverUrl } from '../../settings';
    import PersianDate from '@alireza-ab/persian-date';
    import Buttons from './elements/Buttons.vue';


    export default {
        data() {
          return {
            meetingNamesOptions: Object,
            proceedingNameOptions: Object,
            proceedingData: Object,
            employeeOptions: {},
            resolutionTypeOptions: {},
            meetingId: 0,
            proceedingId: 0,
            resolution_type: '0',
            stockholder_type: '0',
            zinaf: '',
            zinafname: '',
            fullname: '',
            resolutions: [],
            showForm: false,
            showAlert: false,
            message: '',
            errorMessage: '',
            karkonan: 'کارکنان',
            daneshjou: 'دانشجو',
            zinafLabelText: 'ذینفع',
            stockHolderOptions: [
                {'ID': 'دانشجو', 'text': 'دانشجو'},
                {'ID': 'کارکنان', 'text': 'کارکنان'},
            ],
            Agree: 'موافقت',
            Disagree: 'مخالفت',
            searchStart: false,
            searchResults: {},
            pre: '',
            next: '',
            offset: 0,
            pageSize: 0,
            fromDate: '',
            toDate: '',
            searchBy: 'NO',
            actText: '',
          }
        },
        components: {
            DropDown,
            InputText,
            DateInput,
            Radio,
            TableResults,
                Buttons,
        },
        methods: {
            resetMessages(){
                this.message = '';
                this.errorMessage = '';
                this.showAlert = false;
            },
            meetingsName(){
             axios({
                    method: 'get',
                    url: serverUrl+'api/meetings/',
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.meetingNamesOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          employeesName(meetingId){
             axios({
                    method: 'get',
                    url: serverUrl+'api/employees/?meetingid='+meetingId,
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.employeeOptions = response.data;
                })
                .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          getProceedingAPI(proceedingId){
             axios({
                method: 'get',
                url: serverUrl+'api/proceedings/'+proceedingId+'/',
                headers: {"Content-Type": "application/json"},
                })
            .then(response => {
                this.proceedingData = response.data;
                this.preadonly = response.data.readonly;
                })
            .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
          },
          getProceedings(){
            if (this.meetingId != '0') {
                axios({
                    method: 'get',
                    url: serverUrl+`api/proceedings/?meetingid=${this.meetingId}&fromdate=${this.fromDate}&todate=${this.toDate}`,
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.proceedingNameOptions = response.data;
                    this.employeesName(this.meetingId);
                })
                .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
                });
            };
          },
          getResolutionTypes(){
            axios({
                method: 'get',
                url: serverUrl+'api/resolutiontypes/',
                headers: {"Content-Type": "application/json"},
                })
            .then(response => {
                this.resolutionTypeOptions = response.data;
            })
            .catch(error => {
                this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
            });
          },
         updateShType(newValue){
            if (newValue == 'دانشجو'){
                this.zinafLabelText = 'شماره دانشجویی';   
            }
            else if (newValue == 'کارکنان'){
                this.zinafLabelText = 'کد ملی';
            }
            else {
                this.zinafLabelText = 'ذینفع';
            }
            this.stockholder_type = newValue;
          },
          updateType(newValue){
            this.resolution_type = newValue;
          },
          updateSh(newValue, row){
           this.zinaf = newValue; 
          },
          updateFromDate(newValue){
            let p = new PersianDate(newValue,'jalali');
            this.fromDate = p.calendar('gregorian').toString('?YYYY-?MM-?DD');
          },
          updateToDate(newValue){
            let p = new PersianDate(newValue,'jalali');
            this.toDate = p.calendar('gregorian').toString('?YYYY-?MM-?DD');
            console.log(this.toDate);
          },
          updateMeetingId(newValue){
            this.meetingId = newValue;
          },
          updateProceedignId(newValue){
            this.proceedingId = newValue;
          },
          updateShname(newValue){
            this.zinafname = newValue;
          },
          updateActText(newValue){
            this.actText = newValue;
          },
          clearToDate(){
            this.toDate = '';
          },
         submitSearch(){
            let url = serverUrl + 
            `api/searchres/?meetingid=${this.meetingId}&proceedingid=${this.proceedingId}&fromdate=${this.fromDate}&todate=${this.toDate}` + 
            `&restype=${this.resolution_type}&shtype=${this.stockholder_type}&searchtype=${this.searchBy}` +
            `&shno=${this.zinaf}&shname=${this.zinafname}&restext=${this.actText}`;
            
            this.getPage(url);
         },
         getPage(url){
              axios({
                    method: 'get',
                    url: url,
                    headers: {"Content-Type": "application/json"},
                    })
                .then(response => {
                    this.searchResults = response.data;
                    this.next = response.data.next;
                    this.pre = response.data.previous;
                    this.searchStart = false;
                })
                .catch(error => {
                    this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    this.searchStart = false;
                    this.$toast.error('خطا در واکشی اطلاعات از سامانه رخ داد.');
              });
            },
          getNext(){
            this.offset = (parseInt(this.next.split('=')[1]) - 1) * this.pageSize;
            this.getPage(this.next);
             
          },
          getPre(){
            let page = this.pre.split('=')[1];
            if (page){
              this.offset = (parseInt(page) - 1) * this.pageSize;
            }
            else{
              this.offset = 0;
            }
            this.getPage(this.pre);
          },
        },
        created(){
          axios.defaults.withCredentials = true;
          this.meetingsName();
          this.getResolutionTypes();
         },
        computed: {
            isDisabled() {
                // evaluate whatever you need to determine disabled here...
                //let row = parseInt(event.currentTarget.getAttribute('row'));
                //if (this.resolutions[row].item_no == '' || this.resolutions[row].act_text == '')
                //    return true;
                //if (this.preadonly) return true;
                return false;
             },
        }
    }
</script>

<template>
    <div> 
        <span class="block-inline text-lg hover:text-blue-500 p-2 border-2 bg-red-100"> جستجوی مصوبات </span>
        <div class="flex flex-col  font-farsi items-stretch items-center">
            <div class="flex flex-col md:flex-row justify-center w-full md:gap-4 border border-gray pb-5">
                <DropDown class="mt-5 md:mt-10 mx-5 w-4/5 md:w-1/2" label_title="جلسات موجود"  
                    :options="meetingNamesOptions" v-model:itemSelected="meetingId" @onChangeValue="updateMeetingId"/>
                <DateInput class="mt-5 w-5/6 md:mt-10 md:w-1/4 mx-4" label_title="از تاریخ"  v-model:value="fromDate" 
                        @onChangeValue="updateFromDate" :disabled="preadonly" />
                <DateInput class="mt-5 w-5/6 md:mt-10 md:w-1/4 mx-4" label_title="تا تاریخ"  v-model:value="toDate" 
                                 @onChangeValue="updateToDate" :disabled="preadonly" />
            </div>
            <div>
                <div class="flex flex-col md:gap-4 border border-gray mt-1 pb-5 ">
                    <div class="flex flex-col md:flex-row md:gap-4 items-center">
                        <DropDown v-if="meetingId != '0'" class="w-4/5 md:mr-5" label_title="صورتجلسات موجود" 
                        @click="getProceedings" :options="proceedingNameOptions" :itemSelected="proceedingId"
                        @onChangeValue="updateProceedignId"/>
                        <DropDown class="w-4/5" label_title="نوع مصوبه"  @onChangeValue="updateType"
                            :options="resolutionTypeOptions" :itemSelected="resolution_type" />
                        <InputText class="w-4/5"  label_title="متن مصوبه"  @onChangeValue="updateActText"
                                :value="actText" input_placeholder="قسمتی از متن مصوبه را بنویسید"/>
                        <DropDown class="w-4/5 md:ml-5" label_title="نوع ذینفع"  @onChangeValue="updateShType"
                            :options="stockHolderOptions" :itemSelected="stockholder_type" />
                    </div>
                    <div v-if="stockholder_type!='0'" class="flex flex-row justify-center">
                        <div class="flex w-1/4 items-center mr-4">
                            <input id="inline-2-radio" type="radio" v-model="searchBy" value="NO" name="inline-radio-group" class="w-4 h-4 text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                            <label for="inline-2-radio" class="mr-1 text-xs md:text-sm font-medium text-gray-900 dark:text-gray-300">جستجو برحسب <span v-if="stockholder_type==daneshjou">شماره دانشجویی</span> <span v-if="stockholder_type==karkonan">کدملی </span> </label>
                        </div>
                        <div class="flex items-center mr-4">
                            <input id="inline-radio" type="radio" v-model="searchBy" value="NAME" name="inline-radio-group" class="text-blue-600 bg-gray-100 border-gray-300 focus:ring-blue-500 dark:focus:ring-blue-600 dark:ring-offset-gray-800 focus:ring-2 dark:bg-gray-700 dark:border-gray-600">
                            <label for="inline-radio" class="mr-1 text-xs md:text-sm font-medium text-gray-900 dark:text-gray-300"> جستجو برحسب نام </label>
                        </div>
                        <div class="w-1/2 mr-10">
                            <InputText v-if="searchBy=='NO'" class="w-4/5" :label_title="zinafLabelText"  @onChangeValue="updateSh"
                                :value="zinaf" input_placeholder=""/>
                            <InputText v-if="searchBy=='NAME'" class="w-4/5" label_title="قسمتی از نام یا نام‌خانوادگی"  @onChangeValue="updateShname"
                                :value="zinafname"/>
                        </div>
                    </div>

                </div>
                <div class="flex flex-col w-full items-center">
                    <button type="button" @click="submitSearch"
                        class="block w-1/2 mt-7 px-7 py-3 bg-blue-600 text-white font-medium text-sm 
                        leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg 
                        focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 
                        active:shadow-lg transition duration-150 ease-in-out disabled:bg-gray-500">               
                        <svg v-if="searchStart" role="status" class="inline float-center w-4 h-4 mr-3 text-white animate-spin" viewBox="0 0 100 101" fill="none" xmlns="http://www.w3.org/2000/svg">
                            <path d="M100 50.5908C100 78.2051 77.6142 100.591 50 100.591C22.3858 100.591 0 78.2051 0 50.5908C0 22.9766 22.3858 0.59082 50 0.59082C77.6142 0.59082 100 22.9766 100 50.5908ZM9.08144 50.5908C9.08144 73.1895 27.4013 91.5094 50 91.5094C72.5987 91.5094 90.9186 73.1895 90.9186 50.5908C90.9186 27.9921 72.5987 9.67226 50 9.67226C27.4013 9.67226 9.08144 27.9921 9.08144 50.5908Z" fill="#E5E7EB"/>
                            <path d="M93.9676 39.0409C96.393 38.4038 97.8624 35.9116 97.0079 33.5539C95.2932 28.8227 92.871 24.3692 89.8167 20.348C85.8452 15.1192 80.8826 10.7238 75.2124 7.41289C69.5422 4.10194 63.2754 1.94025 56.7698 1.05124C51.7666 0.367541 46.6976 0.446843 41.7345 1.27873C39.2613 1.69328 37.813 4.19778 38.4501 6.62326C39.0873 9.04874 41.5694 10.4717 44.0505 10.1071C47.8511 9.54855 51.7191 9.52689 55.5402 10.0491C60.8642 10.7766 65.9928 12.5457 70.6331 15.2552C75.2735 17.9648 79.3347 21.5619 82.5849 25.841C84.9175 28.9121 86.7997 32.2913 88.1811 35.8758C89.083 38.2158 91.5421 39.6781 93.9676 39.0409Z" fill="currentColor"/>
                        </svg>
                        <span  v-if="!searchStart">
                            جستجو
                        </span>
                    </button>
                    <TableResults class="mt-5" :rows="searchResults" :offset="offset"/>
                </div>
                <div class="flex flex-row items-center my-7">
                    <!-- Previous Button -->
                    <button v-if="next"  type="button" @click="getNext" class="inline-flex items-center py-2 px-4 mr-3 text-sm font-medium text-gray-500 bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        <svg class="mr-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M7.707 14.707a1 1 0 01-1.414 0l-4-4a1 1 0 010-1.414l4-4a1 1 0 011.414 1.414L5.414 9H17a1 1 0 110 2H5.414l2.293 2.293a1 1 0 010 1.414z" clip-rule="evenodd"></path></svg>
                        بعدی    
                    </button>
                    <button v-if="pre"  type="button" @click="getPre" class="inline-flex items-center py-2 px-4 text-sm font-medium text-gray-500 bg-white rounded-lg border border-gray-300 hover:bg-gray-100 hover:text-gray-700 dark:bg-gray-800 dark:border-gray-700 dark:text-gray-400 dark:hover:bg-gray-700 dark:hover:text-white">
                        قبلی    
                        <svg class="ml-2 w-5 h-5" fill="currentColor" viewBox="0 0 20 20" xmlns="http://www.w3.org/2000/svg"><path fill-rule="evenodd" d="M12.293 5.293a1 1 0 011.414 0l4 4a1 1 0 010 1.414l-4 4a1 1 0 01-1.414-1.414L14.586 11H3a1 1 0 110-2h11.586l-2.293-2.293a1 1 0 010-1.414z" clip-rule="evenodd"></path></svg>
                    </button>
                </div>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
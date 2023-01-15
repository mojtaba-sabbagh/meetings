<script>
    import DropDown from './elements/DropDown.vue';
    import InputText from './elements/InputText.vue';
    import DateInput from './elements/DateInput.vue';
    import Toggle from './elements/Toggle.vue';
    import Radio from './elements/Radio.vue';
    import axios from 'axios';
    import { serverUrl } from '../../settings';
    import Confirm from './elements/Confirm.vue';

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
            resolutionObj: {
                id: 0,
                item_no: '',
                act_text: '',
                resolution_type: '0',
                result: true,
                proceeding: 0,
                stockholder_type: '0',
                stockholder: '',
                zinaf: '',
                fullname: '',
                gender: '',
            },
            resolutions: [],
            manipulationMode: 0,
            showForm: false,
            showAlert: false,
            message: '',
            preadonly: false,
            errorMessage: '',
            karkonan: 'کارکنان',
            daneshjou: 'دانشجو',
            stockHolderOptions: [
                {'ID': 'دانشجو', 'text': 'دانشجو'},
                {'ID': 'کارکنان', 'text': 'کارکنان'},
            ],
            Agree: 'موافقت',
            Disagree: 'مخالفت',
            proceedingPDF: '',
          }
        },
        components: {
            DropDown,
            InputText,
            DateInput,
            Radio,
            Confirm,
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
                    });
            },
            getProceedings(meetingId){
                if (meetingId != '0') {
                    axios({
                        method: 'get',
                        url: serverUrl+'api/proceedings/?meetingid='+meetingId,
                        headers: {"Content-Type": "application/json"},
                        })
                    .then(response => {
                        this.proceedingNameOptions = response.data;
                        this.employeesName(meetingId);

                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    });
                };
                this.meetingId = meetingId;
            },
            zinafLabel(stockholderType){
                    //let row = parseInt(event.currentTarget.getAttribute('row'));
                    if (stockholderType == this.daneshjou ){
                        return 'شماره دانشجویی';
                    }
                    else if (stockholderType == this.karkonan) {
                        return 'کد ملی';
                    }
                    else {
                        return 'ذینفع';
                    }
                },
            getResolutions(proceedingId){
                if (proceedingId != '0') {
                    this.getProceedingAPI(proceedingId);
                    axios({
                        method: 'get',
                        url: serverUrl+'api/resolutions/?proceedingid='+proceedingId,
                        headers: {"Content-Type": "application/json"},
                        })
                    .then(response => {
                        this.resolutions = [];
                        for (let res of response.data){
                            res.zinafLabel = this.zinafLabel(res.stockholder_type);
                            this.resolutions.push(res);
                        }
                        this.showForm = true;
                        this.proceedingId = proceedingId;
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
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
                });
            },
            async addResolutionAPI(event){
                let row = parseInt(event.currentTarget.getAttribute('row'));
                if (!this.resolutions[row].id){
                    axios.post(serverUrl+'api/resolutions/', {...this.resolutions[row]})
                        .then(response => {
                            this.showAlertFunc('تغییرات ذخیره شد.');
                        })
                        .catch(error => {
                            this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        });
                }
                else {
                    axios.put(serverUrl+'api/resolutions/'+this.resolutions[row].id+'/',{...this.resolutions[row]})
                        .then(response => {
                            this.showAlertFunc('تغییرات ذخیره شد.');
                        })
                        .catch(error => {
                            this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                        });   
                }
            },
            async resolveStockholder(row){
                //let row = parseInt(event.currentTarget.getAttribute('row'));
                let stockholderType = this.resolutions[row].stockholder_type;
                let zinaf = this.resolutions[row].zinaf;
                if ((stockholderType == '0') || (zinaf == '')){
                    this.resolutions[row].stockholder = 1;
                };
                try {
                    let sh = await axios.get(serverUrl+`api/resstockholder/?zinaf=${zinaf}&stockholder_type=${stockholderType}`);
                    this.resolutions[row].stockholder = sh.data.stockholder;
                    this.resolutions[row].fullname = sh.data.fullname;
                    this.resolutions[row].gender = sh.data.gender;
                } catch (error) {
                    //this.errorMessage = 'کارمند/دانشجوی مورد نظر پیدا نشد، نامشخص درنظر گرفته می‌شود.';
                    this.showAlertFunc('کارمند/دانشجوی مورد نظر پیدا نشد، نامشخص درنظر گرفته می‌شود.');
                    this.resolutions[row].stockholder = 1;
                }
            },

            getProceeding(newValue){
                if (newValue != '0'){
                    this.proceedingId = newValue;
                    this.getProceedingAPI(newValue);
                    this.showForm = true;
                }
                else {
                this.proceedingId = 0;
                this.showForm = false;
                }
            },
            downloadFile() {
                const link = document.createElement('a');
                link.href = this.proceedingPDF;
                link.setAttribute('download', 'proceeding.pdf');
                document.body.appendChild(link);
                link.click();
                link.remove();
            },
            printProceeding() {
                axios({
                    method: 'get',
                    url: serverUrl+`api/printproc/${this.proceedingId}/`,
                    headers: {"Content-Type": "application/json"},
                    responseType: 'blob',
                    })
                .then(response => {
                    const downloadUrl = window.URL.createObjectURL(new Blob([response.data]));
                    this.proceedingPDF = downloadUrl;
                    this.downloadFile()
                })
                .catch(error => {
                    this.errorMessage = error; //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                });
            },
            updateNo(newValue, row){
            this.resolutions[row].item_no = newValue; 
            },
            updateType(newValue, row){
            this.resolutions[row].resolution_type = newValue; 
            },
            updateShType(newValue, row){
                this.resolutions[row].stockholder_type = newValue;
                if (newValue == 'دانشجو'){
                    this.resolutions[row].zinafLabel = 'شماره دانشجویی';   
                }
                else if (newValue == 'کارکنان'){
                    this.resolutions[row].zinafLabel = 'کد ملی';
                }
                else {
                    this.resolutions[row].zinafLabel = 'ذینفع';
                }
            },
            updateSh(newValue, row){
            this.resolutions[row].zinaf = newValue; 
            },
            updateResult(newValue, row){
                this.resolutions[row].result = newValue;
            },
            updateResText(newValue, row){
                this.resolutions[row].act_text = newValue;
            },
            blankForm(){
                var resolutionObj = {
                    id: 0,
                    item_no: '',
                    act_text: '',
                    resolution_type: '0',
                    result: true,
                    proceeding: this.proceedingId,
                    stockholder_type: '0',
                    stockholder: '',
                    zinaf: '',
                    zinafLabel: 'ذینفع',
                    fullname: '',
                    gender: '',
                };
                this.resetMessages();
                return resolutionObj;
            },
            addResolution(){
                var resobj = this.blankForm();
                this.resolutions.push(resobj);
                this.manipulationMode = 0;
            },
            deleteResolution(event){
                let row = parseInt(event.currentTarget.getAttribute('row'));
                let resId = this.resolutions[row].id;
                if (resId != 0) {
                    axios.delete(serverUrl+`api/resolutions/${resId}/`)
                    .then(response => {
                        this.resolutions.splice(row, 1);
                    })
                    .catch(error => {
                        this.errorMessage = error //'خطایی در گرفتن اطلاعات کاربر رخ داد'; //error.data
                    });
                }
                else {
                    this.resolutions.splice(row, 1);
                }
            },
            genResolution(event){
                let pattern = parseInt(event.currentTarget.getAttribute('name'));
                let row = parseInt(event.currentTarget.getAttribute('row'));
                let zinaf = this.resolutions[row].zinaf;
                let fullname = this.resolutions[row].fullname;
                let result = this.resolutions[row].result ? this.Agree : this.Disagree;
                let resolution_type = this.resolutions[row].resolution_type > 0 ? this.resolutionTypeOptions[this.resolutions[row].resolution_type-1].text : ' ';
                let shtype = this.resolutions[row].stockholder_type == this.daneshjou ? 'شماره دانشجویی' : 'کد ملی';
                let title = '';
                let act_text = '';

                if (this.resolutions[row].gender == "M")
                    title = "آقای";
                else {
                    title = "خانم";
                }
                if (pattern == 1){
                    act_text = `با درخواست ${resolution_type} ${title} ${fullname} به ${shtype} ${zinaf} ${result} شد.`
                }
                this.resolutions[row].act_text = act_text;
            },
            showAlertFunc(message){
                this.message = message;
                this.showAlert = true;
                let delayInMilliseconds=2000;
                setTimeout(() => {
                    this.showAlert = false;
                }, delayInMilliseconds);
            },
            resultRes(res) {
                    return  res ? this.Agree : this.Disagree;
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
        <span class="block-inline text-lg hover:text-blue-500 p-2 border-2 bg-red-100"> مدیریت مصوبات </span>
        <div class="flex flex-col font-farsi items-stretch items-center">
            <div class="flex flex-col md:flex-row items-end">
                <DropDown class="mt-5 md:mt-10 mx-5 w-4/5 md:w-2/5" label_title="جلسات موجود"  @onChangeValue="getProceedings"
                    :options="meetingNamesOptions" v-model:itemSelected="meetingId"/>
                <DropDown v-if="meetingId != '0'" class="mt-3 md:mt-10 mx-5 w-4/5 md:w-2/5" label_title="صورتجلسات موجود"  @onChangeValue="getResolutions"
                    :options="proceedingNameOptions" :itemSelected="proceedingId"/>
            </div>
            <div v-if="showForm && meetingId != '0'">
                <div class="flex flex-row">
                    <span class="block-inline float-right text-green-800 text-lg hover:text-blue-500 p-2 mt-1"> مصوبات: </span>
                    <button class="block-inline flex items-center justify-right mt-2" title="چاپ صورتجلسه" 
                            @click="printProceeding">
                        <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/print.png"/>
                    </button>
                </div>
                <div class="border border-gray-500 mt-5 pb-5 mx-5" v-for="(member, i) in resolutions">
                    <form v-on:submit.prevent="">
                        <div class="flex flex-col justify-center md:flex-row md:gap-4 items-center">
                            <InputText  class="w-4/5 md:w-1/6" v-model:value="resolutions[i].item_no" :disabled="preadonly"
                                @onChangeValue="updateNo" label_title="شماره بند" input_placeholder="شماره بند" :row="i" />
                            <DropDown class="w-4/5 md:w-1/4" label_title="نوع مصوبه"  @onChangeValue="updateType"
                                :options="resolutionTypeOptions" :itemSelected="resolutions[i].resolution_type" :row="i" />
                            <DropDown class="w-4/5 md:w-1/6" label_title="نوع ذینفع"  @onChangeValue="updateShType"
                                :options="stockHolderOptions" :itemSelected="resolutions[i].stockholder_type" :row="i" />
                            <InputText class="w-4/5 md:w-1/4" :label_title="resolutions[i].zinafLabel"  @onChangeValue="updateSh"
                                 :value="resolutions[i].zinaf" @onBlur="resolveStockholder" :row="i" />
                            <!--Toggle :value="resolutions[i].result"  @onChangeValue="updateResult" class="w-5/6 md:w-1/12" 
                                    l2r label_title="نتیجه" :disabled="preadonly" :row="i" /-->
                            <Radio :pick="resultRes(resolutions[i].result)"  @onChangeValue="updateResult" class="w-5/6 md:w-1/12" 
                                    l2r label_title="نتیجه" :disabled="preadonly" :row="i" />
                        </div>
                        <div class="flex flex-col items-end">
                            <div class="flex flex-row w-full gap-2 justify-center mt-1">
                                <label class="pt-2 font-farsi text-sm text-green-700 dark:text-green-500">
                                    متن مصوبه
                                </label>
                                <button class="block-inline disabled:bg-gray-100" title="تولید متن مصوبه الگوی ۱" :row="i" name="1"
                                    :disabled="this.resolutions[i].resolution_type=='0' || this.resolutions[i].zinaf==''" @click="genResolution">
                                    <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/1-50.png"/>
                                </button>
                                <button class="block-inline disabled:bg-gray-100" title="تولید متن مصوبه الگوی ۲" :row="i" 
                                    :disabled="this.resolutions[i].resolution_type=='0' || this.resolutions[i].zinaf==''" @click="genResolution">
                                    <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/2-50.png"/>
                                </button>
                            </div>
                            <div class="flex flex-col md:flex-row w-full">
                                <InputText  class="md:w-11/12 mx-2" v-model:value="resolutions[i].act_text" :disabled="preadonly"
                                        @onChangeValue="updateResText" label_title="" input_placeholder="مقرر شد ..." :row="i" />
                                <div class="flex flex-row justify-center">
                                    <button class="block-inline disabled:bg-gray-100" title="بروزرسانی مصوبه" :row="i" 
                                    :disabled="this.resolutions[i].item_no=='' || this.resolutions[i].act_text=='' || this.preadonly"
                                        @click="addResolutionAPI">
                                        <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/ok.png"/>
                                    </button>
                                    <button class="block-inline disabled:bg-gray-100" title="حذف مصوبه" :row="i" :disabled="this.preadonly"
                                        @click="deleteResolution">
                                        <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/minus.png"/>
                                    </button>
                                </div>
                            </div>
                        </div>
                    </form>
                </div>
                <div class="flex justify-center">
                    <div  class="flex flex-col items-center justify-center md:w-1/4 text-black font-farsi text-sm font-bold px-4 py-3" role="alert">
                        <p v-if="showAlert" class="text-red-500"> {{ message }} </p>
                    </div>
                </div>
                <button class="block-inline disabled:bg-gray-100" title="اضافه کردن مصوبه" :disabled="this.preadonly"
                            @click="addResolution">
                    <img class="opacity-60 hover:bg-red-100 w-9 p-1" src="images/plus.png"/>
                </button>
            </div>
        </div>
    </div>
</template>

<style scoped>

</style>
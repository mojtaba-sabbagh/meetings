<script>
    import DatePicker from 'vue3-persian-datetime-picker';
    export default {
    props: {
        label_title: String,
        required: {
            type: Boolean,
            default: false,
        },
        accept_msg: {
            type: String,
            default: "",
        },
        reject_msg: {
            type: String,
            default: "",
        },
        l2r: {
            type: Boolean,
            default: false,
        },
        width_col: {
            type: String,
            default: "w-1",
        },
        order: {
            type: Number,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        value: "",
    },
    data() {
       return {
            date:'',
            hasError: false,
            entered : false,
        }
    },
    computed: {
    },
    methods: {
         constraint() {
            this.entered = true;
            if (this.required & this.date==""){
                this.hasError = true;
            } 
            else {
                this.hasError = false;
            }
            this.$emit('onChangeValue', this.date);
            this.$emit('onStateChange', this.hasError, this.order);
      },
    },
    components: {
        DatePicker,
    },
    created() {
        this.date = this.value;
    },
  }
</script>
<template>    
    <div class="float-right flex flex-col">
        <label for="input-success"
           class="font-farsi mb-2 text-sm"
           v-bind:class="{ 'text-green-700 dark:text-green-500': !hasError,
                       'text-red-700 dark:text-red-500' : hasError,
                        }">
           {{ label_title }}
            <p class="inline text-xl text-red-700 dark:text-red-500"><span v-if="required"> * </span></p>
        </label>
        <DatePicker v-model="date" @change="constraint" 
            :disabled="disabled" :required="required"
           class="font-farsi border text-sm rounded-lg p-1.5
           bg-white-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400"
           v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                           : !hasError & entered,
                            'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                           : hasError,
                           'ltr-grid': l2r}"/>

         <p v-bind:class="{ 'mt-2 text-right text-sm text-green-600 font-farsi dark:text-green-500'
                           : !hasError & entered,
                            'mt-2 text-right text-sm text-red-600 font-farsi dark:text-red-500'
                           : hasError}"> 
                           <span v-if="hasError" class="font-farsi"> <span v-if="required"> این فیلد الزامی است </span> {{ reject_msg }}</span>
                           </p>
    </div>
</template>
<style scoped>
.ltr-grid {
  direction: ltr;
}
</style>
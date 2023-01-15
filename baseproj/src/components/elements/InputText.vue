<script>
    export default {
    props: {
        label_title: String,
        input_placeholder: {
            type: String,
            default: "حمیدرضا"
        },
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
        is_number: {
            type: Boolean,
            default: false,
        },
        value: "",
        order: {
            type: Number,
        },
        disabled: {
            type: Boolean,
            default: false,
        },
        row: 0,
    },
    data() {
       return {
            hasError: false,
            entered : false,
            dataValue: this.value,
        }
    },
    computed: {
    },
    methods: {
        constraint() {
            this.dataValue = this.value;
            this.entered = true;
            if (this.required & this.dataValue==""){
                this.hasError = true;
            } 
            else {
                this.hasError = false;
            }
            if (this.is_number){
               this.dataValue = this.convert(this.dataValue);
            }
            this.$emit('onChangeValue', this.dataValue, this.row);
            this.$emit('onStateChange', this.hasError, this.order);
            this.$emit('onBlur', this.row);
      },
      onEnterFunc(){
        this.constraint();
        this.$emit('onEnterKey');
      },
       convert(str) {
       let
        persianNumbers = [/۰/g, /۱/g, /۲/g, /۳/g, /۴/g, /۵/g, /۶/g, /۷/g, /۸/g, /۹/g],
        arabicNumbers  = [/٠/g, /١/g, /٢/g, /٣/g, /٤/g, /٥/g, /٦/g, /٧/g, /٨/g, /٩/g];
        
        if (typeof str === 'string')
        {
            for(let i=0; i<10; i++)
            {
            str = str.replace(persianNumbers[i], i).replace(arabicNumbers[i], i);
            }
        }
        return str;
        },
    }
  }
</script>
<template>    
    <div class="flex flex-col">
        <label for="input-success"
           class="font-farsi mb-2 text-sm"
           v-bind:class="{ 'text-green-700 dark:text-green-500': !hasError,
                       'text-red-700 dark:text-red-500' : hasError,
                        }">
           {{ label_title }}
            <p class="inline text-xl text-red-700 dark:text-red-500"><span v-if="required"> * </span></p>
        </label>
        <input type="text" id="input-success" v-model="value" @blur="constraint" @keyup.enter="onEnterFunc"
            :disabled="disabled" :required="required"
           class="font-farsi border text-sm rounded-lg p-2.5
           bg-white-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400"
           v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                           : !hasError & entered,
                            'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                           : hasError,
                           'ltr-grid': l2r}"
           v-bind:placeholder="input_placeholder"
        />
    </div>
</template>
<style scoped>
.ltr-grid {
  direction: ltr;
}
</style>
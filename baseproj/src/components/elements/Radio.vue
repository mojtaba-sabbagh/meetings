<script>
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
            default: true,
        },
        width_col: {
            type: String,
            default: "w-1",
        },
        
        pick: "",
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
            dataValue: false,
            Agree: 'موافقت',
            Disagree: 'مخالفت',
        }
    },
    computed: {
        agreeOrDisagree(){
        if (this.pick == this.Agree){
            return true;
        }
        return false;
      },
    },
    methods: {
        constraint() {
            this.dataValue = this.pick == 'agree' ? true : false;
            this.entered = true;
            this.$emit('onChangeValue', this.dataValue, this.row);
            this.$emit('onStateChange', this.hasError, this.order);
      },
      onEnterFunc(){
        this.constraint();
        this.$emit('onEnterKey');
      },
    }
  }
</script>
<template>    
    <div class="flex flex-row md:flex-col gap-4 md:gap-1 items-center justify-right">
        <label for="input-success"
           class="font-farsi mb-2 text-sm"
           v-bind:class="{ 'text-green-700 dark:text-green-500': !hasError,
                       'text-red-700 dark:text-red-500' : hasError,
                        }">
           {{ label_title }}
            <p class="inline text-xl text-red-700 dark:text-red-500"><span v-if="required"> * </span></p>
        </label>
        <div>
            <div>
                <input v-if="!agreeOrDisagree" type="radio"  id="agree" value="agree" v-model="pick"
                    @change="constraint" @keyup.enter="onEnterFunc" :required="required" :disabled="disabled"
                    v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                        : !hasError & entered,
                        'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                        : hasError,
                        'ltr-grid': l2r}" />
                <input  v-if="agreeOrDisagree" type="radio"  id="agree" value="agree" v-model="pick" checked
                    @change="constraint" @keyup.enter="onEnterFunc" :required="required" :disabled="disabled"
                    v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                        : !hasError & entered,
                        'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                        : hasError,
                        'ltr-grid': l2r}" />
                <label class="mr-1" for="agree">موافقت</label>
            </div>
            <div>
                <input v-if="agreeOrDisagree" type="radio" id="disagree" value="disagree"  v-model="pick"
                    @change="constraint" @keyup.enter="onEnterFunc" :required="required" :disabled="disabled"
                    v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                        : !hasError & entered,
                        'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                        : hasError,
                        'ltr-grid': l2r}" />
                <input v-if="!agreeOrDisagree" type="radio" id="disagree" value="disagree"  v-model="pick" checked
                    @change="constraint" @keyup.enter="onEnterFunc" :required="required" :disabled="disabled"
                    v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                        : !hasError & entered,
                        'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                        : hasError,
                        'ltr-grid': l2r}" />
                <label class="mr-1" for="disagree">مخالفت</label>
            </div>
        </div>
    </div>
</template>
<style scoped>
.ltr-grid {
  direction: ltr;
}
</style>
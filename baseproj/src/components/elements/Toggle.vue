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
        
        value: false,
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
    <div class="flex flex-col items-center">
        <label for="input-success"
           class="font-farsi mb-2 text-sm"
           v-bind:class="{ 'text-green-700 dark:text-green-500': !hasError,
                       'text-red-700 dark:text-red-500' : hasError,
                        }">
           {{ label_title }}
            <p class="inline text-xl text-red-700 dark:text-red-500"><span v-if="required"> * </span></p>
        </label>
        <input type="checkbox" v-model="value"
            @change="constraint" @keyup.enter="onEnterFunc" :required="required" :disabled="disabled"
            v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                : !hasError & entered,
                'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                : hasError,
                'ltr-grid': l2r}" />
    </div>
</template>
<style scoped>
.ltr-grid {
  direction: ltr;
}
</style>
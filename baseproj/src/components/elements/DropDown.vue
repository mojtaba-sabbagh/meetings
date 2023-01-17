<script>
     export default {
        data() {
          return {
              hasError: false,
              entered : false,
            }
        },
        props: {
            label_title: String,
            options: {},
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
            itemSelected: '',
            order: {
                type: Number,
            },
            disabled: {
                type: Boolean,
                default: false,
            },
            row: 0,
        },
    methods: {
        constraint() {
            this.entered = true;
            if (this.required & this.itemSelected == ""){
                this.hasError = true;
            } 
            else {
                this.hasError = false;
            }
            this.$emit('onChangeValue', this.itemSelected, this.row);
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
    <div class="float-right flex flex-col">
        <label for="input-success"
           class="font-farsi mb-2 text-sm"
           v-bind:class="{ 'text-green-700 dark:text-green-500': !hasError,
                       'text-red-700 dark:text-red-500' : hasError,
                        }" >
           {{ label_title }} 
            <p class="inline text-xl text-red-700 dark:text-red-500"> <span v-if="required"> * </span> </p>
        </label>
        <select v-model="itemSelected" @change="constraint" :disabled="disabled" :required="required" @keyup.enter="onEnterFunc"
           class="form-select form-select-sm w-full
           appearance-none border text-sm text-center rounded-lg p-2.5
           bg-white-50 border-gray-500 text-gray-900 placeholder-gray-200 focus:ring-gray-500 focus:border-gray-500 dark:bg-gray-100 dark:border-gray-400"
           v-bind:class="{ 'bg-green-50 border-green-500 text-green-900 placeholder-green-200 focus:ring-green-500 focus:border-green-500 dark:bg-green-100 dark:border-green-400'
                           : !hasError & entered,
                            'bg-red-50 border-red-500 text-red-900 placeholder-red-200 focus:ring-red-500 focus:border-red-500 dark:bg-red-100 dark:border-red-400'
                           : hasError,
                           'ltr-grid': l2r}"
                            aria-label=".form-select-sm example">
             <option v-bind:value=0>
                انتخاب کنید
            </option>
            <option v-for="option in options" v-bind:value="option.ID" v-bind:key="option.ID" :selected="option.ID === itemSelected">
                {{ option.text }}
            </option>
        </select>
    </div>
</template>
<style scoped>
    .ltr-grid {
        direction: ltr;
    }
</style>
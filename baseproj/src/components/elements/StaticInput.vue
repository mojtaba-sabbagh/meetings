<script>
    export default {
        props: {
            label: String,
            fvalue: String,
            l2r: {
            type: Boolean,
            default: false,
        },
        }
    }
</script>
<template>
    <div class="pb-6 md:pb-0 flex flex-col">
        <label for="name" class="input-label text-slate-500 text-base mb-2">
            {{ label }}            
        </label>
        <label class="input-field inline-flex items-baseline border-none shadow-md bg-white p-2"
               v-bind:class="{'text-left': l2r}">
            <span class="flex-none w-full text-blue-500 hover:text-blue-600 
                         select-none leading-none text-sm">
                {{ fvalue }}
            </span>
        </label>
    </div>
</template>
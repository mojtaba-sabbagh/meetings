<script>
    export default {
        props: {
            submit_bttn: {
                type: String,
                default: "تایید"
                },

            return_bttn: {
                type: String,
                default: "بازگشت"
                },

        }

    }
</script>

<template>
    <div class="mt-10 grid grid-cols-4 gap-2 font-farsi">
            <button type="button" class="col-start-2 text-white bg-gradient-to-br from-purple-600 to-blue-500 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-blue-300 dark:focus:ring-blue-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2">{{ submit_bttn }}</button>
            <button type="button" class="text-white bg-gradient-to-br from-pink-500 to-orange-400 hover:bg-gradient-to-bl focus:ring-4 focus:outline-none focus:ring-pink-200 dark:focus:ring-pink-800 font-medium rounded-lg text-sm px-5 py-2.5 text-center mr-2 mb-2"> {{ return_bttn }} </button>
    </div>
</template>
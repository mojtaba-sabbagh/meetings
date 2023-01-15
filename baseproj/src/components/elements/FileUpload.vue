<template>
    <div class="file-upload">
      <div class="file-upload__area">
        <input type="file" name="" id="" @change="handleFileChange($event)"/>
        <div v-if="errors.length > 0">
          <div
            class="file-upload__error"
            v-for="(error, index) in errors"
            :key="index"
          >
            <span>{{ error }}</span>
          </div>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "FileUpload",
    props: {
        maxSize: {
            type: Number,
            default: 5,
            required: true,
        },
        accept: {
            type: String,
            default: "image/*",
        },
    },
    data () {
        return {
        isLoading: false,
        uploadReady: true,
        errors: [],
        file: {
            name: "",
            size: 0,
            type: "",
            fileExtention: "",
            url: "",
            isImage: false,
            isUploaded: false,
            },
        };
    },
    methods: {
        handleFileChange(e) {
            this.errors = [];
      // Check if file is selected
      if (e.target.files && e.target.files[0]) {
             // Check if file is valid
        if (this.isFileValid(e.target.files[0])) {
          // Get uploaded file
          const file = e.target.files[0],
            // Get file size
            fileSize = Math.round((file.size / 1024 / 1024) * 100) / 100,
            // Get file extension
            fileExtention = file.name.split(".").pop(),
            // Get file name
            fileName = file.name.split(".").shift(),
            // Check if file is an image
            isImage = ["jpg", "jpeg", "png", "gif"].includes(fileExtention);
          // Print to console
          console.log(fileSize, fileExtention, fileName, isImage);
        } else {
          console.log("Invalid file");
        }
        }
        },
    
    isFileSizeValid(fileSize) {
      if (fileSize <= this.maxSize) {
        console.log("File size is valid");
      } else {
          this.errors.push(`File size should be less than ${this.maxSize} MB`);
      }
    },
    isFileTypeValid(fileExtention) {
      if (this.accept == "*") {
        console.log("File type is valid");
      }
      if (this.accept.split(",").includes(fileExtention)) {
        console.log("File type is valid");
      } else {
        this.errors.push(`File type should be ${this.accept}`);
      }
    },
    isFileValid(file) {
      this.isFileSizeValid(Math.round((file.size / 1024 / 1024) * 100) / 100);
      this.isFileTypeValid(file.name.split(".").pop());
      if (this.errors.length === 0) {
        return true;
      } else {
        return false;
      }
    },
    },
  };
  </script>
  
  <style scoped>
  .file-upload {
    height: 100vh;
    width: 100%;
    display: flex;
    align-items: flex-start;
    justify-content: center;
  }
  .file-upload .file-upload__area {
    width: 600px;
    min-height: 200px;
    display: flex;
    align-items: center;
    justify-content: center;
    border: 2px dashed #ccc;
    margin-top: 40px;
  }
  </style>
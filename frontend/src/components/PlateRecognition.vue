<template>
  <div class="plate-recognition">
    <el-upload
      class="image-uploader"
      action="#"
      :auto-upload="false"
      :show-file-list="false"
      :on-change="handleImageChange"
      accept="image/jpeg,image/png,image/jpg">
      <img v-if="imageUrl" :src="imageUrl" class="preview-image" />
      <el-icon v-else class="image-uploader-icon"><Plus /></el-icon>
    </el-upload>
    <div class="recognition-controls">
      <el-button 
        type="primary" 
        @click="recognizePlate" 
        :loading="isRecognizing"
        :disabled="!selectedFile">
        识别车牌
      </el-button>
      <el-button @click="resetImage">重置</el-button>
    </div>
    <div v-if="recognitionResult" class="recognition-result">
      <h4>识别结果：</h4>
      <el-descriptions :column="1" border>
        <el-descriptions-item label="车牌号">
          {{ recognitionResult.plate_number }}
        </el-descriptions-item>
        <el-descriptions-item label="车牌颜色">
          {{ recognitionResult.plate_color }}
        </el-descriptions-item>
      </el-descriptions>
      <div class="use-result">
        <el-button type="success" size="small" @click="useRecognitionResult">
          使用此结果
        </el-button>
      </div>
    </div>
    <el-alert
      v-if="errorMessage"
      :title="errorMessage"
      type="error"
      show-icon
      @close="errorMessage = ''"
    />
  </div>
</template>

<script>
import { Plus } from '@element-plus/icons-vue'
import parkingApi from '@/api/parkingApi'

export default {
  name: 'PlateRecognition',
  components: {
    Plus
  },
  data() {
    return {
      selectedFile: null,
      imageUrl: '',
      isRecognizing: false,
      recognitionResult: null,
      errorMessage: ''
    }
  },
  methods: {
    handleImageChange(file) {
      this.selectedFile = file.raw;
      this.imageUrl = URL.createObjectURL(file.raw);
      this.recognitionResult = null;
      this.errorMessage = '';
    },
    async recognizePlate() {
      if (!this.selectedFile) {
        this.errorMessage = '请先选择图片';
        return;
      }
      this.isRecognizing = true;
      this.errorMessage = '';
      try {
        const result = await parkingApi.recognizePlate(this.selectedFile);
        if (result.success) {
          this.recognitionResult = result;
        } else {
          this.errorMessage = result.message || '识别失败';
        }
      } catch (error) {
        this.errorMessage = error.message || '识别请求失败';
      } finally {
        this.isRecognizing = false;
      }
    },
    resetImage() {
      this.selectedFile = null;
      this.imageUrl = '';
      this.recognitionResult = null;
      this.errorMessage = '';
    },
    useRecognitionResult() {
      if (this.recognitionResult) {
        this.$emit('result-selected', {
          plateNumber: this.recognitionResult.plate_number,
          plateColor: this.recognitionResult.plate_color
        });
      }
    }
  }
}
</script>

<style scoped>
.plate-recognition {
  margin: 20px 0;
}
.image-uploader {
  width: 178px;
  height: 178px;
  border: 1px dashed #d9d9d9;
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  margin-bottom: 15px;
}
.image-uploader:hover {
  border-color: #409EFF;
}
.image-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  line-height: 178px;
  text-align: center;
}
.preview-image {
  width: 178px;
  height: 178px;
  display: block;
}
.recognition-controls {
  margin: 15px 0;
}
.recognition-result {
  margin-top: 20px;
  padding: 15px;
  border: 1px solid #ebeef5;
  border-radius: 4px;
}
.use-result {
  margin-top: 10px;
  text-align: right;
}
</style>

<template>
  <div class="realtime-plate-recognition">
    <div class="video-container">
      <video ref="videoElement" class="camera-stream" autoplay></video>
      <canvas ref="canvasElement" style="display: none;"></canvas>
    </div>
    
    <div class="controls">
      <el-button type="primary" @click="toggleCamera" :disabled="isRecognizing">
        {{ isCameraActive ? '关闭摄像头' : '打开摄像头' }}
      </el-button>
      <el-button type="success" @click="toggleRecognition" :disabled="!isCameraActive">
        {{ isRecognizing ? '停止识别' : '开始识别' }}
      </el-button>
    </div>
    
    <div v-if="latestRecognition" class="recognition-result">
      <h3>实时识别结果</h3>
      <el-alert
        v-if="latestRecognition.action === 'entry'"
        title="车辆入场"
        type="success"
        :description="`车牌号: ${latestRecognition.plate_number}，颜色: ${latestRecognition.plate_color}`"
        show-icon
      />
      <el-alert
        v-if="latestRecognition.action === 'exit'"
        title="车辆出场"
        type="info"
        :description="`车牌号: ${latestRecognition.plate_number}，停车费: ${latestRecognition.action_result.fee_details?.total_fee || '计算中...'} 元`"
        show-icon
      />
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
import axios from 'axios';

export default {
  name: 'RealtimePlateRecognition',
  data() {
    return {
      isCameraActive: false,
      isRecognizing: false,
      stream: null,
      recognitionInterval: null,
      latestRecognition: null,
      errorMessage: '',
      recognitionFrameRate: 2, // 每秒识别次数
      API_URL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api'
    };
  },
  methods: {
    async toggleCamera() {
      if (this.isCameraActive) {
        this.stopCamera();
      } else {
        await this.startCamera();
      }
    },
    
    async startCamera() {
      try {
        const constraints = {
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        };
        
        this.stream = await navigator.mediaDevices.getUserMedia(constraints);
        this.$refs.videoElement.srcObject = this.stream;
        this.isCameraActive = true;
      } catch (error) {
        this.errorMessage = `无法访问摄像头: ${error.message}`;
        console.error('摄像头访问错误:', error);
      }
    },
    
    stopCamera() {
      this.stopRecognition();
      
      if (this.stream) {
        this.stream.getTracks().forEach(track => track.stop());
        this.stream = null;
      }
      
      this.$refs.videoElement.srcObject = null;
      this.isCameraActive = false;
    },
    
    toggleRecognition() {
      if (this.isRecognizing) {
        this.stopRecognition();
      } else {
        this.startRecognition();
      }
    },
    
    startRecognition() {
      if (!this.isCameraActive) return;
      
      this.isRecognizing = true;
      
      // 设置定时器定期捕获视频帧并发送给后端
      const frameInterval = 1000 / this.recognitionFrameRate;
      this.recognitionInterval = setInterval(() => {
        this.captureAndProcessFrame();
      }, frameInterval);
    },
    
    stopRecognition() {
      if (this.recognitionInterval) {
        clearInterval(this.recognitionInterval);
        this.recognitionInterval = null;
      }
      this.isRecognizing = false;
    },
    
    captureAndProcessFrame() {
      const video = this.$refs.videoElement;
      const canvas = this.$refs.canvasElement;
      const context = canvas.getContext('2d');
      
      // 设置canvas尺寸与视频匹配
      canvas.width = video.videoWidth;
      canvas.height = video.videoHeight;
      
      // 将视频帧绘制到canvas
      context.drawImage(video, 0, 0, canvas.width, canvas.height);
      
      // 将canvas转换为base64图像数据
      const frameData = canvas.toDataURL('image/jpeg', 0.8);
      
      // 发送到后端处理
      this.sendFrameToBackend(frameData);
    },
    
    async sendFrameToBackend(frameData) {
      try {
        const response = await axios.post(`${this.API_URL}/auto-parking/process-frame`, {
          frame_data: frameData
        });
        
        const data = response.data;
        
        // 处理识别结果
        if (data.success && data.action !== 'none') {
          this.latestRecognition = data;
          // 通知父组件
          this.$emit('recognition-result', data);
        }
      } catch (error) {
        console.error('发送帧数据错误:', error);
        // 不显示频繁的错误提示，以免界面刷新太快
        // 仅记录日志
      }
    }
  },
  beforeUnmount() {
    // 组件销毁前确保释放资源
    this.stopCamera();
  }
}
</script>

<style scoped>
.realtime-plate-recognition {
  display: flex;
  flex-direction: column;
  align-items: center;
  margin: 20px 0;
}

.video-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  margin-bottom: 15px;
  width: 640px;
  height: 480px;
  background-color: #f0f0f0;
}

.camera-stream {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.controls {
  display: flex;
  gap: 10px;
  margin-bottom: 15px;
}

.recognition-result {
  width: 100%;
  margin-top: 20px;
}
</style>

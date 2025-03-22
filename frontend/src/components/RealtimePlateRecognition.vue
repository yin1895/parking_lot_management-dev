<template>
  <div class="realtime-plate-recognition">
    <!-- 使用一个固定尺寸的容器减少布局计算 -->
    <div class="video-wrapper">
      <div class="video-container">
        <video ref="videoElement" class="camera-stream" autoplay></video>
        <canvas ref="canvasElement" style="display: none;"></canvas>
      </div>
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
import parkingApi from '@/api/parkingApi';
import { throttle } from 'lodash';

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
      API_URL: process.env.VUE_APP_API_URL || 'http://localhost:5000/api',
      processingFrame: false, // 添加帧处理状态标记
      successCount: 0, // 连续成功识别次数
      failureCount: 0, // 连续失败识别次数
      frameProcessQueue: [], // 添加帧处理队列
      isProcessingQueue: false, // 添加队列处理状态
    };
  },
  created() {
    // 使用节流函数包装sendFrameToBackend方法
    this.throttledSendFrame = throttle(this.sendFrameToBackend, 500);
    
    // 添加requestAnimationFrame优化
    this.rafId = null;
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
      // 首先检查摄像头支持
      const cameraSupport = parkingApi.checkCameraSupport();
      
      if (!cameraSupport.supported) {
        this.errorMessage = cameraSupport.message;
        console.error('摄像头支持问题:', cameraSupport.message);
        return;
      }
      
      try {
        const constraints = {
          video: {
            width: { ideal: 1280 },
            height: { ideal: 720 }
          }
        };
        
        // 确保mediaDevices存在并提供polyfill
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
          // 使用旧的API (摄像头支持检查已处理这种情况，但为了更健壮添加额外检查)
          const getUserMedia = navigator.getUserMedia ||
                            navigator.webkitGetUserMedia ||
                            navigator.mozGetUserMedia ||
                            navigator.msGetUserMedia;
                            
          if (getUserMedia) {
            // 使用回调形式的旧API
            getUserMedia.call(
              navigator, 
              constraints, 
              (stream) => {
                this.$refs.videoElement.srcObject = stream;
                this.stream = stream;
                this.isCameraActive = true;
              },
              (error) => {
                this.errorMessage = `无法访问摄像头: ${error.message || '未知错误'}`;
                console.error('摄像头访问错误:', error);
              }
            );
            return;
          } else {
            throw new Error('浏览器不支持摄像头访问');
          }
        }
        
        // 使用现代API
        this.stream = await navigator.mediaDevices.getUserMedia(constraints);
        this.$refs.videoElement.srcObject = this.stream;
        this.isCameraActive = true;
      } catch (error) {
        this.errorMessage = `无法访问摄像头: ${error.message || '未知错误'}`;
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
      this.successCount = 0;
      this.failureCount = 0;
      
      // 使用新方法启动定时捕获
      this.startIntervalCapture();
    },
    
    stopRecognition() {
      if (this.recognitionInterval) {
        clearInterval(this.recognitionInterval);
        this.recognitionInterval = null;
      }
      this.isRecognizing = false;
    },
    
    captureAndProcessFrame() {
      // 如果正在处理上一帧，则将当前帧添加到队列
      if (this.processingFrame) {
        // 限制队列长度，避免内存问题
        if (this.frameProcessQueue.length < 3) {
          this.queueFrame();
        }
        return;
      }
      
      const video = this.$refs.videoElement;
      if (!video || !video.videoWidth) return; // 避免视频元素未准备好
      
      const canvas = this.$refs.canvasElement;
      const context = canvas.getContext('2d');
      
      // 使用requestAnimationFrame优化渲染
      cancelAnimationFrame(this.rafId);
      this.rafId = requestAnimationFrame(() => {
        // 设置canvas尺寸与视频匹配
        canvas.width = video.videoWidth;
        canvas.height = video.videoHeight;
        
        // 将视频帧绘制到canvas
        context.drawImage(video, 0, 0, canvas.width, canvas.height);
        
        // 将canvas转换为base64图像数据
        const frameData = canvas.toDataURL('image/jpeg', 0.8);
        
        // 发送到后端处理 (使用节流后的方法)
        this.throttledSendFrame(frameData);
      });
    },
    
    // 添加队列帧方法
    queueFrame() {
      this.frameProcessQueue.push(Date.now());
      
      // 如果没有处理队列，开始处理
      if (!this.isProcessingQueue) {
        this.processFrameQueue();
      }
    },
    
    // 处理帧队列
    processFrameQueue() {
      if (this.frameProcessQueue.length === 0) {
        this.isProcessingQueue = false;
        return;
      }
      
      this.isProcessingQueue = true;
      this.frameProcessQueue.shift(); // 移除最旧的帧
      
      // 延迟处理下一帧
      setTimeout(() => {
        this.captureAndProcessFrame();
        this.processFrameQueue();
      }, 100);
    },
    
    async sendFrameToBackend(frameData) {
      // 标记正在处理帧
      this.processingFrame = true;
      
      try {
        // 使用parkingApi而不是直接使用axios
        const result = await parkingApi.processVideoFrame(frameData);
        const data = result;
        
        // 处理识别结果
        if (data.success) {
          if (data.action !== 'none') {
            this.latestRecognition = data;
            this.$emit('recognition-result', data);
            this.successCount++;
            this.failureCount = 0;
            
            // 如果连续成功3次以上，降低帧率节省资源
            if (this.successCount > 3 && this.recognitionFrameRate > 1) {
              clearInterval(this.recognitionInterval);
              this.recognitionFrameRate = 1; // 降低到每秒1帧
              this.startIntervalCapture();
            }
          }
        } else {
          this.failureCount++;
          this.successCount = 0;
          
          // 如果连续失败5次以上，恢复正常帧率
          if (this.failureCount > 5 && this.recognitionFrameRate < 2) {
            clearInterval(this.recognitionInterval);
            this.recognitionFrameRate = 2; // 恢复到每秒2帧
            this.startIntervalCapture();
          }
        }
      } catch (error) {
        console.error('发送帧数据错误:', error);
        this.failureCount++;
      } finally {
        // 处理完成，重置状态
        this.processingFrame = false;
      }
    },
    
    // 新增方法用于启动定时捕获
    startIntervalCapture() {
      const frameInterval = 1000 / this.recognitionFrameRate;
      this.recognitionInterval = setInterval(() => {
        this.captureAndProcessFrame();
      }, frameInterval);
    },
    
    // 组件销毁前清理资源
    beforeUnmount() {
      this.stopCamera();
      if (this.rafId) {
        cancelAnimationFrame(this.rafId);
      }
    }
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

/* 添加固定包装器减少布局变化 */
.video-wrapper {
  width: 100%;
  max-width: 640px;
  position: relative;
  margin-bottom: 15px;
}

.video-container {
  border: 1px solid #dcdfe6;
  border-radius: 4px;
  overflow: hidden;
  width: 100%;
  height: 0;
  padding-bottom: 75%; /* 4:3 比例 */
  position: relative;
  background-color: #f0f0f0;
}

.camera-stream {
  position: absolute;
  top: 0;
  left: 0;
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

/* 添加媒体查询，优化小屏幕显示 */
@media (max-width: 768px) {
  .video-wrapper {
    max-width: 100%;
  }
  
  .controls {
    flex-direction: column;
    width: 100%;
  }
  
  .controls button {
    width: 100%;
    margin-bottom: 10px;
  }
}
</style>

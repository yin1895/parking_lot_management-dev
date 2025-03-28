<template>
  <div class="home">
    <h2>欢迎使用停车场管理系统</h2>
    
    <!-- 添加refreshTrigger属性来触发仪表盘更新 -->
    <Dashboard ref="dashboard" :refreshTrigger="dashboardRefreshTrigger" @load-complete="handleDashboardLoaded" />
    
    <el-row :gutter="20">
      <el-col :span="8">
        <el-card>
          <h3>车辆入场</h3>
          <el-button type="primary" @click="showEntryDialog">入场登记</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <h3>车辆出场</h3>
          <el-button type="success" @click="showExitDialog">出场结算</el-button>
        </el-card>
      </el-col>
      <el-col :span="8">
        <el-card>
          <h3>系统管理</h3>
          <el-button type="info" @click="goToManagement">进入管理</el-button>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 添加实时监控卡片 -->
    <el-row style="margin-top: 20px">
      <el-col :span="24">
        <el-card>
          <h3>实时车牌监控</h3>
          <el-button type="warning" @click="showRealtimeDialog">启动实时监控</el-button>
        </el-card>
      </el-col>
    </el-row>
    
    <!-- 入场对话框 -->
    <el-dialog title="车辆入场" v-model="entryDialogVisible" width="500px">
      <el-tabs v-model="entryActiveTab">
        <el-tab-pane label="手动输入" name="manual">
          <el-form :model="entryForm" label-width="80px">
            <el-form-item label="车牌号">
              <el-input v-model="entryForm.plateNumber" placeholder="请输入车牌号"></el-input>
            </el-form-item>
            <el-form-item label="车牌颜色">
              <el-select v-model="entryForm.plateColor" placeholder="请选择">
                <el-option label="蓝色" value="蓝色"></el-option>
                <el-option label="黄色" value="黄色"></el-option>
                <el-option label="绿色" value="绿色"></el-option>
                <el-option label="黑色" value="黑色"></el-option>
                <el-option label="白色" value="白色"></el-option>
              </el-select>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="AI识别" name="recognition">
          <plate-recognition @result-selected="handleRecognitionResult" />
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="entryDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleVehicleEntry">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 出场对话框 -->
    <el-dialog title="车辆出场" v-model="exitDialogVisible" width="500px">
      <el-tabs v-model="exitActiveTab">
        <el-tab-pane label="手动输入" name="manual">
          <el-form :model="exitForm" label-width="80px">
            <el-form-item label="车牌号">
              <el-input v-model="exitForm.plateNumber" placeholder="请输入车牌号"></el-input>
            </el-form-item>
          </el-form>
        </el-tab-pane>
        <el-tab-pane label="AI识别" name="recognition">
          <plate-recognition @result-selected="handleExitRecognitionResult" />
        </el-tab-pane>
      </el-tabs>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="exitDialogVisible = false">取消</el-button>
          <el-button type="primary" @click="handleVehicleExit">确定</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 实时监控对话框 -->
    <el-dialog title="实时车牌监控" v-model="realtimeDialogVisible" width="700px" @closed="stopRealtimeMonitoring">
      <realtime-plate-recognition 
        @recognition-result="handleRealtimeRecognition" 
        ref="realtimeRecognition" />
    </el-dialog>
  </div>
</template>

<script>
import parkingApi from '../api/parkingApi';
import { ElMessage } from 'element-plus';
import PlateRecognition from '../components/PlateRecognition.vue';
import RealtimePlateRecognition from '../components/RealtimePlateRecognition.vue';
import Dashboard from '../components/Dashboard.vue'; // 导入仪表盘组件

export default {
  name: 'HomeView',
  components: {
    PlateRecognition,
    RealtimePlateRecognition,
    Dashboard // 注册仪表盘组件
  },
  data() {
    return {
      entryDialogVisible: false,
      exitDialogVisible: false,
      realtimeDialogVisible: false,
      entryActiveTab: 'manual',
      exitActiveTab: 'manual',
      entryForm: {
        plateNumber: '',
        plateColor: '蓝色'
      },
      exitForm: {
        plateNumber: ''
      },
      dashboardRefreshTrigger: 0, // 用于触发仪表盘刷新的计数器
      isOperationInProgress: false, // 操作状态标志
    };
  },
  methods: {
    // 处理仪表盘加载完成事件
    handleDashboardLoaded(success) {
      console.log('仪表盘加载状态:', success ? '成功' : '失败');
    },
    
    // 触发仪表盘强制刷新
    triggerDashboardRefresh() {
      this.dashboardRefreshTrigger += 1;
      console.log('触发仪表盘刷新, 计数:', this.dashboardRefreshTrigger);
    },
    
    showEntryDialog() {
      this.entryDialogVisible = true;
    },
    
    showExitDialog() {
      this.exitDialogVisible = true;
    },
    
    goToManagement() {
      this.$router.push('/management');
    },
    
    async handleVehicleEntry() {
      if (this.isOperationInProgress) return;
      this.isOperationInProgress = true;
      
      try {
        if (!this.entryForm.plateNumber) {
          ElMessage.error('请输入车牌号');
          this.isOperationInProgress = false;
          return;
        }
        
        const result = await parkingApi.recordEntry(this.entryForm.plateNumber, this.entryForm.plateColor);
        
        if (result.success) {
          ElMessage.success(result.message);
          this.entryDialogVisible = false;
          
          // 延迟200ms后刷新仪表盘，确保后端数据已更新
          setTimeout(() => {
            this.triggerDashboardRefresh();
            this.isOperationInProgress = false;
          }, 200);
        } else {
          ElMessage.error(result.message || '入场登记失败');
          this.isOperationInProgress = false;
        }
      } catch (error) {
        ElMessage.error('入场登记失败: ' + error.message);
        this.isOperationInProgress = false;
      }
    },
    
    async handleVehicleExit() {
      if (this.isOperationInProgress) return;
      this.isOperationInProgress = true;
      
      try {
        if (!this.exitForm.plateNumber) {
          ElMessage.error('请输入车牌号');
          this.isOperationInProgress = false;
          return;
        }
        
        const result = await parkingApi.recordExit(this.exitForm.plateNumber);
        
        if (result.success) {
          ElMessage.success(result.message);
          this.exitDialogVisible = false;
          
          // 延迟200ms后刷新仪表盘，确保后端数据已更新
          setTimeout(() => {
            this.triggerDashboardRefresh();
            this.isOperationInProgress = false;
          }, 200);
        } else {
          ElMessage.error(result.message || '出场结算失败');
          this.isOperationInProgress = false;
        }
      } catch (error) {
        ElMessage.error('出场结算失败: ' + error.message);
        this.isOperationInProgress = false;
      }
    },
    
    handleRecognitionResult(result) {
      this.entryForm.plateNumber = result.plateNumber;
      this.entryForm.plateColor = result.plateColor;
      this.entryActiveTab = 'manual';
    },
    
    handleExitRecognitionResult(result) {
      this.exitForm.plateNumber = result.plateNumber;
      this.exitActiveTab = 'manual';
    },
    
    showRealtimeDialog() {
      this.realtimeDialogVisible = true;
    },
    
    stopRealtimeMonitoring() {
      if (this.$refs.realtimeRecognition) {
        this.$refs.realtimeRecognition.stopCamera();
      }
    },
    
    handleRealtimeRecognition(result) {
      if (result.action === 'entry') {
        ElMessage.success(`车辆 ${result.plate_number} 已成功入场`);
        // 延迟200ms后刷新仪表盘
        setTimeout(() => this.triggerDashboardRefresh(), 200);
      } else if (result.action === 'exit') {
        const fee = result.action_result.fee_details?.total_fee || '计算中';
        ElMessage.success(`车辆 ${result.plate_number} 已成功出场，停车费: ${fee} 元`);
        // 延迟200ms后刷新仪表盘
        setTimeout(() => this.triggerDashboardRefresh(), 200);
      }
    }
  }
};
</script>

<style scoped>
.home {
  padding: 20px;
}
.el-card {
  margin-bottom: 20px;
  height: 200px;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.el-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 15px rgba(0,0,0,0.1);
}

.dialog-footer {
  display: flex;
  justify-content: flex-end;
}
</style>

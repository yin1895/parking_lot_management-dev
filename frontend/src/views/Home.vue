<template>
  <div class="home">
    <h2 class="home-heading">总览</h2>

    <Dashboard ref="dashboard" :refreshTrigger="dashboardRefreshTrigger" @load-complete="handleDashboardLoaded" />

    <div class="action-grid">
      <div class="action-block" @click="showEntryDialog">
        <span class="action-number">01</span>
        <div class="action-body">
          <span class="action-title">车辆入场</span>
          <span class="action-link">登记 &rarr;</span>
        </div>
      </div>
      <div class="action-divider"></div>
      <div class="action-block" @click="showExitDialog">
        <span class="action-number">02</span>
        <div class="action-body">
          <span class="action-title">车辆出场</span>
          <span class="action-link">结算 &rarr;</span>
        </div>
      </div>
      <div class="action-divider"></div>
      <div class="action-block" @click="goToManagement">
        <span class="action-number">03</span>
        <div class="action-body">
          <span class="action-title">系统管理</span>
          <span class="action-link">进入 &rarr;</span>
        </div>
      </div>
    </div>

    <div class="monitoring-area" @click="showRealtimeDialog">
      <span class="action-title">实时车牌监控</span>
      <span class="action-link">启动 &rarr;</span>
    </div>

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
import Dashboard from '../components/Dashboard.vue';

export default {
  name: 'HomeView',
  components: {
    PlateRecognition,
    RealtimePlateRecognition,
    Dashboard
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
      dashboardRefreshTrigger: 0,
      isOperationInProgress: false,
    };
  },
  methods: {
    handleDashboardLoaded(success) {
      console.log('仪表盘加载状态:', success ? '成功' : '失败');
    },
    triggerDashboardRefresh() {
      this.dashboardRefreshTrigger += 1;
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
          setTimeout(() => { this.triggerDashboardRefresh(); this.isOperationInProgress = false; }, 200);
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
          setTimeout(() => { this.triggerDashboardRefresh(); this.isOperationInProgress = false; }, 200);
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
        setTimeout(() => this.triggerDashboardRefresh(), 200);
      } else if (result.action === 'exit') {
        const fee = result.action_result.fee_details?.total_fee || '计算中';
        ElMessage.success(`车辆 ${result.plate_number} 已成功出场，停车费: ${fee} 元`);
        setTimeout(() => this.triggerDashboardRefresh(), 200);
      }
    }
  }
};
</script>

<style scoped>
.home {
  padding: 0;
  max-width: 1040px;
  margin: 0 auto;
}

.home-heading {
  font-family: var(--font-family-inter);
  font-weight: 700;
  font-size: 22px;
  letter-spacing: 0.02em;
  text-align: left;
  margin: 0 0 12px 0;
  color: var(--el-text-color-primary);
  text-transform: uppercase;
}

/* magazine action grid */
.action-grid {
  display: grid;
  grid-template-columns: 1fr auto 1fr auto 1fr;
  align-items: stretch;
  gap: 0;
  margin-bottom: 32px;
  position: relative;
}

.action-grid::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(196, 136, 60, 0.2) 15%, rgba(196, 136, 60, 0.2) 50%, rgba(196, 136, 60, 0.08) 85%, transparent 100%);
}

.action-grid::after {
  content: "";
  position: absolute;
  bottom: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(196, 136, 60, 0.2) 15%, rgba(196, 136, 60, 0.2) 50%, rgba(196, 136, 60, 0.08) 85%, transparent 100%);
}

.action-block {
  display: flex;
  align-items: center;
  gap: 20px;
  padding: 20px 24px;
  cursor: pointer;
  transition: all 250ms ease;
  position: relative;
  z-index: 1;
}

.action-block:hover {
  background: rgba(196, 136, 60, 0.04);
}

.action-block::after {
  content: "";
  position: absolute;
  inset: 0;
  opacity: 0;
  transition: opacity 250ms ease;
  background: linear-gradient(135deg, rgba(196, 136, 60, 0.06) 0%, transparent 50%);
  z-index: -1;
}

.action-block:hover::after {
  opacity: 1;
}

.action-number {
  font-family: var(--font-family-mono);
  font-size: 20px;
  font-weight: 600;
  color: var(--el-color-primary);
  line-height: 1;
  letter-spacing: 0.04em;
  text-shadow: 0 0 8px rgba(196, 136, 60, 0.15);
}

.action-body {
  display: flex;
  flex-direction: column;
  align-items: flex-start;
  gap: 2px;
}

.action-title {
  font-family: var(--font-family-inter);
  font-size: 14px;
  font-weight: 600;
  color: var(--el-text-color-primary);
  letter-spacing: 0.01em;
}

.action-link {
  font-family: var(--font-family-inter);
  font-size: 11px;
  letter-spacing: 0.04em;
  color: var(--el-text-color-placeholder);
  transition: all 200ms ease;
}

.action-block:hover .action-link {
  color: var(--el-color-primary);
  text-shadow: 0 0 6px rgba(196, 136, 60, 0.25);
}

.action-divider {
  width: 1px;
  background: linear-gradient(180deg, transparent 0%, rgba(196, 136, 60, 0.15) 20%, rgba(196, 136, 60, 0.15) 80%, transparent 100%);
  align-self: stretch;
}

/* monitoring area */
.monitoring-area {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 20px 24px;
  margin-bottom: 24px;
  cursor: pointer;
  border: 1px solid rgba(255, 255, 255, 0.06);
  border-top: 1px solid rgba(255, 255, 255, 0.1);
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.03) 0%,
    rgba(255,255,255,0.008) 30%,
    rgba(0,0,0,0.01) 50%,
    rgba(0,0,0,0.04) 100%
  );
  backdrop-filter: blur(24px);
  -webkit-backdrop-filter: blur(24px);
  box-shadow: 0 8px 32px rgba(0,0,0,0.2), inset 0 1px 0 rgba(255,255,255,0.04);
  transition: all 250ms ease;
}

.monitoring-area:hover {
  border-color: rgba(196, 136, 60, 0.2);
  border-top-color: rgba(196, 136, 60, 0.25);
  background: linear-gradient(
    135deg,
    rgba(255,255,255,0.04) 0%,
    rgba(255,255,255,0.01) 30%,
    rgba(0,0,0,0.01) 50%,
    rgba(0,0,0,0.04) 100%
  );
  box-shadow: 0 12px 48px rgba(0,0,0,0.3), inset 0 1px 0 rgba(255,255,255,0.04), 0 0 20px rgba(196,136,60,0.06);
}

.monitoring-area .action-link {
  font-size: 12px;
}

.monitoring-area:hover .action-link {
  color: var(--el-color-primary);
  text-shadow: 0 0 6px rgba(196, 136, 60, 0.25);
}

.monitoring-area:hover {
  background: var(--el-fill-color);
}

.monitoring-area .action-title {
  font-size: 14px;
}

.monitoring-area .action-link {
  font-size: 12px;
}

.monitoring-area:hover .action-link {
  color: var(--el-color-primary);
}

/* dialog footer */
.dialog-footer {
  display: flex;
  justify-content: flex-end;
}

/* responsive */
@media (max-width: 768px) {
  .action-grid {
    grid-template-columns: 1fr;
    border-top: none;
  }

  .action-divider {
    width: 100%;
    height: 1px;
  }

  .action-block {
    padding: 16px 8px;
  }
}

@keyframes pulse-glow {
  0%, 100% { box-shadow: 0 0 0 0 rgba(196, 136, 60, 0); }
  50% { box-shadow: 0 0 20px 2px rgba(196, 136, 60, 0.06); }
}

@keyframes grid-scroll {
  0% { transform: translate(0, 0); }
  100% { transform: translate(48px, 48px); }
}

</style>

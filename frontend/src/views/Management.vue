<template>
  <div class="management">
    <h2>系统管理</h2>
    <el-tabs v-model="activeTab">
      <el-tab-pane label="停车场状态" name="status">
        <div class="status-container" v-if="parkingStatus">
          <el-row :gutter="20">
            <el-col :span="8">
              <el-card>
                <h3>总车位</h3>
                <div class="status-value">{{ parkingStatus.total_spaces }}</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <h3>已占用</h3>
                <div class="status-value">{{ parkingStatus.occupied_spaces }}</div>
              </el-card>
            </el-col>
            <el-col :span="8">
              <el-card>
                <h3>可用车位</h3>
                <div class="status-value">{{ parkingStatus.available_spaces }}</div>
              </el-card>
            </el-col>
          </el-row>
          <div class="refresh-button">
            <el-button type="primary" @click="loadParkingStatus">刷新数据</el-button>
          </div>
        </div>
        <div v-else class="loading">
          <el-button type="primary" @click="loadParkingStatus">加载数据</el-button>
        </div>
      </el-tab-pane>
    </el-tabs>
  </div>
</template>

<script>
import parkingApi from '../api/parkingApi';
import { ElMessage } from 'element-plus';

export default {
  name: 'ManagementView',
  data() {
    return {
      activeTab: 'status',
      parkingStatus: null
    }
  },
  mounted() {
    this.loadParkingStatus();
  },
  methods: {
    async loadParkingStatus() {
      try {
        const result = await parkingApi.getParkingStatus();
        if (result.success) {
          this.parkingStatus = result;
        } else {
          ElMessage.error('获取停车场状态失败: ' + result.message);
        }
      } catch (error) {
        console.error('获取停车场状态失败:', error);
        ElMessage.error('获取停车场状态失败: ' + error.message);
      }
    }
  }
}
</script>

<style scoped>
.management {
  padding: 20px;
}
.status-container {
  margin-top: 20px;
}
.status-value {
  font-size: 24px;
  font-weight: bold;
  margin-top: 10px;
}
.refresh-button {
  margin-top: 20px;
  text-align: right;
}
.loading {
  text-align: center;
  margin: 20px;
}
</style>

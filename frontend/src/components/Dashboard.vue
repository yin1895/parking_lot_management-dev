<template>
  <div class="dashboard">
    <!-- 确保容器尺寸稳定 -->
    <div class="dashboard-container">
      <el-row :gutter="20">
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <h3>当前车位</h3>
              </div>
            </template>
            <div class="stat-value">
              {{ parkingStatus ? parkingStatus.available_spaces : '加载中...' }}
              <small>可用</small>
            </div>
            <el-progress 
              :percentage="parkingStatus ? Math.round((parkingStatus.occupied_spaces / parkingStatus.total_spaces) * 100) : 0"
              :format="() => ''" 
              :color="getOccupancyColor"
            />
            <div class="stat-label">
              共 {{ parkingStatus ? parkingStatus.total_spaces : '-' }} 个车位，
              已用 {{ parkingStatus ? parkingStatus.occupied_spaces : '-' }} 个
            </div>
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <h3>今日入场</h3>
              </div>
            </template>
            <div class="stat-value">
              {{ todayStats.entries || 0 }}
              <small>车辆</small>
            </div>
            <el-progress 
              :percentage="Math.min(100, (todayStats.entries / 50) * 100)" 
              :format="() => ''" 
              color="#67C23A"
            />
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <h3>今日出场</h3>
              </div>
            </template>
            <div class="stat-value">
              {{ todayStats.exits || 0 }}
              <small>车辆</small>
            </div>
            <el-progress 
              :percentage="Math.min(100, (todayStats.exits / 50) * 100)" 
              :format="() => ''" 
              color="#E6A23C"
            />
          </el-card>
        </el-col>
        
        <el-col :span="6">
          <el-card shadow="hover" class="stat-card">
            <template #header>
              <div class="card-header">
                <h3>今日收入</h3>
              </div>
            </template>
            <div class="stat-value">
              {{ todayStats.income.toFixed(2) }}
              <small>元</small>
            </div>
            <el-progress 
              :percentage="Math.min(100, (todayStats.income / 1000) * 100)" 
              :format="() => ''" 
              color="#409EFF"
            />
          </el-card>
        </el-col>
      </el-row>
    </div>
    
    <!-- 刷新按钮 -->
    <div class="refresh-action">
      <el-button 
        type="primary" 
        size="small" 
        :icon="Refresh"
        :loading="isLoading" 
        @click="loadData"
      >
        刷新数据
      </el-button>
      <span class="last-update" v-if="lastUpdate">
        上次更新: {{ lastUpdate }}
      </span>
    </div>
  </div>
</template>

<script>
import { ref, onMounted, computed, watch } from 'vue'
import parkingApi from '@/api/parkingApi'
import { ElMessage } from 'element-plus'
import { Refresh } from '@element-plus/icons-vue'

export default {
  name: 'DashboardComponent',
  components: {
    Refresh
  },
  props: {
    // 添加prop允许父组件触发刷新
    refreshTrigger: {
      type: Number,
      default: 0
    }
  },
  emits: ['load-complete'],
  setup(props, { emit }) {
    const parkingStatus = ref(null)
    const todayStats = ref({
      entries: 0,
      exits: 0,
      income: 0,
      timestamp: 0
    })
    const isLoading = ref(false)
    const lastUpdate = ref('')
    const loadError = ref(false)
    
    // 添加数据版本监控，确保只显示最新数据
    const dataTimestamp = ref(0)
    
    const getOccupancyColor = computed(() => {
      if (!parkingStatus.value) return '#409EFF'
      
      const rate = parkingStatus.value.occupied_spaces / parkingStatus.value.total_spaces
      if (rate < 0.7) return '#67C23A'  // 绿色 - 宽松
      if (rate < 0.9) return '#E6A23C'  // 橙色 - 繁忙
      return '#F56C6C'  // 红色 - 几乎满了
    })
    
    const formatDateTime = () => {
      const now = new Date()
      return now.toLocaleTimeString()
    }
    
    const loadData = async (forceFresh = false) => {
      if (isLoading.value && !forceFresh) return
      
      isLoading.value = true
      loadError.value = false
      
      try {
        // 加载停车场状态
        const statusRes = await parkingApi.getParkingStatus()
        if (statusRes.success) {
          parkingStatus.value = statusRes
        } else {
          console.warn('获取停车场状态失败:', statusRes.message)
        }
        
        // 加载今日统计数据（从后端API获取）
        const statsRes = await parkingApi.getTodayStats()
        if (statsRes.success) {
          // 检查是否是更新的数据
          if (!statsRes.stats.timestamp || statsRes.stats.timestamp >= dataTimestamp.value) {
            // 更新数据时间戳
            dataTimestamp.value = statsRes.stats.timestamp || Date.now()
            
            // 更新统计数据
            todayStats.value = {
              entries: typeof statsRes.stats.entries === 'number' ? statsRes.stats.entries : 0,
              exits: typeof statsRes.stats.exits === 'number' ? statsRes.stats.exits : 0,
              income: typeof statsRes.stats.income === 'number' ? statsRes.stats.income : 0,
              timestamp: dataTimestamp.value
            }
            
            console.log('仪表盘数据已更新:', todayStats.value)
          } else {
            console.warn('收到过期的统计数据，忽略更新')
          }
        } else {
          console.error('获取统计数据失败:', statsRes.message)
          loadError.value = true
        }
        
        lastUpdate.value = formatDateTime()
      } catch (error) {
        console.error('加载数据失败:', error)
        ElMessage.error('加载数据失败: ' + (error.message || '未知错误'))
        loadError.value = true
      } finally {
        isLoading.value = false
        emit('load-complete', !loadError.value)
      }
    }
    
    // 监听父组件的刷新触发
    watch(() => props.refreshTrigger, () => {
      console.log('收到刷新触发信号，重新加载数据')
      loadData(true)
    })
    
    // 建立定时刷新
    let refreshInterval = null
    
    onMounted(() => {
      loadData()
      
      // 每30秒自动刷新一次数据
      refreshInterval = setInterval(() => {
        loadData()
      }, 30000)
    })
    
    // 组件卸载时清除定时器
    const beforeUnmount = () => {
      if (refreshInterval) {
        clearInterval(refreshInterval)
      }
    }
    
    return {
      parkingStatus,
      todayStats,
      isLoading,
      lastUpdate,
      getOccupancyColor,
      loadData,
      Refresh,
      beforeUnmount
    }
  }
}
</script>

<style scoped>
.dashboard {
  margin-bottom: 30px;
}

/* 添加固定尺寸容器减少布局计算 */
.dashboard-container {
  min-height: 200px;
  position: relative;
}

/* 确保卡片有固定高度，减少大小变化 */
.stat-card {
  height: 180px;
  transition: transform 0.3s;
  will-change: transform;
}

/* 使用transform替代可能触发布局重计算的属性 */
.stat-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 10px 20px rgba(0,0,0,0.1);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.stat-value {
  font-size: 28px;
  font-weight: bold;
  margin: 10px 0;
}

.stat-value small {
  font-size: 14px;
  font-weight: normal;
  opacity: 0.7;
  margin-left: 5px;
}

.stat-label {
  font-size: 12px;
  color: #909399;
  margin-top: 8px;
}

.refresh-action {
  display: flex;
  justify-content: flex-end;
  align-items: center;
  margin-top: 15px;
}

.last-update {
  margin-left: 10px;
  font-size: 12px;
  color: #909399;
}

/* 适配暗色主题 */
[data-theme="dark"] .stat-card {
  background-color: var(--card-bg);
  border-color: var(--border-color);
}

[data-theme="dark"] .stat-label {
  color: #b0b3b8;
}

[data-theme="dark"] .last-update {
  color: #b0b3b8;
}

/* 添加响应式适配，减少动态尺寸变化 */
@media (max-width: 768px) {
  .el-row {
    margin-left: 0 !important;
    margin-right: 0 !important;
  }
  
  .el-col {
    padding-left: 5px !important;
    padding-right: 5px !important;
  }
  
  .stat-card {
    height: auto;
    min-height: 150px;
    margin-bottom: 10px;
  }
}
</style>

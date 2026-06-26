<template>
  <div class="dashboard">
    <div class="stats-grid">
      <div class="stat-block" v-for="(stat, idx) in stats" :key="idx">
        <span class="stat-label">{{ stat.label }}</span>
        <span class="stat-value">{{ stat.value }}</span>
        <div class="stat-bar">
          <div class="stat-bar-fill" :style="{ width: stat.percent + '%' }"></div>
        </div>
        <span class="stat-footnote">{{ stat.footnote }}</span>
      </div>
    </div>

    <div class="dashboard-actions">
      <button class="text-link" @click="loadData" :disabled="isLoading">
        {{ isLoading ? '刷新中...' : '刷新数据' }}
      </button>
      <span class="last-update" v-if="lastUpdate">上次更新: {{ lastUpdate }}</span>
    </div>
  </div>
</template>

<script>
import { ref, computed, watch, onMounted, onBeforeUnmount } from 'vue'
import parkingApi from '@/api/parkingApi'
import { throttle } from '@/utils/debounce'

export default {
  name: 'DashboardComponent',
  props: {
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
    const dataTimestamp = ref(0)

    const getOccupancyRate = computed(() => {
      if (!parkingStatus.value) return 0
      return (parkingStatus.value.occupied_spaces / parkingStatus.value.total_spaces) * 100
    })

    const stats = computed(() => [
      { label: '当前车位', value: parkingStatus.value ? `${parkingStatus.value.available_spaces} / ${parkingStatus.value.total_spaces}` : '---', percent: parkingStatus.value ? getOccupancyRate.value : 0, footnote: `已用 ${parkingStatus.value ? parkingStatus.value.occupied_spaces : '-'} 个` },
      { label: '今日入场', value: String(todayStats.value.entries || 0), percent: Math.min(100, (todayStats.value.entries / 50) * 100), footnote: '辆' },
      { label: '今日出场', value: String(todayStats.value.exits || 0), percent: Math.min(100, (todayStats.value.exits / 50) * 100), footnote: '辆' },
      { label: '今日收入', value: `¥${(todayStats.value.income || 0).toFixed(2)}`, percent: Math.min(100, (todayStats.value.income / 1000) * 100), footnote: '元' }
    ])

    const loadData = async () => {
      if (isLoading.value) return
      isLoading.value = true

      try {
        const statusRes = await parkingApi.getParkingStatus()
        if (statusRes.success) parkingStatus.value = statusRes

        const statsRes = await parkingApi.getTodayStats()
        if (statsRes.success && statsRes.stats) {
          const ts = statsRes.stats.timestamp || Date.now()
          if (ts >= dataTimestamp.value) {
            dataTimestamp.value = ts
            todayStats.value = {
              entries: typeof statsRes.stats.entries === 'number' ? statsRes.stats.entries : 0,
              exits: typeof statsRes.stats.exits === 'number' ? statsRes.stats.exits : 0,
              income: typeof statsRes.stats.income === 'number' ? statsRes.stats.income : 0,
              timestamp: ts
            }
          }
        }
        lastUpdate.value = new Date().toLocaleTimeString()
      } catch (e) {
        console.error(e)
      } finally {
        isLoading.value = false
        emit('load-complete', true)
      }
    }

    const throttledLoad = throttle(loadData, 5000, true)

    watch(() => props.refreshTrigger, () => throttledLoad(true))

    let interval
    onMounted(() => {
      throttledLoad()
      interval = setInterval(() => throttledLoad(), 30000)
    })
    onBeforeUnmount(() => { if (interval) clearInterval(interval) })

    return { stats, isLoading, lastUpdate, loadData: throttledLoad }
  }
}
</script>

<style scoped>
.dashboard {
  margin-bottom: 40px;
}

/* magazine-style stat grid */
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 48px;
  padding: 36px 0;
  position: relative;
}

.stats-grid::after {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 1px;
  background: linear-gradient(90deg, transparent 0%, rgba(196, 136, 60, 0.25) 15%, rgba(196, 136, 60, 0.25) 50%, rgba(196, 136, 60, 0.1) 85%, transparent 100%);
}

.stat-block {
  text-align: left;
  display: flex;
  flex-direction: column;
  gap: 6px;
  padding-top: 28px;
  position: relative;
}

.stat-block::before {
  content: "";
  position: absolute;
  top: 0;
  left: 0;
  width: 28px;
  height: 2px;
  background: var(--el-color-primary);
  box-shadow: 0 0 10px rgba(196, 136, 60, 0.4);
}

.stat-label {
  font-size: 10px;
  font-family: var(--font-family-inter);
  font-weight: 500;
  letter-spacing: 0.12em;
  text-transform: uppercase;
  color: var(--el-text-color-secondary);
}

.stat-value {
  font-family: var(--font-family-mono);
  font-weight: 700;
  font-size: 40px;
  letter-spacing: -0.04em;
  color: var(--el-color-primary);
  line-height: 1.05;
  text-shadow: 0 0 20px rgba(196, 136, 60, 0.12);
}

.stat-bar {
  height: 2px;
  background: rgba(255, 255, 255, 0.06);
  margin: 8px 0 2px;
  width: 100%;
}

.stat-bar-fill {
  height: 100%;
  background: var(--el-color-primary);
  box-shadow: 0 0 6px rgba(196, 136, 60, 0.3);
  transition: width 600ms cubic-bezier(0.22, 1, 0.36, 1);
}

.stat-footnote {
  font-size: 11px;
  color: var(--el-text-color-placeholder);
}

/* actions row */
.dashboard-actions {
  display: flex;
  align-items: center;
  justify-content: flex-end;
  gap: 12px;
  margin-top: 8px;
}

.text-link {
  background: none;
  border: none;
  padding: 0;
  font-family: var(--font-family-inter);
  font-size: 13px;
  color: var(--el-text-color-secondary);
  cursor: pointer;
  transition: color 150ms ease;
}

.text-link:hover {
  color: var(--el-color-primary);
  text-shadow: 0 0 8px rgba(196, 136, 60, 0.3);
}

.text-link:disabled {
  opacity: 0.5;
  cursor: default;
}

.last-update {
  font-size: 12px;
  color: var(--el-text-color-placeholder);
}

/* responsive */
@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
    gap: 32px;
  }

  .stat-value {
    font-size: 24px;
  }
}
</style>

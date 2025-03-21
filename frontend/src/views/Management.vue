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
      
      <!-- 新增会员管理选项卡 -->
      <el-tab-pane label="会员管理" name="members">
        <div class="tip-container" v-if="!memberListLoaded">
          <el-button type="primary" @click="loadMemberList">加载会员列表</el-button>
        </div>
        <div v-else>
          <div class="member-tools">
            <el-button type="primary" @click="showAddMemberForm">添加新会员</el-button>
            <el-input
              v-model="memberSearchQuery"
              placeholder="搜索会员车牌号"
              style="width: 200px"
              clearable
              @clear="filterMembers"
              @input="filterMembers"
            ></el-input>
          </div>
          
          <el-table :data="filteredMembers" style="width: 100%" v-loading="loadingMembers">
            <el-table-column prop="name" label="姓名" />
            <el-table-column prop="plate_number" label="车牌号" />
            <el-table-column prop="phone" label="联系电话" />
            <el-table-column prop="status" label="状态">
              <template #default="{ row }">
                <el-tag :type="row.status === 'active' ? 'success' : 'danger'">
                  {{ row.status === 'active' ? '正常' : '停用' }}
                </el-tag>
              </template>
            </el-table-column>
            <el-table-column label="操作" width="200">
              <template #default="{ row }">
                <el-button size="small" @click="editMember(row)">编辑</el-button>
                <el-button size="small" type="danger" @click="confirmDeleteMember(row)">删除</el-button>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </el-tab-pane>
      
      <!-- 新增停车记录选项卡 -->
      <el-tab-pane label="停车记录" name="records">
        <div class="tip-container" v-if="!recordsLoaded">
          <el-button type="primary" @click="loadParkingRecords">加载停车记录</el-button>
        </div>
        <div v-else>
          <div class="record-tools">
            <el-form :inline="true" class="record-filter-form">
              <el-form-item label="车牌号">
                <el-input v-model="recordsFilter.plate_number" placeholder="搜索车牌号" />
              </el-form-item>
              <el-form-item label="日期范围">
                <el-date-picker
                  v-model="recordsDateRange"
                  type="daterange"
                  range-separator="至"
                  start-placeholder="开始日期"
                  end-placeholder="结束日期"
                  value-format="YYYY-MM-DD"
                />
              </el-form-item>
              <el-form-item>
                <el-button type="primary" @click="searchRecords">搜索</el-button>
                <el-button @click="resetRecordsFilter">重置</el-button>
              </el-form-item>
            </el-form>
          </div>
          
          <el-table :data="parkingRecords" style="width: 100%" v-loading="loadingRecords">
            <el-table-column prop="plate_number" label="车牌号" />
            <el-table-column prop="entry_time" label="入场时间" />
            <el-table-column prop="exit_time" label="出场时间">
              <template #default="{ row }">
                {{ row.exit_time || '尚未出场' }}
              </template>
            </el-table-column>
            <el-table-column prop="parking_fee" label="停车费">
              <template #default="{ row }">
                {{ row.parking_fee ? `¥${row.parking_fee}` : '计费中' }}
              </template>
            </el-table-column>
            <el-table-column label="操作" width="120">
              <template #default="{ row }">
                <el-button size="small" @click="viewRecordDetail(row)">详情</el-button>
              </template>
            </el-table-column>
          </el-table>
          
          <div class="pagination-container">
            <el-pagination
              background
              layout="prev, pager, next"
              :total="recordsTotalCount"
              :page-size="recordsPageSize"
              :current-page="recordsCurrentPage"
              @current-change="onRecordsPageChange"
            />
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>
    
    <!-- 会员编辑对话框 -->
    <el-dialog 
      :title="editingMember.id ? '编辑会员' : '添加会员'" 
      v-model="memberFormVisible"
      width="500px"
    >
      <el-form :model="editingMember" label-width="100px" :rules="memberFormRules" ref="memberFormRef">
        <el-form-item label="姓名" prop="name">
          <el-input v-model="editingMember.name" placeholder="请输入会员姓名"></el-input>
        </el-form-item>
        <el-form-item label="车牌号" prop="plate_number">
          <el-input v-model="editingMember.plate_number" placeholder="请输入车牌号"></el-input>
        </el-form-item>
        <el-form-item label="联系电话" prop="phone">
          <el-input v-model="editingMember.phone" placeholder="请输入联系电话"></el-input>
        </el-form-item>
        <el-form-item label="状态" prop="status">
          <el-select v-model="editingMember.status" placeholder="请选择状态">
            <el-option label="正常" value="active"></el-option>
            <el-option label="停用" value="inactive"></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <template #footer>
        <span class="dialog-footer">
          <el-button @click="memberFormVisible = false">取消</el-button>
          <el-button type="primary" @click="saveMember" :loading="savingMember">保存</el-button>
        </span>
      </template>
    </el-dialog>
    
    <!-- 停车记录详情对话框 -->
    <el-dialog 
      title="停车记录详情" 
      v-model="recordDetailVisible"
      width="600px"
    >
      <div v-if="selectedRecord" class="record-detail">
        <el-descriptions :column="2" border>
          <el-descriptions-item label="车牌号">{{ selectedRecord.plate_number }}</el-descriptions-item>
          <el-descriptions-item label="车牌颜色">{{ selectedRecord.plate_color }}</el-descriptions-item>
          <el-descriptions-item label="入场时间">{{ selectedRecord.entry_time }}</el-descriptions-item>
          <el-descriptions-item label="出场时间">{{ selectedRecord.exit_time || '尚未出场' }}</el-descriptions-item>
          <el-descriptions-item label="停车费用">{{ selectedRecord.parking_fee ? `¥${selectedRecord.parking_fee}` : '计费中' }}</el-descriptions-item>
          <el-descriptions-item label="记录ID">{{ selectedRecord.id }}</el-descriptions-item>
        </el-descriptions>
      </div>
    </el-dialog>
  </div>
</template>

<script>
import parkingApi from '../api/parkingApi';
import { ElMessage, ElMessageBox } from 'element-plus';

export default {
  name: 'ManagementView',
  data() {
    return {
      activeTab: 'status',
      parkingStatus: null,
      
      // 会员管理数据
      members: [],
      filteredMembers: [],
      memberListLoaded: false,
      loadingMembers: false,
      memberSearchQuery: '',
      memberFormVisible: false,
      editingMember: {
        id: null,
        name: '',
        plate_number: '',
        phone: '',
        status: 'active'
      },
      memberFormRules: {
        name: [{ required: true, message: '请输入会员姓名', trigger: 'blur' }],
        plate_number: [{ required: true, message: '请输入车牌号', trigger: 'blur' }]
      },
      savingMember: false,
      
      // 停车记录数据
      parkingRecords: [],
      recordsLoaded: false,
      loadingRecords: false,
      recordsTotalCount: 0,
      recordsPageSize: 10,
      recordsCurrentPage: 1,
      recordsFilter: {
        plate_number: '',
        start_date: '',
        end_date: ''
      },
      recordsDateRange: [],
      recordDetailVisible: false,
      selectedRecord: null
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
    },
    
    // 会员管理方法
    async loadMemberList() {
      this.loadingMembers = true;
      try {
        const result = await parkingApi.getMembers();
        if (result.success) {
          this.members = result.members || [];
          this.filteredMembers = [...this.members];
          this.memberListLoaded = true;
        } else {
          ElMessage.error('获取会员列表失败: ' + result.message);
        }
      } catch (error) {
        ElMessage.error('获取会员列表失败: ' + error.message);
      } finally {
        this.loadingMembers = false;
      }
    },
    
    filterMembers() {
      if (!this.memberSearchQuery) {
        this.filteredMembers = [...this.members];
        return;
      }
      
      const query = this.memberSearchQuery.toLowerCase();
      this.filteredMembers = this.members.filter(member => 
        member.plate_number.toLowerCase().includes(query) || 
        member.name.toLowerCase().includes(query)
      );
    },
    
    showAddMemberForm() {
      this.editingMember = {
        id: null,
        name: '',
        plate_number: '',
        phone: '',
        status: 'active'
      };
      this.memberFormVisible = true;
    },
    
    editMember(member) {
      this.editingMember = { ...member };
      this.memberFormVisible = true;
    },
    
    async saveMember() {
      this.savingMember = true;
      try {
        let result;
        if (this.editingMember.id) {
          // 更新现有会员
          result = await parkingApi.updateMember(this.editingMember.id, this.editingMember);
        } else {
          // 创建新会员
          result = await parkingApi.createMember(this.editingMember);
        }
        
        if (result.success) {
          ElMessage.success(result.message || '会员信息保存成功');
          this.memberFormVisible = false;
          // 刷新会员列表
          await this.loadMemberList();
        } else {
          ElMessage.error(result.message || '保存失败');
        }
      } catch (error) {
        ElMessage.error('保存会员信息失败: ' + error.message);
      } finally {
        this.savingMember = false;
      }
    },
    
    confirmDeleteMember(member) {
      ElMessageBox.confirm(
        `确定要删除会员 ${member.name} (${member.plate_number}) 吗?`,
        '删除确认',
        {
          confirmButtonText: '确定',
          cancelButtonText: '取消',
          type: 'warning'
        }
      ).then(async () => {
        try {
          const result = await parkingApi.deleteMember(member.id);
          if (result.success) {
            ElMessage.success('会员已删除');
            // 刷新会员列表
            await this.loadMemberList();
          } else {
            ElMessage.error(result.message || '删除失败');
          }
        } catch (error) {
          ElMessage.error('删除会员失败: ' + error.message);
        }
      }).catch(() => {
        // 用户取消删除操作
      });
    },
    
    // 停车记录管理方法
    async loadParkingRecords() {
      this.loadingRecords = true;
      try {
        const params = {
          skip: (this.recordsCurrentPage - 1) * this.recordsPageSize,
          limit: this.recordsPageSize,
          ...this.recordsFilter
        };
        
        const result = await parkingApi.getParkingRecords(params);
        if (result.success) {
          this.parkingRecords = result.records || [];
          this.recordsTotalCount = result.total || 0;
          this.recordsLoaded = true;
        } else {
          ElMessage.error('获取停车记录失败: ' + result.message);
        }
      } catch (error) {
        ElMessage.error('获取停车记录失败: ' + error.message);
      } finally {
        this.loadingRecords = false;
      }
    },
    
    onRecordsPageChange(page) {
      this.recordsCurrentPage = page;
      this.loadParkingRecords();
    },
    
    searchRecords() {
      // 处理日期范围
      if (this.recordsDateRange && this.recordsDateRange.length === 2) {
        this.recordsFilter.start_date = this.recordsDateRange[0];
        this.recordsFilter.end_date = this.recordsDateRange[1];
      } else {
        this.recordsFilter.start_date = '';
        this.recordsFilter.end_date = '';
      }
      
      this.recordsCurrentPage = 1; // 重置到第一页
      this.loadParkingRecords();
    },
    
    resetRecordsFilter() {
      this.recordsFilter = {
        plate_number: '',
        start_date: '',
        end_date: ''
      };
      this.recordsDateRange = [];
      this.recordsCurrentPage = 1;
      this.loadParkingRecords();
    },
    
    async viewRecordDetail(record) {
      try {
        // 如果需要更详细的记录信息，可以加载详情
        const result = await parkingApi.getRecordById(record.id);
        if (result.success) {
          this.selectedRecord = result.record;
        } else {
          this.selectedRecord = record; // 使用表格中的数据
        }
        this.recordDetailVisible = true;
      } catch (error) {
        ElMessage.error('获取记录详情失败: ' + error.message);
        // 使用表格中的基本数据
        this.selectedRecord = record;
        this.recordDetailVisible = true;
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
.loading, .tip-container {
  text-align: center;
  margin: 20px;
  padding: 30px;
  background: #f8f8f8;
  border-radius: 4px;
}
.member-tools, .record-tools {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.record-filter-form {
  width: 100%;
}
.pagination-container {
  margin-top: 20px;
  text-align: center;
}
.record-detail {
  padding: 10px 0;
}
</style>

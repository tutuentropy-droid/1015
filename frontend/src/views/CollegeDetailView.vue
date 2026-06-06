<template>
  <div class="page-container">
    <div v-if="volunteerStore.loading.detail" class="empty-tip">
      <el-skeleton :rows="10" animated />
    </div>
    <template v-else-if="volunteerStore.collegeDetail">
      <el-page-header @back="$router.back()" class="back-header">
        <template #content>
          <span class="page-title">院校详情</span>
        </template>
      </el-page-header>

      <div class="section-card">
        <div class="detail-header">
          <div>
            <h1 class="college-title">{{ volunteerStore.collegeDetail.name }}</h1>
            <div class="college-submeta">
              <span>{{ volunteerStore.collegeDetail.province }} · {{ volunteerStore.collegeDetail.city }}</span>
              <el-tag type="primary" effect="plain" style="margin-left: 12px">
                {{ volunteerStore.collegeDetail.level }}
              </el-tag>
              <el-tag type="success" effect="plain" style="margin-left: 6px">
                {{ volunteerStore.collegeDetail.college_type }}
              </el-tag>
            </div>
            <div class="tag-group" style="margin-top: 12px">
              <el-tag
                v-for="(t, i) in volunteerStore.collegeDetail.tags"
                :key="i"
                type="info"
                effect="light"
                style="margin-right: 8px; margin-bottom: 4px"
              >
                {{ t }}
              </el-tag>
            </div>
            <p class="college-desc">{{ volunteerStore.collegeDetail.description }}</p>
          </div>
        </div>
      </div>

      <div class="section-card">
        <h2 class="section-title">开设专业</h2>
        <el-row :gutter="12">
          <el-col
            v-for="m in volunteerStore.collegeDetail.majors"
            :key="m.id"
            :xs="24"
            :sm="12"
            :md="8"
          >
            <div class="major-card">
              <div class="major-name">
                <span style="color:#409eff">📖</span>
                <span>{{ m.name }}</span>
              </div>
              <div class="major-info">
                <span class="major-label">选科要求：</span>
                <span>{{ m.subject_requirements.length ? m.subject_requirements.join('、') : '不限' }}</span>
              </div>
              <div class="major-info">
                <span class="major-label">就业方向：</span>
                <span>{{ m.employment_direction?.slice(0, 2).join('、') }}</span>
              </div>
              <div class="major-info">
                <span class="major-label">典型岗位：</span>
                <span>{{ m.typical_positions?.slice(0, 2).join('、') }}</span>
              </div>
            </div>
          </el-col>
        </el-row>
      </div>

      <div class="section-card">
        <h2 class="section-title">近年各省录取数据</h2>
        <el-table :data="admissionDataList" stripe max-height="500">
          <el-table-column prop="year" label="年份" width="80" sortable />
          <el-table-column prop="province" label="省份" width="100" />
          <el-table-column prop="score" label="最低分" width="100" sortable />
          <el-table-column prop="rank" label="最低位次" width="120" sortable />
          <el-table-column prop="batch" label="批次" width="120" />
          <el-table-column prop="subject_combination" label="选科" min-width="160" />
        </el-table>
      </div>
    </template>
    <div v-else class="empty-tip">
      <el-empty description="未找到院校信息" />
    </div>
  </div>
</template>

<script setup>
import { computed, onMounted, watch } from 'vue'
import { useRoute } from 'vue-router'
import { useVolunteerStore } from '../stores/volunteer'

const route = useRoute()
const volunteerStore = useVolunteerStore()

const admissionDataList = computed(
  () => volunteerStore.collegeDetail?.admission_data || []
)

onMounted(async () => {
  await volunteerStore.loadMeta()
  volunteerStore.fetchCollegeDetail(route.params.id)
})

watch(
  () => route.params.id,
  (id) => {
    if (id) volunteerStore.fetchCollegeDetail(id)
  }
)
</script>

<style scoped>
.back-header {
  margin-bottom: 16px;
  padding: 10px 16px;
  background: #fff;
  border-radius: 8px;
}

.page-title {
  font-size: 18px;
  font-weight: 600;
}

.detail-header {
  padding: 8px 0;
}

.college-title {
  font-size: 28px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 10px 0;
}

.college-submeta {
  font-size: 15px;
  color: #475569;
}

.college-desc {
  margin-top: 16px;
  font-size: 14px;
  color: #64748b;
  line-height: 1.8;
}

.tag-group {
  display: flex;
  flex-wrap: wrap;
}

.major-card {
  padding: 14px 16px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 12px;
  border-left: 3px solid #409eff;
}

.major-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  display: flex;
  align-items: center;
  gap: 6px;
  margin-bottom: 8px;
}

.major-info {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
  line-height: 1.6;
}

.major-label {
  color: #94a3b8;
}
</style>

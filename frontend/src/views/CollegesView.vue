<template>
  <div class="page-container">
    <div class="section-card">
      <h2 class="section-title">院校查询</h2>
      <el-form :inline="true" :model="filters" size="default">
        <el-form-item label="省份">
          <el-select v-model="filters.province" clearable placeholder="全部" style="width: 140px">
            <el-option
              v-for="p in volunteerStore.provinces"
              :key="p"
              :label="p"
              :value="p"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="城市">
          <el-select v-model="filters.city" clearable filterable placeholder="全部" style="width: 140px">
            <el-option
              v-for="c in volunteerStore.cities"
              :key="c"
              :label="c"
              :value="c"
            />
          </el-select>
        </el-form-item>
        <el-form-item label="关键字">
          <el-input v-model="filters.keyword" clearable placeholder="院校名称/标签" style="width: 180px" />
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="doSearch">
            <el-icon><Search /></el-icon>搜索
          </el-button>
          <el-button @click="resetFilters">重置</el-button>
        </el-form-item>
      </el-form>
    </div>

    <div class="section-card">
      <div v-if="volunteerStore.loading.colleges" class="empty-tip">
        <el-skeleton :rows="6" animated />
      </div>
      <div v-else-if="!volunteerStore.collegeList.length" class="empty-tip">
        <el-empty description="未找到院校，请尝试其他条件" />
      </div>
      <el-table v-else :data="volunteerStore.collegeList" stripe style="width: 100%">
        <el-table-column prop="name" label="院校名称" min-width="200">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="goDetail(row.id)">
              {{ row.name }}
            </el-button>
          </template>
        </el-table-column>
        <el-table-column prop="province" label="省份" width="90" />
        <el-table-column prop="city" label="城市" width="90" />
        <el-table-column prop="level" label="层次" width="120">
          <template #default="{ row }">
            <el-tag type="primary" effect="plain" size="small">{{ row.level }}</el-tag>
          </template>
        </el-table-column>
        <el-table-column prop="college_type" label="类型" width="100" />
        <el-table-column label="标签" min-width="240">
          <template #default="{ row }">
            <el-tag
              v-for="(t, i) in (row.tags || []).slice(0, 4)"
              :key="i"
              type="info"
              effect="plain"
              size="small"
              style="margin-right: 4px; margin-bottom: 4px"
            >
              {{ t }}
            </el-tag>
          </template>
        </el-table-column>
        <el-table-column label="专业数" width="80" align="center">
          <template #default="{ row }">{{ row.majors?.length || 0 }}</template>
        </el-table-column>
        <el-table-column label="操作" width="200" align="center" fixed="right">
          <template #default="{ row }">
            <el-button type="primary" link size="small" @click="goDetail(row.id)">
              查看详情
            </el-button>
            <el-button
              :type="volunteerStore.isInCompare(row.id) ? 'success' : 'warning'"
              link
              size="small"
              @click="handleToggleCompare(row)"
            >
              {{ volunteerStore.isInCompare(row.id) ? '已加入' : '加入对比' }}
            </el-button>
          </template>
        </el-table-column>
      </el-table>
    </div>
  </div>
</template>

<script setup>
import { reactive, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useVolunteerStore } from '../stores/volunteer'

const router = useRouter()
const volunteerStore = useVolunteerStore()

const filters = reactive({
  province: '',
  city: '',
  keyword: '',
  level: '',
  college_type: '',
})

onMounted(() => {
  volunteerStore.loadMeta()
  doSearch()
})

async function doSearch() {
  await volunteerStore.fetchColleges({ ...filters, limit: 200 })
}

function resetFilters() {
  filters.province = ''
  filters.city = ''
  filters.keyword = ''
  doSearch()
}

function goDetail(id) {
  router.push(`/colleges/${id}`)
}

function handleToggleCompare(college) {
  const res = volunteerStore.toggleCompare(college)
  const msg = res.message || (res.added === false ? '已移除对比' : '操作成功')
  if (res.success === false) {
    ElMessage.warning(msg)
  } else {
    ElMessage.success(msg)
  }
}
</script>

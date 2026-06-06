<template>
  <div class="page-container">
    <el-page-header @back="$router.back()" class="back-header">
      <template #content>
        <span class="page-title">院校对比</span>
        <span class="compare-count">({{ volunteerStore.compareCount }}/{{ volunteerStore.maxCompare }})</span>
      </template>
    </el-page-header>

    <div v-if="!volunteerStore.compareList.length" class="section-card">
      <el-empty description="对比列表为空，去院校列表选择院校加入对比吧">
        <el-button type="primary" @click="$router.push('/colleges')">去选择院校</el-button>
      </el-empty>
    </div>

    <template v-else>
      <div class="section-card">
        <div class="compare-toolbar">
          <el-button type="danger" plain @click="handleClearAll">清空对比</el-button>
          <div class="toolbar-tip">
            <el-tag type="info" effect="plain">
              💡 高亮显示各维度最优项
            </el-tag>
          </div>
        </div>
      </div>

      <div class="section-card">
        <div class="compare-table-wrap">
          <el-table :data="compareRows" border stripe style="width: 100%">
            <el-table-column
              v-for="(college, idx) in volunteerStore.compareList"
              :key="college.id"
              :label="college.name"
              min-width="200"
              align="center"
            >
              <template #header>
                <div class="college-header">
                  <div class="college-name-cell">{{ college.name }}</div>
                  <el-button
                    type="danger"
                    link
                    size="small"
                    @click="handleRemove(college.id)"
                  >
                    移除
                  </el-button>
                </div>
              </template>
              <template #default="{ row }">
                <div v-if="row.field === 'basic_info'" class="basic-info-cell">
                  <div class="info-row">
                    <el-tag type="primary" effect="plain" size="small">
                      {{ college.level }}
                    </el-tag>
                  </div>
                  <div class="info-row">
                    <el-tag type="success" effect="plain" size="small">
                      {{ college.college_type }}
                    </el-tag>
                  </div>
                  <div class="info-row tags-row">
                    <el-tag
                      v-for="(t, i) in (college.tags || []).slice(0, 3)"
                      :key="i"
                      type="info"
                      effect="light"
                      size="small"
                      style="margin: 2px"
                    >
                      {{ t }}
                    </el-tag>
                  </div>
                </div>
                <div v-else-if="row.field === 'location'" class="location-cell">
                  <span class="loc-icon">📍</span>
                  <span>{{ college.province }} · {{ college.city }}</span>
                </div>
                <div v-else-if="row.field === 'admission_score'" class="score-cell">
                  <div
                    class="score-value"
                    :class="{ highlight: isBest(idx, 'admission_score', true) }"
                  >
                    {{ getLatestScore(college) }} 分
                  </div>
                  <div class="score-sub">最低位次：{{ getLatestRank(college) }}</div>
                </div>
                <div v-else-if="row.field === 'major_strength'" class="major-cell">
                  <div class="major-strength-bar">
                    <div
                      class="strength-inner"
                      :style="{ width: getMajorStrengthWidth(college) + '%' }"
                      :class="{ highlight: isBest(idx, 'major_strength', false) }"
                    ></div>
                  </div>
                  <div class="strength-score" :class="{ highlight: isBest(idx, 'major_strength', false) }">
                    {{ getMajorStrengthScore(college) }}
                  </div>
                  <div class="major-list">
                    <el-tag
                      v-for="(m, i) in (college.majors || []).slice(0, 4)"
                      :key="i"
                      :type="getDisciplineTagType(m.discipline_level)"
                      effect="light"
                      size="small"
                      style="margin: 2px"
                    >
                      {{ m.name }} ({{ m.discipline_level || '-' }})
                    </el-tag>
                  </div>
                </div>
                <div v-else-if="row.field === 'employment_rate'" class="rate-cell">
                  <div
                    class="rate-value"
                    :class="{ highlight: isBest(idx, 'employment_rate', false) }"
                  >
                    {{ (college.employment_rate * 100).toFixed(1) }}%
                  </div>
                  <el-progress
                    :percentage="college.employment_rate * 100"
                    :stroke-width="8"
                    :show-text="false"
                    :color="getRateColor(college.employment_rate)"
                  />
                </div>
                <div v-else-if="row.field === 'average_salary'" class="salary-cell">
                  <div
                    class="salary-value"
                    :class="{ highlight: isBest(idx, 'average_salary', false) }"
                  >
                    ¥{{ formatSalary(college.average_salary) }}
                  </div>
                  <div class="salary-sub">平均年薪</div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <div class="section-card">
        <h2 class="section-title">📚 专业详细对比</h2>
        <div class="majors-compare-wrap">
          <el-table :data="allMajors" border stripe>
            <el-table-column prop="name" label="专业名称" min-width="160" fixed="left" />
            <el-table-column
              v-for="college in volunteerStore.compareList"
              :key="college.id"
              :label="college.name"
              min-width="140"
              align="center"
            >
              <template #default="{ row }">
                <template v-if="getMajorByCollege(college, row.name)">
                  <el-tag
                    :type="getDisciplineTagType(getMajorByCollege(college, row.name).discipline_level)"
                    effect="light"
                  >
                    {{ getMajorByCollege(college, row.name).discipline_level || '未开设' }}
                  </el-tag>
                </template>
                <span v-else class="na-text">—</span>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <div class="section-card">
        <h2 class="section-title">📊 近年录取分数对比</h2>
        <div class="score-compare-wrap">
          <el-table :data="admissionCompareRows" border stripe>
            <el-table-column prop="label" label="年份/省份" width="140" />
            <el-table-column
              v-for="college in volunteerStore.compareList"
              :key="college.id"
              :label="college.name"
              min-width="130"
              align="center"
            >
              <template #default="{ row }">
                <div v-if="row.type === 'year'" class="admission-year-group">
                  <div
                    v-for="d in getCollegeYearData(college, row.year)"
                    :key="d.province"
                    class="admission-item"
                  >
                    <span class="admission-province">{{ d.province }}</span>
                    <span class="admission-score">{{ d.score }}分</span>
                  </div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>
    </template>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useVolunteerStore } from '../stores/volunteer'

const router = useRouter()
const volunteerStore = useVolunteerStore()

const compareRows = [
  { field: 'basic_info', label: '基本信息' },
  { field: 'location', label: '地理位置' },
  { field: 'admission_score', label: '录取分数' },
  { field: 'major_strength', label: '专业强弱' },
  { field: 'employment_rate', label: '就业率' },
  { field: 'average_salary', label: '平均薪资' },
]

const admissionCompareRows = [
  { type: 'year', year: 2025, label: '2025年' },
  { type: 'year', year: 2024, label: '2024年' },
  { type: 'year', year: 2023, label: '2023年' },
]

const allMajors = computed(() => {
  const majorSet = new Set()
  volunteerStore.compareList.forEach((c) => {
    ;(c.majors || []).forEach((m) => majorSet.add(m.name))
  })
  return Array.from(majorSet).map((name) => ({ name }))
})

function handleRemove(id) {
  volunteerStore.removeFromCompare(id)
  ElMessage.success('已移除')
}

async function handleClearAll() {
  try {
    await ElMessageBox.confirm('确定要清空所有对比院校吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    volunteerStore.clearCompare()
    ElMessage.success('已清空')
  } catch (e) {}
}

function getLatestScore(college) {
  const data = (college.admission_data || []).filter((d) => d.year === 2025)
  if (!data.length) return '-'
  return Math.min(...data.map((d) => d.score))
}

function getLatestRank(college) {
  const data = (college.admission_data || []).filter((d) => d.year === 2025)
  if (!data.length) return '-'
  return Math.max(...data.map((d) => d.rank))
}

function getMajorStrengthScore(college) {
  const levelWeight = {
    'A+': 12, A: 10, 'A-': 8,
    'B+': 7, B: 6, 'B-': 5,
    'C+': 4, C: 3, 'C-': 2,
  }
  const majors = college.majors || []
  if (!majors.length) return '弱'
  const total = majors.reduce((sum, m) => sum + (levelWeight[m.discipline_level] || 1), 0)
  const avg = total / majors.length
  if (avg >= 9) return '极强'
  if (avg >= 7) return '强'
  if (avg >= 5) return '中'
  if (avg >= 3) return '一般'
  return '弱'
}

function getMajorStrengthWidth(college) {
  const levelWeight = {
    'A+': 12, A: 10, 'A-': 8,
    'B+': 7, B: 6, 'B-': 5,
    'C+': 4, C: 3, 'C-': 2,
  }
  const majors = college.majors || []
  if (!majors.length) return 20
  const total = majors.reduce((sum, m) => sum + (levelWeight[m.discipline_level] || 1), 0)
  const avg = total / majors.length
  return Math.min(100, (avg / 12) * 100)
}

function getMajorByCollege(college, majorName) {
  return (college.majors || []).find((m) => m.name === majorName)
}

function getDisciplineTagType(level) {
  const map = {
    'A+': 'danger', A: 'danger', 'A-': 'danger',
    'B+': 'warning', B: 'warning', 'B-': 'warning',
    'C+': 'info', C: 'info', 'C-': 'info',
  }
  return map[level] || 'info'
}

function getRateColor(rate) {
  if (rate >= 0.92) return '#22c55e'
  if (rate >= 0.85) return '#3b82f6'
  if (rate >= 0.78) return '#f59e0b'
  return '#ef4444'
}

function formatSalary(salary) {
  if (!salary) return '-'
  if (salary >= 10000) {
    return (salary / 10000).toFixed(1) + '万'
  }
  return salary.toString()
}

function getCollegeYearData(college, year) {
  return (college.admission_data || []).filter((d) => d.year === year).slice(0, 5)
}

function isBest(idx, field, lowerIsBetter) {
  const list = volunteerStore.compareList
  if (list.length < 2) return false
  const values = list.map((c) => {
    switch (field) {
      case 'admission_score':
        return getLatestScore(c) === '-' ? 0 : getLatestScore(c)
      case 'major_strength':
        return getMajorStrengthWidth(c)
      case 'employment_rate':
        return c.employment_rate || 0
      case 'average_salary':
        return c.average_salary || 0
      default:
        return 0
    }
  })
  const best = lowerIsBetter ? Math.min(...values.filter((v) => v > 0)) : Math.max(...values)
  return values[idx] === best
}
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
  margin-right: 8px;
}

.compare-count {
  font-size: 14px;
  color: #64748b;
  font-weight: 400;
}

.compare-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.toolbar-tip {
  font-size: 13px;
  color: #64748b;
}

.compare-table-wrap {
  overflow-x: auto;
}

.college-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.college-name-cell {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.basic-info-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 8px 0;
}

.info-row {
  display: flex;
  justify-content: center;
}

.tags-row {
  flex-wrap: wrap;
}

.location-cell {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 4px;
  font-size: 14px;
  color: #475569;
}

.loc-icon {
  font-size: 16px;
}

.score-cell {
  padding: 4px 0;
}

.score-value {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
}

.score-value.highlight {
  color: #22c55e;
}

.score-sub {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.major-cell {
  padding: 4px 0;
}

.major-strength-bar {
  width: 100%;
  max-width: 160px;
  height: 10px;
  background: #e2e8f0;
  border-radius: 5px;
  margin: 0 auto 6px auto;
  overflow: hidden;
}

.strength-inner {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #8b5cf6);
  border-radius: 5px;
  transition: width 0.3s;
}

.strength-inner.highlight {
  background: linear-gradient(90deg, #22c55e, #10b981);
}

.strength-score {
  font-size: 15px;
  font-weight: 600;
  color: #475569;
  margin-bottom: 8px;
}

.strength-score.highlight {
  color: #22c55e;
}

.major-list {
  display: flex;
  flex-wrap: wrap;
  justify-content: center;
}

.rate-cell {
  padding: 4px 12px;
}

.rate-value {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 6px;
}

.rate-value.highlight {
  color: #22c55e;
}

.salary-cell {
  padding: 4px 0;
}

.salary-value {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
}

.salary-value.highlight {
  color: #22c55e;
}

.salary-sub {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.na-text {
  color: #cbd5e1;
  font-size: 16px;
}

.majors-compare-wrap,
.score-compare-wrap {
  overflow-x: auto;
}

.admission-year-group {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.admission-item {
  display: flex;
  justify-content: space-between;
  padding: 2px 8px;
  font-size: 12px;
  background: #f8fafc;
  border-radius: 3px;
}

.admission-province {
  color: #64748b;
}

.admission-score {
  font-weight: 600;
  color: #1e293b;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px 0;
}
</style>

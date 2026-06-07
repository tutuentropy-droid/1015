<template>
  <div class="page-container">
    <div class="hero-banner section-card">
      <div class="hero-left">
        <h1 class="hero-title">🎯 专业对比分析</h1>
        <p class="hero-desc">
          选择 2-3 个专业进行并排对比，从就业率、薪资水平、考研比例、男女比例、学习难度等核心维度一目了然，
          帮助你在多个专业之间做出科学决策。
        </p>
      </div>
      <div class="hero-right">
        <el-icon :size="80" color="#8b5cf6"><DataLine /></el-icon>
      </div>
    </div>

    <div class="section-card">
      <div class="filter-bar">
        <el-select
          v-model="filterCategory"
          placeholder="按学科门类筛选"
          clearable
          style="width: 180px"
        >
          <el-option
            v-for="cat in categories"
            :key="cat"
            :label="cat"
            :value="cat"
          />
        </el-select>
        <el-input
          v-model="searchKeyword"
          placeholder="搜索专业名称"
          clearable
          style="width: 260px"
        >
          <template #prefix>
            <el-icon><Search /></el-icon>
          </template>
        </el-input>
        <div class="filter-right">
          <el-tag type="info" effect="plain">
            已选 {{ volunteerStore.majorCompareCount }}/{{ volunteerStore.maxMajorCompare }}
          </el-tag>
          <el-button
            type="danger"
            plain
            size="small"
            @click="handleClearAll"
            :disabled="!volunteerStore.majorCompareCount"
          >
            清空已选
          </el-button>
        </div>
      </div>

      <div class="major-grid">
        <div
          v-for="major in filteredMajors"
          :key="major.name"
          class="major-card"
          :class="{ selected: volunteerStore.isMajorInCompare(major.name) }"
          @click="handleToggleMajor(major)"
        >
          <div class="card-head">
            <span class="major-name">{{ major.name }}</span>
            <div class="card-tags">
              <el-tag size="small" type="primary" effect="plain">{{ major.category }}</el-tag>
              <el-tag
                v-if="volunteerStore.isMajorInCompare(major.name)"
                size="small"
                type="success"
                effect="light"
              >
                已选
              </el-tag>
            </div>
          </div>
          <p class="major-brief">{{ major.brief_intro }}</p>
          <div class="card-footer">
            <span class="diff-tag" :class="getDifficultyClass(major.study_difficulty)">
              {{ major.study_difficulty }}
            </span>
            <span class="prospect-tag" :class="getProspectClass(major.employment_prospect)">
              就业{{ major.employment_prospect }}
            </span>
          </div>
        </div>
      </div>
      <div v-if="!filteredMajors.length" class="empty-tip">
        <el-empty description="没有找到匹配的专业" />
      </div>
    </div>

    <div v-if="volunteerStore.majorCompareCount >= 2" class="section-card">
      <div class="compare-toolbar">
        <h2 class="section-title" style="margin-bottom: 0">📊 对比结果</h2>
        <div class="toolbar-right">
          <el-tag type="success" effect="plain">
            💡 高亮显示各维度最优项
          </el-tag>
          <el-button
            type="primary"
            size="small"
            :loading="volunteerStore.loading.majorCompare"
            @click="handleCompare"
          >
            刷新对比数据
          </el-button>
        </div>
      </div>
    </div>

    <template v-if="volunteerStore.majorCompareResult && volunteerStore.majorCompareResult.length >= 2">
      <div class="section-card">
        <h3 class="sub-title">📈 五维雷达图对比</h3>
        <v-chart class="radar-chart" :option="radarOption" autoresize />
      </div>

      <div class="section-card">
        <h3 class="sub-title">📋 核心维度对比表</h3>
        <div class="compare-table-wrap">
          <el-table :data="compareRows" border stripe style="width: 100%">
            <el-table-column label="对比维度" width="140" fixed="left">
              <template #default="{ row }">
                <span class="dim-label">{{ row.label }}</span>
              </template>
            </el-table-column>
            <el-table-column
              v-for="(major, idx) in volunteerStore.majorCompareResult"
              :key="major.name"
              :label="major.name"
              min-width="180"
              align="center"
            >
              <template #header>
                <div class="major-header">
                  <div class="major-name-cell">{{ major.name }}</div>
                  <el-button
                    type="danger"
                    link
                    size="small"
                    @click.stop="handleRemoveMajor(major.name)"
                  >
                    移除
                  </el-button>
                </div>
              </template>
              <template #default="{ row }">
                <div v-if="row.field === 'basic_info'" class="basic-cell">
                  <el-tag type="primary" effect="plain" size="small">
                    {{ major.category }}
                  </el-tag>
                  <el-tag type="info" effect="plain" size="small" style="margin-top: 4px">
                    {{ major.major_type }}
                  </el-tag>
                </div>

                <div v-else-if="row.field === 'employment_rate'" class="rate-cell">
                  <div
                    class="rate-value"
                    :class="{ highlight: isBest(idx, 'employment_rate', false) }"
                  >
                    {{ (major.employment_rate * 100).toFixed(1) }}%
                  </div>
                  <el-progress
                    :percentage="major.employment_rate * 100"
                    :stroke-width="8"
                    :show-text="false"
                    :color="getRateColor(major.employment_rate)"
                  />
                  <div class="rate-sub">就业率</div>
                </div>

                <div v-else-if="row.field === 'salary'" class="salary-cell">
                  <div class="salary-row">
                    <span class="salary-label">应届生</span>
                    <span
                      class="salary-num"
                      :class="{ highlight: isBest(idx, 'salary_fresh', false) }"
                    >
                      ¥{{ formatSalary(major.salary_range.fresh) }}
                    </span>
                  </div>
                  <div class="salary-row">
                    <span class="salary-label">3年后</span>
                    <span
                      class="salary-num"
                      :class="{ highlight: isBest(idx, 'salary_3y', false) }"
                    >
                      ¥{{ formatSalary(major.salary_range.three_years) }}
                    </span>
                  </div>
                  <div class="salary-row">
                    <span class="salary-label">5年+</span>
                    <span
                      class="salary-num"
                      :class="{ highlight: isBest(idx, 'salary_5y', false) }"
                    >
                      ¥{{ formatSalary(major.salary_range.five_years_plus) }}
                    </span>
                  </div>
                </div>

                <div v-else-if="row.field === 'postgraduate'" class="rate-cell">
                  <div
                    class="rate-value"
                    :class="{ highlight: isBest(idx, 'postgraduate', false) }"
                  >
                    {{ (major.postgraduate_ratio * 100).toFixed(0) }}%
                  </div>
                  <el-progress
                    :percentage="major.postgraduate_ratio * 100"
                    :stroke-width="8"
                    :show-text="false"
                    color="#8b5cf6"
                  />
                  <div class="rate-sub">考研/深造比例</div>
                </div>

                <div v-else-if="row.field === 'gender_ratio'" class="gender-cell">
                  <div class="gender-bar">
                    <div
                      class="gender-male"
                      :style="{ width: getMaleRatio(major.gender_ratio) + '%' }"
                    ></div>
                    <div
                      class="gender-female"
                      :style="{ width: getFemaleRatio(major.gender_ratio) + '%' }"
                    ></div>
                  </div>
                  <div class="gender-labels">
                    <span class="male-label">♂ {{ getMaleRatio(major.gender_ratio) }}%</span>
                    <span class="female-label">♀ {{ getFemaleRatio(major.gender_ratio) }}%</span>
                  </div>
                  <div class="gender-raw">{{ major.gender_ratio }}</div>
                </div>

                <div v-else-if="row.field === 'difficulty'" class="difficulty-cell">
                  <div class="diff-stars">
                    <el-rate
                      :model-value="getDifficultyStars(major.study_difficulty)"
                      disabled
                      show-score
                      text-color="#ff6b6b"
                      score-template="{value}"
                    />
                  </div>
                  <div class="diff-text" :class="getDifficultyClass(major.study_difficulty)">
                    {{ major.study_difficulty }}
                  </div>
                  <div class="diff-sub">课程量：{{ major.course_load }}</div>
                </div>
              </template>
            </el-table-column>
          </el-table>
        </div>
      </div>

      <div class="section-card">
        <h3 class="sub-title">💡 对比分析与建议</h3>
        <div class="compare-tips">
          <el-timeline>
            <el-timeline-item
              v-for="(tip, idx) in analysisTips"
              :key="idx"
              :type="tip.type"
              size="large"
            >
              {{ tip.text }}
            </el-timeline-item>
          </el-timeline>
        </div>
      </div>

      <div class="section-card">
        <h3 class="sub-title">📖 专业详细信息</h3>
        <el-tabs>
          <el-tab-pane
            v-for="major in volunteerStore.majorCompareResult"
            :key="major.name"
            :label="major.name"
          >
            <div class="detail-grid">
              <div class="detail-col">
                <h4>专业简介</h4>
                <p class="detail-text">{{ major.introduction }}</p>

                <h4>核心课程</h4>
                <div class="tag-list">
                  <el-tag
                    v-for="c in major.core_courses"
                    :key="c"
                    type="info"
                    effect="plain"
                    style="margin: 3px"
                  >
                    {{ c }}
                  </el-tag>
                </div>
              </div>
              <div class="detail-col">
                <h4>就业方向</h4>
                <div class="tag-list">
                  <el-tag
                    v-for="d in major.employment_direction"
                    :key="d"
                    type="success"
                    effect="light"
                    style="margin: 3px"
                  >
                    {{ d }}
                  </el-tag>
                </div>

                <h4>典型岗位</h4>
                <div class="tag-list">
                  <el-tag
                    v-for="p in major.typical_positions"
                    :key="p"
                    type="warning"
                    effect="light"
                    style="margin: 3px"
                  >
                    {{ p }}
                  </el-tag>
                </div>
              </div>
              <div class="detail-col">
                <h4>适合人群</h4>
                <ul class="trait-list">
                  <li v-for="t in major.suitable_traits" :key="t">✅ {{ t }}</li>
                </ul>

                <h4>不太适合</h4>
                <ul class="trait-list">
                  <li v-for="t in major.unsuitable_people" :key="t">⚠️ {{ t }}</li>
                </ul>
              </div>
            </div>
          </el-tab-pane>
        </el-tabs>
      </div>
    </template>

    <div v-else-if="volunteerStore.majorCompareCount > 0 && volunteerStore.majorCompareCount < 2" class="section-card">
      <el-alert
        type="warning"
        :closable="false"
        show-icon
        title="请至少选择 2 个专业进行对比"
      />
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { ElMessage, ElMessageBox } from 'element-plus'
import { useVolunteerStore } from '../stores/volunteer'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { RadarChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent, RadarComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, RadarChart, TitleComponent, TooltipComponent, LegendComponent, RadarComponent])

const volunteerStore = useVolunteerStore()

const filterCategory = ref('')
const searchKeyword = ref('')

const categories = computed(() => {
  const set = new Set(volunteerStore.majorList.map((m) => m.category))
  return Array.from(set).sort()
})

const filteredMajors = computed(() => {
  let list = volunteerStore.majorList
  if (filterCategory.value) {
    list = list.filter((m) => m.category === filterCategory.value)
  }
  if (searchKeyword.value) {
    const kw = searchKeyword.value.toLowerCase()
    list = list.filter((m) =>
      m.name.toLowerCase().includes(kw) ||
      m.brief_intro.toLowerCase().includes(kw)
    )
  }
  return list
})

const compareRows = [
  { field: 'basic_info', label: '基本信息' },
  { field: 'employment_rate', label: '就业率' },
  { field: 'salary', label: '薪资水平' },
  { field: 'postgraduate', label: '考研比例' },
  { field: 'gender_ratio', label: '男女比例' },
  { field: 'difficulty', label: '学习难度' },
]

const radarOption = computed(() => {
  const majors = volunteerStore.majorCompareResult || []
  if (!majors.length) return {}
  const colors = ['#3b82f6', '#f59e0b', '#22c55e']
  return {
    tooltip: { trigger: 'item' },
    legend: {
      data: majors.map((m) => m.name),
      bottom: 0,
    },
    radar: {
      indicator: [
        { name: '就业率', max: 100 },
        { name: '应届生薪资', max: 100 },
        { name: '考研比例', max: 100 },
        { name: '学习友好度', max: 100 },
        { name: '就业前景', max: 100 },
      ],
      radius: '65%',
      center: ['50%', '50%'],
      splitNumber: 4,
    },
    series: [
      {
        type: 'radar',
        data: majors.map((m, idx) => ({
          name: m.name,
          value: [
            m.employment_rate * 100,
            Math.min(100, (m.salary_range.fresh / 250000) * 100),
            m.postgraduate_ratio * 100,
            (100 - (getDifficultyStars(m.study_difficulty) / 5) * 100 + 20),
            getProspectScore(m.employment_prospect),
          ],
          itemStyle: { color: colors[idx] },
          areaStyle: { opacity: 0.2 },
        })),
      },
    ],
  }
})

const analysisTips = computed(() => {
  const majors = volunteerStore.majorCompareResult || []
  if (majors.length < 2) return []
  const tips = []

  const sortedByEmployment = [...majors].sort((a, b) => b.employment_rate - a.employment_rate)
  tips.push({
    type: 'success',
    text: `就业率最高的是「${sortedByEmployment[0].name}」${(sortedByEmployment[0].employment_rate * 100).toFixed(1)}%，最低的是「${sortedByEmployment[sortedByEmployment.length - 1].name}」${(sortedByEmployment[sortedByEmployment.length - 1].employment_rate * 100).toFixed(1)}%。`,
  })

  const sortedBySalary = [...majors].sort((a, b) => b.salary_range.five_years_plus - a.salary_range.five_years_plus)
  tips.push({
    type: 'warning',
    text: `薪资方面，5年以上经验最高的是「${sortedBySalary[0].name}」年薪约¥${formatSalary(sortedBySalary[0].salary_range.five_years_plus)}，比最低的「${sortedBySalary[sortedBySalary.length - 1].name}」高出约¥${formatSalary(sortedBySalary[0].salary_range.five_years_plus - sortedBySalary[sortedBySalary.length - 1].salary_range.five_years_plus)}。`,
  })

  const sortedByPostgrad = [...majors].sort((a, b) => b.postgraduate_ratio - a.postgraduate_ratio)
  tips.push({
    type: 'primary',
    text: `考研深造比例最高的是「${sortedByPostgrad[0].name}」(${(sortedByPostgrad[0].postgraduate_ratio * 100).toFixed(0)}%)，适合想走学术或高端研发路线的同学；「${sortedByPostgrad[sortedByPostgrad.length - 1].name}」深造比例较低，更偏向本科直接就业。`,
  })

  const hardMajors = majors.filter((m) => m.study_difficulty === '非常难')
  if (hardMajors.length) {
    tips.push({
      type: 'danger',
      text: `注意：「${hardMajors.map((m) => m.name).join('、')}」学习难度为"非常难"，课程压力大，需要投入大量时间精力，请结合自身学习能力慎重选择。`,
    })
  }

  tips.push({
    type: 'info',
    text: '建议综合考虑自身兴趣、能力优势、职业规划和家庭条件来选择专业，不要只看单一维度的数据。',
  })

  return tips
})

onMounted(async () => {
  await volunteerStore.fetchMajors()
  if (volunteerStore.majorCompareCount >= 2) {
    await volunteerStore.compareMajors()
  }
})

watch(
  () => volunteerStore.majorCompareCount,
  (newVal) => {
    if (newVal >= 2) {
      volunteerStore.compareMajors()
    }
  }
)

function handleToggleMajor(major) {
  const res = volunteerStore.toggleMajorCompare(major)
  if (res.success === false) {
    ElMessage.warning(res.message)
  } else {
    ElMessage.success(res.message || '操作成功')
  }
}

function handleRemoveMajor(majorName) {
  volunteerStore.removeMajorFromCompare(majorName)
  ElMessage.success('已移除')
}

async function handleClearAll() {
  try {
    await ElMessageBox.confirm('确定要清空所有对比专业吗？', '提示', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning',
    })
    volunteerStore.clearMajorCompare()
    ElMessage.success('已清空')
  } catch (e) {}
}

async function handleCompare() {
  try {
    await volunteerStore.compareMajors()
    ElMessage.success('对比完成')
  } catch (e) {
    ElMessage.error(e.message || '对比失败')
  }
}

function formatSalary(salary) {
  if (!salary) return '-'
  if (salary >= 10000) {
    return (salary / 10000).toFixed(1) + '万'
  }
  return salary.toString()
}

function getRateColor(rate) {
  if (rate >= 0.92) return '#22c55e'
  if (rate >= 0.85) return '#3b82f6'
  if (rate >= 0.78) return '#f59e0b'
  return '#ef4444'
}

function getDifficultyStars(difficulty) {
  const map = { '轻松': 1, '适中': 2, '较难': 3, '非常难': 5 }
  return map[difficulty] || 2
}

function getDifficultyClass(difficulty) {
  const map = {
    '轻松': 'diff-easy',
    '适中': 'diff-moderate',
    '较难': 'diff-hard',
    '非常难': 'diff-very-hard',
  }
  return map[difficulty] || 'diff-moderate'
}

function getProspectClass(prospect) {
  const map = {
    '极好': 'prospect-excellent',
    '良好': 'prospect-good',
    '一般': 'prospect-normal',
    '较差': 'prospect-poor',
  }
  return map[prospect] || 'prospect-normal'
}

function getProspectScore(prospect) {
  const map = { '极好': 95, '良好': 78, '一般': 55, '较差': 35 }
  return map[prospect] || 50
}

function getMaleRatio(ratioStr) {
  const match = ratioStr.match(/男(\d+(?:\.\d+)?)/)
  if (!match) return 50
  const male = parseFloat(match[1])
  const fmatch = ratioStr.match(/女(\d+(?:\.\d+)?)/)
  const female = fmatch ? parseFloat(fmatch[1]) : 10 - male
  return Math.round((male / (male + female)) * 100)
}

function getFemaleRatio(ratioStr) {
  return 100 - getMaleRatio(ratioStr)
}

function isBest(idx, field, lowerIsBetter) {
  const list = volunteerStore.majorCompareResult || []
  if (list.length < 2) return false
  const values = list.map((m) => {
    switch (field) {
      case 'employment_rate':
        return m.employment_rate || 0
      case 'salary_fresh':
        return m.salary_range?.fresh || 0
      case 'salary_3y':
        return m.salary_range?.three_years || 0
      case 'salary_5y':
        return m.salary_range?.five_years_plus || 0
      case 'postgraduate':
        return m.postgraduate_ratio || 0
      case 'difficulty':
        return getDifficultyStars(m.study_difficulty)
      default:
        return 0
    }
  })
  const validVals = values.filter((v) => v > 0)
  if (!validVals.length) return false
  const best = lowerIsBetter ? Math.min(...validVals) : Math.max(...validVals)
  return values[idx] === best
}
</script>

<style scoped>
.hero-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #faf5ff 0%, #eff6ff 100%);
  border-radius: 12px;
  padding: 28px 32px;
  margin-bottom: 20px;
}

.hero-title {
  font-size: 26px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 8px 0;
}

.hero-desc {
  font-size: 14px;
  color: #64748b;
  line-height: 1.7;
  max-width: 720px;
  margin: 0;
}

.hero-right {
  opacity: 0.7;
}

.filter-bar {
  display: flex;
  gap: 16px;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
}

.filter-right {
  margin-left: auto;
  display: flex;
  gap: 12px;
  align-items: center;
}

.major-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 14px;
}

.major-card {
  padding: 16px 18px;
  background: #fafbfc;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  cursor: pointer;
  transition: all 0.2s;
}

.major-card:hover {
  border-color: #3b82f6;
  background: #eff6ff;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(59, 130, 246, 0.1);
}

.major-card.selected {
  border-color: #22c55e;
  background: #f0fdf4;
  box-shadow: 0 2px 8px rgba(34, 197, 94, 0.15);
}

.card-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 8px;
  gap: 8px;
}

.major-name {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.card-tags {
  display: flex;
  gap: 4px;
  flex-shrink: 0;
  flex-wrap: wrap;
  justify-content: flex-end;
}

.major-brief {
  font-size: 13px;
  color: #64748b;
  line-height: 1.6;
  margin: 0 0 10px 0;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
  overflow: hidden;
}

.card-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.diff-tag,
.prospect-tag {
  font-size: 12px;
  font-weight: 600;
  padding: 2px 8px;
  border-radius: 4px;
}

.diff-easy { background: #ecfdf5; color: #059669; }
.diff-moderate { background: #eff6ff; color: #2563eb; }
.diff-hard { background: #fffbeb; color: #d97706; }
.diff-very-hard { background: #fef2f2; color: #dc2626; }

.prospect-excellent { background: #ecfdf5; color: #059669; }
.prospect-good { background: #eff6ff; color: #2563eb; }
.prospect-normal { background: #fffbeb; color: #d97706; }
.prospect-poor { background: #fef2f2; color: #dc2626; }

.compare-toolbar {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.toolbar-right {
  display: flex;
  gap: 12px;
  align-items: center;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  padding-left: 12px;
  border-left: 4px solid #409eff;
  margin: 0;
}

.sub-title {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 16px 0;
}

.radar-chart {
  height: 380px;
}

.compare-table-wrap {
  overflow-x: auto;
}

.major-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
}

.major-name-cell {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
}

.dim-label {
  font-weight: 600;
  color: #334155;
}

.basic-cell {
  display: flex;
  flex-direction: column;
  gap: 4px;
  padding: 6px 0;
  align-items: center;
}

.rate-cell {
  padding: 6px 12px;
}

.rate-value {
  font-size: 24px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.rate-value.highlight {
  color: #22c55e;
}

.rate-sub {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.salary-cell {
  padding: 6px 8px;
  text-align: left;
}

.salary-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 2px 4px;
}

.salary-label {
  font-size: 12px;
  color: #94a3b8;
}

.salary-num {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.salary-num.highlight {
  color: #22c55e;
}

.gender-cell {
  padding: 6px 12px;
}

.gender-bar {
  display: flex;
  height: 14px;
  border-radius: 7px;
  overflow: hidden;
  margin-bottom: 6px;
}

.gender-male {
  background: #3b82f6;
}

.gender-female {
  background: #ec4899;
}

.gender-labels {
  display: flex;
  justify-content: space-between;
  font-size: 12px;
  margin-bottom: 2px;
}

.male-label {
  color: #3b82f6;
  font-weight: 600;
}

.female-label {
  color: #ec4899;
  font-weight: 600;
}

.gender-raw {
  font-size: 11px;
  color: #94a3b8;
}

.difficulty-cell {
  padding: 6px 8px;
}

.diff-stars {
  margin-bottom: 4px;
}

.diff-text {
  font-size: 14px;
  font-weight: 600;
  margin-bottom: 2px;
}

.diff-sub {
  font-size: 12px;
  color: #94a3b8;
}

.compare-tips {
  padding: 4px 8px;
}

.detail-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
}

.detail-col h4 {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 8px 0;
  padding-bottom: 6px;
  border-bottom: 1px solid #e2e8f0;
}

.detail-col h4:not(:first-child) {
  margin-top: 16px;
}

.detail-text {
  font-size: 13px;
  color: #64748b;
  line-height: 1.7;
  margin: 0 0 8px 0;
}

.tag-list {
  display: flex;
  flex-wrap: wrap;
  margin-bottom: 8px;
}

.trait-list {
  list-style: none;
  padding: 0;
  margin: 0;
  font-size: 13px;
  color: #475569;
}

.trait-list li {
  margin-bottom: 6px;
  line-height: 1.6;
}

@media (max-width: 768px) {
  .major-grid {
    grid-template-columns: 1fr;
  }
  .detail-grid {
    grid-template-columns: 1fr;
  }
  .hero-banner {
    flex-direction: column;
    gap: 16px;
  }
  .compare-toolbar {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
}
</style>

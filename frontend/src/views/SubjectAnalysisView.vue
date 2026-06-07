<template>
  <div class="page-container">
    <div class="hero-banner section-card">
      <div class="hero-left">
        <h1 class="hero-title">📚 选科影响分析</h1>
        <p class="hero-desc">
          专为新高考省份学生打造的选科决策工具。选择你的选科组合，
          即时了解可报与不可报专业范围，对比不同组合的影响差异，
          帮助你做出最优选科决策。
        </p>
      </div>
      <div class="hero-right">
        <el-icon :size="80" color="#409eff"><Reading /></el-icon>
      </div>
    </div>

    <el-tabs v-model="activeTab" class="main-tabs">
      <el-tab-pane label="单组合分析" name="single">
        <div class="section-card">
          <h2 class="section-title">选择你的选科组合</h2>
          <el-form label-width="120px">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="所在省份">
                  <el-select
                    v-model="analysisForm.province"
                    placeholder="请选择省份"
                    filterable
                    style="width: 100%"
                  >
                    <el-option
                      v-for="p in volunteerStore.newGaokaoProvinces"
                      :key="p.province"
                      :label="`${p.province} (${p.policy}模式)`"
                      :value="p.province"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="选科方式">
                  <el-radio-group v-model="analysisForm.selectMode">
                    <el-radio value="combo">从预设组合选</el-radio>
                    <el-radio value="custom">自由选择三科</el-radio>
                  </el-radio-group>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="24" v-if="analysisForm.selectMode === 'combo'">
                <el-form-item label="选科组合">
                  <el-select
                    v-model="analysisForm.combo"
                    placeholder="请选择选科组合"
                    filterable
                    style="width: 100%"
                    @change="onComboChange"
                  >
                    <el-option
                      v-for="c in volunteerStore.subjectCombinations"
                      :key="c"
                      :label="c"
                      :value="c"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="24" v-else>
                <el-form-item label="选择科目">
                  <el-checkbox-group v-model="analysisForm.subjects" @change="onSubjectsChange">
                    <el-checkbox
                      v-for="s in volunteerStore.allSubjects"
                      :key="s"
                      :label="s"
                      :disabled="analysisForm.subjects.length >= 3 && !analysisForm.subjects.includes(s)"
                      style="margin-right: 20px; margin-bottom: 8px"
                    >
                      <span style="font-size: 15px">{{ s }}</span>
                    </el-checkbox>
                  </el-checkbox-group>
                  <span v-if="analysisForm.subjects.length > 0" style="color:#94a3b8; margin-left:12px">
                    已选 {{ analysisForm.subjects.length }}/3
                  </span>
                </el-form-item>
              </el-col>
            </el-row>

            <el-row :gutter="24">
              <el-col :span="24">
                <el-form-item label="目标院校">
                  <div class="target-colleges-wrap">
                    <el-tag
                      v-for="c in targetColleges"
                      :key="c.id"
                      closable
                      type="primary"
                      effect="light"
                      style="margin-right: 8px; margin-bottom: 4px"
                      @close="removeTargetCollege(c.id)"
                    >
                      {{ c.name }}
                    </el-tag>
                    <el-button
                      type="primary"
                      plain
                      size="small"
                      @click="showCollegePicker = true"
                      style="margin-left: 4px"
                    >
                      <el-icon><Plus /></el-icon>
                      <span>添加目标院校</span>
                    </el-button>
                    <span style="color:#94a3b8; margin-left:12px">
                      {{ targetColleges.length ? '已限定以上院校' : '不限院校，分析全部数据' }}
                    </span>
                  </div>
                </el-form-item>
              </el-col>
            </el-row>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="volunteerStore.loading.subjectAnalysis"
                :disabled="!canAnalyze"
                @click="handleAnalyze"
              >
                <el-icon><Search /></el-icon>
                <span>开始分析</span>
              </el-button>
              <el-button size="large" @click="resetAnalysis" style="margin-left: 8px">
                <el-icon><Refresh /></el-icon>
                <span>重置</span>
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <div v-if="volunteerStore.subjectAnalysisResult" class="section-card">
          <h2 class="section-title">📊 分析结果</h2>
          <div class="stats-grid">
            <div class="stat-box total">
              <div class="stat-title">专业总数</div>
              <div class="stat-num">{{ volunteerStore.subjectAnalysisResult.total_majors }}</div>
              <div class="stat-desc">所有覆盖专业</div>
            </div>
            <div class="stat-box eligible">
              <div class="stat-title">✅ 可报专业</div>
              <div class="stat-num">{{ volunteerStore.subjectAnalysisResult.eligible_majors }}</div>
              <div class="stat-desc">满足选科要求</div>
            </div>
            <div class="stat-box ineligible">
              <div class="stat-title">❌ 不可报专业</div>
              <div class="stat-num">{{ volunteerStore.subjectAnalysisResult.ineligible_majors }}</div>
              <div class="stat-desc">不满足选科要求</div>
            </div>
            <div class="stat-box rate">
              <div class="stat-title">可报比例</div>
              <div class="stat-num">
                {{ (volunteerStore.subjectAnalysisResult.eligible_rate * 100).toFixed(1) }}%
              </div>
              <div class="stat-desc">专业覆盖率</div>
            </div>
          </div>

          <div v-if="volunteerStore.subjectAnalysisResult.college_stats.length" class="college-stats-wrap">
            <h3 class="sub-title">🏫 各院校可报情况</h3>
            <el-table :data="volunteerStore.subjectAnalysisResult.college_stats" stripe max-height="300">
              <el-table-column prop="college_name" label="院校名称" min-width="160" />
              <el-table-column prop="total_majors" label="专业总数" width="100" align="center" />
              <el-table-column prop="eligible_majors" label="可报专业" width="100" align="center">
                <template #default="{ row }">
                  <span style="color:#22c55e; font-weight:600">{{ row.eligible_majors }}</span>
                </template>
              </el-table-column>
              <el-table-column prop="ineligible_majors" label="不可报" width="100" align="center">
                <template #default="{ row }">
                  <span style="color:#ef4444">{{ row.ineligible_majors }}</span>
                </template>
              </el-table-column>
              <el-table-column label="可报率" width="140" align="center">
                <template #default="{ row }">
                  <el-progress
                    :percentage="Math.round(row.eligible_rate * 100)"
                    :stroke-width="10"
                    :color="getRateColor(row.eligible_rate)"
                    :show-text="true"
                  />
                </template>
              </el-table-column>
            </el-table>
          </div>
        </div>

        <div v-if="volunteerStore.subjectAnalysisResult" class="section-card">
          <h2 class="section-title">📖 专业详细列表（按学科门类分组）</h2>
          <el-collapse v-model="activeGroups">
            <el-collapse-item
              v-for="group in volunteerStore.subjectAnalysisResult.discipline_groups"
              :key="group.category"
              :name="group.category"
            >
              <template #title>
                <div class="group-title">
                  <span class="group-name">{{ group.category }}</span>
                  <el-tag type="success" effect="light" size="small" style="margin-left:8px">
                    可报 {{ group.eligible_count }}
                  </el-tag>
                  <el-tag type="info" effect="light" size="small" style="margin-left:4px">
                    共 {{ group.total_count }}
                  </el-tag>
                </div>
              </template>
              <div class="major-list">
                <div
                  v-for="m in group.majors"
                  :key="m.major.id"
                  class="major-item"
                  :class="{ ineligible: !m.eligible }"
                >
                  <div class="major-main">
                    <span class="major-status" :class="m.eligible ? 'ok' : 'no'">
                      {{ m.eligible ? '✅' : '❌' }}
                    </span>
                    <span class="major-name" @click="goMajorDetail(m.major)">
                      {{ m.major.name }}
                    </span>
                    <el-tag
                      v-if="m.major.discipline_level"
                      :type="getDisciplineTagType(m.major.discipline_level)"
                      effect="light"
                      size="small"
                      style="margin-left: 8px"
                    >
                      {{ m.major.discipline_level }}
                    </el-tag>
                    <span v-if="m.college_name" class="college-tag">
                      📍 {{ m.college_name }}
                    </span>
                  </div>
                  <div v-if="!m.eligible" class="major-reason">
                    {{ m.reason }}
                  </div>
                  <div v-else class="major-requirements">
                    <span class="req-label">选科要求：</span>
                    <span v-if="m.major.subject_requirements && m.major.subject_requirements.length">
                      {{ m.major.subject_requirements.join('、') }}
                    </span>
                    <span v-else>不限</span>
                  </div>
                </div>
              </div>
            </el-collapse-item>
          </el-collapse>
        </div>
      </el-tab-pane>

      <el-tab-pane label="多组合对比" name="compare">
        <div class="section-card">
          <h2 class="section-title">📊 选科组合对比分析</h2>
          <el-alert
            type="info"
            :closable="false"
            show-icon
            style="margin-bottom: 20px"
          >
            <template #title>
              同时选择 2-3 种选科组合进行并排对比，清晰了解不同选择对专业报考范围的影响差异。
            </template>
          </el-alert>

          <el-form label-width="120px">
            <el-row :gutter="24">
              <el-col :span="12">
                <el-form-item label="所在省份">
                  <el-select
                    v-model="compareForm.province"
                    placeholder="请选择省份"
                    filterable
                    style="width: 100%"
                  >
                    <el-option
                      v-for="p in volunteerStore.newGaokaoProvinces"
                      :key="p.province"
                      :label="`${p.province} (${p.policy}模式)`"
                      :value="p.province"
                    />
                  </el-select>
                </el-form-item>
              </el-col>
              <el-col :span="12">
                <el-form-item label="对比目标院校">
                  <div class="target-colleges-wrap">
                    <el-tag
                      v-for="c in compareTargetColleges"
                      :key="c.id"
                      closable
                      type="warning"
                      effect="light"
                      style="margin-right: 8px; margin-bottom: 4px"
                      @close="removeCompareTargetCollege(c.id)"
                    >
                      {{ c.name }}
                    </el-tag>
                    <el-button
                      type="warning"
                      plain
                      size="small"
                      @click="showCompareCollegePicker = true"
                    >
                      <el-icon><Plus /></el-icon>
                      <span>添加</span>
                    </el-button>
                  </div>
                </el-form-item>
              </el-col>
            </el-row>

            <div class="combination-editors">
              <div
                v-for="(combo, idx) in compareForm.combinations"
                :key="idx"
                class="combo-editor"
              >
                <div class="combo-header">
                  <span class="combo-label">组合 {{ idx + 1 }}</span>
                  <el-button
                    v-if="compareForm.combinations.length > 1"
                    link
                    type="danger"
                    size="small"
                    @click="removeCombination(idx)"
                  >
                    移除
                  </el-button>
                </div>
                <el-select
                  v-model="compareForm.combinations[idx]"
                  placeholder="请选择选科组合"
                  filterable
                  style="width: 100%"
                >
                  <el-option
                    v-for="c in volunteerStore.subjectCombinations"
                    :key="c"
                    :label="c"
                    :value="c"
                  />
                </el-select>
              </div>
            </div>

            <el-form-item style="margin-top: 16px">
              <el-button
                v-if="compareForm.combinations.length < 3"
                type="primary"
                plain
                @click="addCombination"
              >
                <el-icon><Plus /></el-icon>
                <span>添加对比组合 ({{ compareForm.combinations.length }}/3)</span>
              </el-button>
            </el-form-item>

            <el-form-item>
              <el-button
                type="primary"
                size="large"
                :loading="volunteerStore.loading.subjectCompare"
                :disabled="!canCompare"
                @click="handleCompare"
              >
                <el-icon><DataAnalysis /></el-icon>
                <span>开始对比</span>
              </el-button>
              <el-button size="large" @click="resetCompare" style="margin-left: 8px">
                <el-icon><Refresh /></el-icon>
                <span>重置</span>
              </el-button>
            </el-form-item>
          </el-form>
        </div>

        <div v-if="volunteerStore.subjectCompareResult && volunteerStore.subjectCompareResult.items.length" class="section-card">
          <h2 class="section-title">📊 对比结果</h2>
          <div class="compare-stats-grid">
            <div
              v-for="(item, idx) in volunteerStore.subjectCompareResult.items"
              :key="idx"
              class="compare-stat-card"
              :class="`color-${idx}`"
            >
              <div class="compare-combo-label">{{ item.combination_label }}</div>
              <div class="compare-stats-row">
                <div class="compare-stat-item">
                  <div class="cs-value ok">{{ item.eligible_majors }}</div>
                  <div class="cs-label">可报专业</div>
                </div>
                <div class="compare-stat-item">
                  <div class="cs-value no">{{ item.ineligible_majors }}</div>
                  <div class="cs-label">不可报</div>
                </div>
                <div class="compare-stat-item">
                  <div class="cs-value rate">{{ (item.eligible_rate * 100).toFixed(0) }}%</div>
                  <div class="cs-label">覆盖率</div>
                </div>
              </div>
            </div>
          </div>

          <div v-if="volunteerStore.subjectCompareResult.items[0]?.by_college?.length" class="compare-chart-wrap">
            <h3 class="sub-title">🏫 各院校可报专业数对比</h3>
            <v-chart class="compare-chart" :option="compareChartOption" autoresize />
          </div>

          <div class="compare-summary">
            <h3 class="sub-title">💡 对比结论</h3>
            <el-timeline>
              <el-timeline-item
                v-for="(tip, idx) in compareTips"
                :key="idx"
                :type="tip.type"
                size="large"
              >
                {{ tip.text }}
              </el-timeline-item>
            </el-timeline>
          </div>
        </div>
      </el-tab-pane>
    </el-tabs>

    <el-dialog v-model="showCollegePicker" title="选择目标院校" width="700px">
      <el-tabs v-model="collegePickerTab">
        <el-tab-pane label="从收藏院校" name="favorites">
          <div v-if="!volunteerStore.favoriteColleges.length" class="empty-tip">
            <el-empty description="暂无收藏院校，可去院校详情页收藏" />
          </div>
          <div v-else class="college-picker-list">
            <div
              v-for="c in volunteerStore.favoriteColleges"
              :key="c.id"
              class="picker-college-item"
              :class="{ selected: isInTargetColleges(c.id) }"
              @click="toggleTargetCollege(c)"
            >
              <span class="college-picker-name">{{ c.name }}</span>
              <el-tag size="small" :type="isInTargetColleges(c.id) ? 'success' : 'info'">
                {{ isInTargetColleges(c.id) ? '已选' : '选择' }}
              </el-tag>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="搜索添加" name="search">
          <el-input
            v-model="collegeSearchKeyword"
            placeholder="输入院校名称搜索"
            clearable
            style="margin-bottom: 12px"
            @input="searchColleges"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <div v-if="!searchedColleges.length" class="empty-tip">
            <el-empty description="请输入关键词搜索" />
          </div>
          <div v-else class="college-picker-list">
            <div
              v-for="c in searchedColleges"
              :key="c.id"
              class="picker-college-item"
              :class="{ selected: isInTargetColleges(c.id) }"
              @click="toggleTargetCollege(c)"
            >
              <span class="college-picker-name">{{ c.name }}</span>
              <span class="college-picker-meta">{{ c.level }} · {{ c.city }}</span>
              <el-tag size="small" :type="isInTargetColleges(c.id) ? 'success' : 'info'">
                {{ isInTargetColleges(c.id) ? '已选' : '选择' }}
              </el-tag>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>

    <el-dialog v-model="showCompareCollegePicker" title="选择对比目标院校" width="700px">
      <el-tabs v-model="compareCollegePickerTab">
        <el-tab-pane label="从收藏院校" name="favorites">
          <div v-if="!volunteerStore.favoriteColleges.length" class="empty-tip">
            <el-empty description="暂无收藏院校" />
          </div>
          <div v-else class="college-picker-list">
            <div
              v-for="c in volunteerStore.favoriteColleges"
              :key="c.id"
              class="picker-college-item"
              :class="{ selected: isInCompareTargetColleges(c.id) }"
              @click="toggleCompareTargetCollege(c)"
            >
              <span class="college-picker-name">{{ c.name }}</span>
              <el-tag size="small" :type="isInCompareTargetColleges(c.id) ? 'warning' : 'info'">
                {{ isInCompareTargetColleges(c.id) ? '已选' : '选择' }}
              </el-tag>
            </div>
          </div>
        </el-tab-pane>
        <el-tab-pane label="搜索添加" name="search">
          <el-input
            v-model="compareCollegeSearchKeyword"
            placeholder="输入院校名称搜索"
            clearable
            style="margin-bottom: 12px"
            @input="searchCompareColleges"
          >
            <template #prefix>
              <el-icon><Search /></el-icon>
            </template>
          </el-input>
          <div v-if="!compareSearchedColleges.length" class="empty-tip">
            <el-empty description="请输入关键词搜索" />
          </div>
          <div v-else class="college-picker-list">
            <div
              v-for="c in compareSearchedColleges"
              :key="c.id"
              class="picker-college-item"
              :class="{ selected: isInCompareTargetColleges(c.id) }"
              @click="toggleCompareTargetCollege(c)"
            >
              <span class="college-picker-name">{{ c.name }}</span>
              <span class="college-picker-meta">{{ c.level }} · {{ c.city }}</span>
              <el-tag size="small" :type="isInCompareTargetColleges(c.id) ? 'warning' : 'info'">
                {{ isInCompareTargetColleges(c.id) ? '已选' : '选择' }}
              </el-tag>
            </div>
          </div>
        </el-tab-pane>
      </el-tabs>
    </el-dialog>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useVolunteerStore } from '../stores/volunteer'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent, GridComponent,
} from 'echarts/components'
import VChart from 'vue-echarts'

use([CanvasRenderer, BarChart, TitleComponent, TooltipComponent, LegendComponent, GridComponent])

const router = useRouter()
const volunteerStore = useVolunteerStore()

const activeTab = ref('single')
const activeGroups = ref(['工学', '理学', '医学', '经济学', '管理学'])

const analysisForm = ref({
  province: '',
  selectMode: 'combo',
  combo: '',
  subjects: [],
})

const compareForm = ref({
  province: '',
  combinations: ['', ''],
})

const targetColleges = ref([])
const compareTargetColleges = ref([])

const showCollegePicker = ref(false)
const collegePickerTab = ref('favorites')
const collegeSearchKeyword = ref('')
const searchedColleges = ref([])

const showCompareCollegePicker = ref(false)
const compareCollegePickerTab = ref('favorites')
const compareCollegeSearchKeyword = ref('')
const compareSearchedColleges = ref([])

const canAnalyze = computed(() => {
  if (analysisForm.value.selectMode === 'combo') {
    return analysisForm.value.combo
  }
  return analysisForm.value.subjects.length === 3
})

const canCompare = computed(() => {
  return compareForm.value.combinations.filter((c) => c).length >= 2
})

const currentSubjects = computed(() => {
  if (analysisForm.value.selectMode === 'combo' && analysisForm.value.combo) {
    return analysisForm.value.combo.split('+')
  }
  return analysisForm.value.subjects
})

const compareChartOption = computed(() => {
  const items = volunteerStore.subjectCompareResult?.items || []
  if (!items.length || !items[0]?.by_college?.length) return {}
  const colleges = items[0].by_college.map((c) => c.college_name)
  const series = items.map((item, idx) => ({
    name: item.combination_label,
    type: 'bar',
    data: item.by_college.map((c) => c.eligible_majors),
    itemStyle: {
      color: ['#3b82f6', '#f59e0b', '#22c55e'][idx],
    },
  }))
  return {
    tooltip: { trigger: 'axis', axisPointer: { type: 'shadow' } },
    legend: { data: items.map((i) => i.combination_label) },
    grid: { left: '3%', right: '4%', bottom: '3%', containLabel: true },
    xAxis: {
      type: 'category',
      data: colleges,
      axisLabel: { rotate: 30, interval: 0 },
    },
    yAxis: { type: 'value', name: '可报专业数' },
    series,
  }
})

const compareTips = computed(() => {
  const items = volunteerStore.subjectCompareResult?.items || []
  if (items.length < 2) return []
  const tips = []
  const sorted = [...items].sort((a, b) => b.eligible_rate - a.eligible_rate)
  tips.push({
    type: 'success',
    text: `覆盖率最高的组合是「${sorted[0].combination_label}」，可报专业 ${sorted[0].eligible_majors} 个，覆盖率 ${(sorted[0].eligible_rate * 100).toFixed(1)}%。`,
  })
  if (sorted.length >= 2) {
    const diff = sorted[0].eligible_majors - sorted[sorted.length - 1].eligible_majors
    tips.push({
      type: 'warning',
      text: `覆盖率最高与最低组合相差 ${diff} 个专业，选科组合对专业选择范围有显著影响。`,
    })
  }
  const physicsCombo = sorted.find((i) => i.combination.includes('物理'))
  const historyCombo = sorted.find((i) => i.combination.includes('历史'))
  if (physicsCombo && historyCombo) {
    tips.push({
      type: 'primary',
      text: `含「物理」组合（${physicsCombo.eligible_majors}个）相比含「历史」组合（${historyCombo.eligible_majors}个），理工类专业可选范围明显更大。`,
    })
  }
  tips.push({
    type: 'info',
    text: '建议结合个人兴趣、职业规划和目标院校的具体专业要求综合决策，不要仅以覆盖率作为唯一标准。',
  })
  return tips
})

onMounted(async () => {
  await volunteerStore.loadMeta()
  await volunteerStore.fetchColleges({ limit: 100 })
})

function onComboChange(val) {
  if (val) {
    analysisForm.value.subjects = val.split('+')
  }
}

function onSubjectsChange() {
  analysisForm.value.combo = ''
}

function isInTargetColleges(id) {
  return targetColleges.value.some((c) => c.id === id)
}

function toggleTargetCollege(college) {
  if (isInTargetColleges(college.id)) {
    removeTargetCollege(college.id)
  } else {
    targetColleges.value.push(college)
  }
}

function removeTargetCollege(id) {
  const idx = targetColleges.value.findIndex((c) => c.id === id)
  if (idx >= 0) targetColleges.value.splice(idx, 1)
}

function isInCompareTargetColleges(id) {
  return compareTargetColleges.value.some((c) => c.id === id)
}

function toggleCompareTargetCollege(college) {
  if (isInCompareTargetColleges(college.id)) {
    removeCompareTargetCollege(college.id)
  } else {
    compareTargetColleges.value.push(college)
  }
}

function removeCompareTargetCollege(id) {
  const idx = compareTargetColleges.value.findIndex((c) => c.id === id)
  if (idx >= 0) compareTargetColleges.value.splice(idx, 1)
}

function searchColleges(kw) {
  if (!kw) {
    searchedColleges.value = []
    return
  }
  searchedColleges.value = volunteerStore.collegeList.filter(
    (c) => c.name.includes(kw)
  ).slice(0, 20)
}

function searchCompareColleges(kw) {
  if (!kw) {
    compareSearchedColleges.value = []
    return
  }
  compareSearchedColleges.value = volunteerStore.collegeList.filter(
    (c) => c.name.includes(kw)
  ).slice(0, 20)
}

async function handleAnalyze() {
  if (!currentSubjects.value.length) {
    ElMessage.warning('请选择选科组合')
    return
  }
  try {
    await volunteerStore.analyzeSubjects(
      currentSubjects.value,
      analysisForm.value.province || undefined,
      targetColleges.value.map((c) => c.id)
    )
    ElMessage.success('分析完成')
  } catch (e) {
    ElMessage.error('分析失败')
  }
}

function resetAnalysis() {
  analysisForm.value = {
    province: '',
    selectMode: 'combo',
    combo: '',
    subjects: [],
  }
  targetColleges.value = []
  volunteerStore.subjectAnalysisResult = null
}

function addCombination() {
  if (compareForm.value.combinations.length < 3) {
    compareForm.value.combinations.push('')
  }
}

function removeCombination(idx) {
  compareForm.value.combinations.splice(idx, 1)
}

async function handleCompare() {
  const validCombos = compareForm.value.combinations
    .filter((c) => c)
    .map((c) => c.split('+'))
  if (validCombos.length < 2) {
    ElMessage.warning('请至少选择 2 个选科组合进行对比')
    return
  }
  try {
    await volunteerStore.compareSubjectCombinations(
      validCombos,
      compareForm.value.province || undefined,
      compareTargetColleges.value.map((c) => c.id)
    )
    ElMessage.success('对比完成')
  } catch (e) {
    ElMessage.error('对比失败')
  }
}

function resetCompare() {
  compareForm.value = {
    province: '',
    combinations: ['', ''],
  }
  compareTargetColleges.value = []
  volunteerStore.subjectCompareResult = null
}

function goMajorDetail(major) {
  ElMessage.info(`专业百科详情页：${major.name}（已接入专业百科模块）`)
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
  if (rate >= 0.8) return '#22c55e'
  if (rate >= 0.5) return '#3b82f6'
  if (rate >= 0.3) return '#f59e0b'
  return '#ef4444'
}
</script>

<style scoped>
.hero-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #f0f9ff 0%, #fef3c7 100%);
  border-radius: 12px;
  padding: 32px;
  margin-bottom: 20px;
}

.hero-title {
  font-size: 26px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 10px 0;
}

.hero-desc {
  font-size: 14px;
  color: #64748b;
  line-height: 1.7;
  max-width: 600px;
  margin: 0;
}

.hero-right {
  opacity: 0.7;
}

.main-tabs {
  margin-bottom: 20px;
}

.section-title {
  font-size: 18px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 20px 0;
}

.sub-title {
  font-size: 16px;
  font-weight: 600;
  color: #334155;
  margin: 24px 0 16px 0;
}

.target-colleges-wrap {
  display: flex;
  flex-wrap: wrap;
  align-items: center;
  gap: 4px;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
}

.stat-box {
  background: #fff;
  border-radius: 10px;
  padding: 18px 20px;
  text-align: center;
  border-left: 4px solid #cbd5e1;
}

.stat-box.total { border-left-color: #64748b; }
.stat-box.eligible { border-left-color: #22c55e; }
.stat-box.ineligible { border-left-color: #ef4444; }
.stat-box.rate { border-left-color: #3b82f6; }

.stat-title {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 6px;
}

.stat-num {
  font-size: 30px;
  font-weight: 700;
  color: #1e293b;
}

.stat-box.eligible .stat-num { color: #22c55e; }
.stat-box.ineligible .stat-num { color: #ef4444; }
.stat-box.rate .stat-num { color: #3b82f6; }

.stat-desc {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.college-stats-wrap {
  margin-top: 24px;
}

.group-title {
  display: flex;
  align-items: center;
  font-size: 15px;
  font-weight: 600;
}

.group-name {
  color: #1e293b;
}

.major-list {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 10px;
}

.major-item {
  padding: 12px 14px;
  background: #f8fafc;
  border-radius: 8px;
  border-left: 3px solid #22c55e;
  transition: all 0.2s;
}

.major-item.ineligible {
  border-left-color: #ef4444;
  background: #fef2f2;
}

.major-item:hover {
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
}

.major-main {
  display: flex;
  align-items: center;
  flex-wrap: wrap;
  gap: 4px;
  margin-bottom: 4px;
}

.major-status {
  font-size: 14px;
}

.major-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  cursor: pointer;
}

.major-name:hover {
  color: #2563eb;
}

.college-tag {
  font-size: 12px;
  color: #64748b;
  margin-left: 8px;
}

.major-reason {
  font-size: 12px;
  color: #dc2626;
  margin-top: 2px;
  padding-left: 22px;
}

.major-requirements {
  font-size: 12px;
  color: #64748b;
  padding-left: 22px;
}

.req-label {
  color: #94a3b8;
}

.combination-editors {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-top: 8px;
}

.combo-editor {
  background: #f8fafc;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
}

.combo-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 10px;
}

.combo-label {
  font-size: 14px;
  font-weight: 600;
  color: #475569;
}

.compare-stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(240px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.compare-stat-card {
  padding: 18px 20px;
  border-radius: 12px;
  border: 2px solid;
}

.compare-stat-card.color-0 {
  background: #eff6ff;
  border-color: #3b82f6;
}
.compare-stat-card.color-1 {
  background: #fffbeb;
  border-color: #f59e0b;
}
.compare-stat-card.color-2 {
  background: #f0fdf4;
  border-color: #22c55e;
}

.compare-combo-label {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 14px;
  text-align: center;
}

.compare-stats-row {
  display: flex;
  justify-content: space-around;
}

.compare-stat-item {
  text-align: center;
}

.cs-value {
  font-size: 26px;
  font-weight: 700;
}
.cs-value.ok { color: #22c55e; }
.cs-value.no { color: #ef4444; }
.cs-value.rate { color: #3b82f6; }

.cs-label {
  font-size: 12px;
  color: #64748b;
  margin-top: 2px;
}

.compare-chart-wrap {
  margin-top: 24px;
}

.compare-chart {
  height: 340px;
}

.compare-summary {
  margin-top: 24px;
  padding: 16px 20px;
  background: #f8fafc;
  border-radius: 10px;
}

.college-picker-list {
  max-height: 400px;
  overflow-y: auto;
}

.picker-college-item {
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 10px 14px;
  border-radius: 8px;
  cursor: pointer;
  margin-bottom: 6px;
  transition: all 0.2s;
  border: 1px solid #e2e8f0;
}

.picker-college-item:hover {
  background: #f1f5f9;
}

.picker-college-item.selected {
  background: #eff6ff;
  border-color: #3b82f6;
}

.college-picker-name {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
}

.college-picker-meta {
  font-size: 12px;
  color: #64748b;
  margin-left: 12px;
}

.empty-tip {
  padding: 20px 0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .major-list {
    grid-template-columns: 1fr;
  }
}
</style>

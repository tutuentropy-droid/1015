<template>
  <div class="page-container">
    <template v-if="volunteerStore.volunteerPlan">
      <div class="plan-header-card section-card">
        <div class="plan-head">
          <div>
            <h1 class="plan-title">🎓 志愿填报方案</h1>
            <p class="plan-subtitle">
              {{ volunteerStore.volunteerPlan.user_input.province }} 考生 ·
              {{ volunteerStore.volunteerPlan.user_input.score }} 分 ·
              位次 {{ volunteerStore.volunteerPlan.user_input.rank }} ·
              {{ volunteerStore.volunteerPlan.user_input.subject_combination }}
            </p>
          </div>
          <el-button type="success" size="large" :loading="volunteerStore.loading.pdf" @click="handleExport">
            <el-icon><Download /></el-icon>
            <span>导出 PDF</span>
          </el-button>
        </div>

        <div class="stats-grid">
          <div class="stat-box reach">
            <div class="stat-title">冲</div>
            <div class="stat-num">{{ volunteerStore.volunteerPlan.reach_count }}</div>
            <div class="stat-desc">冲刺院校（10%~45%）</div>
          </div>
          <div class="stat-box stable">
            <div class="stat-title">稳</div>
            <div class="stat-num">{{ volunteerStore.volunteerPlan.stable_count }}</div>
            <div class="stat-desc">稳妥院校（45%~80%）</div>
          </div>
          <div class="stat-box safe">
            <div class="stat-title">保</div>
            <div class="stat-num">{{ volunteerStore.volunteerPlan.safe_count }}</div>
            <div class="stat-desc">保底院校（80%+）</div>
          </div>
          <div class="stat-box success">
            <div class="stat-title">总成功率</div>
            <div class="stat-num">
              {{ (volunteerStore.volunteerPlan.overall_success_probability * 100).toFixed(1) }}%
            </div>
            <div class="stat-desc">综合录取概率</div>
          </div>
        </div>
      </div>

      <div class="section-card" style="margin-bottom: 20px">
        <VolunteerWarning
          :volunteers="volunteerStore.volunteerPlan.volunteers"
          :reach-count="volunteerStore.volunteerPlan.reach_count"
          :stable-count="volunteerStore.volunteerPlan.stable_count"
          :safe-count="volunteerStore.volunteerPlan.safe_count"
          :overall-success-probability="volunteerStore.volunteerPlan.overall_success_probability"
        />
      </div>

      <div class="section-card">
        <h2 class="section-title">推荐志愿顺序</h2>
        <div class="volunteer-list">
          <div
            v-for="item in volunteerStore.volunteerPlan.volunteers"
            :key="item.order"
            class="volunteer-item"
            :class="`cat-${categoryClass(item.category)}`"
          >
            <div class="item-left">
              <div class="order-badge" :class="`badge-${categoryClass(item.category)}`">
                {{ item.order }}
              </div>
              <div class="cat-tag" :class="`tag-${categoryClass(item.category)}`">
                {{ item.category }}
              </div>
            </div>
            <div class="item-main">
              <div class="item-header">
                <h3 class="college-name" @click="goDetail(item.college.id)">
                  {{ item.college.name }}
                </h3>
                <div class="header-actions">
                  <el-button
                    :type="volunteerStore.isInCompare(item.college.id) ? 'success' : 'warning'"
                    link
                    size="small"
                    @click.stop="handleToggleCompare(item.college)"
                  >
                    {{ volunteerStore.isInCompare(item.college.id) ? '已加入对比' : '加入对比' }}
                  </el-button>
                  <div class="prob-wrap">
                    <div class="probability-bar" style="width: 180px">
                      <div
                        class="inner"
                        :style="{ width: `${item.probability * 100}%`, background: probColor(item.probability) }"
                      ></div>
                    </div>
                    <span class="prob-value" :style="{ color: probColor(item.probability) }">
                      {{ (item.probability * 100).toFixed(1) }}%
                    </span>
                  </div>
                </div>
              </div>
              <div class="item-meta">
                <span>📍 {{ item.college.province }} {{ item.college.city }}</span>
                <span class="dot">·</span>
                <span>{{ item.college.level }}</span>
                <span class="dot">·</span>
                <span>{{ item.college.college_type }}</span>
              </div>
              <div class="item-major">
                <span class="major-label">📚 推荐专业：</span>
                <span class="major-name">{{ item.recommended_major.name }}</span>
              </div>
              <div class="item-major-desc">
                <span class="sub">就业：</span>
                {{ item.recommended_major.employment_direction?.join('、') }}
              </div>
              <div class="item-prediction">
                <div>
                  <span class="sub">预估位次：</span>
                  <b>{{ item.predicted_rank }}</b>
                </div>
                <div>
                  <span class="sub">预估分数：</span>
                  <b>{{ item.predicted_score }}</b>
                </div>
                <div>
                  <span class="sub">大小年：</span>
                  {{ item.size_year_pattern }}
                </div>
                <div>
                  <span class="sub">调剂：</span>
                  {{ item.adjustment_impact }}
                </div>
              </div>
              <el-collapse class="admission-collapse">
                <el-collapse-item :title="`📊 查看历年录取趋势与数据`" :name="String(item.order)">
                  <div style="margin-bottom: 16px">
                    <ScoreTrendChart
                      :admission-data="item.college.admission_data || []"
                      :college-name="item.college.name"
                      :user-score="volunteerStore.volunteerPlan.user_input.score"
                      :user-rank="volunteerStore.volunteerPlan.user_input.rank"
                    />
                  </div>
                  <el-table :data="(item.college.admission_data || []).slice(0, 9)" size="small" stripe>
                    <el-table-column prop="year" label="年份" width="80" />
                    <el-table-column prop="province" label="省份" width="100" />
                    <el-table-column prop="score" label="最低分" width="100" />
                    <el-table-column prop="rank" label="最低位次" width="120" />
                    <el-table-column prop="batch" label="批次" width="120" />
                    <el-table-column prop="subject_combination" label="选科" min-width="160" />
                  </el-table>
                </el-collapse-item>
              </el-collapse>
            </div>
          </div>
        </div>
      </div>

      <div class="section-card">
        <h2 class="section-title">🎯 平行志愿录取推演</h2>
        <el-alert type="info" :closable="false" show-icon style="margin-bottom: 16px">
          <template #title>
            基于去年（参考年份）分数线，按照平行志愿投档规则模拟真实录取流程。
            你可以调整志愿顺序后重新推演，对比不同排列方式的最终录取结果差异。
          </template>
        </el-alert>

        <div class="sim-header">
          <div class="sim-user-info">
            <el-tag type="primary">{{ volunteerStore.volunteerPlan.user_input.province }}</el-tag>
            <el-tag type="success">分数 {{ volunteerStore.volunteerPlan.user_input.score }}</el-tag>
            <el-tag type="warning">位次 {{ volunteerStore.volunteerPlan.user_input.rank }}</el-tag>
          </div>
          <div class="sim-header-actions">
            <el-button @click="resetSimVolunteers">
              <el-icon><Refresh /></el-icon>
              <span>恢复推荐顺序</span>
            </el-button>
            <el-button type="primary" :loading="volunteerStore.loading.simulation" @click="runSim">
              <el-icon><VideoPlay /></el-icon>
              <span>开始推演</span>
            </el-button>
          </div>
        </div>

        <div class="sim-layout">
          <div class="sim-left">
            <h3 class="sim-subtitle">📝 调整志愿顺序（点击箭头上下移动）</h3>
            <div class="sim-volunteer-list">
              <div
                v-for="(item, idx) in simVolunteers"
                :key="item.order + '_' + idx"
                class="sim-volunteer-item"
                :class="{ active: volunteerStore.simulationResult && getActiveStepVolunteerOrder() === item.order }"
              >
                <div class="sim-vol-left">
                  <div class="sim-order-badge" :class="`badge-${categoryClass(item.category)}`">
                    {{ item.order }}
                  </div>
                  <div class="sim-move-btns">
                    <el-button
                      size="small"
                      circle
                      :disabled="idx === 0"
                      @click="moveVolunteer(idx, -1)"
                    >
                      <el-icon><ArrowUp /></el-icon>
                    </el-button>
                    <el-button
                      size="small"
                      circle
                      :disabled="idx === simVolunteers.length - 1"
                      @click="moveVolunteer(idx, 1)"
                    >
                      <el-icon><ArrowDown /></el-icon>
                    </el-button>
                  </div>
                </div>
                <div class="sim-vol-main">
                  <div class="sim-college-name">{{ item.college.name }}</div>
                  <div class="sim-major-row">
                    <el-icon><Notebook /></el-icon>
                    <span class="sim-major-name">{{ item.recommended_major.name }}</span>
                  </div>
                  <div class="sim-accept-row">
                    <el-checkbox v-model="item.accept_adjustment" size="small">
                      服从专业调剂
                    </el-checkbox>
                  </div>
                </div>
                <div class="sim-vol-right">
                  <div class="sim-cat-tag" :class="`tag-${categoryClass(item.category)}`">
                    {{ item.category }}
                  </div>
                  <div class="sim-prob" :style="{ color: probColor(item.probability) }">
                    {{ (item.probability * 100).toFixed(0) }}%
                  </div>
                </div>
              </div>
            </div>
          </div>

          <div class="sim-right">
            <div class="sim-tabs">
              <el-radio-group v-model="simRightTab" size="default">
                <el-radio-button label="process">推演过程</el-radio-button>
                <el-radio-button label="compare">结果对比</el-radio-button>
              </el-radio-group>
            </div>

            <div v-if="simRightTab === 'process'" class="sim-process">
              <template v-if="!volunteerStore.simulationResult">
                <el-empty description="点击「开始推演」按钮，查看平行志愿投档录取全过程" />
              </template>
              <template v-else>
                <div class="sim-result-summary" :class="volunteerStore.simulationResult.success ? 'success' : 'fail'">
                  <div class="sim-result-icon">
                    {{ volunteerStore.simulationResult.success ? '🎉' : '⚠️' }}
                  </div>
                  <div class="sim-result-text">{{ volunteerStore.simulationResult.summary }}</div>
                  <el-button
                    size="small"
                    type="primary"
                    plain
                    @click="handleSaveHistory"
                    style="margin-top: 8px"
                  >
                    保存本次结果用于对比
                  </el-button>
                </div>

                <div class="sim-step-controls">
                  <el-button size="small" :disabled="currentStepIndex <= 0" @click="prevStep">
                    <el-icon><ArrowLeft /></el-icon>
                    <span>上一步</span>
                  </el-button>
                  <span class="sim-step-counter">
                    步骤 {{ currentStepIndex + 1 }} / {{ volunteerStore.simulationResult.steps.length }}
                  </span>
                  <el-button
                    size="small"
                    :disabled="currentStepIndex >= volunteerStore.simulationResult.steps.length - 1"
                    @click="nextStep"
                  >
                    <span>下一步</span>
                    <el-icon><ArrowRight /></el-icon>
                  </el-button>
                  <el-button size="small" @click="playAllSteps" :disabled="isPlaying">
                    <el-icon><VideoPlay /></el-icon>
                    <span>{{ isPlaying ? '播放中...' : '自动播放' }}</span>
                  </el-button>
                </div>

                <div class="sim-steps">
                  <div
                    v-for="(step, idx) in volunteerStore.simulationResult.steps"
                    :key="step.step_index"
                    class="sim-step"
                    :class="{
                      active: idx === currentStepIndex,
                      done: idx < currentStepIndex,
                      final: step.is_final,
                      [`step-${step.step_type}`]: true,
                    }"
                    @click="setCurrentStep(idx)"
                  >
                    <div class="sim-step-dot">
                      <div class="dot-inner">
                        <span v-if="step.step_type === 'ADMITTED'">✓</span>
                        <span v-else-if="step.step_type === 'WITHDRAW'">✗</span>
                        <span v-else-if="step.passed === true">✓</span>
                        <span v-else-if="step.passed === false">✗</span>
                        <span v-else>{{ idx + 1 }}</span>
                      </div>
                    </div>
                    <div class="sim-step-content">
                      <div class="sim-step-title">{{ step.title }}</div>
                      <div v-if="idx <= currentStepIndex" class="sim-step-desc">
                        {{ step.description }}
                        <div v-if="step.threshold_score && idx <= currentStepIndex" class="sim-step-threshold">
                          <div class="threshold-row">
                            <span>你的分数</span>
                            <b :class="step.user_score >= step.threshold_score ? 'pass' : 'fail'">
                              {{ step.user_score }} 分
                            </b>
                            <span>→</span>
                            <span>投档线</span>
                            <b>{{ step.threshold_score }} 分</b>
                          </div>
                          <div class="threshold-row">
                            <span>你的位次</span>
                            <b :class="step.user_rank <= step.threshold_rank ? 'pass' : 'fail'">
                              {{ step.user_rank }}
                            </b>
                            <span>→</span>
                            <span>投档位次</span>
                            <b>{{ step.threshold_rank }}</b>
                          </div>
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
              </template>
            </div>

            <div v-else class="sim-compare">
              <template v-if="volunteerStore.simulationHistory.length === 0">
                <el-empty description="暂无历史推演结果，请先推演并保存结果" />
              </template>
              <template v-else>
                <div class="sim-compare-header">
                  <span>已保存 {{ volunteerStore.simulationHistory.length }} 个推演方案</span>
                  <el-button size="small" type="danger" plain @click="volunteerStore.clearSimulationHistory()">
                    清空对比
                  </el-button>
                </div>
                <el-table :data="volunteerStore.simulationHistory" stripe size="small">
                  <el-table-column label="方案" width="140">
                    <template #default="{ row }">
                      <el-input
                        v-model="row.label"
                        size="small"
                        placeholder="方案名称"
                      />
                    </template>
                  </el-table-column>
                  <el-table-column label="录取结果">
                    <template #default="{ row }">
                      <el-tag :type="row.result.success ? 'success' : 'danger'" size="small">
                        {{ row.result.success ? '录取成功' : '未录取/退档' }}
                      </el-tag>
                      <span v-if="row.result.success" style="margin-left: 8px; font-size: 13px">
                        第{{ row.result.admitted_order }}志愿 · {{ row.result.admitted_college }} · {{ row.result.admitted_major }}
                      </span>
                      <span v-else style="margin-left: 8px; font-size: 13px; color: #64748b">
                        {{ row.result.summary }}
                      </span>
                    </template>
                  </el-table-column>
                  <el-table-column label="推演时间" width="170" prop="createdAt" />
                  <el-table-column label="操作" width="120">
                    <template #default="{ $index }">
                      <el-button
                        size="small"
                        type="danger"
                        link
                        @click="removeHistory($index)"
                      >
                        删除
                      </el-button>
                    </template>
                  </el-table-column>
                </el-table>

                <div v-if="volunteerStore.simulationHistory.length >= 2" class="sim-compare-insight">
                  <el-alert type="warning" :closable="false" show-icon>
                    <template #title>
                      💡 对比洞察：不同志愿顺序可能导致完全不同的录取结果。
                      平行志愿按照「分数优先、遵循志愿、一轮投档」原则，
                      将最想去的学校放在前面，同时确保保底院校放在最后，是最优策略。
                    </template>
                  </el-alert>
                </div>
              </template>
            </div>
          </div>
        </div>
      </div>

      <div class="section-card">
        <h2 class="section-title">📋 报考建议</h2>
        <el-alert type="info" :closable="false" show-icon style="margin-bottom: 12px">
          <template #title>
            <b>重要提示：</b>本方案基于历年数据通过 AI 模型预测生成，仅供参考，最终填报请结合官方招生简章和本省考试院最新信息。
          </template>
        </el-alert>
        <el-timeline>
          <el-timeline-item timestamp="梯度原则" type="primary" size="large">
            建议遵循"冲-稳-保"的梯度原则，志愿之间保持合理分差，不要全部填报同一层次院校。
          </el-timeline-item>
          <el-timeline-item timestamp="服从调剂" type="warning" size="large">
            建议勾选"服从调剂"，以降低退档风险，特别是对于冲刺类院校。
          </el-timeline-item>
          <el-timeline-item timestamp="选科要求" type="success" size="large">
            注意检查目标院校和专业的选科要求、身体条件、外语语种等特殊限制。
          </el-timeline-item>
          <el-timeline-item timestamp="就业方向" type="danger" size="large">
            结合个人兴趣和职业规划选择专业，不要盲目跟风热门专业。
          </el-timeline-item>
        </el-timeline>
      </div>
    </template>
    <div v-else class="empty-tip">
      <el-empty description="尚未生成志愿方案">
        <el-button type="primary" @click="$router.push('/')">去生成方案</el-button>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { ref, reactive, watch, onMounted, onBeforeUnmount } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import {
  Download, Refresh, VideoPlay, ArrowUp, ArrowDown,
  ArrowLeft, ArrowRight, Notebook
} from '@element-plus/icons-vue'
import { useVolunteerStore } from '../stores/volunteer'
import ScoreTrendChart from '../components/ScoreTrendChart.vue'
import VolunteerWarning from '../components/VolunteerWarning.vue'

const router = useRouter()
const volunteerStore = useVolunteerStore()

onMounted(() => {
  volunteerStore.loadMeta()
})

const simRightTab = ref('process')
const simVolunteers = ref([])
const currentStepIndex = ref(0)
const isPlaying = ref(false)
let playTimer = null

watch(
  () => volunteerStore.volunteerPlan,
  (plan) => {
    if (plan) {
      resetSimVolunteers()
    }
  },
  { immediate: true }
)

onBeforeUnmount(() => {
  if (playTimer) clearInterval(playTimer)
})

function resetSimVolunteers() {
  if (!volunteerStore.volunteerPlan) return
  simVolunteers.value = volunteerStore.volunteerPlan.volunteers.map((v, idx) => ({
    ...JSON.parse(JSON.stringify(v)),
    order: idx + 1,
    accept_adjustment: volunteerStore.volunteerPlan.user_input.accept_adjustment,
  }))
  volunteerStore.clearSimulation()
  currentStepIndex.value = 0
}

function moveVolunteer(idx, direction) {
  const arr = simVolunteers.value
  const targetIdx = idx + direction
  if (targetIdx < 0 || targetIdx >= arr.length) return
  const temp = arr[idx]
  arr[idx] = arr[targetIdx]
  arr[targetIdx] = temp
  arr.forEach((item, i) => {
    item.order = i + 1
  })
  simVolunteers.value = [...arr]
}

async function runSim() {
  if (!volunteerStore.volunteerPlan) return
  const userInput = volunteerStore.volunteerPlan.user_input
  const volunteers = simVolunteers.value.map((v) => ({
    order: v.order,
    college_id: v.college.id,
    college_name: v.college.name,
    major_id: v.recommended_major?.id,
    major_name: v.recommended_major?.name,
    accept_adjustment: v.accept_adjustment,
  }))
  try {
    await volunteerStore.runSimulation({
      province: userInput.province,
      score: userInput.score,
      rank: userInput.rank,
      subject_combination: userInput.subject_combination,
      volunteers,
      reference_year: 2025,
    })
    currentStepIndex.value = 0
    simRightTab.value = 'process'
    ElMessage.success('推演完成！')
  } catch (e) {
    ElMessage.error(e.message || '推演失败')
  }
}

function getActiveStepVolunteerOrder() {
  if (!volunteerStore.simulationResult) return -1
  const step = volunteerStore.simulationResult.steps[currentStepIndex.value]
  return step ? step.volunteer_order : -1
}

function setCurrentStep(idx) {
  currentStepIndex.value = idx
}

function prevStep() {
  if (currentStepIndex.value > 0) {
    currentStepIndex.value--
  }
}

function nextStep() {
  if (volunteerStore.simulationResult &&
      currentStepIndex.value < volunteerStore.simulationResult.steps.length - 1) {
    currentStepIndex.value++
  }
}

function playAllSteps() {
  if (!volunteerStore.simulationResult) return
  isPlaying.value = true
  currentStepIndex.value = 0
  if (playTimer) clearInterval(playTimer)
  playTimer = setInterval(() => {
    if (currentStepIndex.value >= volunteerStore.simulationResult.steps.length - 1) {
      clearInterval(playTimer)
      playTimer = null
      isPlaying.value = false
      return
    }
    currentStepIndex.value++
  }, 1800)
}

function handleSaveHistory() {
  const defaultLabel = `方案${volunteerStore.simulationHistory.length + 1}`
  volunteerStore.saveSimulationToHistory(defaultLabel, simVolunteers.value)
  ElMessage.success('已保存到对比列表')
  simRightTab.value = 'compare'
}

function removeHistory(idx) {
  volunteerStore.simulationHistory.splice(idx, 1)
}

function categoryClass(cat) {
  const map = { 冲: 'reach', 稳: 'stable', 保: 'safe' }
  return map[cat] || 'stable'
}

function probColor(p) {
  if (p >= 0.8) return '#22c55e'
  if (p >= 0.45) return '#f59e0b'
  return '#ef4444'
}

function goDetail(id) {
  router.push(`/colleges/${id}`)
}

async function handleExport() {
  try {
    await volunteerStore.exportPdf()
    ElMessage.success('PDF 下载成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
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

<style scoped>
.plan-header-card {
  background: linear-gradient(135deg, #eff6ff 0%, #f0fdfa 100%);
  border-radius: 12px;
}

.plan-head {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
}

.plan-title {
  font-size: 26px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px 0;
}

.plan-subtitle {
  font-size: 14px;
  color: #64748b;
  margin: 0;
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

.stat-box.reach { border-left-color: #ef4444; }
.stat-box.stable { border-left-color: #f59e0b; }
.stat-box.safe { border-left-color: #22c55e; }
.stat-box.success { border-left-color: #2563eb; }

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

.stat-box.reach .stat-num { color: #ef4444; }
.stat-box.stable .stat-num { color: #f59e0b; }
.stat-box.safe .stat-num { color: #22c55e; }
.stat-box.success .stat-num { color: #2563eb; }

.stat-desc {
  font-size: 12px;
  color: #94a3b8;
  margin-top: 4px;
}

.volunteer-list {
  display: flex;
  flex-direction: column;
  gap: 16px;
}

.volunteer-item {
  display: flex;
  gap: 20px;
  padding: 20px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  border-left: 5px solid #94a3b8;
  transition: all 0.2s;
}

.volunteer-item:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.06);
}

.volunteer-item.cat-reach { border-left-color: #ef4444; }
.volunteer-item.cat-stable { border-left-color: #f59e0b; }
.volunteer-item.cat-safe { border-left-color: #22c55e; }

.item-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
  min-width: 56px;
}

.order-badge {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  font-weight: 700;
  color: #fff;
}

.badge-reach { background: #ef4444; }
.badge-stable { background: #f59e0b; }
.badge-safe { background: #22c55e; }

.cat-tag {
  padding: 2px 10px;
  border-radius: 10px;
  font-size: 12px;
  font-weight: 600;
}

.tag-reach { background: #fef2f2; color: #dc2626; }
.tag-stable { background: #fffbeb; color: #d97706; }
.tag-safe { background: #f0fdf4; color: #16a34a; }

.item-main {
  flex: 1;
  min-width: 0;
}

.item-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
  gap: 16px;
}

.header-actions {
  display: flex;
  align-items: center;
  gap: 12px;
}

.college-name {
  font-size: 18px;
  font-weight: 700;
  color: #1e293b;
  margin: 0;
  cursor: pointer;
}

.college-name:hover {
  color: #2563eb;
}

.prob-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.prob-value {
  font-size: 18px;
  font-weight: 700;
  min-width: 65px;
  text-align: right;
}

.item-meta {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
}

.dot {
  margin: 0 8px;
  color: #cbd5e1;
}

.item-major {
  font-size: 14px;
  color: #334155;
  margin-bottom: 4px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.major-label {
  color: #64748b;
}

.major-name {
  font-weight: 600;
  color: #1e293b;
}

.item-major-desc {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 10px;
  padding-left: 20px;
}

.sub {
  color: #94a3b8;
}

.item-prediction {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 8px 24px;
  font-size: 13px;
  color: #475569;
  margin-bottom: 10px;
}

.admission-collapse {
  margin-top: 6px;
  --el-collapse-border-color: #e2e8f0;
}

@media (max-width: 768px) {
  .stats-grid {
    grid-template-columns: repeat(2, 1fr);
  }
  .item-prediction {
    grid-template-columns: 1fr;
  }
  .item-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }
}

.sim-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  flex-wrap: wrap;
  gap: 12px;
}

.sim-user-info {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.sim-header-actions {
  display: flex;
  gap: 10px;
}

.sim-layout {
  display: grid;
  grid-template-columns: 380px 1fr;
  gap: 24px;
}

.sim-subtitle {
  font-size: 15px;
  font-weight: 600;
  color: #334155;
  margin: 0 0 14px 0;
}

.sim-volunteer-list {
  display: flex;
  flex-direction: column;
  gap: 10px;
  max-height: 720px;
  overflow-y: auto;
  padding-right: 4px;
}

.sim-volunteer-item {
  display: flex;
  align-items: center;
  gap: 12px;
  padding: 12px 14px;
  background: #fff;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  border-left: 4px solid #cbd5e1;
  transition: all 0.25s;
}

.sim-volunteer-item.active {
  border-color: #2563eb;
  box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.12);
  transform: translateX(3px);
}

.sim-volunteer-item.cat-reach { border-left-color: #ef4444; }
.sim-volunteer-item.cat-stable { border-left-color: #f59e0b; }
.sim-volunteer-item.cat-safe { border-left-color: #22c55e; }

.sim-vol-left {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 6px;
  min-width: 48px;
}

.sim-order-badge {
  width: 38px;
  height: 38px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  font-weight: 700;
  color: #fff;
}

.sim-move-btns {
  display: flex;
  flex-direction: column;
  gap: 3px;
}

.sim-vol-main {
  flex: 1;
  min-width: 0;
}

.sim-college-name {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sim-major-row {
  display: flex;
  align-items: center;
  gap: 4px;
  font-size: 12px;
  color: #64748b;
  margin-bottom: 4px;
}

.sim-major-name {
  font-weight: 500;
  color: #334155;
}

.sim-accept-row {
  font-size: 12px;
}

.sim-vol-right {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 4px;
  min-width: 54px;
}

.sim-cat-tag {
  padding: 2px 8px;
  border-radius: 8px;
  font-size: 11px;
  font-weight: 600;
}

.sim-prob {
  font-size: 15px;
  font-weight: 700;
}

.sim-right {
  display: flex;
  flex-direction: column;
  min-width: 0;
}

.sim-tabs {
  margin-bottom: 16px;
}

.sim-process, .sim-compare {
  flex: 1;
}

.sim-result-summary {
  padding: 18px 20px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  gap: 14px;
  margin-bottom: 16px;
  border: 1px solid;
}

.sim-result-summary.success {
  background: #f0fdf4;
  border-color: #bbf7d0;
}

.sim-result-summary.fail {
  background: #fef2f2;
  border-color: #fecaca;
}

.sim-result-icon {
  font-size: 34px;
  flex-shrink: 0;
}

.sim-result-text {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  flex: 1;
}

.sim-step-controls {
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 14px;
  margin-bottom: 18px;
  padding: 10px;
  background: #f8fafc;
  border-radius: 10px;
}

.sim-step-counter {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
  min-width: 90px;
  text-align: center;
}

.sim-steps {
  position: relative;
  padding-left: 6px;
  max-height: 560px;
  overflow-y: auto;
}

.sim-step {
  display: flex;
  gap: 14px;
  padding: 12px 12px 12px 0;
  cursor: pointer;
  position: relative;
  transition: all 0.2s;
  border-radius: 8px;
}

.sim-step:hover {
  background: #f8fafc;
}

.sim-step.active {
  background: #eff6ff;
}

.sim-step.done .sim-step-title {
  color: #64748b;
}

.sim-step.final {
  background: #fffbeb;
}

.sim-step-dot {
  position: relative;
  flex-shrink: 0;
  width: 34px;
  display: flex;
  justify-content: center;
  z-index: 1;
}

.sim-step:not(:last-child) .sim-step-dot::after {
  content: '';
  position: absolute;
  left: 50%;
  top: 34px;
  bottom: -12px;
  width: 2px;
  background: #e2e8f0;
  transform: translateX(-50%);
}

.sim-step.done:not(:last-child) .sim-step-dot::after {
  background: #94a3b8;
}

.sim-step.active:not(:last-child) .sim-step-dot::after {
  background: #2563eb;
}

.dot-inner {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: #fff;
  border: 2px solid #cbd5e1;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 12px;
  font-weight: 700;
  color: #94a3b8;
}

.sim-step.done .dot-inner {
  background: #e2e8f0;
  border-color: #94a3b8;
  color: #475569;
}

.sim-step.active .dot-inner {
  background: #2563eb;
  border-color: #2563eb;
  color: #fff;
  transform: scale(1.1);
  box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.18);
}

.sim-step.step-ADMITTED .dot-inner,
.sim-step.step-ADMITTED.active .dot-inner {
  background: #22c55e;
  border-color: #22c55e;
  color: #fff;
}

.sim-step.step-WITHDRAW .dot-inner,
.sim-step.step-WITHDRAW.active .dot-inner {
  background: #ef4444;
  border-color: #ef4444;
  color: #fff;
}

.sim-step.step-THRESHOLD_CHECK.active .dot-inner,
.sim-step.step-MAJOR_CHECK.active .dot-inner {
  background: #2563eb;
}

.sim-step.step-ADJUSTMENT.active .dot-inner {
  background: #f59e0b;
  border-color: #f59e0b;
}

.sim-step-content {
  flex: 1;
  min-width: 0;
}

.sim-step-title {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  margin-bottom: 4px;
}

.sim-step-desc {
  font-size: 13px;
  color: #475569;
  line-height: 1.6;
}

.sim-step-threshold {
  margin-top: 10px;
  padding: 10px 12px;
  background: #fff;
  border-radius: 8px;
  border: 1px solid #e2e8f0;
}

.threshold-row {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 12px;
  color: #64748b;
  padding: 3px 0;
}

.threshold-row b {
  font-size: 13px;
  min-width: 70px;
}

.threshold-row b.pass {
  color: #22c55e;
}

.threshold-row b.fail {
  color: #ef4444;
}

.sim-compare-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 14px;
  font-size: 14px;
  color: #475569;
  font-weight: 500;
}

.sim-compare-insight {
  margin-top: 16px;
}

@media (max-width: 1100px) {
  .sim-layout {
    grid-template-columns: 1fr;
  }
}
</style>

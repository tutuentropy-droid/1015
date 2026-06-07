<template>
  <div class="page-container">
    <div class="hero-banner section-card">
      <div class="hero-left">
        <h1 class="hero-title">智能高考志愿填报助手</h1>
        <p class="hero-desc">
          基于近三年录取数据，结合线性回归预测模型，智能分析冲稳保梯度，
          为您生成科学合理的志愿填报方案。
        </p>
        <div class="hero-actions">
          <el-button type="primary" size="large" @click="scrollToForm">
            <el-icon><MagicStick /></el-icon>
            <span>立即生成方案</span>
          </el-button>
          <el-button size="large" @click="$router.push('/subject-analysis')" style="margin-left: 12px">
            <span style="margin-right: 4px">📚</span>
            <span>选科影响分析</span>
          </el-button>
        </div>
        <div class="hero-stats">
          <div class="stat-item">
            <div class="stat-number">{{ volunteerStore.provinces.length }}</div>
            <div class="stat-label">覆盖省份</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">150+</div>
            <div class="stat-label">院校数据</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">70+</div>
            <div class="stat-label">专业方向</div>
          </div>
          <div class="stat-item">
            <div class="stat-number">AI</div>
            <div class="stat-label">智能预测</div>
          </div>
        </div>
      </div>
      <div class="hero-right">
        <el-icon :size="140" color="#409eff"><DataAnalysis /></el-icon>
      </div>
    </div>

    <div class="section-card">
      <h2 class="section-title">填写你的高考信息</h2>
      <el-form
        ref="formRef"
        :model="volunteerStore.userInput"
        label-width="120px"
        label-position="right"
        size="default"
      >
        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="高考省份" required>
              <el-select
                v-model="volunteerStore.userInput.province"
                placeholder="请选择省份"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="p in volunteerStore.provinces"
                  :key="p"
                  :label="p"
                  :value="p"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="选科组合" required>
              <el-select
                v-model="volunteerStore.userInput.subject_combination"
                placeholder="请选择选科组合"
                filterable
                style="width: 100%"
              >
                <el-option
                  v-for="s in volunteerStore.subjectCombinations"
                  :key="s"
                  :label="s"
                  :value="s"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="高考分数" required>
              <el-input-number
                v-model="volunteerStore.userInput.score"
                :min="0"
                :max="750"
                placeholder="请输入高考总分"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="全省位次" required>
              <el-input-number
                v-model="volunteerStore.userInput.rank"
                :min="1"
                :max="500000"
                placeholder="请输入全省位次"
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="可接受城市">
              <el-select
                v-model="volunteerStore.userInput.acceptable_cities"
                multiple
                filterable
                placeholder="不选则默认全国"
                style="width: 100%"
              >
                <el-option
                  v-for="c in volunteerStore.cities"
                  :key="c"
                  :label="c"
                  :value="c"
                />
              </el-select>
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="意向专业方向">
              <el-select
                v-model="volunteerStore.userInput.target_major_directions"
                multiple
                filterable
                placeholder="不选则默认不限"
                style="width: 100%"
              >
                <el-option
                  v-for="d in volunteerStore.majorDirections"
                  :key="d"
                  :label="d"
                  :value="d"
                />
              </el-select>
            </el-form-item>
          </el-col>
        </el-row>

        <el-row :gutter="24">
          <el-col :span="12">
            <el-form-item label="志愿数量">
              <el-slider
                v-model="volunteerStore.userInput.volunteer_count"
                :min="5"
                :max="20"
                :step="1"
                show-input
                style="width: 100%"
              />
            </el-form-item>
          </el-col>
          <el-col :span="12">
            <el-form-item label="服从调剂">
              <el-switch
                v-model="volunteerStore.userInput.accept_adjustment"
                active-text="是（推荐）"
                inactive-text="否"
              />
            </el-form-item>
          </el-col>
        </el-row>

        <el-form-item>
          <el-button
            type="primary"
            size="large"
            :loading="volunteerStore.loading.plan"
            @click="handleGenerate"
          >
            <el-icon><MagicStick /></el-icon>
            <span>生成志愿方案</span>
          </el-button>
          <el-button
            size="large"
            :loading="volunteerStore.loading.predict"
            @click="handlePredict"
            style="margin-left: 12px"
          >
            <el-icon><Search /></el-icon>
            <span>筛选匹配院校</span>
          </el-button>
          <el-button size="large" @click="volunteerStore.resetUserInput()">
            <el-icon><Refresh /></el-icon>
            <span>重置</span>
          </el-button>
        </el-form-item>
      </el-form>
    </div>

    <div v-if="volunteerStore.predictions.length" class="section-card">
      <h2 class="section-title">匹配院校预测结果（{{ volunteerStore.predictions.length }} 所）</h2>
      <el-tabs v-model="activeTab">
        <el-tab-pane label="全部" name="all">
          <college-result-list :predictions="volunteerStore.predictions" />
        </el-tab-pane>
        <el-tab-pane :label="`冲 (${reachCount})`" name="reach">
          <college-result-list :predictions="volunteerStore.reachColleges" />
        </el-tab-pane>
        <el-tab-pane :label="`稳 (${stableCount})`" name="stable">
          <college-result-list :predictions="volunteerStore.stableColleges" />
        </el-tab-pane>
        <el-tab-pane :label="`保 (${safeCount})`" name="safe">
          <college-result-list :predictions="volunteerStore.safeColleges" />
        </el-tab-pane>
      </el-tabs>
    </div>

    <div v-if="volunteerStore.volunteerPlan" class="section-card">
      <div class="plan-header">
        <h2 class="section-title" style="margin-bottom: 0">✅ 志愿方案已生成</h2>
        <el-button type="success" :loading="volunteerStore.loading.pdf" @click="handleExport">
          <el-icon><Download /></el-icon>
          <span>导出 PDF</span>
        </el-button>
      </div>
      <div class="plan-overview">
        <div class="overview-item">
          <span class="overview-label">冲</span>
          <span class="overview-value reach">{{ volunteerStore.volunteerPlan.reach_count }} 所</span>
        </div>
        <div class="overview-item">
          <span class="overview-label">稳</span>
          <span class="overview-value stable">{{ volunteerStore.volunteerPlan.stable_count }} 所</span>
        </div>
        <div class="overview-item">
          <span class="overview-label">保</span>
          <span class="overview-value safe">{{ volunteerStore.volunteerPlan.safe_count }} 所</span>
        </div>
        <div class="overview-item">
          <span class="overview-label">综合成功率</span>
          <span class="overview-value success">
            {{ (volunteerStore.volunteerPlan.overall_success_probability * 100).toFixed(1) }}%
          </span>
        </div>
      </div>
      <el-button type="primary" plain @click="goPlan">查看完整方案 →</el-button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useVolunteerStore } from '../stores/volunteer'
import CollegeResultList from '../components/CollegeResultList.vue'

const router = useRouter()
const volunteerStore = useVolunteerStore()
const activeTab = ref('all')
const formRef = ref(null)

const reachCount = computed(() => volunteerStore.reachColleges.length)
const stableCount = computed(() => volunteerStore.stableColleges.length)
const safeCount = computed(() => volunteerStore.safeColleges.length)

onMounted(() => {
  volunteerStore.loadMeta()
})

async function handlePredict() {
  try {
    await volunteerStore.predictColleges()
    ElMessage.success(`找到 ${volunteerStore.predictions.length} 所匹配院校`)
  } catch (e) {
    ElMessage.error(e.message || '预测失败')
  }
}

async function handleGenerate() {
  try {
    await volunteerStore.generatePlan()
    ElMessage.success('志愿方案生成成功')
    router.push('/plan')
  } catch (e) {
    ElMessage.error(e.message || '方案生成失败')
  }
}

function goPlan() {
  router.push('/plan')
}

function scrollToForm() {
  const formCard = document.querySelector('.hero-banner')?.nextElementSibling
  if (formCard) {
    formCard.scrollIntoView({ behavior: 'smooth' })
  }
}

async function handleExport() {
  try {
    await volunteerStore.exportPdf()
    ElMessage.success('PDF 下载成功')
  } catch (e) {
    ElMessage.error('导出失败')
  }
}
</script>

<style scoped>
.hero-banner {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(135deg, #eff6ff 0%, #ecfeff 100%);
  border-radius: 12px;
  padding: 36px;
  margin-bottom: 24px;
}

.hero-title {
  font-size: 32px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 12px 0;
}

.hero-desc {
  font-size: 15px;
  color: #64748b;
  line-height: 1.7;
  margin: 0 0 24px 0;
  max-width: 600px;
}

.hero-actions {
  margin-bottom: 24px;
}

.hero-stats {
  display: flex;
  gap: 40px;
}

.stat-item {
  text-align: center;
}

.stat-number {
  font-size: 26px;
  font-weight: 700;
  color: #2563eb;
  line-height: 1.2;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-top: 4px;
}

.hero-right {
  opacity: 0.75;
}

.plan-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
}

.plan-overview {
  display: flex;
  gap: 32px;
  padding: 20px;
  background: #f8fafc;
  border-radius: 8px;
  margin-bottom: 16px;
}

.overview-item {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.overview-label {
  font-size: 13px;
  color: #94a3b8;
}

.overview-value {
  font-size: 22px;
  font-weight: 700;
}

.overview-value.reach { color: #ef4444; }
.overview-value.stable { color: #f59e0b; }
.overview-value.safe { color: #22c55e; }
.overview-value.success { color: #2563eb; }
</style>

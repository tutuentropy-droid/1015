<template>
  <div class="page-container">
    <template v-if="volunteerStore.volunteerPlan">
      <div class="plan-header-card section-card">
        <div class="plan-head">
          <div>
            <h1 class="plan-title">🎓 志愿填报方案</h1>
            <p class="plan-subtitle">
              {{ volunteerStore.volunteerPlan.userInput.province }} 考生 ·
              {{ volunteerStore.volunteerPlan.userInput.score }} 分 ·
              位次 {{ volunteerStore.volunteerPlan.userInput.rank }} ·
              {{ volunteerStore.volunteerPlan.userInput.subject_combination }}
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
              <div class="item-meta">
                <span>📍 {{ item.college.province }} {{ item.college.city }}</span>
                <span class="dot">·</span>
                <span>{{ item.college.level }}</span>
                <span class="dot">·</span>
                <span>{{ item.college.college_type }}</span>
              </div>
              <div class="item-major">
                <el-icon color="#409eff"><Reading /></el-icon>
                <span class="major-label">推荐专业：</span>
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
                <el-collapse-item :title="`查看近三年录取数据`" :name="item.order">
                  <el-table :data="item.college.admission_data.slice(0, 9)" size="small" stripe>
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
import { onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { ElMessage } from 'element-plus'
import { useVolunteerStore } from '../stores/volunteer'

const router = useRouter()
const volunteerStore = useVolunteerStore()

onMounted(() => {
  volunteerStore.loadMeta()
})

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
</style>

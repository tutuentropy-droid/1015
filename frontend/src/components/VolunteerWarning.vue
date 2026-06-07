<template>
  <div class="warning-panel">
    <div class="panel-header" @click="collapsed = !collapsed">
      <div class="header-left">
        <div class="header-icon" :class="{ 'has-warn': warnings.length > 0, 'all-good': warnings.length === 0 }">
          {{ warnings.length > 0 ? '⚠️' : '✅' }}
        </div>
        <div>
          <h3 class="panel-title">智能志愿风险检测</h3>
          <p class="panel-subtitle">
            <span v-if="warnings.length === 0">恭喜！志愿方案整体健康</span>
            <span v-else>共发现 {{ warnings.length }} 个风险点</span>
          </p>
        </div>
      </div>
      <el-icon class="collapse-icon" :class="{ expanded: !collapsed }">
        <ArrowDown />
      </el-icon>
    </div>

    <div v-show="!collapsed" class="panel-body">
      <div v-if="warnings.length === 0" class="all-good-box">
        <el-result icon="success" title="志愿方案合理" sub-title="冲-稳-保梯度搭配均衡，专业顺序合理，继续保持！">
          <template #extra>
            <el-tag type="success" size="large">🎯 录取概率：{{ successProbText }}</el-tag>
          </template>
        </el-result>
      </div>

      <div v-else class="warning-list">
        <div
          v-for="(w, idx) in warnings"
          :key="idx"
          class="warning-item"
          :class="`level-${w.level}`"
        >
          <div class="warn-icon">
            <el-icon v-if="w.level === 'danger'" color="#dc2626" :size="20"><CircleCloseFilled /></el-icon>
            <el-icon v-else-if="w.level === 'warning'" color="#d97706" :size="20"><WarningFilled /></el-icon>
            <el-icon v-else color="#2563eb" :size="20"><InfoFilled /></el-icon>
          </div>
          <div class="warn-content">
            <div class="warn-title">{{ w.title }}</div>
            <div class="warn-desc">{{ w.description }}</div>
            <div class="warn-suggestion">
              <span class="sug-label">💡 调整建议：</span>
              <span>{{ w.suggestion }}</span>
            </div>
            <div v-if="w.affectedItems && w.affectedItems.length" class="affected">
              <span class="affected-label">涉及志愿：</span>
              <el-tag
                v-for="item in w.affectedItems"
                :key="item.order"
                size="small"
                effect="plain"
                :type="getAffectedTagType(item.category)"
                style="margin-right: 6px; margin-bottom: 4px"
              >
                第{{ item.order }}志愿 · {{ item.collegeName }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <div class="health-score">
        <div class="score-label">方案健康度</div>
        <div class="score-bar-wrap">
          <div
            class="score-bar-inner"
            :style="{ width: healthScore + '%', background: healthScoreColor }"
          ></div>
        </div>
        <div class="score-num" :style="{ color: healthScoreColor }">{{ healthScore }}分</div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { ArrowDown, CircleCloseFilled, WarningFilled, InfoFilled } from '@element-plus/icons-vue'

const props = defineProps({
  volunteers: {
    type: Array,
    default: () => []
  },
  reachCount: {
    type: Number,
    default: 0
  },
  stableCount: {
    type: Number,
    default: 0
  },
  safeCount: {
    type: Number,
    default: 0
  },
  overallSuccessProbability: {
    type: Number,
    default: 0
  }
})

const collapsed = ref(false)

const successProbText = computed(() =>
  (props.overallSuccessProbability * 100).toFixed(1) + '%'
)

const warnings = computed(() => {
  const list = []
  const total = props.volunteers.length || 1
  const reachRatio = props.reachCount / total
  const stableRatio = props.stableCount / total
  const safeRatio = props.safeCount / total

  if (reachRatio > 0.5) {
    const reachVolunteers = props.volunteers.filter(v => v.category === '冲')
    list.push({
      level: 'danger',
      title: '冲刺院校过多',
      description: `当前冲档院校 ${props.reachCount} 所，占比 ${(reachRatio * 100).toFixed(0)}%，超过合理范围（建议 20%~35%）。`,
      suggestion: `建议减少 ${Math.ceil(props.reachCount - total * 0.35)} 所冲档院校，替换为稳或保档位院校，降低滑档风险。`,
      affectedItems: reachVolunteers.slice(-2).map(v => ({
        order: v.order,
        category: v.category,
        collegeName: v.college?.name || ''
      }))
    })
  }

  if (props.stableCount < 2 && total >= 5) {
    const stableVolunteers = props.volunteers.filter(v => v.category === '稳')
    list.push({
      level: 'danger',
      title: '稳妥档位严重不足',
      description: `稳档院校仅 ${props.stableCount} 所，无法形成有效保障。`,
      suggestion: '建议至少增加 2~3 所录取概率在 45%~80% 之间的稳妥院校，作为中坚力量。',
      affectedItems: stableVolunteers.map(v => ({
        order: v.order,
        category: v.category,
        collegeName: v.college?.name || ''
      }))
    })
  } else if (stableRatio < 0.2 && total >= 5) {
    list.push({
      level: 'warning',
      title: '稳妥档位占比偏低',
      description: `稳档院校占比仅 ${(stableRatio * 100).toFixed(0)}%，低于建议的 30%~50%。`,
      suggestion: '建议适当增加稳妥院校，形成合理的中间梯队。'
    })
  }

  if (props.safeCount < 1 && total >= 5) {
    list.push({
      level: 'danger',
      title: '缺少保底院校',
      description: '当前方案没有设置保底院校，存在全部滑档的风险。',
      suggestion: '务必增加 2 所以上录取概率 80%+ 的保底院校，确保至少能被一所大学录取。'
    })
  } else if (safeRatio < 0.15 && total >= 5) {
    const safeVolunteers = props.volunteers.filter(v => v.category === '保')
    list.push({
      level: 'warning',
      title: '保底院校偏少',
      description: `保底院校仅 ${props.safeCount} 所，占比 ${(safeRatio * 100).toFixed(0)}%。`,
      suggestion: '建议再增加 1~2 所保底院校，进一步降低退档风险。',
      affectedItems: safeVolunteers.map(v => ({
        order: v.order,
        category: v.category,
        collegeName: v.college?.name || ''
      }))
    })
  }

  if (props.volunteers.length >= 3) {
    const stableIndices = props.volunteers
      .map((v, i) => ({ v, i }))
      .filter(x => x.v.category === '稳')
      .map(x => x.i)
    if (stableIndices.length >= 2) {
      let hasGap = false
      for (let i = 1; i < stableIndices.length; i++) {
        if (stableIndices[i] - stableIndices[i - 1] > 3) {
          hasGap = true
          break
        }
      }
      if (!hasGap && stableIndices.length > 0) {
        const lastStable = stableIndices[stableIndices.length - 1]
        const remaining = props.volunteers.length - lastStable - 1
        const safeAfter = props.volunteers.slice(lastStable + 1).filter(v => v.category === '保').length
        if (remaining > 0 && safeAfter < remaining) {
          const midVolunteers = props.volunteers.slice(lastStable + 1).filter(v => v.category !== '保')
          list.push({
            level: 'warning',
            title: '稳-保之间可能断档',
            description: '稳妥院校之后没有过渡到足够的保底院校，中间存在梯度断层。',
            suggestion: '建议在稳档院校与保底院校之间合理过渡，逐步降低预期，避免突然跳跃。',
            affectedItems: midVolunteers.slice(0, 3).map(v => ({
              order: v.order,
              category: v.category,
              collegeName: v.college?.name || ''
            }))
          })
        }
      }
    }
  }

  const reachItems = props.volunteers.filter(v => v.category === '冲')
  if (reachItems.length >= 2) {
    reachItems.forEach((item, idx) => {
      if (idx > 0) {
        const prev = reachItems[idx - 1]
        if (prev.probability < item.probability && item.order - prev.order <= 5) {
          list.push({
            level: 'info',
            title: '冲档志愿排序可优化',
            description: `第${prev.order}志愿（${prev.college?.name || ''}）录取概率低于第${item.order}志愿（${item.college?.name || ''}），排序不太合理。`,
            suggestion: '建议将录取概率更低的冲刺院校排在更前面，概率较高的稍后排列。'
          })
        }
      }
    })
  }

  const collegeIds = props.volunteers.map(v => v.college?.id).filter(Boolean)
  const duplicates = collegeIds.filter((id, i) => collegeIds.indexOf(id) !== i)
  if (duplicates.length > 0) {
    const dupItems = props.volunteers.filter(v => duplicates.includes(v.college?.id))
    list.push({
      level: 'warning',
      title: '同一院校重复填报',
      description: `发现 ${new Set(duplicates).size} 所院校被重复填报，浪费志愿名额。`,
      suggestion: '建议移除重复院校，补充更多不同院校以增加选择面。',
      affectedItems: dupItems.map(v => ({
        order: v.order,
        category: v.category,
        collegeName: v.college?.name || ''
      }))
    })
  }

  if (props.volunteers.length >= 3) {
    for (let i = 1; i < props.volunteers.length; i++) {
      const prev = props.volunteers[i - 1]
      const curr = props.volunteers[i]
      if (prev.predicted_score && curr.predicted_score && prev.predicted_score < curr.predicted_score - 5) {
        list.push({
          level: 'info',
          title: '志愿梯度存在倒挂',
          description: `第${prev.order}志愿（${prev.college?.name || ''}，预估${prev.predicted_score}分）分数低于第${curr.order}志愿（${curr.college?.name || ''}，预估${curr.predicted_score}分）。`,
          suggestion: '志愿应按分数从高到低排列，确保前面的志愿冲刺更高目标。'
        })
        break
      }
    }
  }

  if (props.overallSuccessProbability < 0.7 && props.volunteers.length >= 3) {
    list.push({
      level: 'danger',
      title: '整体录取概率偏低',
      description: `当前方案综合录取概率仅 ${(props.overallSuccessProbability * 100).toFixed(1)}%，低于建议的 70% 安全线。`,
      suggestion: '强烈建议增加保底院校数量，或替换部分高风险院校为稳妥院校，以确保录取。'
    })
  }

  return list
})

const healthScore = computed(() => {
  let score = 100
  warnings.value.forEach(w => {
    if (w.level === 'danger') score -= 20
    else if (w.level === 'warning') score -= 10
    else score -= 5
  })
  return Math.max(0, Math.min(100, score))
})

const healthScoreColor = computed(() => {
  if (healthScore.value >= 80) return '#22c55e'
  if (healthScore.value >= 60) return '#f59e0b'
  return '#ef4444'
})

function getAffectedTagType(cat) {
  const map = { '冲': 'danger', '稳': 'warning', '保': 'success' }
  return map[cat] || 'info'
}
</script>

<style scoped>
.warning-panel {
  background: linear-gradient(135deg, #fffbeb 0%, #fefce8 100%);
  border-radius: 12px;
  border: 1px solid #fde68a;
  overflow: hidden;
}

.panel-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  cursor: pointer;
  user-select: none;
}

.panel-header:hover {
  background: rgba(251, 191, 36, 0.08);
}

.header-left {
  display: flex;
  align-items: center;
  gap: 12px;
}

.header-icon {
  width: 44px;
  height: 44px;
  border-radius: 12px;
  background: #fff;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
  border: 2px solid #fde68a;
}

.header-icon.has-warn {
  background: #fff7ed;
  border-color: #fdba74;
}

.header-icon.all-good {
  background: #f0fdf4;
  border-color: #86efac;
}

.panel-title {
  font-size: 17px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 2px 0;
}

.panel-subtitle {
  font-size: 13px;
  color: #78716c;
  margin: 0;
}

.collapse-icon {
  color: #a8a29e;
  transition: transform 0.25s;
  font-size: 18px;
}

.collapse-icon.expanded {
  transform: rotate(180deg);
}

.panel-body {
  padding: 0 20px 20px;
  border-top: 1px solid #fde68a;
}

.all-good-box {
  padding: 16px 0;
}

.warning-list {
  display: flex;
  flex-direction: column;
  gap: 12px;
  padding-top: 16px;
}

.warning-item {
  display: flex;
  gap: 12px;
  padding: 14px 16px;
  background: #fff;
  border-radius: 10px;
  border-left: 4px solid #94a3b8;
}

.warning-item.level-danger {
  border-left-color: #dc2626;
  background: #fff5f5;
}

.warning-item.level-warning {
  border-left-color: #d97706;
  background: #fffbeb;
}

.warning-item.level-info {
  border-left-color: #2563eb;
  background: #eff6ff;
}

.warn-icon {
  flex-shrink: 0;
  padding-top: 2px;
}

.warn-content {
  flex: 1;
  min-width: 0;
}

.warn-title {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  margin-bottom: 4px;
}

.level-danger .warn-title { color: #991b1b; }
.level-warning .warn-title { color: #92400e; }
.level-info .warn-title { color: #1e40af; }

.warn-desc {
  font-size: 13px;
  color: #475569;
  margin-bottom: 8px;
  line-height: 1.6;
}

.warn-suggestion {
  font-size: 13px;
  color: #065f46;
  background: #ecfdf5;
  padding: 8px 12px;
  border-radius: 8px;
  line-height: 1.6;
}

.sug-label {
  font-weight: 600;
  margin-right: 4px;
}

.affected {
  margin-top: 10px;
}

.affected-label {
  font-size: 12px;
  color: #94a3b8;
  margin-right: 6px;
}

.health-score {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-top: 20px;
  padding: 14px 16px;
  background: #fff;
  border-radius: 10px;
}

.score-label {
  font-size: 14px;
  font-weight: 600;
  color: #1e293b;
  flex-shrink: 0;
}

.score-bar-wrap {
  flex: 1;
  height: 10px;
  background: #f1f5f9;
  border-radius: 5px;
  overflow: hidden;
}

.score-bar-inner {
  height: 100%;
  border-radius: 5px;
  transition: width 0.5s;
}

.score-num {
  font-size: 20px;
  font-weight: 800;
  flex-shrink: 0;
  min-width: 60px;
  text-align: right;
}

@media (max-width: 600px) {
  .panel-header { padding: 12px 16px; }
  .panel-body { padding: 0 16px 16px; }
  .header-icon { width: 36px; height: 36px; font-size: 18px; }
  .panel-title { font-size: 15px; }
  .panel-subtitle { font-size: 12px; }
  .health-score { flex-wrap: wrap; }
  .score-num { font-size: 18px; min-width: auto; }
}
</style>

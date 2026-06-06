<template>
  <div v-if="!predictions || !predictions.length" class="empty-tip">
    <el-empty description="暂无匹配的院校" />
  </div>
  <div v-else>
    <el-row :gutter="16">
      <el-col
        v-for="p in predictions"
        :key="p.college.id"
        :xs="24"
        :sm="12"
        :md="8"
        :lg="6"
      >
        <el-card class="college-card" shadow="hover" @click="goDetail(p.college.id)">
          <div class="card-header">
            <div class="college-name">{{ p.college.name }}</div>
            <el-tag
              :class="`tag-${categoryClass(p.category)}`"
              effect="light"
              size="small"
              round
            >
              {{ p.category }}
            </el-tag>
          </div>
          <div class="college-meta">
            <span>{{ p.college.city }}</span>
            <span class="dot">·</span>
            <span>{{ p.college.level }}</span>
          </div>
          <div class="probability-row">
            <span class="prob-label">录取概率</span>
            <span class="prob-value" :style="{ color: probColor(p.probability) }">
              {{ (p.probability * 100).toFixed(1) }}%
            </span>
          </div>
          <div class="probability-bar">
            <div
              class="inner"
              :style="{ width: `${p.probability * 100}%`, background: probColor(p.probability) }"
            ></div>
          </div>
          <div class="prediction-row">
            <div>
              <span class="sub-label">预估位次</span>
              <span class="sub-value">{{ p.predicted_rank }}</span>
            </div>
            <div>
              <span class="sub-label">预估分数</span>
              <span class="sub-value">{{ p.predicted_score }}</span>
            </div>
          </div>
          <div class="tag-row">
            <el-tag
              v-for="(t, i) in p.college.tags.slice(0, 3)"
              :key="i"
              type="info"
              effect="plain"
              size="small"
            >
              {{ t }}
            </el-tag>
          </div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { useRouter } from 'vue-router'

defineProps({
  predictions: {
    type: Array,
    default: () => [],
  },
})

const router = useRouter()

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
</script>

<style scoped>
.college-card {
  margin-bottom: 16px;
  cursor: pointer;
  transition: transform 0.2s;
}

.college-card:hover {
  transform: translateY(-2px);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.college-name {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.college-meta {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 12px;
}

.dot {
  margin: 0 6px;
  color: #cbd5e1;
}

.probability-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 6px;
}

.prob-label {
  font-size: 13px;
  color: #64748b;
}

.prob-value {
  font-size: 16px;
  font-weight: 700;
}

.prediction-row {
  display: flex;
  justify-content: space-between;
  margin-top: 10px;
}

.sub-label {
  font-size: 12px;
  color: #94a3b8;
  display: block;
  margin-bottom: 2px;
}

.sub-value {
  font-size: 14px;
  font-weight: 600;
  color: #334155;
}

.tag-row {
  margin-top: 12px;
  display: flex;
  gap: 6px;
  flex-wrap: wrap;
}
</style>

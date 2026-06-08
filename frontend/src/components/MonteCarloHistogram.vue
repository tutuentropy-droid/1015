<template>
  <div class="monte-carlo-wrapper">
    <div class="mc-header">
      <div>
        <h3 class="mc-title">
          <span class="mc-icon">🎲</span>
          蒙特卡洛模拟：录取概率分布
        </h3>
        <p class="mc-subtitle">
          基于历年分数线标准差，运行 {{ numSimulations }} 次随机模拟，展示录取概率的不确定性分布
        </p>
      </div>
      <div v-if="showRunButton && canRun" class="mc-actions">
        <el-button
          type="primary"
          :loading="loading"
          @click="handleRunSimulation"
          size="default"
        >
          <el-icon><Promotion /></el-icon>
          <span>运行模拟</span>
        </el-button>
      </div>
    </div>

    <div v-if="loading" class="mc-loading">
      <el-icon class="is-loading" :size="32"><Loading /></el-icon>
      <div class="loading-text">正在进行蒙特卡洛模拟...</div>
    </div>

    <template v-else-if="results && results.length">
      <div class="mc-summary-grid">
        <div
          v-for="(result, idx) in results"
          :key="result.college_id"
          class="mc-summary-card"
          :style="{ borderLeftColor: getColor(idx) }"
        >
          <div class="summary-header">
            <span class="summary-color-dot" :style="{ background: getColor(idx) }"></span>
            <span class="summary-name">{{ result.college_name }}</span>
          </div>
          <div class="summary-stats">
            <div class="stat-row">
              <span class="stat-label">基础概率</span>
              <span class="stat-value" :style="{ color: getColor(idx) }">
                <b>{{ (result.base_probability * 100).toFixed(1) }}%</b>
              </span>
            </div>
            <div class="stat-row">
              <span class="stat-label">模拟均值</span>
              <span class="stat-value">
                <b>{{ (result.simulated_probability_mean * 100).toFixed(1) }}%</b>
              </span>
            </div>
            <div class="stat-row">
              <span class="stat-label">标准差</span>
              <span class="stat-value">±{{ (result.simulated_probability_std * 100).toFixed(1) }}%</span>
            </div>
            <div class="stat-row">
              <span class="stat-label">95%置信区间</span>
              <span class="stat-value">
                {{ (result.ci_lower_95 * 100).toFixed(1) }}% ~ {{ (result.ci_upper_95 * 100).toFixed(1) }}%
              </span>
            </div>
            <div class="stat-row">
              <span class="stat-label">稳定性评分</span>
              <span class="stat-value">
                <el-progress
                  :percentage="result.stability_score * 100"
                  :stroke-width="6"
                  :show-text="false"
                  :color="getStabilityColor(result.stability_score)"
                  style="width: 60px; display: inline-block; vertical-align: middle; margin-right: 6px"
                />
                <b :style="{ color: getStabilityColor(result.stability_score) }">
                  {{ (result.stability_score * 100).toFixed(0) }}分
                </b>
              </span>
            </div>
            <div class="stat-row volatility-row">
              <span class="stat-label">波动评级</span>
              <el-tag :type="getVolatilityTagType(result.volatility_rating)" effect="light" size="small">
                {{ result.volatility_rating }}
              </el-tag>
            </div>
          </div>
        </div>
      </div>

      <div class="mc-chart-card">
        <h4 class="chart-subtitle">📊 录取概率分布直方图（多校叠加对比）</h4>
        <v-chart :option="histogramOption" autoresize style="height: 420px; width: 100%" />
      </div>

      <div class="mc-chart-card">
        <h4 class="chart-subtitle">🎯 置信区间与稳定性对比</h4>
        <v-chart :option="ciOption" autoresize style="height: 320px; width: 100%" />
      </div>
    </template>

    <div v-else class="mc-empty">
      <el-empty description="暂无模拟数据，请选择院校后运行模拟">
        <div slot="description" class="empty-desc">
          <p>💡 蒙特卡洛模拟会基于历年分数线的波动情况</p>
          <p>运行上千次随机采样，给出录取概率的分布区间</p>
        </div>
      </el-empty>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { BarChart, LineChart, CustomChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, MarkLineComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import { Loading, Promotion } from '@element-plus/icons-vue'

use([
  CanvasRenderer, BarChart, LineChart, CustomChart,
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, MarkLineComponent
])

const COLORS = [
  '#3b82f6',
  '#ef4444',
  '#22c55e',
  '#f59e0b',
  '#8b5cf6',
]

const props = defineProps({
  results: {
    type: Array,
    default: () => []
  },
  commonBins: {
    type: Array,
    default: () => []
  },
  numSimulations: {
    type: Number,
    default: 1000
  },
  loading: {
    type: Boolean,
    default: false
  },
  showRunButton: {
    type: Boolean,
    default: false
  },
  canRun: {
    type: Boolean,
    default: true
  }
})

const emit = defineEmits(['run'])

function getColor(idx) {
  return COLORS[idx % COLORS.length]
}

function getStabilityColor(score) {
  if (score >= 0.85) return '#22c55e'
  if (score >= 0.7) return '#3b82f6'
  if (score >= 0.55) return '#f59e0b'
  if (score >= 0.4) return '#f97316'
  return '#ef4444'
}

function getVolatilityTagType(rating) {
  if (rating.includes('极为稳定')) return 'success'
  if (rating.includes('较为稳定')) return 'primary'
  if (rating.includes('一定波动')) return 'warning'
  if (rating.includes('波动较大')) return 'warning'
  return 'danger'
}

function handleRunSimulation() {
  emit('run')
}

const histogramOption = computed(() => {
  if (!props.results || !props.results.length) {
    return {}
  }

  const series = []
  const legendData = []

  props.results.forEach((result, idx) => {
    const color = getColor(idx)
    legendData.push(result.college_name)

    const bins = result.histogram_bins || []
    const binLabels = bins.map(b => {
      const mid = (b.bin_start + b.bin_end) / 2
      return (mid * 100).toFixed(0) + '%'
    })
    const binData = bins.map(b => b.probability)

    series.push({
      name: result.college_name,
      type: 'bar',
      data: binData,
      barGap: '-100%',
      barCategoryGap: '10%',
      itemStyle: {
        color: color + '55',
        borderColor: color,
        borderWidth: 1,
        borderRadius: [2, 2, 0, 0],
      },
      emphasis: {
        itemStyle: {
          color: color + 'AA',
        }
      }
    })
  })

  const binLabels = (props.results[0]?.histogram_bins || []).map(b => {
    const mid = (b.bin_start + b.bin_end) / 2
    return (mid * 100).toFixed(0) + '%'
  })

  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255,255,255,0.98)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => {
        if (!params || !params.length) return ''
        let html = `<div style="font-weight:600;margin-bottom:8px">概率区间：${params[0].axisValue}</div>`
        params.forEach(p => {
          if (p.value !== null && p.value !== undefined) {
            html += `<div style="display:flex;align-items:center;gap:6px;margin:4px 0">
              <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${p.color}"></span>
              <span>${p.seriesName}：</span>
              <b>${(p.value * 100).toFixed(1)}%</b>
            </div>`
          }
        })
        return html
      }
    },
    legend: {
      data: legendData,
      bottom: 0,
      textStyle: { color: '#475569' },
      type: 'scroll',
    },
    grid: {
      left: 60,
      right: 30,
      top: 20,
      bottom: 60,
    },
    xAxis: {
      type: 'category',
      data: binLabels,
      name: '录取概率区间',
      nameLocation: 'middle',
      nameGap: 30,
      nameTextStyle: { color: '#64748b', fontSize: 12 },
      axisLine: { lineStyle: { color: '#cbd5e1' } },
      axisLabel: {
        color: '#475569',
        fontSize: 11,
        interval: 0,
        rotate: binLabels.length > 15 ? 45 : 0,
      },
    },
    yAxis: {
      type: 'value',
      name: '出现频率',
      nameTextStyle: { color: '#64748b', fontSize: 12 },
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f1f5f9' } },
      axisLabel: {
        color: '#64748b',
        formatter: (val) => (val * 100).toFixed(0) + '%'
      }
    },
    series: series,
  }
})

const ciOption = computed(() => {
  if (!props.results || !props.results.length) {
    return {}
  }

  const categories = props.results.map(r => r.college_name)
  const ci95LowData = props.results.map(r => r.ci_lower_95 * 100)
  const ci95HighData = props.results.map(r => r.ci_upper_95 * 100)
  const meanData = props.results.map(r => r.simulated_probability_mean * 100)
  const baseData = props.results.map(r => r.base_probability * 100)
  const rangeData = props.results.map((r, i) => [i, r.ci_lower_95 * 100, r.ci_upper_95 * 100])

  return {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.98)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => {
        if (!params || !params.length) return ''
        const idx = params[0].dataIndex
        const r = props.results[idx]
        return `<div style="font-weight:600;margin-bottom:8px">${r.college_name}</div>
          <div>基础概率：<b>${(r.base_probability * 100).toFixed(1)}%</b></div>
          <div>模拟均值：<b>${(r.simulated_probability_mean * 100).toFixed(1)}%</b></div>
          <div>90%置信区间：<b>${(r.ci_lower_90 * 100).toFixed(1)}% ~ ${(r.ci_upper_90 * 100).toFixed(1)}%</b></div>
          <div>95%置信区间：<b>${(r.ci_lower_95 * 100).toFixed(1)}% ~ ${(r.ci_upper_95 * 100).toFixed(1)}%</b></div>
          <div>波动范围：<b>${((r.ci_upper_95 - r.ci_lower_95) * 100).toFixed(1)}%</b></div>`
      }
    },
    legend: {
      data: ['模拟均值', '基础概率', '95%置信区间'],
      bottom: 0,
      textStyle: { color: '#475569' },
    },
    grid: {
      left: 60,
      right: 30,
      top: 30,
      bottom: 60,
    },
    xAxis: {
      type: 'category',
      data: categories,
      axisLine: { lineStyle: { color: '#cbd5e1' } },
      axisLabel: { color: '#475569', fontWeight: 500 },
    },
    yAxis: {
      type: 'value',
      name: '录取概率 (%)',
      nameTextStyle: { color: '#64748b', fontSize: 12 },
      min: 0,
      max: 100,
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f1f5f9' } },
      axisLabel: {
        color: '#64748b',
        formatter: (val) => val + '%'
      }
    },
    series: [
      {
        name: '95%置信区间',
        type: 'custom',
        renderItem: (params, api) => {
          const categoryIndex = api.value(0)
          const start = api.coord([categoryIndex, api.value(1)])
          const end = api.coord([categoryIndex, api.value(2)])
          const height = end[1] - start[1] || 1
          const color = COLORS[categoryIndex % COLORS.length]
          return {
            type: 'rect',
            shape: {
              x: start[0] - 20,
              y: start[1],
              width: 40,
              height: height,
            },
            style: {
              fill: color + '33',
              stroke: color,
              lineWidth: 2,
            },
            info: params.value,
          }
        },
        encode: {
          x: 0,
          y: [1, 2],
        },
        data: rangeData,
        z: 1,
      },
      {
        name: '基础概率',
        type: 'line',
        data: baseData,
        symbol: 'diamond',
        symbolSize: 12,
        lineStyle: { color: '#94a3b8', width: 2, type: 'dashed' },
        itemStyle: { color: '#94a3b8' },
        z: 3,
      },
      {
        name: '模拟均值',
        type: 'line',
        data: meanData,
        symbol: 'circle',
        symbolSize: 14,
        lineStyle: { width: 3 },
        itemStyle: {
          color: (params) => COLORS[params.dataIndex % COLORS.length],
          borderColor: '#fff',
          borderWidth: 2,
        },
        label: {
          show: true,
          position: 'top',
          formatter: (p) => p.value.toFixed(1) + '%',
          color: '#1e293b',
          fontWeight: 'bold',
          fontSize: 11,
        },
        z: 4,
      },
    ]
  }
})
</script>

<style scoped>
.monte-carlo-wrapper {
  background: #fff;
  border-radius: 12px;
  border: 1px solid #e2e8f0;
  padding: 24px;
}

.mc-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 24px;
  flex-wrap: wrap;
  gap: 16px;
}

.mc-title {
  font-size: 20px;
  font-weight: 700;
  color: #1e293b;
  margin: 0 0 6px 0;
  display: flex;
  align-items: center;
  gap: 8px;
}

.mc-icon {
  font-size: 24px;
}

.mc-subtitle {
  font-size: 13px;
  color: #64748b;
  margin: 0;
}

.mc-summary-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(260px, 1fr));
  gap: 16px;
  margin-bottom: 20px;
}

.mc-summary-card {
  background: linear-gradient(135deg, #f8fafc 0%, #fff 100%);
  border-radius: 10px;
  padding: 16px 18px;
  border-left: 4px solid #3b82f6;
}

.summary-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.summary-color-dot {
  width: 10px;
  height: 10px;
  border-radius: 50%;
  flex-shrink: 0;
}

.summary-name {
  font-size: 15px;
  font-weight: 700;
  color: #1e293b;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.summary-stats {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.stat-row {
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.stat-label {
  color: #64748b;
}

.stat-value {
  color: #334155;
  font-weight: 500;
}

.volatility-row {
  padding-top: 4px;
}

.mc-chart-card {
  background: #fafbfc;
  border-radius: 10px;
  padding: 18px 20px;
  margin-bottom: 16px;
  border: 1px solid #f1f5f9;
}

.chart-subtitle {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px 0;
}

.mc-loading {
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  padding: 60px 20px;
  color: #64748b;
  gap: 12px;
}

.loading-text {
  font-size: 14px;
}

.mc-empty {
  padding: 40px 20px;
}

.empty-desc p {
  margin: 4px 0;
  color: #94a3b8;
  font-size: 13px;
}

@media (max-width: 768px) {
  .mc-summary-grid {
    grid-template-columns: 1fr;
  }
}
</style>

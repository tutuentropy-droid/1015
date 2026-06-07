<template>
  <div class="trend-chart-wrapper">
    <div v-if="collegeName" class="chart-header">
      <h3 class="chart-title">📈 {{ collegeName }} 近五年录取趋势</h3>
      <div class="year-type-tags">
        <span
          v-for="(item, idx) in yearTypeAnalysis"
          :key="idx"
          class="year-tag"
          :class="`tag-${item.type}`"
        >
          {{ item.year }}年：{{ item.label }}
        </span>
      </div>
    </div>
    <div v-if="chartData.length === 0" class="chart-empty">
      <el-empty description="暂无历年录取数据" />
    </div>
    <v-chart v-else :option="chartOption" autoresize style="height: 320px; width: 100%" />
    <div v-if="trendSummary" class="trend-summary">
      <el-alert :type="summaryAlertType" :closable="false" show-icon>
        <template #title>
          <b>趋势分析：</b>{{ trendSummary }}
        </template>
      </el-alert>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { LineChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, MarkPointComponent, MarkLineComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer, LineChart, TitleComponent,
  TooltipComponent, LegendComponent, GridComponent,
  MarkPointComponent, MarkLineComponent
])

const props = defineProps({
  admissionData: {
    type: Array,
    default: () => []
  },
  collegeName: {
    type: String,
    default: ''
  },
  userScore: {
    type: Number,
    default: 0
  },
  userRank: {
    type: Number,
    default: 0
  }
})

const chartData = computed(() => {
  if (!props.admissionData || props.admissionData.length === 0) return []
  const yearMap = new Map()
  props.admissionData.forEach(d => {
    if (!yearMap.has(d.year)) {
      yearMap.set(d.year, { year: d.year, scores: [], ranks: [] })
    }
    const entry = yearMap.get(d.year)
    if (d.score) entry.scores.push(d.score)
    if (d.rank) entry.ranks.push(d.rank)
  })
  const result = Array.from(yearMap.values())
    .map(e => ({
      year: e.year,
      avgScore: e.scores.length ? Math.round(e.scores.reduce((a, b) => a + b, 0) / e.scores.length) : null,
      avgRank: e.ranks.length ? Math.round(e.ranks.reduce((a, b) => a + b, 0) / e.ranks.length) : null,
      minScore: e.scores.length ? Math.min(...e.scores) : null,
      maxScore: e.scores.length ? Math.max(...e.scores) : null
    }))
    .sort((a, b) => a.year - b.year)
    .slice(-5)
  return result
})

const yearTypeAnalysis = computed(() => {
  const data = chartData.value
  if (data.length < 3) return []
  const scores = data.map(d => d.avgScore).filter(s => s !== null)
  if (scores.length < 3) return []
  const avg = scores.reduce((a, b) => a + b, 0) / scores.length
  const std = Math.sqrt(scores.reduce((a, b) => a + (b - avg) ** 2, 0) / scores.length)
  return data.slice(-3).map(d => {
    let type = 'normal'
    let label = '正常'
    if (d.avgScore !== null) {
      if (d.avgScore > avg + std * 0.5) {
        type = 'big'
        label = '大年（分数偏高）'
      } else if (d.avgScore < avg - std * 0.5) {
        type = 'small'
        label = '小年（分数偏低）'
      } else {
        type = 'normal'
        label = '正常'
      }
    }
    return { year: d.year, type, label }
  })
})

const trendSummary = computed(() => {
  const data = chartData.value
  if (data.length < 2) return ''
  const recent = data.slice(-3).filter(d => d.avgScore !== null)
  if (recent.length < 2) return ''
  const oldest = recent[0].avgScore
  const newest = recent[recent.length - 1].avgScore
  const diff = newest - oldest
  const pct = (diff / oldest * 100).toFixed(1)
  const userScoreLine = props.userScore ? `，你的分数 ${props.userScore} 分` : ''
  if (Math.abs(diff) <= 3) {
    return `近三年录取分数基本稳定${userScoreLine}，报考风险可控。`
  } else if (diff > 0) {
    return `近三年录取分数呈上升趋势（上涨 ${diff} 分，约 ${pct}%）${userScoreLine}，今年可能继续走高，需谨慎。`
  } else {
    return `近三年录取分数呈下降趋势（下降 ${Math.abs(diff)} 分，约 ${Math.abs(pct)}%）${userScoreLine}，今年可能为小年，可考虑冲刺。`
  }
})

const summaryAlertType = computed(() => {
  const data = chartData.value
  if (data.length < 2) return 'info'
  const recent = data.slice(-3).filter(d => d.avgScore !== null)
  if (recent.length < 2) return 'info'
  const diff = recent[recent.length - 1].avgScore - recent[0].avgScore
  if (Math.abs(diff) <= 3) return 'success'
  if (diff > 5) return 'warning'
  if (diff < -5) return 'info'
  return 'info'
})

const chartOption = computed(() => {
  const years = chartData.value.map(d => d.year + '年')
  const avgScores = chartData.value.map(d => d.avgScore)
  const minScores = chartData.value.map(d => d.minScore)
  const maxScores = chartData.value.map(d => d.maxScore)
  const series = [
    {
      name: '平均分',
      type: 'line',
      data: avgScores,
      smooth: true,
      symbol: 'circle',
      symbolSize: 10,
      lineStyle: { width: 3, color: '#3b82f6' },
      itemStyle: { color: '#3b82f6' },
      label: {
        show: true,
        position: 'top',
        color: '#1e40af',
        fontWeight: 'bold'
      },
      areaStyle: {
        color: {
          type: 'linear',
          x: 0, y: 0, x2: 0, y2: 1,
          colorStops: [
            { offset: 0, color: 'rgba(59, 130, 246, 0.3)' },
            { offset: 1, color: 'rgba(59, 130, 246, 0.02)' }
          ]
        }
      }
    },
    {
      name: '最低分',
      type: 'line',
      data: minScores,
      smooth: true,
      symbol: 'diamond',
      symbolSize: 8,
      lineStyle: { width: 2, color: '#22c55e', type: 'dashed' },
      itemStyle: { color: '#22c55e' },
      label: {
        show: true,
        position: 'bottom',
        color: '#15803d',
        fontSize: 11
      }
    },
    {
      name: '最高分',
      type: 'line',
      data: maxScores,
      smooth: true,
      symbol: 'triangle',
      symbolSize: 8,
      lineStyle: { width: 2, color: '#ef4444', type: 'dashed' },
      itemStyle: { color: '#ef4444' },
      label: {
        show: true,
        position: 'top',
        color: '#b91c1c',
        fontSize: 11
      }
    }
  ]
  const markLines = []
  if (props.userScore) {
    markLines.push({
      name: '你的分数',
      type: 'line',
      markLine: {
        silent: false,
        symbol: 'none',
        data: [{
          yAxis: props.userScore,
          label: {
            formatter: `你的分数: ${props.userScore}`,
            position: 'insideEndTop',
            color: '#f59e0b',
            fontWeight: 'bold'
          },
          lineStyle: {
            color: '#f59e0b',
            type: 'solid',
            width: 2
          }
        }]
      }
    })
  }
  return {
    title: {
      text: '',
      left: 'center'
    },
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => {
        let html = `<div style="font-weight:600;margin-bottom:6px">${params[0].name}</div>`
        params.forEach(p => {
          if (p.value !== null && p.value !== undefined) {
            html += `<div style="display:flex;align-items:center;gap:6px;margin:4px 0">
              <span style="display:inline-block;width:10px;height:10px;border-radius:50%;background:${p.color}"></span>
              <span>${p.seriesName}：</span>
              <b>${p.value} 分</b>
            </div>`
          }
        })
        return html
      }
    },
    legend: {
      data: ['平均分', '最低分', '最高分'],
      bottom: 0,
      textStyle: { color: '#475569' }
    },
    grid: {
      left: 50,
      right: 30,
      top: 30,
      bottom: 50
    },
    xAxis: {
      type: 'category',
      data: years,
      axisLine: { lineStyle: { color: '#cbd5e1' } },
      axisLabel: { color: '#475569', fontWeight: 500 }
    },
    yAxis: {
      type: 'value',
      name: '分数',
      axisLine: { show: false },
      axisTick: { show: false },
      splitLine: { lineStyle: { color: '#f1f5f9' } },
      axisLabel: { color: '#64748b' }
    },
    series: series.map((s, i) => i === 0 && markLines.length ? { ...s, ...markLines[0] } : s)
  }
})
</script>

<style scoped>
.trend-chart-wrapper {
  background: #fff;
  border-radius: 10px;
  padding: 16px;
  border: 1px solid #e2e8f0;
}

.chart-header {
  margin-bottom: 12px;
}

.chart-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 10px 0;
}

.year-type-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.year-tag {
  padding: 3px 10px;
  border-radius: 12px;
  font-size: 12px;
  font-weight: 500;
}

.tag-big {
  background: #fef2f2;
  color: #dc2626;
}

.tag-small {
  background: #ecfdf5;
  color: #059669;
}

.tag-normal {
  background: #f1f5f9;
  color: #475569;
}

.chart-empty {
  height: 200px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.trend-summary {
  margin-top: 12px;
}
</style>

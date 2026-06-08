<template>
  <div class="employment-analysis">
    <div v-if="loading" class="loading-wrap">
      <el-skeleton :rows="6" animated />
    </div>
    <template v-else-if="employmentData">
      <div class="employment-header">
        <div class="header-stats">
          <div class="stat-item">
            <div class="stat-icon">🎓</div>
            <div class="stat-content">
              <div class="stat-label">毕业生总数</div>
              <div class="stat-value">{{ employmentData.total_graduates.toLocaleString() }} 人</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">✅</div>
            <div class="stat-content">
              <div class="stat-label">就业率</div>
              <div class="stat-value green">{{ (employmentData.employment_rate * 100).toFixed(2) }}%</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">💰</div>
            <div class="stat-content">
              <div class="stat-label">平均年薪</div>
              <div class="stat-value blue">¥{{ formatSalary(employmentData.average_salary) }}</div>
            </div>
          </div>
          <div class="stat-item">
            <div class="stat-icon">📅</div>
            <div class="stat-content">
              <div class="stat-label">数据年度</div>
              <div class="stat-value">{{ employmentData.year }}年</div>
            </div>
          </div>
        </div>
        <div class="data-source-tag">
          <el-tag
            :type="employmentData.data_source === '官方就业报告' ? 'success' : 'warning'"
            effect="light"
            size="default"
          >
            <span style="margin-right: 4px">📊</span>
            数据来源：{{ employmentData.data_source }}
          </el-tag>
          <el-tooltip v-if="employmentData.note" :content="employmentData.note" placement="top">
            <el-icon class="info-icon"><QuestionFilled /></el-icon>
          </el-tooltip>
        </div>
      </div>

      <el-tabs v-model="activeTab" class="employment-tabs">
        <el-tab-pane label="行业分布" name="industry">
          <div class="chart-row">
            <div class="chart-card">
              <h3 class="chart-title">🏭 行业分布饼图</h3>
              <v-chart :option="industryPieOption" autoresize style="height: 380px; width: 100%" />
            </div>
            <div class="chart-card">
              <h3 class="chart-title">📊 行业分布条形图（按占比排序）</h3>
              <v-chart :option="industryBarOption" autoresize style="height: 380px; width: 100%" />
            </div>
          </div>
          <div class="data-table-wrap">
            <h4 class="table-title">📋 行业详细数据</h4>
            <el-table :data="employmentData.industry_distribution" stripe size="default">
              <el-table-column type="index" label="排名" width="70" align="center" />
              <el-table-column prop="industry" label="行业" min-width="160" />
              <el-table-column prop="count" label="就业人数" width="120" align="center" />
              <el-table-column label="占比" width="150" align="center">
                <template #default="{ row }">
                  <el-progress
                    :percentage="parseFloat((row.percentage * 100).toFixed(1))"
                    :stroke-width="10"
                    :show-text="true"
                    :color="getProgressColor(row.percentage)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="平均年薪" width="140" align="center">
                <template #default="{ row }">
                  <span class="salary-text">¥{{ formatSalary(row.avg_salary) }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="职位类型" name="position">
          <div class="chart-row">
            <div class="chart-card">
              <h3 class="chart-title">💼 职位类型分布饼图</h3>
              <v-chart :option="positionPieOption" autoresize style="height: 380px; width: 100%" />
            </div>
            <div class="chart-card">
              <h3 class="chart-title">📊 职位类型分布条形图</h3>
              <v-chart :option="positionBarOption" autoresize style="height: 380px; width: 100%" />
            </div>
          </div>
          <div class="data-table-wrap">
            <h4 class="table-title">📋 职位类型详细数据</h4>
            <el-table :data="employmentData.position_distribution" stripe size="default">
              <el-table-column type="index" label="排名" width="70" align="center" />
              <el-table-column prop="position_type" label="职位类型" min-width="160" />
              <el-table-column prop="count" label="就业人数" width="120" align="center" />
              <el-table-column label="占比" width="150" align="center">
                <template #default="{ row }">
                  <el-progress
                    :percentage="parseFloat((row.percentage * 100).toFixed(1))"
                    :stroke-width="10"
                    :show-text="true"
                    :color="getProgressColor(row.percentage)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="平均年薪" width="140" align="center">
                <template #default="{ row }">
                  <span class="salary-text">¥{{ formatSalary(row.avg_salary) }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>

        <el-tab-pane label="城市分布" name="city">
          <EmploymentCityHeatmap :city-data="employmentData.city_distribution" />
          <div class="data-table-wrap">
            <h4 class="table-title">📋 城市详细数据</h4>
            <el-table :data="employmentData.city_distribution" stripe size="default">
              <el-table-column type="index" label="排名" width="70" align="center" />
              <el-table-column prop="city" label="城市" width="120" />
              <el-table-column prop="province" label="省份" width="100" align="center" />
              <el-table-column prop="count" label="就业人数" width="120" align="center" />
              <el-table-column label="占比" width="150" align="center">
                <template #default="{ row }">
                  <el-progress
                    :percentage="parseFloat((row.percentage * 100).toFixed(1))"
                    :stroke-width="10"
                    :show-text="true"
                    :color="getProgressColor(row.percentage)"
                  />
                </template>
              </el-table-column>
              <el-table-column label="平均年薪" width="140" align="center">
                <template #default="{ row }">
                  <span class="salary-text">¥{{ formatSalary(row.avg_salary) }}</span>
                </template>
              </el-table-column>
            </el-table>
          </div>
        </el-tab-pane>
      </el-tabs>
    </template>
    <div v-else class="empty-wrap">
      <el-empty description="暂无就业数据" />
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { QuestionFilled } from '@element-plus/icons-vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { PieChart, BarChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, DataZoomComponent
} from 'echarts/components'
import VChart from 'vue-echarts'
import EmploymentCityHeatmap from './EmploymentCityHeatmap.vue'

use([
  CanvasRenderer, PieChart, BarChart, TitleComponent,
  TooltipComponent, LegendComponent, GridComponent, DataZoomComponent
])

const props = defineProps({
  employmentData: {
    type: Object,
    default: null
  },
  loading: {
    type: Boolean,
    default: false
  },
  defaultTab: {
    type: String,
    default: 'industry'
  }
})

const activeTab = ref(props.defaultTab)

const CHART_COLORS = [
  '#3b82f6', '#22c55e', '#f59e0b', '#ef4444', '#8b5cf6',
  '#ec4899', '#06b6d4', '#f97316', '#84cc16', '#6366f1',
  '#14b8a6', '#eab308', '#a855f7', '#0ea5e9', '#fb923c'
]

function formatSalary(salary) {
  if (!salary) return '-'
  if (salary >= 10000) {
    return (salary / 10000).toFixed(1) + '万'
  }
  return salary.toString()
}

function getProgressColor(pct) {
  if (pct >= 0.2) return '#22c55e'
  if (pct >= 0.1) return '#3b82f6'
  if (pct >= 0.05) return '#f59e0b'
  return '#94a3b8'
}

const industryPieOption = computed(() => {
  const data = (props.employmentData?.industry_distribution || []).map((d, i) => ({
    name: d.industry,
    value: d.count,
    avgSalary: d.avg_salary,
    itemStyle: { color: CHART_COLORS[i % CHART_COLORS.length] }
  }))
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => `
        <div style="font-weight:600;margin-bottom:6px">${params.name}</div>
        <div>就业人数：<b>${params.value}</b> 人</div>
        <div>占比：<b>${(params.percent).toFixed(1)}%</b></div>
        <div>平均年薪：<b style="color:#2563eb">¥${formatSalary(params.data.avgSalary)}</b></div>
      `
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#475569', fontSize: 12 }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['38%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}\n{d}%',
        fontSize: 11,
        color: '#475569'
      },
      labelLine: { show: true, length: 12, length2: 8 },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' },
        itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.2)' }
      },
      data: data
    }]
  }
})

const industryBarOption = computed(() => {
  const raw = props.employmentData?.industry_distribution || []
  const sorted = [...raw].sort((a, b) => a.percentage - b.percentage)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => {
        const d = params[0]
        const row = sorted[d.dataIndex]
        return `
          <div style="font-weight:600;margin-bottom:6px">${d.name}</div>
          <div>就业人数：<b>${row.count}</b> 人</div>
          <div>占比：<b>${(row.percentage * 100).toFixed(1)}%</b></div>
          <div>平均年薪：<b style="color:#2563eb">¥${formatSalary(row.avg_salary)}</b></div>
        `
      }
    },
    grid: { left: 140, right: 60, top: 20, bottom: 30 },
    xAxis: {
      type: 'value',
      axisLabel: {
        color: '#64748b',
        formatter: (v) => (v * 100).toFixed(0) + '%'
      },
      splitLine: { lineStyle: { color: '#f1f5f9' } }
    },
    yAxis: {
      type: 'category',
      data: sorted.map(d => d.industry),
      axisLabel: { color: '#475569', fontSize: 12 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [{
      type: 'bar',
      data: sorted.map((d, i) => ({
        value: d.percentage,
        itemStyle: {
          color: CHART_COLORS[i % CHART_COLORS.length],
          borderRadius: [0, 4, 4, 0]
        }
      })),
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        formatter: (p) => (p.value * 100).toFixed(1) + '%',
        color: '#1e293b',
        fontSize: 11,
        fontWeight: 600
      }
    }]
  }
})

const positionPieOption = computed(() => {
  const data = (props.employmentData?.position_distribution || []).map((d, i) => ({
    name: d.position_type,
    value: d.count,
    avgSalary: d.avg_salary,
    itemStyle: { color: CHART_COLORS[i % CHART_COLORS.length] }
  }))
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => `
        <div style="font-weight:600;margin-bottom:6px">${params.name}</div>
        <div>就业人数：<b>${params.value}</b> 人</div>
        <div>占比：<b>${(params.percent).toFixed(1)}%</b></div>
        <div>平均年薪：<b style="color:#2563eb">¥${formatSalary(params.data.avgSalary)}</b></div>
      `
    },
    legend: {
      type: 'scroll',
      orient: 'vertical',
      right: 10,
      top: 'center',
      textStyle: { color: '#475569', fontSize: 12 }
    },
    series: [{
      type: 'pie',
      radius: ['40%', '70%'],
      center: ['38%', '50%'],
      avoidLabelOverlap: true,
      itemStyle: {
        borderRadius: 6,
        borderColor: '#fff',
        borderWidth: 2
      },
      label: {
        show: true,
        formatter: '{b}\n{d}%',
        fontSize: 11,
        color: '#475569'
      },
      labelLine: { show: true, length: 12, length2: 8 },
      emphasis: {
        label: { show: true, fontSize: 14, fontWeight: 'bold' },
        itemStyle: { shadowBlur: 10, shadowOffsetX: 0, shadowColor: 'rgba(0,0,0,0.2)' }
      },
      data: data
    }]
  }
})

const positionBarOption = computed(() => {
  const raw = props.employmentData?.position_distribution || []
  const sorted = [...raw].sort((a, b) => a.percentage - b.percentage)
  return {
    tooltip: {
      trigger: 'axis',
      axisPointer: { type: 'shadow' },
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => {
        const d = params[0]
        const row = sorted[d.dataIndex]
        return `
          <div style="font-weight:600;margin-bottom:6px">${d.name}</div>
          <div>就业人数：<b>${row.count}</b> 人</div>
          <div>占比：<b>${(row.percentage * 100).toFixed(1)}%</b></div>
          <div>平均年薪：<b style="color:#2563eb">¥${formatSalary(row.avg_salary)}</b></div>
        `
      }
    },
    grid: { left: 140, right: 60, top: 20, bottom: 30 },
    xAxis: {
      type: 'value',
      axisLabel: {
        color: '#64748b',
        formatter: (v) => (v * 100).toFixed(0) + '%'
      },
      splitLine: { lineStyle: { color: '#f1f5f9' } }
    },
    yAxis: {
      type: 'category',
      data: sorted.map(d => d.position_type),
      axisLabel: { color: '#475569', fontSize: 12 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    series: [{
      type: 'bar',
      data: sorted.map((d, i) => ({
        value: d.percentage,
        itemStyle: {
          color: CHART_COLORS[i % CHART_COLORS.length],
          borderRadius: [0, 4, 4, 0]
        }
      })),
      barWidth: '60%',
      label: {
        show: true,
        position: 'right',
        formatter: (p) => (p.value * 100).toFixed(1) + '%',
        color: '#1e293b',
        fontSize: 11,
        fontWeight: 600
      }
    }]
  }
})
</script>

<style scoped>
.employment-analysis {
  width: 100%;
}

.loading-wrap, .empty-wrap {
  padding: 40px 0;
}

.employment-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  flex-wrap: wrap;
  gap: 16px;
  margin-bottom: 24px;
  padding: 20px;
  background: linear-gradient(135deg, #eff6ff 0%, #f0fdf4 100%);
  border-radius: 10px;
}

.header-stats {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
}

.stat-item {
  display: flex;
  align-items: center;
  gap: 12px;
}

.stat-icon {
  font-size: 28px;
}

.stat-label {
  font-size: 13px;
  color: #64748b;
  margin-bottom: 4px;
}

.stat-value {
  font-size: 22px;
  font-weight: 700;
  color: #1e293b;
}

.stat-value.green { color: #22c55e; }
.stat-value.blue { color: #3b82f6; }

.data-source-tag {
  display: flex;
  align-items: center;
  gap: 8px;
}

.info-icon {
  font-size: 18px;
  color: #94a3b8;
  cursor: help;
}

.employment-tabs {
  margin-top: 8px;
}

.chart-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 20px;
  margin-bottom: 24px;
}

.chart-card {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px;
}

.chart-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px 0;
}

.data-table-wrap {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 16px;
}

.table-title {
  font-size: 15px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 12px 0;
}

.salary-text {
  color: #2563eb;
  font-weight: 600;
}

@media (max-width: 900px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
  .header-stats {
    gap: 20px;
  }
  .stat-value {
    font-size: 18px;
  }
}
</style>

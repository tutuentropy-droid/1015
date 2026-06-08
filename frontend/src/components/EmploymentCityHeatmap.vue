<template>
  <div class="city-heatmap">
    <div class="chart-row">
      <div class="chart-card">
        <h3 class="chart-title">🗺️ 城市分布气泡图（气泡大小=就业人数）</h3>
        <v-chart :option="bubbleOption" autoresize style="height: 380px; width: 100%" />
      </div>
      <div class="chart-card">
        <h3 class="chart-title">📊 城市分布热力条形图（颜色深浅=占比）</h3>
        <v-chart :option="barOption" autoresize style="height: 380px; width: 100%" />
      </div>
    </div>
    <div class="city-cards-wrap">
      <h3 class="section-title">🏙️ 热门就业城市 TOP 10</h3>
      <div class="city-cards">
        <div
          v-for="(city, idx) in topCities"
          :key="city.city"
          class="city-card"
          :style="{ background: getCardGradient(city.percentage, idx) }"
        >
          <div class="city-rank">{{ idx + 1 }}</div>
          <div class="city-info">
            <div class="city-name">
              <span class="city-text">{{ city.city }}</span>
              <el-tag size="small" effect="dark" type="info" class="province-tag">{{ city.province }}</el-tag>
            </div>
            <div class="city-stats">
              <span class="stat">
                <span class="stat-label">就业</span>
                <span class="stat-value">{{ city.count.toLocaleString() }}人</span>
              </span>
              <span class="stat">
                <span class="stat-label">占比</span>
                <span class="stat-value">{{ (city.percentage * 100).toFixed(1) }}%</span>
              </span>
              <span class="stat">
                <span class="stat-label">平均年薪</span>
                <span class="stat-value salary">¥{{ formatSalary(city.avg_salary) }}</span>
              </span>
            </div>
            <div class="city-bar">
              <div
                class="city-bar-inner"
                :style="{ width: (city.percentage / maxPercentage * 100).toFixed(1) + '%' }"
              ></div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { use } from 'echarts/core'
import { CanvasRenderer } from 'echarts/renderers'
import { ScatterChart, BarChart } from 'echarts/charts'
import {
  TitleComponent, TooltipComponent, LegendComponent,
  GridComponent, VisualMapComponent
} from 'echarts/components'
import VChart from 'vue-echarts'

use([
  CanvasRenderer, ScatterChart, BarChart, TitleComponent,
  TooltipComponent, LegendComponent, GridComponent, VisualMapComponent
])

const props = defineProps({
  cityData: {
    type: Array,
    default: () => []
  }
})

const CITY_COORDS = {
  '北京': [116.46, 39.92], '上海': [121.48, 31.22], '广州': [113.23, 23.16],
  '深圳': [114.07, 22.62], '杭州': [120.19, 30.26], '南京': [118.78, 32.04],
  '成都': [104.06, 30.67], '武汉': [114.31, 30.52], '西安': [108.95, 34.27],
  '苏州': [120.62, 31.32], '天津': [117.2, 39.13], '重庆': [106.54, 29.59],
  '青岛': [120.33, 36.07], '长沙': [112.98, 28.19], '郑州': [113.65, 34.76],
  '厦门': [118.1, 24.46], '合肥': [117.27, 31.86], '福州': [119.3, 26.08],
  '济南': [117.0, 36.65], '大连': [121.62, 38.92], '沈阳': [123.38, 41.8],
  '哈尔滨': [126.63, 45.75], '长春': [125.35, 43.88], '南昌': [115.89, 28.68],
  '南宁': [108.33, 22.84], '昆明': [102.73, 25.04], '贵阳': [106.71, 26.57],
  '太原': [112.53, 37.87], '石家庄': [114.48, 38.03], '兰州': [103.82, 36.06],
  '乌鲁木齐': [87.68, 43.77], '呼和浩特': [111.65, 40.82], '海口': [110.35, 20.02],
  '银川': [106.27, 38.47], '西宁': [101.74, 36.56], '拉萨': [91.11, 29.97],
  '宁波': [121.56, 29.86], '无锡': [120.29, 31.59], '佛山': [113.11, 23.05],
  '东莞': [113.75, 23.04], '珠海': [113.55, 22.19], '中山': [113.38, 22.52],
  '温州': [120.65, 28.01], '金华': [119.64, 29.12], '烟台': [121.39, 37.52],
  '潍坊': [119.1, 36.62], '泉州': [118.58, 24.93], '徐州': [117.2, 34.26],
  '常州': [119.95, 31.79], '南通': [120.86, 32.01], '惠州': [114.41, 23.11],
  '汕头': [116.69, 23.39], '咸阳': [108.72, 34.36], '绵阳': [104.73, 31.48],
  '南充': [106.11, 30.83], '宜昌': [111.3, 30.7], '襄阳': [112.14, 32.04],
  '湘潭': [112.94, 27.83], '株洲': [113.16, 27.83], '洛阳': [112.44, 34.7],
  '开封': [114.35, 34.79], '秦皇岛': [119.6, 39.93], '保定': [115.48, 38.85],
  '唐山': [118.02, 39.63], '延吉': [129.51, 42.89], '石河子': [86.03, 44.3],
  '雅安': [103.0, 29.98], '威海': [122.1, 37.5], '扬州': [119.42, 32.39],
  '镇江': [119.44, 32.2], '桂林': [110.28, 25.29], '三亚': [109.51, 18.25],
  '大理': [100.23, 25.59], '丽江': [100.25, 26.86], '包头': [109.84, 40.65],
}

function formatSalary(salary) {
  if (!salary) return '-'
  if (salary >= 10000) {
    return (salary / 10000).toFixed(1) + '万'
  }
  return salary.toString()
}

const topCities = computed(() => {
  return [...props.cityData].sort((a, b) => b.percentage - a.percentage).slice(0, 10)
})

const maxPercentage = computed(() => {
  if (!topCities.value.length) return 0.01
  return Math.max(...topCities.value.map(c => c.percentage))
})

function getCardGradient(pct, idx) {
  const gradients = [
    'linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%)',
    'linear-gradient(135deg, #f0fdf4 0%, #dcfce7 100%)',
    'linear-gradient(135deg, #fffbeb 0%, #fef3c7 100%)',
    'linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%)',
    'linear-gradient(135deg, #f5f3ff 0%, #ede9fe 100%)',
    'linear-gradient(135deg, #ecfeff 0%, #cffafe 100%)',
    'linear-gradient(135deg, #fff7ed 0%, #ffedd5 100%)',
    'linear-gradient(135deg, #fdf4ff 0%, #fae8ff 100%)',
    'linear-gradient(135deg, #f0f9ff 0%, #e0f2fe 100%)',
    'linear-gradient(135deg, #f1f5f9 0%, #e2e8f0 100%)',
  ]
  return gradients[idx % gradients.length]
}

const bubbleOption = computed(() => {
  const data = props.cityData.map(d => {
    const coords = CITY_COORDS[d.city] || [100 + Math.random() * 20, 30 + Math.random() * 10]
    return {
      name: d.city,
      value: [coords[0], coords[1], d.count, d.percentage, d.avg_salary, d.province]
    }
  })
  const maxCount = Math.max(...props.cityData.map(d => d.count), 1)
  return {
    tooltip: {
      trigger: 'item',
      backgroundColor: 'rgba(255,255,255,0.95)',
      borderColor: '#e2e8f0',
      borderWidth: 1,
      textStyle: { color: '#1e293b' },
      formatter: (params) => {
        const d = params.data.value
        return `
          <div style="font-weight:600;margin-bottom:6px;font-size:14px">${params.data.name}</div>
          <div>省份：<b>${d[5]}</b></div>
          <div>就业人数：<b>${d[2].toLocaleString()}</b> 人</div>
          <div>占比：<b>${(d[3] * 100).toFixed(1)}%</b></div>
          <div>平均年薪：<b style="color:#2563eb">¥${formatSalary(d[4])}</b></div>
        `
      }
    },
    grid: { left: 40, right: 40, top: 30, bottom: 40 },
    xAxis: {
      show: false,
      type: 'value',
      min: 85,
      max: 130
    },
    yAxis: {
      show: false,
      type: 'value',
      min: 20,
      max: 50
    },
    visualMap: {
      show: true,
      orient: 'horizontal',
      left: 'center',
      bottom: 5,
      min: 0,
      max: maxCount,
      dimension: 2,
      text: ['多', '少'],
      textStyle: { color: '#64748b', fontSize: 11 },
      inRange: {
        color: ['#93c5fd', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8']
      },
      calculable: true
    },
    series: [{
      type: 'scatter',
      symbolSize: (val) => {
        const baseSize = Math.sqrt(val[2] / maxCount) * 60 + 12
        return Math.max(12, Math.min(70, baseSize))
      },
      data: data,
      emphasis: {
        scale: 1.2,
        label: {
          show: true,
          formatter: (p) => p.data.name,
          position: 'top',
          fontSize: 12,
          fontWeight: 600,
          color: '#1e293b'
        }
      },
      label: {
        show: true,
        formatter: (p) => p.data.name,
        position: 'right',
        fontSize: 11,
        color: '#475569'
      },
      itemStyle: {
        shadowBlur: 10,
        shadowColor: 'rgba(0,0,0,0.15)',
        opacity: 0.85
      }
    }]
  }
})

const barOption = computed(() => {
  const sorted = [...props.cityData].sort((a, b) => a.percentage - b.percentage).slice(-15)
  const maxPct = Math.max(...sorted.map(d => d.percentage), 0.01)
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
          <div style="font-weight:600;margin-bottom:6px">${row.city} (${row.province})</div>
          <div>就业人数：<b>${row.count.toLocaleString()}</b> 人</div>
          <div>占比：<b>${(row.percentage * 100).toFixed(1)}%</b></div>
          <div>平均年薪：<b style="color:#2563eb">¥${formatSalary(row.avg_salary)}</b></div>
        `
      }
    },
    grid: { left: 80, right: 60, top: 20, bottom: 30 },
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
      data: sorted.map(d => d.city),
      axisLabel: { color: '#475569', fontSize: 12 },
      axisLine: { show: false },
      axisTick: { show: false }
    },
    visualMap: {
      show: false,
      min: 0,
      max: maxPct,
      inRange: {
        color: ['#bfdbfe', '#93c5fd', '#60a5fa', '#3b82f6', '#2563eb', '#1d4ed8']
      }
    },
    series: [{
      type: 'bar',
      data: sorted.map(d => d.percentage),
      barWidth: '65%',
      itemStyle: {
        borderRadius: [0, 4, 4, 0]
      },
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
.city-heatmap {
  width: 100%;
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

.city-cards-wrap {
  background: #fff;
  border: 1px solid #e2e8f0;
  border-radius: 10px;
  padding: 20px;
}

.section-title {
  font-size: 16px;
  font-weight: 600;
  color: #1e293b;
  margin: 0 0 16px 0;
}

.city-cards {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 12px;
}

.city-card {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  padding: 14px 16px;
  border-radius: 10px;
  border: 1px solid #e2e8f0;
  transition: transform 0.2s, box-shadow 0.2s;
}

.city-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.08);
}

.city-rank {
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: linear-gradient(135deg, #3b82f6, #2563eb);
  color: #fff;
  font-weight: 700;
  font-size: 16px;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.city-card:nth-child(1) .city-rank { background: linear-gradient(135deg, #fbbf24, #f59e0b); }
.city-card:nth-child(2) .city-rank { background: linear-gradient(135deg, #94a3b8, #64748b); }
.city-card:nth-child(3) .city-rank { background: linear-gradient(135deg, #d97706, #b45309); }

.city-info {
  flex: 1;
  min-width: 0;
}

.city-name {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.city-text {
  font-size: 16px;
  font-weight: 700;
  color: #1e293b;
}

.province-tag {
  font-size: 11px;
}

.city-stats {
  display: flex;
  flex-wrap: wrap;
  gap: 12px;
  margin-bottom: 8px;
}

.stat {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.stat-label {
  font-size: 11px;
  color: #94a3b8;
}

.stat-value {
  font-size: 13px;
  font-weight: 600;
  color: #475569;
}

.stat-value.salary {
  color: #2563eb;
}

.city-bar {
  height: 6px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 3px;
  overflow: hidden;
}

.city-bar-inner {
  height: 100%;
  background: linear-gradient(90deg, #3b82f6, #2563eb);
  border-radius: 3px;
  transition: width 0.5s ease;
}

@media (max-width: 900px) {
  .chart-row {
    grid-template-columns: 1fr;
  }
  .city-cards {
    grid-template-columns: 1fr;
  }
}
</style>

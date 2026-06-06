<template>
  <el-container class="app-container">
    <el-header class="app-header">
      <div class="header-inner">
        <div class="logo-wrap">
          <el-icon :size="32" color="#409eff"><School /></el-icon>
          <span class="logo-text">高考志愿填报决策系统</span>
        </div>
        <el-menu
          :default-active="activeMenu"
          mode="horizontal"
          router
          class="nav-menu"
          background-color="transparent"
          text-color="#606266"
          active-text-color="#409eff"
        >
          <el-menu-item index="/">
            <el-icon><DataAnalysis /></el-icon>
            <span>智能填报</span>
          </el-menu-item>
          <el-menu-item index="/colleges">
            <el-icon><OfficeBuilding /></el-icon>
            <span>院校查询</span>
          </el-menu-item>
          <el-menu-item index="/plan" v-if="volunteerStore.volunteerPlan">
            <el-icon><Tickets /></el-icon>
            <span>志愿方案</span>
          </el-menu-item>
        </el-menu>
      </div>
    </el-header>

    <el-main class="app-main">
      <router-view v-slot="{ Component }">
        <transition name="fade" mode="out-in">
          <component :is="Component" />
        </transition>
      </router-view>
    </el-main>

    <el-footer class="app-footer">
      <div class="footer-inner">
        <span>© 2026 高考志愿填报决策系统 · 数据仅供参考，请以官方公布为准</span>
      </div>
    </el-footer>
  </el-container>
</template>

<script setup>
import { computed, onMounted } from 'vue'
import { useRoute } from 'vue-router'
import { useVolunteerStore } from './stores/volunteer'

const route = useRoute()
const volunteerStore = useVolunteerStore()

const activeMenu = computed(() => route.path)

onMounted(() => {
  volunteerStore.loadMeta()
})
</script>

<style scoped>
.app-container {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}

.app-header {
  background: #fff;
  border-bottom: 1px solid #ebeef5;
  padding: 0;
  height: 64px;
  position: sticky;
  top: 0;
  z-index: 100;
}

.header-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: space-between;
}

.logo-wrap {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo-text {
  font-size: 18px;
  font-weight: 700;
  color: #2c3e50;
  letter-spacing: 1px;
}

.nav-menu {
  border-bottom: none;
}

.app-main {
  flex: 1;
  padding: 0;
}

.app-footer {
  background: #fff;
  border-top: 1px solid #ebeef5;
  padding: 0;
  height: 48px;
  color: #909399;
  font-size: 13px;
}

.footer-inner {
  max-width: 1280px;
  margin: 0 auto;
  padding: 0 24px;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>

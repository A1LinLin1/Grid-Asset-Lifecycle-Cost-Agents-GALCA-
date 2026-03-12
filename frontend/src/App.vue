<template>
  <div class="app-container">
    <el-container>
      <el-header class="header">
        <div class="logo">⚡ GALCA 工业智能体平台</div>
        <div class="subtitle">电网资产全寿命成本(LCC)多智能体分析系统</div>
      </el-header>
      <el-main>
        <Dashboard />
      </el-main>
    </el-container>
  </div>
</template>

<script setup>
import Dashboard from './components/Dashboard.vue'
</script>

<style scoped>
.header {
  background-color: #001529;
  color: white;
  display: flex;
  align-items: center;
  justify-content: space-between;
  padding: 0 40px;
}
.logo {
  font-size: 24px;
  font-weight: bold;
}
.subtitle {
  font-size: 14px;
  color: #a6adb4;
}
.app-container {
  min-height: 100vh;
}
</style>

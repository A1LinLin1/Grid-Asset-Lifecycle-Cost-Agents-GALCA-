<template>
  <div class="dashboard">
    <el-row :gutter="20">
      <!-- 左侧：上传区与任务控制 -->
      <el-col :span="8">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>📤 多模态数据摄取</span>
            </div>
          </template>
          <el-upload
            class="upload-demo"
            drag
            action="/api/v1/upload"
            multiple
            :on-success="handleUploadSuccess"
          >
            <el-icon class="el-icon--upload"><upload-filled /></el-icon>
            <div class="el-upload__text">
              拖拽台账表格/现场发票图片到此处，或 <em>点击上传</em>
            </div>
          </el-upload>
          <div class="status-box" v-if="taskStatus">
            <el-alert :title="taskStatus" type="success" show-icon :closable="false" />
          </div>
        </el-card>
      </el-col>

      <!-- 右侧：预测曲线展示 -->
      <el-col :span="16">
        <el-card class="box-card">
          <template #header>
            <div class="card-header">
              <span>📈 LCC 成本拟合曲线 (Echarts)</span>
            </div>
          </template>
          <div id="lcc-chart" style="height: 350px;"></div>
        </el-card>
      </el-col>
    </el-row>

    <!-- 下方：解析出的结构化台账数据 -->
    <el-row style="margin-top: 20px;">
      <el-col :span="24">
        <el-card>
          <template #header>
            <div class="card-header">
              <span>🗄️ 智能体提取的结构化台账</span>
              <el-button type="primary" size="small" @click="fetchRecords">刷新数据</el-button>
            </div>
          </template>
          <el-table :data="tableData" style="width: 100%" border stripe>
            <el-table-column prop="equipment_type" label="设备类型" width="180" />
            <el-table-column prop="equipment_model" label="型号" width="180" />
            <el-table-column prop="cost_category" label="成本类别" width="180" />
            <el-table-column prop="amount" label="金额(万元)" />
            <el-table-column prop="date" label="发生日期" />
            <el-table-column prop="source_document" label="来源文件" />
          </el-table>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import * as echarts from 'echarts'

const taskStatus = ref('')
const tableData = ref([])

const handleUploadSuccess = (response) => {
  taskStatus.value = response.message || '文件已进入后台处理队列！'
}

const fetchRecords = async () => {
  try {
    const res = await axios.get('/api/v1/records')
    tableData.value = res.data
  } catch (error) {
    console.error('获取台账失败', error)
  }
}

// 初始化一个空的 Echarts 图表
const initChart = () => {
  const chartDom = document.getElementById('lcc-chart')
  const myChart = echarts.init(chartDom)
  const option = {
    title: { text: '设备全生命周期成本预测', left: 'center' },
    tooltip: { trigger: 'axis' },
    xAxis: { type: 'category', data: ['2020', '2021', '2022', '2023', '2024', '2025 (预测)', '2026 (预测)'] },
    yAxis: { type: 'value', name: '成本(万元)' },
    series: [
      {
        data: [150, 230, 224, 218, 135, 147, 260],
        type: 'line',
        smooth: true,
        itemStyle: { color: '#5470C6' },
        areaStyle: { opacity: 0.3 }
      }
    ]
  }
  myChart.setOption(option)
}

onMounted(() => {
  initChart()
  fetchRecords()
})
</script>

<style scoped>
.card-header {
  font-weight: bold;
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.status-box {
  margin-top: 15px;
}
</style>

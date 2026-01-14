<template>
  <div id="app">
    <el-container>
      <el-header>
        <h1>Photo Collection System - Admin</h1>
      </el-header>
      <el-main>
        <router-view />
      </el-main>
    </el-container>
  </div>
</template>

<script setup lang="ts">
// Admin app component
</script>

<style scoped>
.el-header {
  background-color: #67c23a;
  color: white;
  display: flex;
  align-items: center;
}

.el-main {
  padding: 20px;
}
</style>

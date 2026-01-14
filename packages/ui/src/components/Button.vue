<template>
  <el-button :type="type" :size="size" @click="handleClick">
    <slot />
  </el-button>
</template>

<script setup lang="ts">
import { ElButton } from 'element-plus'

interface Props {
  type?: 'primary' | 'success' | 'warning' | 'danger' | 'info'
  size?: 'large' | 'default' | 'small'
}

withDefaults(defineProps<Props>(), {
  type: 'primary',
  size: 'default'
})

const emit = defineEmits<{
  click: [event: MouseEvent]
}>()

const handleClick = (event: MouseEvent) => {
  emit('click', event)
}
</script>

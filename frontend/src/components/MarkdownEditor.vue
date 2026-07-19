<template>
  <div class="markdown-editor">
    <t-textarea
      v-if="!preview"
      v-model="localValue"
      :placeholder="placeholder"
      :maxlength="maxlength"
      :autosize="{ minRows: 3, maxRows: 10 }"
    />
    <div v-else class="markdown-preview">
      <ChatMarkdown :content="localValue" />
    </div>
    <div class="editor-toolbar">
      <t-button variant="text" size="small" @click="preview = !preview">
        {{ preview ? 'Edit' : 'Preview' }}
      </t-button>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed } from 'vue'
import { ChatMarkdown } from '@tdesign-vue-next/chat'

const props = defineProps<{
  modelValue: string
  placeholder?: string
  maxlength?: number
}>()

const emit = defineEmits<{
  'update:modelValue': [value: string]
}>()

const preview = ref(false)

const localValue = computed({
  get: () => props.modelValue,
  set: (val: string) => emit('update:modelValue', val),
})
</script>

<style scoped>
.markdown-editor {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.markdown-preview {
  border: 1px solid var(--td-border-level-2-color, #e0e0e0);
  border-radius: var(--td-radius-default, 3px);
  padding: 8px 12px;
  min-height: 80px;
  background: var(--td-bg-color-secondarycontainer, #f3f3f3);
}

.editor-toolbar {
  display: flex;
  justify-content: flex-end;
}
</style>
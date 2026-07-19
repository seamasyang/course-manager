<template>
  <div style="padding: 24px">
    <t-row justify="space-between" align="center" style="margin-bottom: 16px">
      <t-col>
        <t-heading :level="4">Courses</t-heading>
      </t-col>
      <t-col>
        <t-button theme="primary" @click="openCreateDialog">Add Course</t-button>
      </t-col>
    </t-row>

    <t-table
      :data="store.courses"
      :loading="store.loading"
      row-key="id"
      :columns="columns"
      :pagination="pagination"
      @page-change="onPageChange"
    >
      <template #schedule_id="{ row }">
        {{ getScheduleLabel(row.schedule_id) }}
      </template>
      <template #content="{ row }">
        <ChatMarkdown :content="row.content || ''" />
      </template>
      <template #follow_up="{ row }">
        <ChatMarkdown :content="row.follow_up || ''" />
      </template>
      <template #operation="{ row }">
        <t-button variant="text" theme="primary" @click="openEditDialog(row)">Edit</t-button>
        <t-popconfirm content="Are you sure you want to delete this course?" @confirm="handleDelete(row.id)">
          <t-button variant="text" theme="danger">Delete</t-button>
        </t-popconfirm>
      </template>
    </t-table>

    <t-dialog
      v-model:visible="dialogVisible"
      :header="isEditing ? 'Edit Course' : 'Add Course'"
      :confirm-on-enter="true"
      @confirm="handleSubmit"
    >
      <t-form :data="formData" :rules="rules" ref="formRef" @submit="handleSubmit">
        <t-form-item label="Schedule" name="schedule_id">
          <t-select v-model="formData.schedule_id" placeholder="Select schedule">
            <t-option
              v-for="sched in scheduleStore.schedules"
              :key="sched.id"
              :value="sched.id"
              :label="`${getInstitutionName(sched.institution_id)} - ${sched.subject}`"
            />
          </t-select>
        </t-form-item>
        <t-form-item label="Date" name="date">
          <t-date-picker v-model="formData.date" placeholder="Select date" />
        </t-form-item>
        <t-form-item label="Content" name="content">
          <MarkdownEditor v-model="formData.content" placeholder="Enter content (markdown supported)" :maxlength="500" />
        </t-form-item>
        <t-form-item label="Follow Up" name="follow_up">
          <MarkdownEditor v-model="formData.follow_up" placeholder="Enter follow up (markdown supported)" />
        </t-form-item>
      </t-form>
    </t-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { useCourseStore } from '@/stores/course'
import { useScheduleStore } from '@/stores/schedule'
import { useInstitutionStore } from '@/stores/institution'
import { ChatMarkdown } from '@tdesign-vue-next/chat'
import MarkdownEditor from '@/components/MarkdownEditor.vue'
import type { Course } from '@/types/course'
import type { FormInstanceFunctions, FormRule } from 'tdesign-vue-next'

const store = useCourseStore()
const scheduleStore = useScheduleStore()
const institutionStore = useInstitutionStore()
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<string | null>(null)
const formRef = ref<FormInstanceFunctions>()

const formData = reactive({
  schedule_id: '',
  date: '',
  content: '',
  follow_up: '',
})

const rules: Record<string, FormRule[]> = {
  schedule_id: [{ required: true, message: 'Schedule is required', type: 'warning' }],
}

const pagination = reactive({
  defaultPageSize: 10,
  total: 0,
  defaultCurrent: 1,
})

const columns = [
  { colKey: 'schedule_id', title: 'Schedule', width: '200' },
  { colKey: 'date', title: 'Date', width: '120' },
  { colKey: 'content', title: 'Content', width: '200' },
  { colKey: 'follow_up', title: 'Follow Up', width: '150' },
  { colKey: 'operation', title: 'Actions', width: '150' },
]

function getInstitutionName(id: string): string {
  const inst = institutionStore.institutions.find((i) => i.id === id)
  return inst ? inst.name : id
}

function getScheduleLabel(id: string): string {
  const sched = scheduleStore.schedules.find((s) => s.id === id)
  if (!sched) return id
  return `${getInstitutionName(sched.institution_id)} - ${sched.subject}`
}

function resetForm() {
  formData.schedule_id = ''
  formData.date = ''
  formData.content = ''
  formData.follow_up = ''
}

function openCreateDialog() {
  isEditing.value = false
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(course: Course) {
  isEditing.value = true
  editingId.value = course.id
  formData.schedule_id = course.schedule_id
  formData.date = course.date || ''
  formData.content = course.content || ''
  formData.follow_up = course.follow_up || ''
  dialogVisible.value = true
}

async function handleSubmit() {
  const valid = await formRef.value?.validate()
  if (!valid) return

  if (isEditing.value && editingId.value) {
    await store.update(editingId.value, formData)
  } else {
    await store.create(formData)
  }
  dialogVisible.value = false
  await store.fetchAll()
}

async function handleDelete(id: string) {
  await store.remove(id)
}

function onPageChange(_pageInfo: { current: number; pageSize: number }) {
  // Handled by the table internally since all data is in store
}

watch(
  () => store.courses,
  (val) => {
    pagination.total = val.length
  },
  { immediate: true }
)

onMounted(() => {
  store.fetchAll()
  scheduleStore.fetchAll()
  institutionStore.fetchAll()
})
</script>
<template>
  <div style="padding: 24px">
    <t-row justify="space-between" align="center" style="margin-bottom: 16px">
      <t-col>
        <t-heading :level="4">Schedules</t-heading>
      </t-col>
      <t-col>
        <t-button theme="primary" @click="openCreateDialog">Add Schedule</t-button>
      </t-col>
    </t-row>

    <t-table
      :data="store.schedules"
      :loading="store.loading"
      row-key="id"
      :columns="columns"
      :pagination="pagination"
      @page-change="onPageChange"
    >
      <template #institution_id="{ row }">
        {{ row.institution.name }}
      </template>
      <template #start_time="{ row }">
        {{ formatTime(row.start_time) }}
      </template>
      <template #end_time="{ row }">
        {{ formatTime(row.end_time) }}
      </template>
      <template #operation="{ row }">
        <t-button variant="text" theme="primary" @click="openEditDialog(row)">Edit</t-button>
        <t-popconfirm content="Are you sure you want to delete this schedule?" @confirm="handleDelete(row.id)">
          <t-button variant="text" theme="danger">Delete</t-button>
        </t-popconfirm>
      </template>
    </t-table>

    <t-dialog
      v-model:visible="dialogVisible"
      :header="isEditing ? 'Edit Schedule' : 'Add Schedule'"
      :confirm-on-enter="true"
      @confirm="handleSubmit"
    >
      <t-form :data="formData" :rules="rules" ref="formRef" @submit="handleSubmit">
        <t-form-item label="Institution" name="institution_id">
          <t-select v-model="formData.institution_id" placeholder="Select institution">
            <t-option
              v-for="inst in institutionStore.institutions"
              :key="inst.id"
              :value="inst.id"
              :label="inst.name"
            />
          </t-select>
        </t-form-item>
        <t-form-item label="Subject" name="subject">
          <t-select v-model="formData.subject" placeholder="Select subject">
            <t-option value="数学" label="数学" />
            <t-option value="英语" label="英语" />
            <t-option value="物理" label="物理" />
            <t-option value="体育" label="体育" />
            <t-option value="化学" label="化学" />
            <t-option value="语文" label="语文" />
          </t-select>
        </t-form-item>
        <t-form-item label="Teacher Name" name="teacher_name">
          <t-input v-model="formData.teacher_name" placeholder="Enter teacher name" />
        </t-form-item>
        <t-form-item label="Start Date" name="start_date">
          <t-date-picker v-model="formData.start_date" placeholder="Select start date" />
        </t-form-item>
        <t-form-item label="End Date" name="end_date">
          <t-date-picker v-model="formData.end_date" placeholder="Select end date" />
        </t-form-item>
        <t-form-item label="Start Time" name="start_time">
          <t-time-picker v-model="formData.start_time" format="HH:mm" placeholder="Select start time" />
        </t-form-item>
        <t-form-item label="End Time" name="end_time">
          <t-time-picker v-model="formData.end_time" format="HH:mm" placeholder="Select end time" />
        </t-form-item>
        <t-form-item label="Remarks" name="remarks">
          <t-input v-model="formData.remarks" placeholder="Enter remarks" />
        </t-form-item>
      </t-form>
    </t-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, watch } from 'vue'
import { useScheduleStore } from '@/stores/schedule'
import { useInstitutionStore } from '@/stores/institution'
import type { Schedule } from '@/types/schedule'
import type { FormInstanceFunctions, FormRule } from 'tdesign-vue-next'

const store = useScheduleStore()
const institutionStore = useInstitutionStore()
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<string | null>(null)
const formRef = ref<FormInstanceFunctions>()

const formData = reactive({
  institution_id: '',
  subject: '数学',
  teacher_name: '',
  start_date: '',
  end_date: '',
  start_time: '',
  end_time: '',
  remarks: '',
})

const rules: Record<string, FormRule[]> = {
  institution_id: [{ required: true, message: 'Institution is required', type: 'warning' }],
  subject: [{ required: true, message: 'Subject is required', type: 'warning' }],
}

const pagination = reactive({
  defaultPageSize: 10,
  total: 0,
  defaultCurrent: 1,
})

const columns = [
  { colKey: 'institution_id', title: 'Institution', width: '150' },
  { colKey: 'subject', title: 'Subject', width: '100' },
  { colKey: 'teacher_name', title: 'Teacher', width: '120' },
  { colKey: 'start_date', title: 'Start Date', width: '120' },
  { colKey: 'end_date', title: 'End Date', width: '120' },
  { colKey: 'start_time', title: 'Start Time', width: '100' },
  { colKey: 'end_time', title: 'End Time', width: '100' },
  { colKey: 'remarks', title: 'Remarks', width: '150' },
  { colKey: 'operation', title: 'Actions', width: '150' },
]

function formatTime(time: string | null | undefined): string {
  if (!time) return ''
  // time format from backend may be HH:mm:ss or HH:mm
  return time.substring(0, 5)
}

function resetForm() {
  formData.institution_id = ''
  formData.subject = '数学'
  formData.teacher_name = ''
  formData.start_date = ''
  formData.end_date = ''
  formData.start_time = ''
  formData.end_time = ''
  formData.remarks = ''
}

async function openCreateDialog() {
  isEditing.value = false
  editingId.value = null
  resetForm()
  await ensureReferenceData()
  dialogVisible.value = true
}

async function openEditDialog(schedule: Schedule) {
  isEditing.value = true
  editingId.value = schedule.id
  formData.institution_id = schedule.institution_id
  formData.subject = schedule.subject
  formData.teacher_name = schedule.teacher_name || ''
  formData.start_date = schedule.start_date || ''
  formData.end_date = schedule.end_date || ''
  formData.start_time = schedule.start_time || ''
  formData.end_time = schedule.end_time || ''
  formData.remarks = schedule.remarks || ''
  await ensureReferenceData()
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
  () => store.schedules,
  (val) => {
    pagination.total = val.length
  },
  { immediate: true }
)

onMounted(() => {
  store.fetchAll()
})

async function ensureReferenceData() {
  if (institutionStore.institutions.length === 0) {
    await institutionStore.fetchAll()
  }
}
</script>
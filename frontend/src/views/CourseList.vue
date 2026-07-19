<template>
  <div style="padding: 24px">
    <t-row justify="space-between" align="center" style="margin-bottom: 16px">
      <t-col>
        <t-heading :level="4">Courses</t-heading>
      </t-col>
      <t-col>
        <t-button theme="primary" @click="openCreate">Add Course</t-button>
      </t-col>
    </t-row>

    <t-table :data="store.courses" :loading="store.loading" row-key="id" :columns="columns" :pagination="pagination"
      @page-change="onPageChange">
      <template #institution_id="{ row }">
        {{ row.schedule.institution.name }}
      </template>
      <template #schedule_id="{ row }">
        {{ row.schedule.subject }}
      </template>
      <template #content="{ row }">
        <ChatMarkdown :content="row.content || ''" />
      </template>
      <template #follow_up="{ row }">
        <ChatMarkdown :content="row.follow_up || ''" />
      </template>
      <template #operation="{ row }">
        <t-button variant="text" theme="primary" @click="openView(row)">View</t-button>
        <t-button variant="text" theme="primary" @click="openEdit(row)">Edit</t-button>
        <t-popconfirm content="Are you sure you want to delete this course?" @confirm="handleDelete(row.id)">
          <t-button variant="text" theme="danger">Delete</t-button>
        </t-popconfirm>
      </template>
    </t-table>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/course'
import { useScheduleStore } from '@/stores/schedule'
import { useInstitutionStore } from '@/stores/institution'
import { ChatMarkdown } from '@tdesign-vue-next/chat'
import type { Course } from '@/types/course'

const router = useRouter()
const store = useCourseStore()
const scheduleStore = useScheduleStore()
const institutionStore = useInstitutionStore()

const pagination = reactive({
  defaultPageSize: 10,
  total: 0,
  defaultCurrent: 1,
})

const columns = [
  { colKey: 'institution_id', title: 'Institution', width: '120' },
  { colKey: 'schedule_id', title: 'Subject', width: '60' },
  { colKey: 'date', title: 'Date', width: '120' },
  { colKey: 'operation', title: 'Actions', width: '150' },
]


function openCreate() {
  router.push('/courses/new')
}

function openView(course: Course) {
  router.push(`/courses/${course.id}`)
}

function openEdit(course: Course) {
  router.push(`/courses/${course.id}?mode=edit`)
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
  if (scheduleStore.schedules.length === 0) {
    scheduleStore.fetchAll()
  }
  if (institutionStore.institutions.length === 0) {
    institutionStore.fetchAll()
  }
})
</script>
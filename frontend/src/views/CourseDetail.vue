<template>
  <div style="padding: 24px;">
    <t-row justify="space-between" align="center" style="margin-bottom: 16px">
      <t-col>
        <t-button variant="text" @click="goBack">
          <template #icon><chevron-left-icon /></template>
          Back
        </t-button>
        <t-heading :level="4" style="display: inline-block; margin-left: 8px">
          {{ pageTitle }}
        </t-heading>
      </t-col>
    </t-row>

    <t-card :loading="loading">
      <t-form :data="formData" :rules="rules" ref="formRef" label-align="top">
        <t-form-item label="Schedule" name="schedule_id">
          <t-select
            v-model="formData.schedule_id"
            :disabled="isViewMode"
            placeholder="Select schedule"
          >
            <t-option
              v-for="sched in scheduleStore.schedules"
              :key="sched.id"
              :value="sched.id"
              :label="`${sched.institution.name} - ${sched.subject}`"
            />
          </t-select>
        </t-form-item>
        <t-form-item label="Date" name="date">
          <t-date-picker v-model="formData.date" :disabled="isViewMode" placeholder="Select date" />
        </t-form-item>
        <t-form-item label="Content" name="content">
          <template v-if="isViewMode">
            <div class="markdown-preview">
              <ChatMarkdown :content="formData.content || ''"/>
            </div>
          </template>
          <template v-else>
            <MarkdownEditor v-model="formData.content" placeholder="Enter content (markdown supported)" :maxlength="500" />
          </template>
        </t-form-item>
        <t-form-item label="Follow Up" name="follow_up">
          <template v-if="isViewMode">
            <div class="markdown-preview">
              <ChatMarkdown :content="formData.follow_up || ''" />
            </div>
          </template>
          <template v-else>
            <MarkdownEditor v-model="formData.follow_up" placeholder="Enter follow up (markdown supported)" />
          </template>
        </t-form-item>
        <t-form-item v-if="!isViewMode">
          <t-space>
            <t-button theme="primary" @click="handleSave">{{ isCreateMode ? 'Create' : 'Save' }}</t-button>
            <t-button variant="outline" @click="goBack">Cancel</t-button>
          </t-space>
        </t-form-item>
      </t-form>
    </t-card>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref, computed } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { useCourseStore } from '@/stores/course'
import { useScheduleStore } from '@/stores/schedule'
import { useInstitutionStore } from '@/stores/institution'
import { ChatMarkdown } from '@tdesign-vue-next/chat'
import { ChevronLeftIcon } from 'tdesign-icons-vue-next'
import MarkdownEditor from '@/components/MarkdownEditor.vue'
import type { FormInstanceFunctions, FormRule } from 'tdesign-vue-next'

const route = useRoute()
const router = useRouter()
const courseStore = useCourseStore()
const scheduleStore = useScheduleStore()
const institutionStore = useInstitutionStore()

const isCreateMode = computed(() => route.name === 'CourseCreate')
const isViewMode = computed(() => !isCreateMode.value && route.query.mode !== 'edit')
const courseId = computed(() => route.params.id as string | undefined)
const loading = ref(false)
const formRef = ref<FormInstanceFunctions>()

const pageTitle = computed(() => {
  if (isCreateMode.value) return 'Add Course'
  if (isViewMode.value) return 'Course Details'
  return 'Edit Course'
})

const formData = reactive({
  schedule_id: '',
  date: '',
  content: '',
  follow_up: '',
})

const rules: Record<string, FormRule[]> = {
  schedule_id: [{ required: true, message: 'Schedule is required', type: 'warning' }],
}

function goBack() {
  router.push('/courses')
}

async function loadCourse() {
  if (isCreateMode.value) return

  loading.value = true
  try {
    if (scheduleStore.schedules.length === 0) {
      await scheduleStore.fetchAll()
    }    

    const id = courseId.value
    if (!id) return

    let course = courseStore.courses.find((c) => c.id === id)
    if (!course) {
      const { getCourse } = await import('@/api/course')
      course = await getCourse(id)
    }
    if (course) {
      formData.schedule_id = course.schedule_id
      formData.date = course.date || ''
      formData.content = course.content || ''
      formData.follow_up = course.follow_up || ''
      formData.schedule = course.schedule || null
    }
  } finally {
    loading.value = false
  }
}

async function handleSave() {
  const valid = await formRef.value?.validate()
  if (!valid) return

  if (isCreateMode.value) {
    await courseStore.create(formData)
  } else if (courseId.value) {
    await courseStore.update(courseId.value, formData)
  }

  router.push('/courses')
}

onMounted(async () => {
  // Always load reference data for select options
  if (scheduleStore.schedules.length === 0) {
    await scheduleStore.fetchAll()
  }
  if (institutionStore.institutions.length === 0) {
    await institutionStore.fetchAll()
  }
  loadCourse()
})
</script>

<style scoped>
.markdown-preview {
  width: 100%;
  padding: 8px 12px;
  border: 1px solid var(--td-border-level-2-color, #e0e0e0);
  border-radius: var(--td-radius-default, 3px);
  min-height: 80px;
  background: var(--td-bg-color-secondarycontainer, #f3f3f3);
}
</style>
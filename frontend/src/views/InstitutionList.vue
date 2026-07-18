<template>
  <div style="padding: 24px">
    <t-row justify="space-between" align="center" style="margin-bottom: 16px">
      <t-col>
        <t-heading :level="4">Institutions</t-heading>
      </t-col>
      <t-col>
        <t-button theme="primary" @click="openCreateDialog">Add Institution</t-button>
      </t-col>
    </t-row>

    <t-table
      :data="store.institutions"
      :loading="store.loading"
      row-key="id"
      :columns="columns"
      :pagination="pagination"
      @page-change="onPageChange"
    >
      <template #operation="{ row }">
        <t-button variant="text" theme="primary" @click="openEditDialog(row)">Edit</t-button>
        <t-popconfirm content="Are you sure you want to delete this institution?" @confirm="handleDelete(row.id)">
          <t-button variant="text" theme="danger">Delete</t-button>
        </t-popconfirm>
      </template>
    </t-table>

    <t-dialog
      v-model:visible="dialogVisible"
      :header="isEditing ? 'Edit Institution' : 'Add Institution'"
      :confirm-on-enter="true"
      @confirm="handleSubmit"
    >
      <t-form :data="formData" :rules="rules" ref="formRef" @submit="handleSubmit">
        <t-form-item label="Name" name="name">
          <t-input v-model="formData.name" placeholder="Enter institution name" />
        </t-form-item>
        <t-form-item label="Location" name="location">
          <t-input v-model="formData.location" placeholder="Enter location" />
        </t-form-item>
        <t-form-item label="Contact Name" name="contact_name">
          <t-input v-model="formData.contact_name" placeholder="Enter contact name" />
        </t-form-item>
        <t-form-item label="Contact Mobile" name="contact_mobile">
          <t-input v-model="formData.contact_mobile" placeholder="Enter mobile number" />
        </t-form-item>
        <t-form-item label="Contact WeChat" name="contact_wechat">
          <t-input v-model="formData.contact_wechat" placeholder="Enter WeChat ID" />
        </t-form-item>
      </t-form>
    </t-dialog>
  </div>
</template>

<script setup lang="ts">
import { onMounted, reactive, ref } from 'vue'
import { useInstitutionStore } from '@/stores/institution'
import type { Institution } from '@/types/institution'
import type { FormInstanceFunctions, FormRule } from 'tdesign-vue-next'

const store = useInstitutionStore()
const dialogVisible = ref(false)
const isEditing = ref(false)
const editingId = ref<string | null>(null)
const formRef = ref<FormInstanceFunctions>()

const formData = reactive({
  name: '',
  location: '',
  contact_name: '',
  contact_mobile: '',
  contact_wechat: '',
})

const rules: Record<string, FormRule[]> = {
  name: [{ required: true, message: 'Name is required', type: 'warning' }],
}

const pagination = reactive({
  defaultPageSize: 10,
  total: 0,
  defaultCurrent: 1,
})

const columns = [
  { colKey: 'name', title: 'Name', width: '150' },
  { colKey: 'location', title: 'Location', width: '150' },
  { colKey: 'contact_name', title: 'Contact Name', width: '120' },
  { colKey: 'contact_mobile', title: 'Contact Mobile', width: '130' },
  { colKey: 'contact_wechat', title: 'WeChat', width: '130' },
  { colKey: 'operation', title: 'Actions', width: '150' },
]

function resetForm() {
  formData.name = ''
  formData.location = ''
  formData.contact_name = ''
  formData.contact_mobile = ''
  formData.contact_wechat = ''
}

function openCreateDialog() {
  isEditing.value = false
  editingId.value = null
  resetForm()
  dialogVisible.value = true
}

function openEditDialog(institution: Institution) {
  isEditing.value = true
  editingId.value = institution.id
  formData.name = institution.name
  formData.location = institution.location || ''
  formData.contact_name = institution.contact_name || ''
  formData.contact_mobile = institution.contact_mobile || ''
  formData.contact_wechat = institution.contact_wechat || ''
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

function onPageChange(pageInfo: { current: number; pageSize: number }) {
  // Handled by the table internally since all data is in store
}

onMounted(() => {
  store.fetchAll()
})
</script>
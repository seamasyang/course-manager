<template>
  <t-layout style="min-height: 100vh">
    <t-aside
      :width="collapsed ? 64 : 200"
      :style="{
        position: 'sticky',
        top: 0,
        height: '100vh',
        alignSelf: 'flex-start',
        flexShrink: 0,
        overflow: 'hidden',
        minWidth: collapsed ? '64px' : '200px',
        maxWidth: collapsed ? '64px' : '200px',
        transition: 'width 0.2s, min-width 0.2s, max-width 0.2s',
      }"
    >
      <t-menu theme="light" :value="$route.path" @change="navigate" :collapsed="collapsed">
        <template #logo>
          <h3 v-if="!collapsed" style="margin: 0; padding: 16px; text-align: center; white-space: nowrap;">Course manager</h3>
          <h3 v-else style="margin: 0; padding: 16px; text-align: center;">CM</h3>
        </template>
        <t-menu-item value="/institutions">
          <template #icon><t-icon name="city-11" /></template>
          <span v-if="!collapsed">Institutions</span>
        </t-menu-item>
        <t-menu-item value="/schedules">
          <template #icon><t-icon name="calendar" /></template>
          <span v-if="!collapsed">Schedules</span>
        </t-menu-item>
        <t-menu-item value="/courses">
          <template #icon><t-icon name="book" /></template>
          <span v-if="!collapsed">Courses</span>
        </t-menu-item>
      </t-menu>
      <div
        style="
          position: absolute;
          bottom: 16px;
          width: 100%;
          display: flex;
          justify-content: center;
          cursor: pointer;
        "
        @click="collapsed = !collapsed"
        @keydown.enter="collapsed = !collapsed"
        tabindex="0"
        role="button"
        :aria-label="collapsed ? 'Expand sidebar' : 'Collapse sidebar'"
      >
        <t-button variant="text" shape="square">
          <template #icon><t-icon :name="collapsed ? 'chevron-right' : 'chevron-left'" /></template>
        </t-button>
      </div>
    </t-aside>
    <t-layout>
      <t-content>
        <router-view />
      </t-content>
      <t-footer>Copyright @ {{ new Date().getFullYear() }} David Yang.</t-footer>
    </t-layout>
  </t-layout>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const collapsed = ref(false)

function navigate(path: string) {
  router.push(path)
}
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
<template>
  <t-layout>
    <t-header>
      <t-heading :level="3" style="margin: 0">Course Manager</t-heading>
    </t-header>
    <t-content>
      <router-view />
    </t-content>
  </t-layout>
</template>

<script setup lang="ts">
</script>

<style>
body {
  margin: 0;
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
}
</style>
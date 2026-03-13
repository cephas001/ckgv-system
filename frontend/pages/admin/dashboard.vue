<template>
  <div class="w-full h-full bg-white">
    <div class="p-10">
      <h1 class="text-2xl font-extrabold tracking-tight text-slate-900">
        Welcome to the Admin Portal
      </h1>
      <p class="text-sm font-semibold text-slate-500 mt-2">
        This page is protected by auth middleware.
      </p>
    </div>
  </div>
</template>

<script setup>
definePageMeta({
  middleware: "auth",
});
</script>


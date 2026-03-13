<template>
  <div class="flex h-screen bg-[#f8fafc] antialiased text-slate-800">
    <Sidebar />
    <main class="flex-1 flex flex-col min-w-0 relative pl-64">
      <NuxtPage />
    </main>
    <ToastNotification />
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const activeClass =
  "bg-indigo-50/70 text-black font-semibold border-indigo-100";
const inactiveClass =
  "text-slate-500 font-medium border-transparent hover:bg-slate-50 hover:text-slate-800";

const route = useRoute();

const isActive = (path) => {
  if (path === "/") return route.path === "/" || route.path === "/graph";
  return route.path === path;
};

const pageTitle = computed(() =>
  isActive("/directory") ? "Course Directory" : "Specialization Explorer",
);

const pageSubtitle = computed(() =>
  isActive("/directory")
    ? "Browse all courses and filter by course code or title."
    : "Interactive physics map of the Computer Science curriculum.",
);

const pageActionLabel = computed(() =>
  isActive("/directory") ? "Export List" : "Export Map",
);
</script>

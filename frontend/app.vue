<template>
  <div class="flex h-screen bg-[#f8fafc] antialiased text-slate-800">
    <Sidebar />
    <main class="flex-1 flex flex-col min-w-0 relative pl-64">
      <NuxtPage />
      <!-- <header class="h-20 px-8 flex items-center justify-between shrink-0">
        <div>
          <h2 class="text-2xl font-bold tracking-tight text-slate-800">
            {{ pageTitle }}
          </h2>
          <p class="text-sm font-medium text-slate-500 mt-0.5">
            {{ pageSubtitle }}
          </p>
        </div>
        <button
          class="bg-[#e33e38] hover:bg-[#c93631] text-white px-5 py-2 rounded-xl text-sm font-bold shadow-[0_4px_14px_0_rgba(227,62,56,0.39)] transition-all transform hover:-translate-y-0.5"
        >
          {{ pageActionLabel }}
        </button>
      </header> -->

      <!-- <div class="flex-1 px-8 pb-8 overflow-hidden flex flex-col">
        <div
          class="flex-1 bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden relative group"
        >
         
        </div>
      </div> -->
    </main>
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

<template>
  <div class="flex h-screen bg-[#f8fafc] antialiased text-slate-800">
    <aside
      class="w-64 bg-white border-r border-slate-200 flex flex-col shadow-sm z-20"
    >
      <div class="h-20 flex items-center px-6 border-b border-slate-100">
        <div
          class="w-8 h-8 rounded-lg bg-[#160d27] flex items-center justify-center mr-3 shadow-md"
        >
          <span class="text-white font-bold text-sm tracking-wider">MU</span>
        </div>
        <h1 class="font-bold text-lg text-slate-800 tracking-tight">
          Curriculum<span class="text-[#e33e38]">OS</span>
        </h1>
      </div>

      <nav class="flex-1 px-4 py-6 space-y-2">
        <NuxtLink
          to="/"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
          :class="
            isActive('/')
              ? 'bg-indigo-50/70 text-[#160d27] font-semibold border-indigo-100'
              : 'text-slate-500 font-medium border-transparent hover:bg-slate-50 hover:text-slate-800'
          "
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 opacity-75"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M14 10l-2 1m0 0l-2-1m2 1v2.5M20 7l-2 1m2-1l-2-1m2 1v2.5M14 4l-2-1-2 1M4 7l2-1M4 7l2 1M4 7v2.5M12 21l-2-1m2 1l2-1m-2 1v-2.5M6 18l-2-1v-2.5M18 18l2-1v-2.5"
            />
          </svg>
          Knowledge Graph
        </NuxtLink>

        <NuxtLink
          to="/directory"
          class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
          :class="
            isActive('/directory')
              ? 'bg-indigo-50/70 text-[#160d27] font-semibold border-indigo-100'
              : 'text-slate-500 font-medium border-transparent hover:bg-slate-50 hover:text-slate-800'
          "
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-5 w-5 opacity-75"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5H7a2 2 0 00-2 2v12a2 2 0 002 2h10a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2m-3 7h3m-3 4h3m-6-4h.01M9 16h.01"
            />
          </svg>
          Course Directory
        </NuxtLink>
      </nav>

      <div class="p-4 border-t border-slate-100 space-y-3">
        <NuxtLink
          to="/admin/login"
          class="flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold text-slate-400 hover:text-slate-700 hover:bg-slate-50 transition-colors"
        >
          <span class="tracking-widest uppercase">Admin</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 opacity-70"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M9 5l7 7-7 7"
            />
          </svg>
        </NuxtLink>

        <div class="flex items-center gap-3 px-2 py-2">
          <div
            class="w-9 h-9 rounded-full bg-slate-200 border-2 border-white shadow-sm flex items-center justify-center text-sm font-bold text-slate-600"
          >
            PO
          </div>
          <div class="flex flex-col">
            <span class="text-sm font-bold text-slate-700 leading-none mb-1"
              >Peter O.</span
            >
            <span class="text-xs font-medium text-slate-400 leading-none"
              >Administrator</span
            >
          </div>
        </div>
      </div>
    </aside>

    <main class="flex-1 flex flex-col min-w-0 overflow-hidden relative">
      <header class="h-20 px-8 flex items-center justify-between shrink-0">
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
      </header>

      <div class="flex-1 px-8 pb-8 overflow-hidden flex flex-col">
        <div
          class="flex-1 bg-white rounded-3xl shadow-[0_8px_30px_rgb(0,0,0,0.04)] border border-slate-100 overflow-hidden relative group"
        >
          <NuxtPage />
        </div>
      </div>
    </main>
  </div>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

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

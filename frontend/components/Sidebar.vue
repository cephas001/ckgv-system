<template>
  <aside
    class="w-64 bg-white border-r border-slate-200 flex flex-col shadow-sm z-20 fixed inset-y-0 left-0 shrink-0"
  >
    <NuxtLink
      to="/"
      class="h-20 flex items-center px-6 border-b border-slate-100"
    >
      <div
        class="w-8 h-8 rounded-lg bg-[#160d27] flex items-center justify-center mr-3 shadow-md text-center"
      >
        <span class="text-white font-bold text-sm tracking-wider">MU</span>
      </div>
      <h1 class="font-bold text-lg text-black tracking-tight">CKGV System</h1>
    </NuxtLink>

    <nav class="flex-1 px-4 py-6 space-y-2">
      <NuxtLink
        to="/"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
        :class="isActive('/') ? activeClass : inactiveClass"
      >
        <IconsKnowledgeGraph />
        Knowledge Graph
      </NuxtLink>

      <NuxtLink
        to="/directory"
        class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
        :class="isActive('/directory') ? activeClass : inactiveClass"
      >
        <IconsList />
        Course Directory
      </NuxtLink>
    </nav>

    <div class="p-4 border-t border-slate-100 space-y-3">
      <NuxtLink
        to="/admin/login"
        :class="[
          route.path.startsWith('/admin')
            ? 'text-black'
            : ' text-slate-400 hover:text-slate-700',
          'flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold hover:bg-slate-50 transition-colors',
        ]"
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
        <div class="w-9 h-9 rounded-full flex items-center justify-center">
          <img
            src="/assets/images/avatar.png"
            alt="Peter O."
            class="w-full h-full object-cover rounded-full"
          />
        </div>
        <div class="flex flex-col">
          <span class="text-sm font-bold text-black/90 leading-none mb-1"
            >Peter O.</span
          >
          <span class="text-xs font-medium text-black/70 leading-none"
            >Administrator</span
          >
        </div>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const activeClass = "bg-indigo-50/70 text-black border-indigo-100";
const inactiveClass =
  "text-slate-500 font-medium border-transparent hover:bg-slate-50 hover:text-slate-800";

const route = useRoute();

const isActive = (path) => {
  if (path === "/") return route.path === "/" || route.path === "/graph";
  return route.path === path;
};
</script>

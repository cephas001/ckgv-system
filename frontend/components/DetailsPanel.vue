<template>
  <div
    class="absolute top-0 right-0 w-80 lg:w-96 h-full bg-slate-800 border-l border-slate-700 shadow-2xl transition-transform duration-300 ease-in-out z-20 flex flex-col"
    :class="selectedData ? 'translate-x-0' : 'translate-x-full'"
  >
    <div v-if="selectedData" class="p-6 overflow-y-auto flex-1 text-slate-200">
      <button
        @click="$emit('close')"
        class="absolute top-4 right-4 text-slate-400 hover:text-white transition-colors"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-6 w-6"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M6 18L18 6M6 6l12 12"
          />
        </svg>
      </button>

      <div v-if="selectedData.type === 'course'">
        <div
          class="mb-2 text-xs font-bold text-blue-400 tracking-widest uppercase"
        >
          {{ selectedData.specialization }}
        </div>
        <h2 class="text-2xl font-bold text-white mb-1">
          {{ selectedData.title }}
        </h2>
        <p class="text-slate-400 text-sm mb-6">
          {{ selectedData.course_id }} • {{ selectedData.credits }} Units
        </p>

        <div
          class="mb-6 bg-slate-900/50 p-4 rounded-lg border border-slate-700"
        >
          <h3
            class="text-sm font-semibold text-slate-300 mb-2 uppercase tracking-wide"
          >
            Academic Synopsis
          </h3>
          <p class="text-sm text-slate-400 leading-relaxed">
            {{ selectedData.synopsis }}
          </p>
        </div>

        <div
          v-if="
            selectedData.technical_skills &&
            selectedData.technical_skills.length > 0
          "
          class="mb-6"
        >
          <h3
            class="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide"
          >
            Extracted Skills
          </h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="skill in selectedData.technical_skills"
              :key="skill"
              class="px-2.5 py-1 text-xs font-semibold bg-amber-500/10 text-amber-400 border border-amber-500/20 rounded-md"
            >
              {{ skill }}
            </span>
          </div>
        </div>

        <div
          v-if="
            selectedData.prerequisites && selectedData.prerequisites.length > 0
          "
        >
          <h3
            class="text-sm font-semibold text-slate-300 mb-3 uppercase tracking-wide"
          >
            Required Prerequisites
          </h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="pre in selectedData.prerequisites"
              :key="pre"
              class="px-2.5 py-1 text-xs font-semibold bg-blue-500/10 text-blue-400 border border-blue-500/20 rounded-md"
            >
              {{ pre }}
            </span>
          </div>
        </div>
      </div>

      <div
        v-else-if="selectedData.type === 'skill'"
        class="flex flex-col h-full justify-center items-center text-center mt-20"
      >
        <div
          class="w-20 h-20 bg-amber-500/10 rounded-full flex items-center justify-center mb-6 border border-amber-500/30"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-10 w-10 text-amber-400"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M13 10V3L4 14h7v7l9-11h-7z"
            />
          </svg>
        </div>
        <h2 class="text-2xl font-bold text-white mb-2">
          {{ selectedData.id }}
        </h2>
        <p class="text-slate-400 text-sm">Verified Technical Competency</p>
      </div>
    </div>
  </div>
</template>

<script setup>
defineProps({
  selectedData: Object,
});
defineEmits(["close"]);
</script>

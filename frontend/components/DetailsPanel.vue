<template>
  <div
    class="absolute top-0 right-0 w-80 lg:w-96 h-full bg-white border-l border-white text-black shadow-2xl transition-transform duration-300 ease-in-out z-20 flex flex-col pt-5"
    :class="selectedData ? 'translate-x-0' : 'translate-x-full'"
  >
    <div v-if="selectedData" class="p-6 overflow-y-auto flex-1 text-black">
      <button
        @click="$emit('close')"
        class="absolute top-9 right-5 text-black hover:text-purple-900 transition-colors"
      >
        <IconsX />
      </button>

      <div v-if="selectedData.type === 'course'">
        <div
          class="mb-5 text-xs font-bold text-blue-700 tracking-widest uppercase"
        >
          {{ selectedData.specialization }}
        </div>
        <h2 class="text-2xl font-bold text-black mb-5">
          {{ selectedData.title }}
        </h2>
        <p class="text-black text-sm mb-6">
          {{ selectedData.course_id }} • {{ selectedData.credits }} Units
        </p>

        <div class="mb-6 bg-gray-100 p-4 rounded-lg border border-slate-700">
          <h3
            class="text-sm font-semibold text-black mb-2 uppercase tracking-wider"
          >
            Academic Synopsis
          </h3>
          <p class="text-sm text-black leading-relaxed">
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
            class="text-sm font-semibold text-black mb-3 uppercase tracking-wide"
          >
            Extracted Skills
          </h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="skill in selectedData.technical_skills"
              :key="skill"
              class="px-2.5 py-1 text-xs font-semibold bg-amber-500/10 text-amber-600 border border-amber-500/20 rounded-md tracking-wide"
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
            class="text-sm font-semibold text-black mb-3 uppercase tracking-wide"
          >
            Required Prerequisites
          </h3>
          <div class="flex flex-wrap gap-2">
            <span
              v-for="pre in selectedData.prerequisites"
              :key="pre"
              class="px-2.5 py-1 text-xs font-semibold bg-blue-500/10 text-blue-700 border border-blue-500/20 rounded-md"
            >
              {{ pre }}
            </span>
          </div>
        </div>
      </div>

      <div
        v-else-if="selectedData.type === 'skill'"
        class="flex flex-col h-[80%] justify-center items-center text-center mt-20"
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
        <h2 class="text-2xl font-bold text-black mb-2">
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

<template>
  <div
    class="w-full h-full relative overflow-hidden flex flex-col bg-[#160d27]"
  >
    <div
      class="absolute top-4 md:top-6 left-1/2 -translate-x-1/2 z-30 w-[90%] md:w-[450px] flex gap-3"
    >
      <div class="relative flex-1">
        <button
          @click="isDropdownOpen = !isDropdownOpen"
          class="w-full flex justify-between items-center bg-slate-800/90 border border-slate-600 px-5 py-2.5 rounded-xl text-sm font-semibold text-slate-200 shadow-xl backdrop-blur-md hover:bg-slate-700 transition-all"
        >
          <span class="truncate">{{
            selectedTrack || "All Specializations"
          }}</span>
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-4 w-4 transition-transform duration-200 shrink-0 ml-2"
            :class="isDropdownOpen ? 'rotate-180' : ''"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        <transition
          enter-active-class="transition duration-100 ease-out"
          enter-from-class="transform scale-95 opacity-0"
          enter-to-class="transform scale-100 opacity-100"
          leave-active-class="transition duration-75 ease-in"
          leave-from-class="transform scale-100 opacity-100"
          leave-to-class="transform scale-95 opacity-0"
        >
          <div
            v-show="isDropdownOpen"
            class="absolute top-full left-0 mt-2 w-full bg-slate-800 border border-slate-600 rounded-xl shadow-2xl overflow-hidden py-1 z-40 max-h-96 overflow-y-auto"
          >
            <button
              @click="handleTrackSelect(null)"
              class="w-full text-left px-5 py-2.5 text-sm transition-colors"
              :class="
                !selectedTrack
                  ? 'bg-blue-500/20 text-blue-400 font-bold'
                  : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
              "
            >
              All Specializations
            </button>
            <div class="h-px w-full bg-slate-700 my-1"></div>
            <button
              v-for="track in availableTracks"
              :key="track"
              @click="handleTrackSelect(track)"
              class="w-full text-left px-5 py-2.5 text-sm transition-colors"
              :class="
                selectedTrack === track
                  ? 'bg-blue-500/20 text-blue-400 font-bold'
                  : 'text-slate-300 hover:bg-slate-700/50 hover:text-white'
              "
            >
              {{ track }}
            </button>
          </div>
        </transition>
      </div>

      <button
        @click="showSkills = !showSkills"
        class="flex items-center gap-2 bg-slate-800/90 border px-4 py-2.5 rounded-xl text-sm font-semibold shadow-xl backdrop-blur-md transition-all shrink-0"
        :class="
          showSkills
            ? 'border-amber-500/50 text-amber-400'
            : 'border-slate-600 text-slate-400 hover:text-slate-200 hover:bg-slate-700'
        "
      >
        <svg
          v-if="showSkills"
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          viewBox="0 0 20 20"
          fill="currentColor"
        >
          <path
            fill-rule="evenodd"
            d="M10 2a1 1 0 011 1v1a1 1 0 11-2 0V3a1 1 0 011-1zm4 8a4 4 0 11-8 0 4 4 0 018 0zm-.464 4.95l.707.707a1 1 0 001.414-1.414l-.707-.707a1 1 0 00-1.414 1.414zm2.12-10.607a1 1 0 010 1.414l-.706.707a1 1 0 11-1.414-1.414l.707-.707a1 1 0 011.414 0zM17 11a1 1 0 100-2h-1a1 1 0 100 2h1zm-7 4a1 1 0 011 1v1a1 1 0 11-2 0v-1a1 1 0 011-1zM5.05 6.464A1 1 0 106.465 5.05l-.708-.707a1 1 0 00-1.414 1.414l.707.707zm1.414 8.486l-.707.707a1 1 0 01-1.414-1.414l.707-.707a1 1 0 011.414 1.414zM4 11a1 1 0 100-2H3a1 1 0 000 2h1z"
            clip-rule="evenodd"
          />
        </svg>
        <svg
          v-else
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13.875 18.825A10.05 10.05 0 0112 19c-4.478 0-8.268-2.943-9.543-7a9.97 9.97 0 011.563-3.029m5.858.908a3 3 0 114.243 4.243M9.878 9.878l4.242 4.242M9.88 9.88l-3.29-3.29m7.532 7.532l3.29 3.29M3 3l3.59 3.59m0 0A9.953 9.953 0 0112 5c4.478 0 8.268 2.943 9.543 7a10.025 10.025 0 01-4.132 5.411m0 0L21 21"
          />
        </svg>
        <span class="hidden sm:inline">{{
          showSkills ? "Hide Skills" : "Show Skills"
        }}</span>
      </button>
    </div>

    <GraphCanvas
      v-if="courses"
      :courses="courses"
      :selectedTrack="selectedTrack"
      :showSkills="showSkills"
      @nodeClicked="handleNodeClick"
      class="flex-1"
    />

    <div
      class="absolute top-0 right-0 w-full md:w-96 h-full bg-slate-800 border-l border-slate-700 shadow-2xl transition-transform duration-300 ease-in-out z-30"
      :class="selectedData ? 'translate-x-0' : 'translate-x-full'"
    >
      <DetailsPanel :selectedData="selectedData" @close="selectedData = null" />
    </div>

    <div
      class="absolute bottom-6 left-10 z-20 flex flex-col items-start gap-3 pointer-events-auto"
    >
      <transition
        enter-active-class="transition duration-200 ease-out"
        enter-from-class="transform scale-95 opacity-0 translate-y-4"
        enter-to-class="transform scale-100 opacity-100 translate-y-0"
        leave-active-class="transition duration-150 ease-in"
        leave-from-class="transform scale-100 opacity-100 translate-y-0"
        leave-to-class="transform scale-95 opacity-0 translate-y-4"
      >
        <div
          v-show="showLegend"
          class="bg-slate-800/95 border border-slate-700 p-5 rounded-xl shadow-2xl backdrop-blur-md w-64"
        >
          <h3
            class="text-xs font-bold text-slate-400 mb-4 uppercase tracking-widest border-b border-slate-700 pb-2 flex justify-between items-center"
          >
            Track Legend
            <button
              @click="showLegend = false"
              class="text-slate-500 hover:text-slate-300"
            >
              ✕
            </button>
          </h3>
          <div class="flex flex-col gap-3">
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-blue-500 shadow-[0_0_8px_theme(colors.blue.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium">Core CS</span>
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-emerald-500 shadow-[0_0_8px_theme(colors.emerald.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium"
                >Software Engineering</span
              >
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-red-500 shadow-[0_0_8px_theme(colors.red.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium"
                >Cybersecurity</span
              >
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-purple-500 shadow-[0_0_8px_theme(colors.purple.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium"
                >Data & Algorithms</span
              >
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-cyan-500 shadow-[0_0_8px_theme(colors.cyan.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium"
                >Systems Architecture</span
              >
            </div>
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-fuchsia-500 shadow-[0_0_8px_theme(colors.fuchsia.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium"
                >Artificial Intelligence</span
              >
            </div>
            <div class="h-px w-full bg-slate-700 my-1"></div>
            <div class="flex items-center gap-3">
              <div
                class="w-3.5 h-3.5 rounded-full bg-amber-500 shadow-[0_0_8px_theme(colors.amber.500)]"
              ></div>
              <span class="text-sm text-slate-200 font-medium"
                >Technical Skill</span
              >
            </div>
          </div>
        </div>
      </transition>

      <button
        @click="showLegend = !showLegend"
        class="flex items-center gap-2 bg-slate-800 border border-slate-600 px-4 py-2 rounded-full shadow-lg text-slate-300 hover:text-white hover:bg-slate-700 transition-all"
      >
        <IconsMap />
        <span class="text-sm font-semibold">Map Legend</span>
      </button>
    </div>

    <div
      v-if="pending"
      class="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-40"
    >
      <span class="text-blue-400 animate-pulse font-semibold text-lg"
        >Fetching Curriculum Intelligence...</span
      >
    </div>
    <div
      v-else-if="error"
      class="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-40"
    >
      <span class="text-red-400 font-semibold text-lg"
        >Connection Error. Is FastAPI running?</span
      >
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const selectedData = ref(null);
const selectedTrack = ref(null);
const isDropdownOpen = ref(false);
const showLegend = ref(false);
const showSkills = ref(false); // NEW: Default to a clean view!

const availableTracks = [
  "Core Computer Science",
  "Software Engineering",
  "Cybersecurity",
  "Data & Algorithms",
  "Systems & Architecture",
  "Artificial Intelligence",
];

const {
  data: courses,
  pending,
  error,
} = await useFetch("http://127.0.0.1:8000/api/graph");

// Function to handle selection and close the menu
const handleTrackSelect = (track) => {
  selectedTrack.value = track;
  isDropdownOpen.value = false;
};

const handleNodeClick = (nodeData) => {
  if (nodeData.group === "course") {
    const courseDetails = courses.value.find(
      (c) => c.course_id === nodeData.id,
    );
    selectedData.value = { type: "course", ...courseDetails };
  } else {
    selectedData.value = { type: "skill", id: nodeData.id };
  }
};
</script>

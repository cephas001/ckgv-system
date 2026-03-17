<template>
  <div
    class="fixed top-0 right-0 w-80 lg:w-96 h-screen bg-white border-l border-slate-100 text-black shadow-2xl transition-transform duration-300 ease-in-out z-[100] flex flex-col"
    :class="currentViewData ? 'translate-x-0' : 'translate-x-full'"
  >
    <div v-if="currentViewData" class="p-6 overflow-y-auto flex-1 text-black">
      <div class="flex justify-between items-center mb-6 relative h-8">
        <button
          v-if="historyStack.length > 0"
          @click="goBack"
          class="flex items-center gap-1 text-sm font-semibold tracking-wider text-blue-600 hover:text-blue-800 transition-colors"
        >
          <svg
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
              d="M10 19l-7-7m0 0l7-7m-7 7h18"
            />
          </svg>
          Back
        </button>
        <div v-else></div>
        <button
          @click="closePanel"
          class="text-black hover:text-purple-900 transition-colors absolute right-0"
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
      </div>

      <div v-if="currentViewData.type === 'course'">
        <div
          class="mb-5 text-xs font-bold text-blue-700 tracking-widest uppercase"
        >
          {{ currentViewData.specialization }}
        </div>
        <h2 class="text-2xl font-bold text-black mb-5">
          {{ currentViewData.title }}
        </h2>
        <p class="text-black text-sm mb-6">
          {{ currentViewData.course_id }} • {{ currentViewData.credits }} Units
        </p>

        <div class="mb-6 bg-gray-100 p-4 rounded-lg border border-slate-200">
          <h3
            class="text-sm font-semibold text-black mb-2 uppercase tracking-wider"
          >
            Academic Synopsis
          </h3>
          <p class="text-sm text-black leading-relaxed">
            {{ currentViewData.synopsis }}
          </p>
        </div>

        <div
          v-if="
            currentViewData.technical_skills &&
            currentViewData.technical_skills.length > 0
          "
          class="mb-6"
        >
          <h3
            class="text-sm font-semibold text-black mb-3 uppercase tracking-wide"
          >
            Extracted Skills
          </h3>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="skill in currentViewData.technical_skills"
              :key="skill"
              @click="navigateToNode({ type: 'skill', id: skill })"
              class="px-2.5 py-1 text-xs font-semibold bg-amber-500/10 text-amber-700 border border-amber-500/30 rounded-md tracking-wide hover:bg-amber-500/20 hover:scale-105 transition-all cursor-pointer text-left"
              title="Click to view courses teaching this skill"
            >
              {{ skill }}
            </button>
          </div>
        </div>

        <div
          v-if="
            currentViewData.prerequisites &&
            currentViewData.prerequisites.length > 0
          "
        >
          <h3
            class="text-sm font-semibold text-black mb-3 uppercase tracking-wide"
          >
            Required Prerequisites
          </h3>
          <div class="flex flex-wrap gap-2">
            <button
              v-for="pre in currentViewData.prerequisites"
              :key="pre"
              @click="navigateToCourse(pre)"
              class="px-2.5 py-1 text-xs font-semibold bg-blue-500/10 text-blue-700 border border-blue-500/20 rounded-md hover:bg-blue-500/20 hover:scale-105 transition-all cursor-pointer"
              title="Click to view prerequisite details"
            >
              {{ pre }}
            </button>
          </div>
        </div>
      </div>

      <div
        v-else-if="currentViewData.type === 'skill'"
        class="flex flex-col mt-7"
      >
        <div class="flex items-center gap-4 mb-8">
          <div
            class="w-16 h-16 bg-amber-500/10 rounded-full flex items-center justify-center shrink-0 border border-amber-500/30"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-8 w-8 text-amber-500"
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
          <div>
            <h2 class="text-xl font-bold text-black leading-tight">
              {{ currentViewData.id }}
            </h2>
            <p
              class="text-slate-700 text-xs font-semibold uppercase tracking-wider mt-1"
            >
              Technical Skill
            </p>
          </div>
        </div>

        <div v-if="skillAnalytics" class="pl-2 pt-1">
          <div class="mb-8">
            <h3
              class="text-xs font-bold text-black mb-3 uppercase tracking-widest border-b border-slate-200 pb-2"
            >
              Foundational For Specializations
            </h3>
            <div class="flex flex-col gap-2">
              <span
                v-for="track in skillAnalytics.tracks"
                :key="track"
                class="text-sm font-medium text-black flex items-center gap-3"
              >
                <div class="w-1.5 h-1.5 rounded-full bg-black"></div>
                {{ track }}
              </span>
            </div>
          </div>

          <div>
            <h3
              class="text-xs font-bold text-black mb-3 uppercase tracking-widest border-b border-slate-200 pb-2"
            >
              Acquired In Courses ({{ skillAnalytics.courses.length }})
            </h3>
            <div class="flex flex-col gap-3">
              <div
                v-for="course in skillAnalytics.courses"
                :key="course.id"
                @click="navigateToCourse(course.id)"
                class="bg-slate-50 p-3 rounded-lg border border-slate-100 hover:border-blue-400 hover:shadow-md transition-all cursor-pointer"
              >
                <div
                  class="text-xs text-blue-600 mb-1 font-semibold tracking-wider"
                >
                  {{ course.id }}
                </div>
                <div class="text-sm text-slate-800 leading-snug">
                  {{ course.title }}
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch } from "vue";

const props = defineProps({
  selectedData: Object,
  courses: Array,
});

const emit = defineEmits(["close"]);

// --- NAVIGATION STATE MANAGEMENT ---
// Stack to keep track of navigation history
const historyStack = ref([]);
// The data currently being displayed in the panel
const currentViewData = ref(null);

// When the parent component passes new data (e.g., user clicks a node on the main graph)
// We reset the history stack and show the new data.
watch(
  () => props.selectedData,
  (newData) => {
    if (newData) {
      historyStack.value = []; // Reset history when a new node is clicked from the main graph
      currentViewData.value = newData;
    } else {
      currentViewData.value = null; // Handle close
    }
  },
  { immediate: true },
);

// Function to handle clicking a link INSIDE the panel
const navigateToNode = (targetData) => {
  if (currentViewData.value) {
    // Save current view to history before changing
    historyStack.value.push(currentViewData.value);
  }
  currentViewData.value = targetData;
};

// Helper function to find course details by ID and navigate to it
const navigateToCourse = (courseId) => {
  const courseDetails = props.courses.find((c) => c.course_id === courseId);
  if (courseDetails) {
    navigateToNode({ type: "course", ...courseDetails });
  }
};

// Function to go back one step in history
const goBack = () => {
  if (historyStack.value.length > 0) {
    currentViewData.value = historyStack.value.pop();
  }
};

// Completely close the panel and reset
const closePanel = () => {
  historyStack.value = [];
  emit("close");
};

// --- ANALYTICS ENGINE ---
const skillAnalytics = computed(() => {
  if (
    !currentViewData.value ||
    currentViewData.value.type !== "skill" ||
    !props.courses
  ) {
    return null;
  }

  const targetSkill = currentViewData.value.id;
  const relatedCourses = [];
  const relatedTracks = new Set();

  props.courses.forEach((course) => {
    if (
      course.technical_skills &&
      course.technical_skills.includes(targetSkill)
    ) {
      relatedCourses.push({
        id: course.course_id,
        title: course.title,
      });
      if (course.specialization) {
        relatedTracks.add(course.specialization);
      }
    }
  });

  return {
    courses: relatedCourses,
    tracks: Array.from(relatedTracks).sort(),
  };
});
</script>

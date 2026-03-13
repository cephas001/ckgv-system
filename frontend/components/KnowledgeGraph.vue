<template>
  <div class="w-full h-full relative overflow-hidden flex">
    <GraphCanvas
      v-if="courses"
      :courses="courses"
      @nodeClicked="handleNodeClick"
      class="flex-1"
    />

    <DetailsPanel :selectedData="selectedData" @close="selectedData = null" />

    <div
      v-if="pending"
      class="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-10"
    >
      <span class="text-blue-400 animate-pulse font-semibold text-lg"
        >Fetching Curriculum Intelligence...</span
      >
    </div>

    <div
      v-else-if="error"
      class="absolute inset-0 flex items-center justify-center bg-slate-900/90 z-10"
    >
      <span class="text-red-400 font-semibold text-lg"
        >Connection Error. Is FastAPI running?</span
      >
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
// Nuxt auto-imports GraphCanvas and DetailsPanel!

const selectedData = ref(null);

// 1. Fetch data from FastAPI
const {
  data: courses,
  pending,
  error,
} = await useFetch("http://127.0.0.1:8000/api/graph");

// 2. Handle the click event emitted from GraphCanvas
const handleNodeClick = (nodeData) => {
  if (nodeData.group === "course") {
    // Find the full course data and send it to the panel
    const courseDetails = courses.value.find(
      (c) => c.course_id === nodeData.id,
    );
    selectedData.value = { type: "course", ...courseDetails };
  } else {
    // Send generic skill data to the panel
    selectedData.value = { type: "skill", id: nodeData.id };
  }
};
</script>

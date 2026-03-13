<template>
  <div class="w-full h-full relative">
    <svg id="graph-canvas" class="w-full h-full"></svg>

    <div
      v-if="pending"
      class="absolute inset-0 flex items-center justify-center bg-slate-800/90 z-10"
    >
      <span class="text-blue-400 animate-pulse font-semibold text-lg">
        Fetching Curriculum Intelligence from FastAPI...
      </span>
    </div>

    <div
      v-else-if="error"
      class="absolute inset-0 flex items-center justify-center bg-slate-800/90 z-10"
    >
      <span class="text-red-400 font-semibold text-lg">
        Connection Error. Is the FastAPI server running?
      </span>
    </div>
  </div>
</template>

<script setup>
import * as d3 from "d3";

// Fetch data from your Python backend
const {
  data: courses,
  pending,
  error,
} = await useFetch("http://127.0.0.1:8000/api/graph");

onMounted(() => {
  if (courses.value) {
    console.log(
      "✅ SUCCESS: Curriculum data loaded from backend!",
      courses.value,
    );
  }
});
</script>

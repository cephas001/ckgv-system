<template>
  <div
    class="w-full h-full p-8 max-w-7xl mx-auto overflow-y-auto bg-slate-50 min-h-screen"
  >
    <div class="mb-10 flex items-center justify-between">
      <div>
        <h2 class="text-3xl font-bold text-black tracking-tight">
          Graph Analytics
        </h2>
        <p class="text-black/80 mt-2 text-sm font-medium">
          Curriculum insights and bottleneck detection.
        </p>
      </div>
      <button
        @click="printReport"
        class="bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 hover:text-indigo-600 px-4 py-2 rounded-xl text-sm font-bold shadow-sm transition-all flex items-center gap-2"
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
            d="M17 17h2a2 2 0 002-2v-4a2 2 0 00-2-2H5a2 2 0 00-2 2v4a2 2 0 002 2h2m2 4h6a2 2 0 002-2v-4a2 2 0 00-2-2H9a2 2 0 00-2 2v4a2 2 0 002 2zm8-12V5a2 2 0 00-2-2H9a2 2 0 00-2 2v4h10z"
          />
        </svg>
        Export PDF Report
      </button>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
      <div
        class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex items-center gap-5"
      >
        <div
          class="w-14 h-14 bg-blue-50 text-blue-600 rounded-2xl flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-7 w-7"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M12 6.253v13m0-13C10.832 5.477 9.246 5 7.5 5S4.168 5.477 3 6.253v13C4.168 18.477 5.754 18 7.5 18s3.332.477 4.5 1.253m0-13C13.168 5.477 14.754 5 16.5 5c1.747 0 3.332.477 4.5 1.253v13C19.832 18.477 18.247 18 16.5 18c-1.746 0-3.332.477-4.5 1.253"
            />
          </svg>
        </div>
        <div>
          <p class="text-sm font-bold text-slate-400 uppercase tracking-widest">
            Total Courses
          </p>
          <p class="text-3xl font-extrabold text-slate-900">
            {{ courses?.length || 0 }}
          </p>
        </div>
      </div>

      <div
        class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex items-center gap-5"
      >
        <div
          class="w-14 h-14 bg-amber-50 text-amber-600 rounded-2xl flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-7 w-7"
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
          <p class="text-sm font-bold text-slate-400 uppercase tracking-widest">
            Extracted Skills
          </p>
          <p class="text-3xl font-extrabold text-slate-900">
            {{ totalSkills }}
          </p>
        </div>
      </div>

      <div
        class="bg-white p-6 rounded-3xl border border-slate-100 shadow-sm flex items-center gap-5"
      >
        <div
          class="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-7 w-7"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M21 13.255A23.931 23.931 0 0112 15c-3.183 0-6.22-.62-9-1.745M16 6V4a2 2 0 00-2-2h-4a2 2 0 00-2 2v2m4 6h.01M5 20h14a2 2 0 002-2V8a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
            />
          </svg>
        </div>
        <div>
          <p class="text-sm font-bold text-slate-400 uppercase tracking-widest">
            Active Tracks
          </p>
          <p class="text-3xl font-extrabold text-slate-900">
            {{ specializationDistribution.length }}
          </p>
        </div>
      </div>
    </div>

    <div class="grid grid-cols-1 lg:grid-cols-2 gap-8">
      <div class="bg-white rounded-3xl border border-slate-100 shadow-sm p-8">
        <h3
          class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2"
        >
          Specialization Balance
          <span
            class="text-xs font-medium bg-slate-100 text-slate-500 px-2 py-1 rounded-md"
            >Distribution</span
          >
        </h3>

        <div class="space-y-6">
          <div
            v-for="spec in specializationDistribution"
            :key="spec.name"
            class="relative"
          >
            <div class="flex justify-between text-sm mb-2">
              <span class="font-bold text-slate-700">{{ spec.name }}</span>
              <span class="text-slate-500 font-medium"
                >{{ spec.count }}
                {{ spec.count == 1 ? "Course" : "Courses" }} ({{
                  spec.percentage
                }}%)</span
              >
            </div>
            <div class="w-full bg-slate-100 rounded-full h-2.5 overflow-hidden">
              <div
                class="bg-indigo-500 h-2.5 rounded-full transition-all duration-1000 ease-out"
                :style="{ width: `${spec.percentage}%` }"
              ></div>
            </div>
          </div>
        </div>
      </div>

      <div class="bg-white rounded-3xl border border-slate-100 shadow-sm p-8">
        <h3
          class="text-lg font-bold text-slate-900 mb-6 flex items-center gap-2"
        >
          Curriculum Bottlenecks
          <span
            class="text-xs font-medium bg-red-100 text-red-600 px-2 py-1 rounded-md"
            >High Priority</span
          >
        </h3>
        <p class="text-sm text-slate-500 mb-6 font-medium">
          These courses are the most frequently required prerequisites. Failing
          these blocks the highest number of future classes.
        </p>

        <div class="space-y-3">
          <div
            v-for="(course, index) in bottleneckCourses"
            :key="course.id"
            class="flex items-center justify-between p-4 rounded-2xl border transition-colors hover:bg-slate-50"
            :class="
              index === 0 ? 'border-red-200 bg-red-50/50' : 'border-slate-100'
            "
          >
            <div class="flex items-center gap-4">
              <div
                class="w-8 h-8 rounded-full flex items-center justify-center font-bold text-sm"
                :class="
                  index === 0
                    ? 'bg-red-500 text-white shadow-md shadow-red-200'
                    : 'bg-slate-200 text-slate-600'
                "
              >
                {{ index + 1 }}
              </div>
              <div>
                <p class="font-bold text-slate-900">{{ course.id }}</p>
              </div>
            </div>
            <div class="flex flex-col items-end">
              <span class="text-xl font-black text-slate-800">{{
                course.count
              }}</span>
              <span
                class="text-[10px] font-bold text-slate-400 uppercase tracking-widest"
                >Dependent Courses</span
              >
            </div>
          </div>

          <div
            v-if="bottleneckCourses.length === 0"
            class="text-center py-8 text-sm text-slate-400 font-medium border-2 border-dashed border-slate-100 rounded-2xl"
          >
            No prerequisite dependencies detected yet.
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from "vue";

// Protect the route!
definePageMeta({
  middleware: "auth",
});

// Fetch all graph data
const { data: courses } = await useFetch("http://127.0.0.1:8000/api/graph");

// 1. Calculate Total Unique Skills
const totalSkills = computed(() => {
  if (!courses.value) return 0;
  const uniqueSkills = new Set();

  courses.value.forEach((course) => {
    if (course.technical_skills && Array.isArray(course.technical_skills)) {
      course.technical_skills.forEach((skill) => uniqueSkills.add(skill));
    }
  });

  return uniqueSkills.size;
});

// 2. Calculate Specialization Distribution
const specializationDistribution = computed(() => {
  if (!courses.value || courses.value.length === 0) return [];

  const counts = {};
  const total = courses.value.length;

  courses.value.forEach((course) => {
    const spec = course.specialization || "Uncategorized";
    counts[spec] = (counts[spec] || 0) + 1;
  });

  return Object.entries(counts)
    .map(([name, count]) => ({
      name,
      count,
      percentage: Math.round((count / total) * 100),
    }))
    .sort((a, b) => b.count - a.count); // Highest percentage first
});

// 3. Calculate Curriculum Bottlenecks (Most required prerequisites)
const bottleneckCourses = computed(() => {
  if (!courses.value) return [];

  const preReqCounts = {};

  courses.value.forEach((course) => {
    if (course.prerequisites && Array.isArray(course.prerequisites)) {
      course.prerequisites.forEach((preReq) => {
        preReqCounts[preReq] = (preReqCounts[preReq] || 0) + 1;
      });
    }
  });

  // Convert object to array, sort by count descending, and grab top 5
  return Object.entries(preReqCounts)
    .map(([id, count]) => ({ id, count }))
    .sort((a, b) => b.count - a.count)
    .slice(0, 5);
});

// Simple print function for the export button
const printReport = () => {
  window.print();
};
</script>

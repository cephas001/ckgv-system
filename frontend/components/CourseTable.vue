<template>
  <div class="w-full h-full flex flex-col bg-white relative overflow-hidden">
    <div class="px-8 pt-7 pb-5 border-b border-slate-100">
      <div class="flex items-center justify-between gap-4">
        <div class="w-full max-w-md">
          <label class="sr-only" for="course-search">Search</label>
          <div class="relative">
            <div
              class="pointer-events-none absolute inset-y-0 left-0 pl-4 flex items-center text-black"
            >
              <svg
                xmlns="http://www.w3.org/2000/svg"
                class="h-5 w-5"
                fill="none"
                viewBox="0 0 24 24"
                stroke="currentColor"
              >
                <path
                  stroke-linecap="round"
                  stroke-linejoin="round"
                  stroke-width="2"
                  d="M21 21l-4.35-4.35m0 0A7.5 7.5 0 103.5 10.5a7.5 7.5 0 0013.15 6.15z"
                />
              </svg>
            </div>
            <input
              id="course-search"
              v-model.trim="query"
              type="text"
              placeholder="e.g. CSC 201, Data Structures..."
              class="w-full pl-12 pr-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm text-black/90 placeholder:text-black/90 focus:outline-none focus:ring-1 focus:ring-black"
            />
          </div>
        </div>
      </div>
    </div>

    <div class="flex-1 min-h-0 overflow-auto">
      <div v-if="pending" class="p-8">
        <div
          class="w-full rounded-2xl border border-slate-100 bg-slate-50 p-6 text-sm font-semibold text-slate-500"
        >
          Loading courses…
        </div>
      </div>

      <div v-else-if="error" class="p-8">
        <div
          class="w-full rounded-2xl border border-red-100 bg-red-50 p-6 text-sm font-semibold text-red-700"
        >
          Couldn’t load courses. Is FastAPI running on `http://127.0.0.1:8000`?
        </div>
      </div>

      <div v-else class="px-8 py-6">
        <div
          class="rounded-3xl border border-slate-100 shadow-[0_10px_30px_rgba(2,6,23,0.06)] overflow-y-auto"
        >
          <table class="min-w-full divide-y divide-slate-100">
            <thead class="bg-slate-50">
              <tr>
                <th
                  scope="col"
                  class="px-6 py-4 text-left text-xs font-bold tracking-widest uppercase text-black"
                >
                  Code
                </th>
                <th
                  scope="col"
                  class="px-6 py-4 text-left text-xs font-bold tracking-widest uppercase text-black"
                >
                  Title
                </th>
                <th
                  scope="col"
                  class="px-6 py-4 text-left text-xs font-bold tracking-widest uppercase text-black"
                >
                  Specialization
                </th>
                <th scope="col" class="px-6 py-4 text-right">
                  <span
                    class="text-xs font-bold tracking-widest uppercase text-black"
                    >Actions</span
                  >
                </th>
              </tr>
            </thead>

            <tbody class="divide-y divide-slate-100 bg-white">
              <tr
                v-for="course in filteredCourses"
                :key="course.course_id"
                class="hover:bg-slate-50/70 transition-colors"
              >
                <td class="px-6 py-4 whitespace-nowrap">
                  <div class="text-sm text-black">{{ course.course_id }}</div>
                </td>
                <td class="px-6 py-4 min-w-[320px]">
                  <div class="text-sm text-black">
                    {{ course.title || "Untitled Course" }}
                  </div>
                </td>
                <td class="px-6 py-4 whitespace-nowrap">
                  <span
                    class="inline-flex items-center rounded-full px-3 py-1 text-xs font-extrabold ring-1 ring-inset"
                    :style="tagStyle(course.specialization)"
                  >
                    {{ course.specialization || "Unknown" }}
                  </span>
                </td>
                <td class="px-6 py-4 whitespace-nowrap text-right">
                  <button
                    type="button"
                    class="inline-flex items-center justify-center rounded-xl bg-purple-700 hover:bg-purple-900 text-white px-4 py-2 text-sm shadow-[0_4px_14px_0_rgba(227,62,56,0.25)] transition-all transform hover:-translate-y-0.5"
                    @click="openDetails(course)"
                  >
                    View Details
                  </button>
                </td>
              </tr>
              <tr v-if="filteredCourses.length === 0">
                <td colspan="4" class="px-6 py-10 text-center">
                  <div class="text-sm font-semibold text-slate-500">
                    No courses match your search.
                  </div>
                </td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>

    <DetailsPanel
      :selectedData="selectedCourse"
      @close="selectedCourse = null"
    />
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const query = ref("");
const selectedCourse = ref(null);

const {
  data: courses,
  pending,
  error,
} = await useFetch("http://127.0.0.1:8000/api/graph");

const normalizedCourses = computed(() => {
  return Array.isArray(courses.value) ? courses.value : [];
});

const filteredCourses = computed(() => {
  const q = query.value.toLowerCase();
  if (!q) return normalizedCourses.value;

  return normalizedCourses.value.filter((c) => {
    const id = String(c?.course_id ?? "").toLowerCase();
    const title = String(c?.title ?? "").toLowerCase();
    return id.includes(q) || title.includes(q);
  });
});

const openDetails = (course) => {
  selectedCourse.value = { ...course, type: "course" };
};

const tagStyle = (specialization) => {
  const colorMap = {
    "Core Computer Science": "#3b82f6",
    "Software Engineering": "#10b981",
    Cybersecurity: "#ef4444",
    "Data & Algorithms": "#8b5cf6",
    "Systems & Architecture": "#06b6d4",
    "Artificial Intelligence": "#d946ef",
    default: "#64748b",
  };

  const bg = colorMap[specialization] || colorMap.default;
  return {
    backgroundColor: `${bg}1a`,
    color: bg,
    borderColor: `${bg}33`,
  };
};
</script>

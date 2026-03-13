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
                    class="inline-flex items-center justify-center rounded-xl bg-purple-700 hover:bg-purple-900 text-white px-4 py-2 text-sm shadow-[0_4px_14px_0_rgba(227,62,56,0.25)] transition-all"
                    @click="openDetails(course)"
                  >
                    View Details
                  </button>
                  <button
                    v-if="isAdmin"
                    type="button"
                    class="inline-flex items-center justify-center rounded-xl bg-white border border-slate-200 text-slate-700 hover:bg-slate-50 px-4 py-2 text-sm shadow-sm transition-all ml-2"
                    @click="openEdit(course)"
                  >
                    Edit
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

    <div
      v-if="isEditing"
      class="fixed inset-0 z-[150] flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm"
    >
      <div
        class="bg-white rounded-3xl w-full max-w-lg shadow-2xl overflow-hidden"
      >
        <div
          class="px-6 py-4 border-b border-slate-100 flex justify-between items-center bg-slate-50"
        >
          <h3 class="font-bold text-lg text-black">Edit Node Data</h3>
          <button
            @click="isEditing = false"
            class="text-slate-400 hover:text-slate-700"
          >
            ✕
          </button>
        </div>
        <div class="p-6 space-y-4">
          <div>
            <label
              class="block text-xs font-bold text-black uppercase tracking-wide mb-2"
              >Course Title</label
            >
            <input
              v-model="editForm.title"
              type="text"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 text-sm focus:ring-1 focus:ring-indigo-500"
            />
          </div>
          <div>
            <label
              class="block text-xs font-bold text-black uppercase tracking-wide mb-2"
              >Specialization</label
            >
            <select
              v-model="editForm.specialization"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 text-sm focus:ring-1 focus:ring-indigo-500"
            >
              <option>Core Computer Science</option>
              <option>Software Engineering</option>
              <option>Cybersecurity</option>
              <option>Data & Algorithms</option>
              <option>Systems & Architecture</option>
              <option>Artificial Intelligence</option>
            </select>
          </div>
          <div>
            <label
              class="block text-xs font-bold text-black uppercase tracking-wide mb-2"
              >Extracted Skills (Comma Separated)</label
            >
            <textarea
              :value="editForm.technical_skills?.join(', ')"
              class="w-full px-4 py-2 rounded-xl border border-slate-200 text-sm h-20 focus:ring-1 focus:ring-indigo-500 resize-none"
            ></textarea>
            <p class="text-[10px] text-slate-400 mt-1">
              Manual override for spaCy NLP extraction.
            </p>
          </div>
        </div>
        <div
          class="px-6 py-4 border-t border-slate-100 flex justify-end gap-3 bg-slate-50"
        >
          <button
            @click="isEditing = false"
            class="px-5 py-2 text-sm font-bold text-black hover:text-slate-700"
          >
            Cancel
          </button>
          <button
            @click="saveEdit"
            :disabled="isSaving"
            class="bg-indigo-600 hover:bg-indigo-700 disabled:opacity-70 text-white px-5 py-2 rounded-xl text-sm shadow-md transition-all flex items-center gap-2"
          >
            <svg
              v-if="isSaving"
              class="animate-spin h-4 w-4 text-white"
              xmlns="http://www.w3.org/2000/svg"
              fill="none"
              viewBox="0 0 24 24"
            >
              <circle
                class="opacity-25"
                cx="12"
                cy="12"
                r="10"
                stroke="currentColor"
                stroke-width="4"
              ></circle>
              <path
                class="opacity-75"
                fill="currentColor"
                d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
              ></path>
            </svg>
            {{ isSaving ? "Saving..." : "Save Changes" }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref } from "vue";

const query = ref("");
const selectedCourse = ref(null);
const isSaving = ref(false);

const { triggerNotification } = useNotification();

// --- ADD THIS TO CHECK IF ADMIN IS LOGGED IN ---
const isAdmin = computed(() => {
  return !!useCookie("auth_token").value;
});

const isEditing = ref(false);
const editForm = ref(null);

// --- ADD THIS TO HANDLE EDIT CLICK ---
const openEdit = (course) => {
  // Create a deep copy of the course so we don't accidentally mutate the table before saving
  editForm.value = JSON.parse(JSON.stringify(course));
  isEditing.value = true;
};

const saveEdit = async () => {
  isSaving.value = true;

  try {
    // 1. Format the technical skills back into an array
    let updatedSkills = [];
    if (typeof editForm.value.technical_skills === "string") {
      // Splits by comma, removes extra spaces, and filters out empty strings
      updatedSkills = editForm.value.technical_skills
        .split(",")
        .map((skill) => skill.trim())
        .filter((skill) => skill.length > 0);
    } else if (Array.isArray(editForm.value.technical_skills)) {
      updatedSkills = editForm.value.technical_skills;
    }

    // 2. Send the real update request to FastAPI
    await $fetch(
      `http://127.0.0.1:8000/api/courses/${editForm.value.course_id}`,
      {
        method: "PUT",
        body: {
          title: editForm.value.title,
          specialization: editForm.value.specialization,
          technical_skills: updatedSkills,
        },
      },
    );

    // 3. Update the local UI state so the table and graph reflect the change instantly
    const index = courses.value.findIndex(
      (c) => c.course_id === editForm.value.course_id,
    );
    if (index !== -1) {
      courses.value[index].title = editForm.value.title;
      courses.value[index].specialization = editForm.value.specialization;
      courses.value[index].technical_skills = updatedSkills;
    }

    // Close modal and clean up
    isEditing.value = false;
    editForm.value = null;

    // Optional: You can replace this alert with your beautiful Toast Notification!
    triggerNotification(
      `Successfully updated: ${courses.value[index].course_id}`,
      "success",
    );
  } catch (error) {
    console.error("Update failed:", error);
    triggerNotification(
      "Failed to update course. Ensure the backend is running.",
      "error",
    );
  } finally {
    isSaving.value = false;
  }
};

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

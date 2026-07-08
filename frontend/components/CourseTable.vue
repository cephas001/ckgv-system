<template>
  <div class="w-full h-full flex flex-col bg-white relative overflow-hidden">
    <div class="px-8 pt-7 pb-5 border-b border-slate-100">
      <div
        class="flex flex-col sm:flex-row items-start sm:items-center justify-between gap-4"
      >
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

        <div class="flex items-center gap-3 w-full sm:w-auto">
          <label for="sort-select" class="text-sm text-black whitespace-nowrap">
            Sort by:
          </label>
          <div class="relative w-full sm:w-48">
            <select
              id="sort-select"
              v-model="sortBy"
              class="w-full appearance-none pl-2 py-1 border border-slate-200 bg-white text-sm text-black outline-none cursor-pointer"
            >
              <option value="code_asc">Code (A-Z)</option>
              <option value="code_desc">Code (Z-A)</option>
              <option value="title_asc">Title (A-Z)</option>
              <option value="title_desc">Title (Z-A)</option>
              <option value="spec_asc">Specialization (A-Z)</option>
            </select>
            <div
              class="pointer-events-none absolute inset-y-0 right-0 flex items-center px-4 text-slate-500"
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
                  d="M19 9l-7 7-7-7"
                />
              </svg>
            </div>
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
                  <div class="flex items-center justify-end gap-2">
                    <button
                      type="button"
                      class="p-2 rounded-lg text-slate-700 hover:text-blue-600 hover:bg-blue-50 transition-all"
                      title="View Course Analytics"
                      @click="openDetails(course)"
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
                          d="M15 12a3 3 0 11-6 0 3 3 0 016 0z"
                        />
                        <path
                          stroke-linecap="round"
                          stroke-linejoin="round"
                          stroke-width="2"
                          d="M2.458 12C3.732 7.943 7.523 5 12 5c4.478 0 8.268 2.943 9.542 7-1.274 4.057-5.064 7-9.542 7-4.477 0-8.268-2.943-9.542-7z"
                        />
                      </svg>
                    </button>

                    <button
                      v-if="isAdmin"
                      type="button"
                      class="p-2 rounded-lg text-slate-700 hover:text-emerald-600 hover:bg-emerald-50 transition-all"
                      title="Edit Course Data"
                      @click="openEdit(course)"
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
                          d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"
                        />
                      </svg>
                    </button>

                    <button
                      v-if="isAdmin"
                      type="button"
                      class="p-2 rounded-lg text-slate-700 hover:text-red-600 hover:bg-red-50 transition-all"
                      title="Delete Course"
                      @click="deleteCourse(course.course_id)"
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
                          d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"
                        />
                      </svg>
                    </button>
                  </div>
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
      :courses="courses"
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
          <h3 class="font-bold text-lg text-black">Edit Course Data</h3>
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
            >
              Course Title
            </label>
            <input
              v-model="editForm.title"
              type="text"
              class="w-full px-4 py-2 rounded-xl border border-slate-300 focus:border-black outline-none text-sm text-black"
            />
          </div>
          <div>
            <label
              class="block text-xs font-bold text-black uppercase tracking-wide mb-2"
            >
              Specialization
            </label>
            <select
              v-model="editForm.specialization"
              class="w-full px-4 py-2 rounded-xl border border-slate-300 focus:border-black outline-none text-sm text-black"
            >
              <option
                v-for="track in availableSpecializations"
                :key="track"
                :value="track"
              >
                {{ track }}
              </option>
            </select>
          </div>

          <div>
            <label
              class="block text-xs font-bold text-black uppercase tracking-wide mb-2"
            >
              Prerequisites (Comma Separated)
            </label>
            <input
              v-model="editForm.prerequisites_str"
              type="text"
              placeholder="e.g. CMP 101, MTH 101"
              class="w-full px-4 py-2 rounded-xl border border-slate-300 focus:border-black outline-none text-sm text-black"
            />
          </div>

          <div>
            <label
              class="block text-xs font-bold text-black uppercase tracking-wide mb-2"
            >
              Extracted Skills (Comma Separated)
            </label>
            <textarea
              v-model="editForm.technical_skills_str"
              class="w-full px-4 py-2 rounded-xl border border-slate-300 focus:border-black outline-none text-sm h-20 resize-none text-black"
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
            class="px-5 py-2 text-sm text-black hover:text-slate-700"
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
const sortBy = ref("code_asc");

const { triggerNotification } = useNotification();

const config = useRuntimeConfig();

// --- ADD THIS TO CHECK IF ADMIN IS LOGGED IN ---
const isAdmin = computed(() => {
  return !!useCookie("auth_token").value;
});

const isEditing = ref(false);
const editForm = ref(null);

// --- ADD THIS TO HANDLE EDIT CLICK ---
const openEdit = (course) => {
  // Create a deep copy of the course
  editForm.value = JSON.parse(JSON.stringify(course));

  // Convert arrays to comma-separated strings for the input fields
  editForm.value.prerequisites_str = (course.prerequisites || []).join(", ");
  editForm.value.technical_skills_str = (course.technical_skills || []).join(
    ", ",
  );

  isEditing.value = true;
};

// --- UPDATED: SAVE EDITS ---
const saveEdit = async () => {
  isSaving.value = true;

  try {
    // 1. Format the strings back into clean arrays
    const updatedSkills = editForm.value.technical_skills_str
      .split(",")
      .map((skill) => skill.trim())
      .filter((skill) => skill.length > 0);

    const updatedPrereqs = editForm.value.prerequisites_str
      .split(",")
      .map((pre) => pre.trim().toUpperCase()) // Force course codes to be uppercase
      .filter((pre) => pre.length > 0);

    // 2. Send the real update request to FastAPI
    await $fetch(
      `${config.public.apiBase}/courses/${editForm.value.course_id}`,
      {
        method: "PUT",
        body: {
          title: editForm.value.title,
          specialization: editForm.value.specialization,
          technical_skills: updatedSkills,
          prerequisites: updatedPrereqs, // NEW: Sending prereqs to backend
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
      courses.value[index].prerequisites = updatedPrereqs; // NEW: Updating local state
    }

    // Close modal and clean up
    isEditing.value = false;
    editForm.value = null;

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
// --- ADD THIS TO HANDLE DELETE CLICK ---
const deleteCourse = async (courseId) => {
  // 1. Prevent accidental clicks
  if (
    !confirm(
      `Are you sure you want to permanently delete ${courseId}? This action cannot be undone.`,
    )
  ) {
    return;
  }

  try {
    // 2. Send the delete request to FastAPI
    await $fetch(`${config.public.apiBase}/courses/${courseId}`, {
      method: "DELETE",
    });

    // 3. Update the local UI state so it instantly disappears from the table
    courses.value = courses.value.filter((c) => c.course_id !== courseId);

    triggerNotification(`Successfully deleted ${courseId}`, "success");
  } catch (error) {
    console.error("Delete failed:", error);
    triggerNotification(
      "Failed to delete course. Ensure the backend is running.",
      "error",
    );
  }
};

const {
  data: courses,
  pending,
  error,
} = await useFetch(`${config.public.apiBase}/api/graph`);

const normalizedCourses = computed(() => {
  return Array.isArray(courses.value) ? courses.value : [];
});

const filteredCourses = computed(() => {
  let result = normalizedCourses.value;

  // 1. Filter by search query
  const q = query.value.toLowerCase();
  if (q) {
    result = result.filter((c) => {
      const id = String(c?.course_id ?? "").toLowerCase();
      const title = String(c?.title ?? "").toLowerCase();
      return id.includes(q) || title.includes(q);
    });
  }

  // 2. Sort the results
  // We spread into a new array [...result] to avoid mutating the original data
  return [...result].sort((a, b) => {
    const codeA = String(a.course_id || "").toLowerCase();
    const codeB = String(b.course_id || "").toLowerCase();
    const titleA = String(a.title || "").toLowerCase();
    const titleB = String(b.title || "").toLowerCase();
    const specA = String(a.specialization || "").toLowerCase();
    const specB = String(b.specialization || "").toLowerCase();

    switch (sortBy.value) {
      case "code_asc":
        return codeA.localeCompare(codeB);
      case "code_desc":
        return codeB.localeCompare(codeA);
      case "title_asc":
        return titleA.localeCompare(titleB);
      case "title_desc":
        return titleB.localeCompare(titleA);
      case "spec_asc":
        return specA.localeCompare(specB);
      default:
        return 0;
    }
  });
});

const openDetails = (course) => {
  selectedCourse.value = { ...course, type: "course" };
};

// --- NEW: DYNAMICALLY EXTRACT SPECIALIZATIONS ---
const availableSpecializations = computed(() => {
  if (!normalizedCourses.value) return [];
  const tracks = new Set(
    normalizedCourses.value
      .map((c) => c.specialization)
      .filter((s) => s && s.trim() !== ""),
  );
  return Array.from(tracks).sort();
});

// --- NEW: DYNAMIC BADGE COLORS ---
const colorPalette = [
  "#3b82f6", // blue
  "#10b981", // emerald
  "#a855f7", // purple
  "#06b6d4", // cyan
  "#f43f5e", // rose
  "#6366f1", // indigo
];

const tagStyle = (specialization) => {
  const specs = availableSpecializations.value;
  const index = specs.indexOf(specialization);

  // Assign a consistent color from the palette based on its alphabetical index
  const bg =
    index !== -1 ? colorPalette[index % colorPalette.length] : "#64748b";

  return {
    backgroundColor: `${bg}1a`,
    color: bg,
    borderColor: `${bg}33`,
  };
};
</script>

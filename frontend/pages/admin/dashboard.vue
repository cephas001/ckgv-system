<template>
  <div class="w-full h-full p-8 max-w-7xl mx-auto">
    <div class="mb-10">
      <h2 class="text-3xl font-bold text-black tracking-tight">
        Admin Control Center
      </h2>
      <p class="text-black/70 mt-2">
        Manage the McPherson University Curriculum Knowledge Graph.
      </p>
    </div>

    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
      <div
        @click="showAddModal = true"
        class="group bg-white border border-slate-100 rounded-3xl p-8 shadow-sm hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col items-start"
      >
        <div
          class="w-14 h-14 bg-red-50 text-[#e33e38] rounded-2xl flex items-center justify-center mb-6 group-hover:bg-[#e33e38] group-hover:text-white transition-colors duration-300"
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
              d="M12 4v16m8-8H4"
            />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-black mb-2">Add Single Course</h3>
        <p class="text-sm text-black/80 leading-relaxed">
          Manually add a new course to the graph using the AI-assisted NLP
          extraction tool.
        </p>
      </div>

      <div
        @click="showBulkModal = true"
        class="group bg-white border border-slate-100 rounded-3xl p-8 shadow-sm hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col items-start"
      >
        <div
          class="w-14 h-14 bg-indigo-50 text-indigo-600 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-indigo-600 group-hover:text-white transition-colors duration-300"
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
              d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-8l-4-4m0 0L8 8m4-4v12"
            />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-black mb-2">Bulk CSV Import</h3>
        <p class="text-sm text-black/80 leading-relaxed">
          Upload the McPherson curriculum handbook as a CSV to populate the
          entire graph at once.
        </p>
      </div>

      <NuxtLink
        to="/admin/analytics"
        class="group bg-white border border-slate-100 rounded-3xl p-8 shadow-sm hover:shadow-[0_20px_40px_rgba(0,0,0,0.06)] hover:-translate-y-1 transition-all duration-300 cursor-pointer flex flex-col items-start"
      >
        <div
          class="w-14 h-14 bg-emerald-50 text-emerald-600 rounded-2xl flex items-center justify-center mb-6 group-hover:bg-emerald-600 group-hover:text-white transition-colors duration-300"
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
              d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
            />
          </svg>
        </div>
        <h3 class="text-lg font-bold text-black mb-2">Graph Analytics</h3>
        <p class="text-sm text-black/80 leading-relaxed">
          View bottleneck courses, skill distribution, and overall health of the
          curriculum map.
        </p>
      </NuxtLink>
    </div>

    <div
      v-if="showAddModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm transition-opacity"
    >
      <div
        class="relative w-full max-w-2xl bg-white rounded-3xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-200"
      >
        <button
          @click="showAddModal = false"
          class="absolute top-6 right-6 text-slate-400 hover:text-slate-800 hover:bg-slate-100 p-2 rounded-full transition-all z-10"
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
        <div class="max-h-[85vh] overflow-y-auto">
          <AdminAddCourseForm @course-added="handleCourseAdded" />
        </div>
      </div>
    </div>

    <div
      v-if="showBulkModal"
      class="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/40 backdrop-blur-sm transition-opacity"
    >
      <div
        class="relative w-full max-w-lg bg-white rounded-3xl p-8 shadow-2xl text-center"
      >
        <button
          @click="showBulkModal = false"
          class="absolute top-4 right-4 text-slate-400 hover:text-slate-800 p-2"
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
        <div
          class="w-16 h-16 bg-indigo-50 text-indigo-500 rounded-full flex items-center justify-center mx-auto mb-4"
        >
          <svg
            xmlns="http://www.w3.org/2000/svg"
            class="h-8 w-8"
            fill="none"
            viewBox="0 0 24 24"
            stroke="currentColor"
          >
            <path
              stroke-linecap="round"
              stroke-linejoin="round"
              stroke-width="2"
              d="M19 11H5m14 0a2 2 0 012 2v6a2 2 0 01-2 2H5a2 2 0 01-2-2v-6a2 2 0 012-2m14 0V9a2 2 0 00-2-2M5 11V9a2 2 0 002-2m0 0V5a2 2 0 012-2h6a2 2 0 012 2v2M7 7h10"
            />
          </svg>
        </div>
        <h3 class="text-xl font-bold mb-2 text-black">Bulk Importer</h3>
        <p class="text-black/70 text-sm mb-6">
          This feature will parse the CSV and automatically run the NLP
          extraction on all courses simultaneously.
        </p>
        <div class="mt-4">
          <AdminBulkCourseUpload
            @success="handleCourseAdded"
            @error="handleUploadError"
          />
        </div>
      </div>
    </div>
    <Transition
      enter-active-class="transform ease-out duration-300 transition"
      enter-from-class="translate-y-2 opacity-0 sm:translate-y-0 sm:translate-x-2"
      enter-to-class="translate-y-0 opacity-100 sm:translate-x-0"
      leave-active-class="transition ease-in duration-100"
      leave-from-class="opacity-100"
      leave-to-class="opacity-0"
    >
      <div
        v-if="notification.show"
        class="fixed bottom-10 right-10 z-[100] max-w-sm w-full"
      >
        <div
          class="rounded-2xl p-4 shadow-2xl flex items-center gap-4 border"
          :class="
            notification.type === 'success'
              ? 'bg-white border-emerald-100'
              : 'bg-white border-red-100'
          "
        >
          <div
            :class="
              notification.type === 'success'
                ? 'text-emerald-500'
                : 'text-red-500'
            "
          >
            <svg
              v-if="notification.type === 'success'"
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
                d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
            <svg
              v-else
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
                d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
              />
            </svg>
          </div>
          <div class="flex-1">
            <p class="text-sm font-bold text-slate-900">
              {{
                notification.type === "success"
                  ? "Success"
                  : "Attention Required"
              }}
            </p>
            <p class="text-xs text-slate-500 font-medium">
              {{ notification.message }}
            </p>
          </div>
          <button
            @click="notification.show = false"
            class="text-slate-300 hover:text-slate-500"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M4.293 4.293a1 1 0 011.414 0L10 8.586l4.293-4.293a1 1 0 111.414 1.414L11.414 10l4.293 4.293a1 1 0 01-1.414 1.414L10 11.414l-4.293 4.293a1 1 0 01-1.414-1.414L8.586 10 4.293 5.707a1 1 0 010-1.414z"
                clip-rule="evenodd"
              />
            </svg>
          </button>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { ref } from "vue";

definePageMeta({
  middleware: "auth",
});

const showAddModal = ref(false);
const showBulkModal = ref(false);

const notification = ref({
  show: false,
  message: "",
  type: "success", // 'success' or 'error'
});

const triggerNotification = (message, type = "success") => {
  notification.value = { show: true, message, type };
  // Auto-hide after 4 seconds
  setTimeout(() => {
    notification.value.show = false;
  }, 4000);
};

const handleCourseAdded = (msg) => {
  showAddModal.value = false;
  showBulkModal.value = false;
  triggerNotification(msg || "Curriculum updated successfully!");
};

const handleUploadError = (msg) => {
  triggerNotification(msg || "An error occurred during the update.", "error");
};
</script>

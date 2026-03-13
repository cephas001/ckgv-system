<template>
  <div class="flex flex-col items-center">
    <div
      @dragover.prevent="isDragging = true"
      @dragleave.prevent="isDragging = false"
      @drop.prevent="handleDrop"
      class="w-full border-2 border-dashed rounded-2xl p-8 transition-all duration-300 flex flex-col items-center justify-center cursor-pointer"
      :class="[
        isDragging
          ? 'border-indigo-500 bg-indigo-50'
          : 'border-slate-200 bg-slate-50',
        uploadStatus === 'loading' ? 'pointer-events-none opacity-50' : '',
      ]"
      @click="$refs.fileInput.click()"
    >
      <input
        type="file"
        ref="fileInput"
        class="hidden"
        accept=".csv"
        @change="handleFileSelect"
      />

      <div
        class="w-12 h-12 bg-white rounded-xl shadow-sm flex items-center justify-center mb-4 text-slate-400 group-hover:text-indigo-500"
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
            d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"
          />
        </svg>
      </div>

      <p class="text-sm font-bold text-black">
        {{
          selectedFile ? selectedFile.name : "Click to upload or drag & drop"
        }}
      </p>
      <p
        class="text-[10px] text-black/70 mt-1 uppercase tracking-widest font-bold"
      >
        Supported: CSV only
      </p>
    </div>

    <div v-if="uploadStatus" class="mt-4 w-full">
      <div
        v-if="uploadStatus === 'loading'"
        class="flex items-center justify-center gap-2 text-indigo-600 text-sm font-bold"
      >
        <svg class="animate-spin h-4 w-4" viewBox="0 0 24 24">
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
        AI Analyzing Curriculum...
      </div>
      <p
        v-if="uploadStatus === 'success'"
        class="text-emerald-600 text-xs font-bold text-center"
      >
        {{ responseMessage }}
      </p>
      <p
        v-if="uploadStatus === 'error'"
        class="text-red-500 text-xs font-bold text-center"
      >
        {{ responseMessage }}
      </p>
    </div>

    <div class="mt-6 flex flex-col gap-3 w-full">
      <button
        @click.stop="triggerUpload"
        :disabled="!selectedFile || uploadStatus === 'loading'"
        class="w-full bg-indigo-600 text-white font-bold py-3 rounded-xl shadow-lg shadow-indigo-200 hover:bg-indigo-700 disabled:opacity-50 transition-all transform active:scale-95 tracking-wide"
      >
        Process Bulk Import
      </button>

      <button
        @click.stop="downloadTemplate"
        class="text-[10px] font-bold text-black hover:text-black/80 uppercase tracking-widest transition-colors"
      >
        Download CSV Template
      </button>
    </div>
  </div>
</template>

<script setup>
const selectedFile = ref(null);
const isDragging = ref(false);
const uploadStatus = ref(null); // 'loading', 'success', 'error'
const responseMessage = ref("");

const emit = defineEmits(["success"]);

const handleFileSelect = (e) => {
  const file = e.target.files[0];
  if (file && file.type === "text/csv") {
    selectedFile.value = file;
    uploadStatus.value = null;
  }
};

const handleDrop = (e) => {
  isDragging.value = false;
  const file = e.dataTransfer.files[0];
  if (file && file.name.endsWith(".csv")) {
    selectedFile.value = file;
    uploadStatus.value = null;
  }
};

const triggerUpload = async () => {
  if (!selectedFile.value) return;

  uploadStatus.value = "loading";
  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await $fetch("http://127.0.0.1:8000/api/courses/bulk", {
      method: "POST",
      body: formData,
    });

    uploadStatus.value = "success";
    // Emit the success message to the dashboard
    emit("success", response.message);
  } catch (err) {
    uploadStatus.value = "error";
    const errorMsg = err.data?.detail || "Upload failed.";
    // You can also emit an error if you want the dashboard to handle it
    emit("error", errorMsg);
  }
};

const downloadTemplate = () => {
  const csvContent =
    "course_id,title,credits,synopsis\nCMP 401,Advanced Compilers,3,Study of register allocation and code optimization.";
  const blob = new Blob([csvContent], { type: "text/csv" });
  const url = window.URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.setAttribute("href", url);
  a.setAttribute("download", "curriculum_template.csv");
  a.click();
};
</script>

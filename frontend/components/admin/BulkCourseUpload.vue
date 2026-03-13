<template>
  <div class="w-full text-left">
    <div v-if="currentStep === 1" class="space-y-4">
      <div
        class="border-2 border-dashed border-slate-200 rounded-2xl p-8 text-center hover:bg-slate-50 transition-colors cursor-pointer"
        @click="$refs.fileInput.click()"
      >
        <input
          type="file"
          ref="fileInput"
          accept=".csv"
          class="hidden"
          @change="handleFileUpload"
        />
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-10 w-10 text-indigo-400 mx-auto mb-3"
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
        <p class="text-sm font-bold text-black">
          Click to upload curriculum CSV
        </p>
        <p class="text-xs text-black/70 mt-1">
          {{ selectedFile ? selectedFile.name : "No file selected" }}
        </p>
      </div>

      <button
        @click="processWithAI"
        :disabled="!selectedFile || isProcessing"
        class="w-full bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 text-white py-3 rounded-xl shadow-md transition-all flex justify-center items-center gap-2 cursor-pointer"
      >
        <svg
          v-if="isProcessing"
          class="animate-spin h-5 w-5 text-white"
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
        {{
          isProcessing
            ? "AI Processing Document..."
            : "Extract Entities with spaCy"
        }}
      </button>
    </div>

    <div v-else-if="currentStep === 2" class="space-y-4">
      <div
        class="bg-amber-50 border border-amber-200 rounded-xl p-4 flex gap-3"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-amber-600 shrink-0 mt-0.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"
          />
        </svg>
        <div>
          <p class="text-sm text-amber-800">Step 1: Pending Approval</p>
          <p class="text-xs text-amber-700">
            Review and validate the AI's extracted skills before proceeding.
          </p>
        </div>
      </div>

      <div
        class="max-h-[40vh] overflow-y-auto overflow-x-hidden border border-slate-200 rounded-xl"
      >
        <table class="min-w-full divide-y divide-slate-200">
          <thead class="bg-slate-50 sticky top-0 z-10">
            <tr>
              <th
                class="px-4 py-2 text-left text-xs font-bold text-black uppercase"
              >
                Course
              </th>
              <th
                class="px-4 py-2 text-left text-xs font-bold text-black uppercase"
              >
                AI Extracted Skills
              </th>
            </tr>
          </thead>
          <tbody class="bg-white divide-y divide-slate-100">
            <tr v-for="(course, index) in pendingData" :key="index">
              <td
                class="px-4 py-3 whitespace-nowrap text-sm text-black align-top pt-4"
              >
                {{ course.course_id }}
              </td>
              <td class="px-4 py-3">
                <textarea
                  v-model="course.technical_skills_raw"
                  rows="2"
                  class="w-full px-3 py-2 text-sm border border-slate-200 rounded-lg focus:ring-2 focus:ring-indigo-500 resize-none overflow-y-auto"
                  title="Comma separated skills"
                ></textarea>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <div class="flex gap-3 pt-2">
        <button
          @click="resetState"
          class="flex-1 px-4 py-3 text-sm text-black bg-white border border-slate-200 hover:bg-slate-50 rounded-xl transition-colors"
        >
          Discard & Cancel
        </button>
        <button
          @click="currentStep = 3"
          class="flex-1 bg-indigo-600 hover:bg-indigo-700 text-white py-3 rounded-xl shadow-md transition-colors flex justify-center items-center gap-2"
        >
          Choose Strategy
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
              d="M9 5l7 7-7 7"
            />
          </svg>
        </button>
      </div>
    </div>

    <div v-else-if="currentStep === 3" class="space-y-4">
      <div
        class="bg-blue-50 border border-blue-200 rounded-xl p-4 flex gap-3 mb-4"
      >
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-5 w-5 text-blue-600 shrink-0 mt-0.5"
          fill="none"
          viewBox="0 0 24 24"
          stroke="currentColor"
        >
          <path
            stroke-linecap="round"
            stroke-linejoin="round"
            stroke-width="2"
            d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"
          />
        </svg>
        <div>
          <p class="text-sm text-blue-800">Step 2: Finalize Import</p>
          <p class="text-xs text-blue-700">
            Choose how this data should be written to the Knowledge Graph
            database.
          </p>
        </div>
      </div>

      <div class="bg-slate-50 border border-slate-200 rounded-xl p-5">
        <div class="flex flex-col gap-4">
          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              type="radio"
              v-model="importMode"
              value="update"
              class="mt-1 text-indigo-600 focus:ring-indigo-500"
            />
            <div>
              <p
                class="text-sm text-black group-hover:text-indigo-600 transition-colors"
              >
                Merge & Update (Safe)
              </p>
              <p class="text-xs text-slate-500 mt-1">
                Updates existing courses and appends new ones. Retains the
                current graph structure.
              </p>
            </div>
          </label>

          <div class="h-px w-full bg-slate-200"></div>

          <label class="flex items-start gap-3 cursor-pointer group">
            <input
              type="radio"
              v-model="importMode"
              value="overwrite"
              class="mt-1 text-red-600 focus:ring-red-500"
            />
            <div>
              <p
                class="text-sm text-black group-hover:text-red-600 transition-colors"
              >
                Archive & Overwrite (Destructive)
              </p>
              <p class="text-xs text-slate-500 mt-1">
                Archives the current curriculum and replaces it entirely with
                this newly validated data.
              </p>
            </div>
          </label>
        </div>
      </div>

      <div class="flex gap-3 pt-4">
        <button
          @click="currentStep = 2"
          class="flex-1 px-4 py-3 text-sm text-black bg-white border border-slate-200 hover:bg-slate-50 rounded-xl transition-colors flex items-center justify-center gap-2"
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
              d="M15 19l-7-7 7-7"
            />
          </svg>
          Back to Review
        </button>
        <button
          @click="commitToGraph"
          :disabled="isSaving"
          class="flex-1 bg-emerald-500 hover:bg-emerald-600 text-white py-3 rounded-xl shadow-md transition-colors flex justify-center items-center gap-2"
        >
          <svg
            v-if="isSaving"
            class="animate-spin h-5 w-5 text-white"
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
          {{ isSaving ? "Committing..." : "Commit to Graph" }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

const emit = defineEmits(["success", "error"]);

// --- UI STATE ---
const currentStep = ref(1); // Controls the wizard (1: Upload, 2: Validate, 3: Strategy)
const fileInput = ref(null);
const selectedFile = ref(null);
const isProcessing = ref(false);
const isSaving = ref(false);

// --- DATA STATE ---
const importMode = ref("update");
const pendingData = ref([]);

const handleFileUpload = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
  }
};

const resetState = () => {
  pendingData.value = [];
  selectedFile.value = null;
  currentStep.value = 1;
};

// ==========================================
// STEP 1: UPLOAD CSV & GET AI PREVIEW
// ==========================================
const processWithAI = async () => {
  if (!selectedFile.value) return;

  isProcessing.value = true;
  const formData = new FormData();
  formData.append("file", selectedFile.value);

  try {
    const response = await $fetch("http://127.0.0.1:8000/api/upload/preview", {
      method: "POST",
      body: formData,
    });

    pendingData.value = response.extracted_courses.map((course) => ({
      ...course,
      technical_skills_raw: course.technical_skills?.join(", ") || "",
    }));

    // Move to Step 2!
    currentStep.value = 2;
  } catch (error) {
    emit("error", "AI Extraction failed. Check the CSV format.");
  } finally {
    isProcessing.value = false;
  }
};

// ==========================================
// STEP 3: VALIDATE AND COMMIT TO GRAPH
// ==========================================
const commitToGraph = async () => {
  isSaving.value = true;

  try {
    const validatedPayload = pendingData.value.map((course) => {
      const skillsArray = course.technical_skills_raw
        .split(",")
        .map((s) => s.trim())
        .filter((s) => s.length > 0);

      return {
        ...course,
        technical_skills: skillsArray,
      };
    });

    await $fetch("http://127.0.0.1:8000/api/upload/commit", {
      method: "POST",
      body: {
        courses: validatedPayload,
        import_mode: importMode.value,
      },
    });

    emit(
      "success",
      `Data successfully committed using '${importMode.value}' strategy!`,
    );
    resetState(); // Clear everything and return to Step 1
  } catch (error) {
    emit("error", "Failed to save to database. Check FastAPI terminal.");
  } finally {
    isSaving.value = false;
  }
};
</script>

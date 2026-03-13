<template>
  <div
    class="bg-white p-8 sm:p-10 rounded-[2rem] shadow-sm max-w-2xl mx-auto font-poppins relative"
  >
    <div class="flex items-center justify-between mb-8">
      <div>
        <h3 class="text-2xl font-bold text-black tracking-tight">
          Add New Course
        </h3>
        <p class="text-sm text-black/80 mt-1 font-medium">
          Manually expand the curriculum graph.
        </p>
      </div>
      <div
        class="flex items-center gap-2 px-3 py-1.5 bg-indigo-50/80 text-indigo-600 rounded-full border border-indigo-100"
      >
        <div class="w-2 h-2 rounded-full bg-indigo-500 animate-pulse"></div>
        <span class="text-[10px] font-bold uppercase tracking-widest"
          >Admin Portal</span
        >
      </div>
    </div>

    <div
      class="mb-8 p-6 bg-gradient-to-br from-slate-50 to-indigo-50/30 rounded-2xl border border-indigo-100/50 relative overflow-hidden group transition-all duration-300 hover:border-indigo-200"
    >
      <div class="absolute top-0 left-0 w-1 h-full bg-indigo-400"></div>

      <label
        class="text-xs font-bold text-indigo-900 uppercase tracking-wide mb-3 flex items-center gap-2"
      >
        <IconsLightening />
        AI Analysis Pipeline
      </label>

      <textarea
        v-model="rawDescription"
        rows="3"
        class="w-full p-4 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-white resize-none"
        placeholder="Paste syllabus description here... (e.g., 'An introduction to Agile, Scrum, and Git.')"
      ></textarea>

      <div class="flex justify-between items-center mt-3">
        <span class="text-[10px] font-medium text-slate-400"
          >Powered by spaCy NLP</span
        >
        <button
          @click.prevent="runNLPAnalysis"
          :disabled="isAnalyzing || !rawDescription"
          class="text-xs font-bold px-4 py-2 rounded-lg bg-indigo-600 text-white hover:bg-indigo-700 flex items-center gap-2 disabled:opacity-50 disabled:hover:bg-indigo-600 transition-all shadow-sm"
        >
          <svg
            v-if="isAnalyzing"
            class="animate-spin h-3 w-3 text-white"
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
          <span v-if="isAnalyzing">Extracting Entities...</span>
          <span v-else>Auto-Fill Fields</span>
        </button>
      </div>
    </div>

    <form @submit.prevent="submitForm" class="space-y-6">
      <div class="grid grid-cols-1 md:grid-cols-4 gap-5">
        <div class="md:col-span-1">
          <label
            class="block text-[11px] font-bold text-black uppercase tracking-wide mb-2 ml-1"
          >
            Course Code <span class="text-red-400">*</span>
          </label>
          <input
            v-model="form.course_id"
            type="text"
            placeholder="CMP 401"
            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-slate-50 focus:bg-white"
            required
          />
        </div>

        <div class="md:col-span-1">
          <label
            class="block text-[11px] font-bold text-black uppercase tracking-wide mb-2 ml-1"
          >
            Credits <span class="text-red-400">*</span>
          </label>
          <input
            v-model.number="form.credits"
            type="number"
            min="1"
            max="6"
            placeholder="3"
            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-slate-50 focus:bg-white"
            required
          />
        </div>

        <div class="md:col-span-2">
          <label
            class="block text-[11px] font-bold text-black uppercase tracking-wide mb-2 ml-1"
          >
            Specialization Track <span class="text-red-400">*</span>
          </label>
          <select
            v-model="form.specialization"
            class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-slate-50 focus:bg-white appearance-none cursor-pointer"
          >
            <option>Core Computer Science</option>
            <option>Software Engineering</option>
            <option>Cybersecurity</option>
            <option>Data & Algorithms</option>
            <option>Systems & Architecture</option>
            <option>Artificial Intelligence</option>
          </select>
        </div>
      </div>

      <div>
        <label
          class="block text-[11px] font-bold text-black uppercase tracking-wide mb-2 ml-1"
        >
          Full Course Title <span class="text-red-400">*</span>
        </label>
        <input
          v-model="form.title"
          type="text"
          placeholder="e.g. Advanced Database Management Systems"
          class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-slate-50 focus:bg-white"
          required
        />
      </div>

      <div>
        <label
          class="block text-[11px] font-bold text-black uppercase tracking-wide"
        >
          Technical Skills
        </label>
        <p class="text-[10px] text-slate-400 mb-2 ml-1 font-medium">
          Comma separated (e.g. Python, Git)
        </p>
        <input
          v-model="skillsInput"
          type="text"
          placeholder="Extracted skills appear here..."
          class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-white"
        />
      </div>

      <div>
        <label
          class="block text-[11px] font-bold text-black uppercase tracking-wide"
        >
          Prerequisites (Optional)
        </label>
        <p class="text-[10px] text-slate-400 mb-2 ml-1 font-medium">
          Comma separated (e.g. CMP 201, CMP 202)
        </p>
        <input
          v-model="prereqInput"
          type="text"
          placeholder="Leave blank if none..."
          class="w-full px-4 py-3 rounded-xl border border-slate-200 focus:border-black/70 outline-none text-sm text-black transition-all bg-white"
        />
      </div>

      <div class="pt-2">
        <button
          type="submit"
          :disabled="isSubmitting"
          class="w-full bg-[#e33e38] text-white py-4 rounded-xl shadow-[0_8px_20px_rgba(227,62,56,0.25)] hover:bg-[#c93631] hover:shadow-[0_12px_25px_rgba(227,62,56,0.35)] transition-all duration-300 transform hover:-translate-y-0.5 disabled:opacity-70 disabled:hover:translate-y-0 flex items-center justify-center gap-2"
        >
          <svg
            v-if="isSubmitting"
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
            isSubmitting ? "Committing to Database..." : "Save to Curriculum"
          }}
        </button>
      </div>
    </form>
  </div>
</template>

<script setup>
import { ref } from "vue";

const rawDescription = ref("");
const skillsInput = ref("");
const prereqInput = ref("");
const isAnalyzing = ref(false);
const isSubmitting = ref(false);

const emit = defineEmits(["course-added"]);

// UPDATED: Added credits property with a default of 3
const form = ref({
  course_id: "",
  credits: 3,
  title: "",
  specialization: "Core Computer Science",
  prerequisites: [],
  technical_skills: [],
  synopsis: "",
});

const runNLPAnalysis = async () => {
  isAnalyzing.value = true;
  try {
    const data = await $fetch("http://127.0.0.1:8000/api/nlp/analyze", {
      method: "POST",
      body: { description: rawDescription.value },
    });

    form.value.specialization = data.suggested_specialization;
    skillsInput.value = data.extracted_skills.join(", ");
  } catch (error) {
    console.error("NLP Error:", error);
    alert("AI Analysis failed. Please ensure the backend is running.");
  } finally {
    isAnalyzing.value = false;
  }
};

const submitForm = async () => {
  isSubmitting.value = true;

  form.value.technical_skills = skillsInput.value
    ? skillsInput.value
        .split(",")
        .map((s) => s.trim())
        .filter(Boolean)
    : [];

  form.value.prerequisites = prereqInput.value
    ? prereqInput.value
        .split(",")
        .map((s) => s.trim().toUpperCase())
        .filter(Boolean)
    : [];

  form.value.synopsis = rawDescription.value.trim();

  try {
    await $fetch("http://127.0.0.1:8000/api/courses", {
      method: "POST",
      body: form.value,
    });

    emit("course-added");

    // UPDATED: Reset credits back to 3
    form.value = {
      course_id: "",
      credits: 3,
      title: "",
      specialization: "Core Computer Science",
      prerequisites: [],
      technical_skills: [],
      synopsis: "",
    };
    rawDescription.value = "";
    skillsInput.value = "";
    prereqInput.value = "";
  } catch (error) {
    console.error("Submit Error:", error);
    alert("Failed to save course. Check console for details.");
  } finally {
    isSubmitting.value = false;
  }
};
</script>

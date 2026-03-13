<template>
  <div class="w-full h-full bg-[#160d27] flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <div
        class="bg-white rounded-3xl shadow-[0_18px_55px_rgba(0,0,0,0.35)] border border-white/30 overflow-hidden"
      >
        <div class="px-8 pt-5 pb-6 border-b border-slate-100">
          <h1 class="text-2xl font-extrabold tracking-tight text-black">
            Admin Login
          </h1>
          <p class="text-sm text-black/90 mt-1">
            Sign in to access the Admin Portal.
          </p>
        </div>

        <form class="px-8 py-7 space-y-5" @submit.prevent="handleLogin">
          <div
            v-if="errorMessage"
            class="bg-red-50 text-red-600 p-3 rounded-xl text-xs flex items-center gap-2"
          >
            <svg
              xmlns="http://www.w3.org/2000/svg"
              class="h-4 w-4"
              viewBox="0 0 20 20"
              fill="currentColor"
            >
              <path
                fill-rule="evenodd"
                d="M10 18a8 8 0 100-16 8 8 0 000 16zM8.707 7.293a1 1 0 00-1.414 1.414L8.586 10l-1.293 1.293a1 1 0 101.414 1.414L10 11.414l1.293 1.293a1 1 0 001.414-1.414L11.414 10l1.293-1.293a1 1 0 00-1.414-1.414L10 8.586 8.707 7.293z"
                clip-rule="evenodd"
              />
            </svg>
            {{ errorMessage }}
          </div>

          <div>
            <label
              class="block text-sm font-bold text-black mb-2"
              for="username"
              >Username</label
            >
            <input
              id="username"
              v-model.trim="username"
              type="text"
              autocomplete="username"
              required
              placeholder="e.g. admin"
              class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm text-black placeholder:text-slate-400 shadow-sm focus:outline-none focus:ring-1 focus:ring-black"
              @input="errorMessage = ''"
            />
          </div>

          <div>
            <label
              class="block text-sm font-bold text-black mb-2"
              for="password"
              >Password</label
            >
            <input
              id="password"
              v-model="password"
              type="password"
              autocomplete="current-password"
              required
              placeholder="••••••••"
              class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm text-slate-900 placeholder:text-slate-400 shadow-sm focus:outline-none focus:ring-1 focus:ring-black"
              @input="errorMessage = ''"
            />
          </div>

          <button
            type="submit"
            :disabled="isLoading"
            class="w-full bg-[#e33e38] hover:bg-[#c93631] disabled:opacity-70 text-white px-5 py-3 rounded-2xl text-sm font-extrabold shadow-[0_8px_22px_rgba(227,62,56,0.28)] transition-all transform hover:-translate-y-0.5 flex justify-center items-center gap-2"
          >
            <svg
              v-if="isLoading"
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
            {{ isLoading ? "Authenticating..." : "Sign In" }}
          </button>

          <p class="text-xs text-black/70 text-center font-medium">
            Protected area — authorized personnel only.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";

definePageMeta({
  layout: false,
});

const username = ref("");
const password = ref("");
const errorMessage = ref("");
const isLoading = ref(false);

const router = useRouter();

// Clear any existing session when visiting the login page
const token = useCookie("auth_token");
token.value = null;

const handleLogin = async () => {
  isLoading.value = true;
  errorMessage.value = "";

  try {
    const response = await $fetch("http://127.0.0.1:8000/api/auth/login", {
      method: "POST",
      body: {
        username: username.value,
        password: password.value,
      },
    });

    // Save the secure token to a cookie
    token.value = response.access_token;

    // Redirect to dashboard
    await router.push("/admin/dashboard");
  } catch (error) {
    if (error.response?.status === 401) {
      errorMessage.value = "Invalid username or password.";
    } else {
      errorMessage.value = "Server error. Is the backend running?";
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

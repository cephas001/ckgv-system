<template>
  <div class="w-full h-full bg-[#160d27] flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <div
        class="bg-white rounded-3xl shadow-[0_18px_55px_rgba(0,0,0,0.35)] border border-white/30 overflow-hidden"
      >
        <div class="px-8 pt-8 pb-6 border-b border-slate-100">
          <h1 class="text-2xl font-extrabold tracking-tight text-black">
            Admin Login
          </h1>
          <p class="text-sm text-black/90 mt-1">
            Sign in to access the Admin Portal.
          </p>
        </div>

        <form class="px-8 py-7 space-y-5" @submit.prevent="handleLogin">
          <div>
            <label class="block text-sm text-black mb-2" for="email"
              >Email</label
            >
            <input
              id="email"
              v-model.trim="email"
              type="email"
              autocomplete="email"
              required
              placeholder="admin@mcpherson.edu"
              class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm text-black placeholder:text-slate-400 shadow-sm focus:outline-none focus:ring-1 focus:ring-black"
            />
          </div>

          <div>
            <label class="block text-sm text-black mb-2" for="password"
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
            />
          </div>

          <button
            type="submit"
            class="w-full bg-[#e33e38] hover:bg-[#c93631] text-white px-5 py-3 rounded-2xl text-sm font-extrabold shadow-[0_8px_22px_rgba(227,62,56,0.28)] transition-all transform hover:-translate-y-0.5"
          >
            Sign In
          </button>

          <p class="text-xs text-black/70 text-center">
            Protected area — authorized personnel only.
          </p>
        </form>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from "vue";

definePageMeta({
  layout: false,
});

const email = ref("");
const password = ref("");

const { login } = useAuth();

const handleLogin = async () => {
  await login(email.value, password.value);
  await navigateTo("/admin/dashboard");
};
</script>

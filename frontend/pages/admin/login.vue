<template>
  <div class="w-full h-full bg-[#160d27] flex items-center justify-center p-6">
    <div class="w-full max-w-md">
      <div class="mb-6 flex items-center justify-center">
        <div
          class="w-12 h-12 rounded-2xl bg-white/10 border border-white/15 flex items-center justify-center shadow-lg"
        >
          <span class="text-white font-extrabold tracking-wider">MU</span>
        </div>
      </div>

      <div
        class="bg-white rounded-3xl shadow-[0_18px_55px_rgba(0,0,0,0.35)] border border-white/30 overflow-hidden"
      >
        <div class="px-8 pt-8 pb-6 border-b border-slate-100">
          <h1 class="text-2xl font-extrabold tracking-tight text-slate-900">
            Admin Login
          </h1>
          <p class="text-sm font-semibold text-slate-500 mt-1">
            Sign in to access the Admin Portal.
          </p>
        </div>

        <form class="px-8 py-7 space-y-5" @submit.prevent="handleLogin">
          <div>
            <label class="block text-sm font-bold text-slate-700 mb-2" for="email"
              >Email</label
            >
            <input
              id="email"
              v-model.trim="email"
              type="email"
              autocomplete="email"
              required
              placeholder="admin@mcpherson.edu"
              class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm font-semibold text-slate-900 placeholder:text-slate-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-[#160d27]/25 focus:border-[#160d27]/40"
            />
          </div>

          <div>
            <label
              class="block text-sm font-bold text-slate-700 mb-2"
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
              class="w-full px-4 py-3 rounded-2xl border border-slate-200 bg-white text-sm font-semibold text-slate-900 placeholder:text-slate-400 shadow-sm focus:outline-none focus:ring-2 focus:ring-[#160d27]/25 focus:border-[#160d27]/40"
            />
          </div>

          <button
            type="submit"
            class="w-full bg-[#e33e38] hover:bg-[#c93631] text-white px-5 py-3 rounded-2xl text-sm font-extrabold shadow-[0_8px_22px_rgba(227,62,56,0.28)] transition-all transform hover:-translate-y-0.5"
          >
            Sign In
          </button>

          <p class="text-xs font-semibold text-slate-400 text-center">
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


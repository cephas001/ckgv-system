<template>
  <aside
    class="w-64 bg-white border-r border-slate-200 flex flex-col shadow-sm z-20 fixed inset-y-0 left-0 shrink-0"
  >
    <NuxtLink
      to="/"
      class="h-20 flex items-center px-6 border-b border-slate-100"
    >
      <div
        class="w-8 h-8 rounded-lg bg-[#160d27] flex items-center justify-center mr-3 shadow-md text-center"
      >
        <span class="text-white font-bold text-sm tracking-wider">MU</span>
      </div>
      <h1 class="font-bold text-lg text-black tracking-tight">CKGV System</h1>
    </NuxtLink>

    <nav class="flex-1 px-4 py-6 space-y-6 overflow-y-auto">
      <div>
        <p
          class="px-4 text-[10px] font-bold tracking-widest uppercase text-slate-400 mb-3"
        >
          Public Views
        </p>
        <div class="space-y-2">
          <NuxtLink
            to="/"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
            :class="isActive('/') ? activeClass : inactiveClass"
          >
            <IconsKnowledgeGraph />
            Knowledge Graph
          </NuxtLink>

          <NuxtLink
            to="/directory"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
            :class="isActive('/directory') ? activeClass : inactiveClass"
          >
            <IconsList />
            Course Directory
          </NuxtLink>
        </div>
      </div>

      <div v-if="adminUsername">
        <p
          class="px-4 text-[10px] font-bold tracking-widest uppercase text-slate-400 mb-3"
        >
          Admin Views
        </p>
        <div class="space-y-2">
          <NuxtLink
            to="/admin/dashboard"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
            :class="isActive('/admin/dashboard') ? activeClass : inactiveClass"
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
                d="M4 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2V6zM14 6a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2V6zM4 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2H6a2 2 0 01-2-2v-2zM14 16a2 2 0 012-2h2a2 2 0 012 2v2a2 2 0 01-2 2h-2a2 2 0 01-2-2v-2z"
              />
            </svg>
            Control Center
          </NuxtLink>

          <NuxtLink
            to="/admin/analytics"
            class="w-full flex items-center gap-3 px-4 py-3 rounded-xl border transition-colors"
            :class="isActive('/admin/analytics') ? activeClass : inactiveClass"
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
                d="M9 19v-6a2 2 0 00-2-2H5a2 2 0 00-2 2v6a2 2 0 002 2h2a2 2 0 002-2zm0 0V9a2 2 0 012-2h2a2 2 0 012 2v10m-6 0a2 2 0 002 2h2a2 2 0 002-2m0 0V5a2 2 0 012-2h2a2 2 0 012 2v14a2 2 0 01-2 2h-2a2 2 0 01-2-2z"
              />
            </svg>
            Graph Analytics
          </NuxtLink>
        </div>
      </div>
    </nav>

    <div class="p-4 border-t border-slate-100 space-y-3">
      <NuxtLink
        v-if="!adminUsername"
        to="/admin/login"
        :class="[
          route.path.startsWith('/admin')
            ? 'text-black'
            : 'text-slate-400 hover:text-slate-700',
          'flex items-center justify-between px-3 py-2 rounded-xl text-xs font-bold hover:bg-slate-50 transition-colors',
        ]"
      >
        <span class="tracking-widest uppercase">Admin Login</span>
        <svg
          xmlns="http://www.w3.org/2000/svg"
          class="h-4 w-4 opacity-70"
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
      </NuxtLink>

      <div
        v-if="adminUsername"
        class="flex items-center justify-between px-2 py-2 bg-slate-50 rounded-xl border border-slate-100"
      >
        <div class="flex items-center gap-3">
          <div
            class="w-9 h-9 rounded-full bg-indigo-100 text-indigo-700 flex items-center justify-center font-bold text-sm"
          >
            {{ adminUsername.charAt(0).toUpperCase() }}
          </div>
          <div class="flex flex-col">
            <span
              class="text-sm font-semibold text-black leading-none mb-1 capitalize"
            >
              {{ adminUsername }}
            </span>
            <span
              class="text-[10px] font-semibold tracking-widest uppercase text-emerald-600 leading-none"
            >
              Online
            </span>
          </div>
        </div>

        <button
          @click="handleLogout"
          class="p-2 text-slate-400 hover:text-[#e33e38] hover:bg-red-50 rounded-lg transition-colors"
          title="Secure Logout"
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
              d="M17 16l4-4m0 0l-4-4m4 4H7m6 4v1a3 3 0 01-3 3H6a3 3 0 01-3-3V7a3 3 0 013-3h4a3 3 0 013 3v1"
            />
          </svg>
        </button>
      </div>
    </div>
  </aside>
</template>

<script setup>
import { computed } from "vue";
import { useRoute } from "vue-router";

const activeClass = "bg-indigo-50/70 text-black border-indigo-100";
const inactiveClass =
  "text-slate-500 font-medium border-transparent hover:bg-slate-50 hover:text-slate-800";

const route = useRoute();

const isActive = (path) => {
  if (path === "/") return route.path === "/" || route.path === "/graph";
  return route.path === path;
};

// --- LOGOUT LOGIC ---
const handleLogout = async () => {
  const token = useCookie("auth_token");
  token.value = null; // Destroy the cookie
  await navigateTo("/"); // Redirect to the public home page
};

// --- DYNAMIC JWT DECODING ---
const adminUsername = computed(() => {
  const token = useCookie("auth_token").value;
  if (!token) return null;

  try {
    // A JWT is split into 3 parts by periods. We want the payload (index 1).
    const payloadBase64 = token.split(".")[1];

    // Decode from Base64
    // We use a safe decode method to prevent SSR hydration errors
    const decodedJson =
      typeof window !== "undefined"
        ? window.atob(payloadBase64)
        : Buffer.from(payloadBase64, "base64").toString("ascii");

    const parsedData = JSON.parse(decodedJson);

    // 'sub' is the key we used in FastAPI for the username
    return parsedData.sub;
  } catch (error) {
    console.error("Could not decode token", error);
    return null;
  }
});
</script>

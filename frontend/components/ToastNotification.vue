<template>
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
      class="fixed bottom-10 right-10 z-[200] max-w-sm w-full pointer-events-auto"
    >
      <div
        class="rounded-2xl p-4 shadow-2xl flex items-center gap-4 border backdrop-blur-md"
        :class="
          notification.type === 'success'
            ? 'bg-white/95 border-emerald-100'
            : 'bg-white/95 border-red-100'
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
              notification.type === "success" ? "Success" : "Attention Required"
            }}
          </p>
          <p class="text-xs text-slate-500 font-medium">
            {{ notification.message }}
          </p>
        </div>
        <button
          @click="closeNotification"
          class="text-slate-300 hover:text-slate-500 p-1"
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
</template>

<script setup>
// Nuxt auto-imports composables, so we just call it!
const { notification, closeNotification } = useNotification();
</script>

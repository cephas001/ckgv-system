<template>
  <main class="p-8">
    <header class="mb-8 border-b border-slate-700 pb-4">
      <h1 class="text-3xl font-bold text-white">McPherson University</h1>
      <p class="text-slate-400">
        Curriculum Knowledge Graph: Computer Science Specializations
      </p>
    </header>

    <div class="grid grid-cols-12 gap-6">
      <section
        class="col-span-12 lg:col-span-9 bg-slate-800 rounded-xl border border-slate-700 shadow-inner h-[700px] relative overflow-hidden"
      >
        <KnowledgeGraph />
      </section>
    </div>
  </main>
</template>

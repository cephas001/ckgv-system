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

      <aside class="col-span-12 lg:col-span-3 space-y-4">
        <div class="bg-slate-800 p-4 rounded-xl border border-slate-700">
          <h2 class="font-bold text-blue-400 mb-2">Legend</h2>
          <ul class="text-sm space-y-2">
            <li class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-blue-500"></span> Core Course
            </li>
            <li class="flex items-center gap-2">
              <span class="w-3 h-3 rounded-full bg-orange-400"></span> Technical
              Skill
            </li>
          </ul>
        </div>
      </aside>
    </div>
  </main>
</template>

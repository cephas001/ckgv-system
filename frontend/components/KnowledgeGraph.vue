<template>
  <div class="w-full h-full relative" ref="containerRef">
    <svg
      ref="svgRef"
      class="w-full h-full cursor-grab active:cursor-grabbing"
    ></svg>

    <div
      v-if="pending"
      class="absolute inset-0 flex items-center justify-center bg-slate-800/90 z-10"
    >
      <span class="text-blue-400 animate-pulse font-semibold text-lg">
        Calculating Bipartite Graph Physics...
      </span>
    </div>

    <div
      v-else-if="error"
      class="absolute inset-0 flex items-center justify-center bg-slate-800/90 z-10"
    >
      <span class="text-red-400 font-semibold text-lg">
        Connection Error. Is the FastAPI server running?
      </span>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, watch } from "vue";
import * as d3 from "d3";

// DOM Refs
const svgRef = ref(null);
const containerRef = ref(null);

// Fetch data from FastAPI
const {
  data: courses,
  pending,
  error,
} = await useFetch("http://127.0.0.1:8000/api/graph");

console.log(courses.value);

// Main D3 Render Function
const renderGraph = () => {
  if (!courses.value || !svgRef.value || !containerRef.value) return;

  // 1. Transform JSON into Nodes and Links
  const nodes = [];
  const links = [];
  const skillSet = new Set();

  courses.value.forEach((course) => {
    nodes.push({ id: course.course_id, group: "course", title: course.title });

    // 1. Add Skill Links
    if (course.technical_skills) {
      course.technical_skills.forEach((skill) => {
        if (!skillSet.has(skill)) {
          skillSet.add(skill);
          nodes.push({ id: skill, group: "skill" });
        }
        links.push({ source: course.course_id, target: skill, type: "skill" });
      });
    }

    // 2. NEW: Add Prerequisite Links
    if (course.prerequisites) {
      course.prerequisites.forEach((pre) => {
        links.push({
          source: pre,
          target: course.course_id,
          type: "prerequisite",
        });
      });
    }
  });

  // 2. Setup SVG and Canvas Dimensions
  const width = containerRef.value.clientWidth || 800;
  const height = containerRef.value.clientHeight || 600;

  const svg = d3.select(svgRef.value).attr("viewBox", [0, 0, width, height]);

  // Clear previous renders (important for hot-reloading)
  svg.selectAll("*").remove();

  const g = svg.append("g"); // Main group for zooming

  // Add Zoom capabilities
  svg.call(
    d3
      .zoom()
      .extent([
        [0, 0],
        [width, height],
      ])
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => g.attr("transform", event.transform)),
  );

  // 3. Configure the Physics Simulation
  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(100),
    )
    .force("charge", d3.forceManyBody().strength(-300)) // Repulsion
    .force("center", d3.forceCenter(width / 2, height / 2)) // Gravity to center
    .force("collide", d3.forceCollide().radius(30)); // Prevent overlapping

  // 4. Draw Links (Lines)
  const link = g
    .append("g")
    .attr("stroke", "#475569") // Slate-600
    .attr("stroke-opacity", 0.6)
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke-width", 1.5);

  // 5. Draw Nodes (Circles)
  const node = g
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", (d) => (d.group === "course" ? 12 : 8)) // Courses are larger
    .attr("fill", (d) => (d.group === "course" ? "#3b82f6" : "#f59e0b")) // Blue for courses, Amber for skills
    .call(drag(simulation)); // Attach drag behavior

  // 6. Add Text Labels
  const labels = g
    .append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.id)
    .attr("font-size", (d) => (d.group === "course" ? "12px" : "10px"))
    .attr("fill", "#e2e8f0") // Slate-200
    .attr("dx", 15)
    .attr("dy", 4);

  // 7. Physics Tick Function (Updates positions every frame)
  simulation.on("tick", () => {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);

    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);

    labels.attr("x", (d) => d.x).attr("y", (d) => d.y);
  });
};

// Drag Behavior Function
const drag = (simulation) => {
  function dragstarted(event) {
    if (!event.active) simulation.alphaTarget(0.3).restart();
    event.subject.fx = event.subject.x;
    event.subject.fy = event.subject.y;
  }
  function dragged(event) {
    event.subject.fx = event.x;
    event.subject.fy = event.y;
  }
  function dragended(event) {
    if (!event.active) simulation.alphaTarget(0);
    event.subject.fx = null;
    event.subject.fy = null;
  }
  return d3
    .drag()
    .on("start", dragstarted)
    .on("drag", dragged)
    .on("end", dragended);
};

// Mount and Watch for data
onMounted(() => {
  if (!pending.value && courses.value) {
    renderGraph();
  }
});

// If data loads slightly after mount, watch for it
watch(courses, (newCourses) => {
  if (newCourses) {
    renderGraph();
  }
});
</script>

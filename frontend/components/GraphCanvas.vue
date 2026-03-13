<template>
  <div class="w-full h-full" ref="containerRef">
    <svg
      ref="svgRef"
      class="w-full h-full cursor-grab active:cursor-grabbing"
    ></svg>
  </div>
</template>

<script setup>
import { ref, watch, onMounted } from "vue";
import * as d3 from "d3";

const props = defineProps({
  courses: Array,
});

const emit = defineEmits(["nodeClicked"]);

const svgRef = ref(null);
const containerRef = ref(null);

const renderGraph = () => {
  if (!props.courses || !svgRef.value || !containerRef.value) return;

  const nodes = [];
  const links = [];
  const skillSet = new Set();

  props.courses.forEach((course) => {
    nodes.push({ id: course.course_id, group: "course", title: course.title });

    if (course.technical_skills) {
      course.technical_skills.forEach((skill) => {
        if (!skillSet.has(skill)) {
          skillSet.add(skill);
          nodes.push({ id: skill, group: "skill" });
        }
        links.push({ source: course.course_id, target: skill, type: "skill" });
      });
    }

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

  const width = containerRef.value.clientWidth || 800;
  const height = containerRef.value.clientHeight || 600;

  const svg = d3.select(svgRef.value).attr("viewBox", [0, 0, width, height]);
  svg.selectAll("*").remove();

  const g = svg.append("g");

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

  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(100),
    )
    .force("charge", d3.forceManyBody().strength(-300))
    .force("center", d3.forceCenter(width / 2, height / 2))
    .force("collide", d3.forceCollide().radius(30));

  const link = g
    .append("g")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", (d) => (d.type === "prerequisite" ? "#3b82f6" : "#475569"))
    .attr("stroke-opacity", 0.5)
    .attr("stroke-width", 1.5)
    .attr("stroke-dasharray", (d) => (d.type === "prerequisite" ? "5,5" : "0"));

  const node = g
    .append("g")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", (d) => (d.group === "course" ? 12 : 8))
    .attr("fill", (d) => (d.group === "course" ? "#3b82f6" : "#f59e0b"))
    .attr("cursor", "pointer")
    .call(drag(simulation));

  const labels = g
    .append("g")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.id)
    .attr("font-size", (d) => (d.group === "course" ? "12px" : "10px"))
    .attr("fill", "#e2e8f0")
    .attr("dx", 15)
    .attr("dy", 4)
    .style("pointer-events", "none");

  // Fire an event up to the parent when clicked
  node.on("click", (event, d) => {
    emit("nodeClicked", d);
  });

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

onMounted(() => renderGraph());

// Re-render if the parent passes new data
watch(
  () => props.courses,
  (newCourses) => {
    if (newCourses) renderGraph();
  },
  { deep: true },
);
</script>

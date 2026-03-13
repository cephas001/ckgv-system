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
  selectedTrack: String,
  showSkills: Boolean,
});

const emit = defineEmits(["nodeClicked"]);

const svgRef = ref(null);
const containerRef = ref(null);
let d3Group = null;

const renderGraph = () => {
  if (!props.courses || !svgRef.value || !containerRef.value) return;

  const nodesMap = new Map();
  const links = [];

  const colorMap = {
    "Core Computer Science": "#3b82f6",
    "Software Engineering": "#10b981",
    Cybersecurity: "#ef4444",
    "Data & Algorithms": "#8b5cf6",
    "Systems & Architecture": "#06b6d4",
    "Artificial Intelligence": "#d946ef",
    default: "#94a3b8",
  };

  props.courses.forEach((course) => {
    nodesMap.set(course.course_id, {
      id: course.course_id,
      group: "course",
      title: course.title,
      specialization: course.specialization,
      tracks: new Set([course.specialization]),
    });
  });

  props.courses.forEach((course) => {
    const spec = course.specialization;

    if (props.showSkills && course.technical_skills) {
      course.technical_skills.forEach((skill) => {
        if (!nodesMap.has(skill)) {
          nodesMap.set(skill, { id: skill, group: "skill", tracks: new Set() });
        }
        nodesMap.get(skill).tracks.add(spec);
        links.push({
          source: course.course_id,
          target: skill,
          type: "skill",
          tracks: new Set([spec]),
        });
      });
    }

    if (course.prerequisites) {
      course.prerequisites.forEach((pre) => {
        if (nodesMap.has(pre)) {
          nodesMap.get(pre).tracks.add(spec);
        }
        links.push({
          source: pre,
          target: course.course_id,
          type: "prerequisite",
          tracks: new Set([spec]),
        });
      });
    }
  });

  const nodes = Array.from(nodesMap.values());
  const width = containerRef.value.clientWidth || 800;
  const height = containerRef.value.clientHeight || 600;

  const svg = d3.select(svgRef.value).attr("viewBox", [0, 0, width, height]);
  svg.selectAll("*").remove();

  d3Group = svg.append("g");

  svg.call(
    d3
      .zoom()
      .extent([
        [0, 0],
        [width, height],
      ])
      .scaleExtent([0.1, 4])
      .on("zoom", (event) => d3Group.attr("transform", event.transform)),
  );

  // 1. MAX EXPANDED PENTAGON: Pushed to 0.48 to use the absolute edges of the screen
  const radius = Math.min(width, height) * 0.48;
  const angleStep = (2 * Math.PI) / 5;

  const clusterCenters = {
    "Core Computer Science": { x: width / 2, y: height / 2 },
    "Software Engineering": {
      x: width / 2 + radius * Math.cos(0),
      y: height / 2 + radius * Math.sin(0),
    },
    Cybersecurity: {
      x: width / 2 + radius * Math.cos(angleStep),
      y: height / 2 + radius * Math.sin(angleStep),
    },
    "Data & Algorithms": {
      x: width / 2 + radius * Math.cos(angleStep * 2),
      y: height / 2 + radius * Math.sin(angleStep * 2),
    },
    "Systems & Architecture": {
      x: width / 2 + radius * Math.cos(angleStep * 3),
      y: height / 2 + radius * Math.sin(angleStep * 3),
    },
    "Artificial Intelligence": {
      x: width / 2 + radius * Math.cos(angleStep * 4),
      y: height / 2 + radius * Math.sin(angleStep * 4),
    },
  };

  // 2. MAX PHYSICS: Longest links, strongest repulsion, largest collision boundaries
  const simulation = d3
    .forceSimulation(nodes)
    .force(
      "link",
      d3
        .forceLink(links)
        .id((d) => d.id)
        .distance(160),
    ) // Pushed to 160
    .force(
      "charge",
      d3.forceManyBody().strength(props.showSkills ? -600 : -1200),
    ) // Massive repulsion
    .force("collide", d3.forceCollide().radius(55)) // Pushed to 55
    .force(
      "x",
      d3
        .forceX((d) =>
          d.group === "course" && clusterCenters[d.specialization]
            ? clusterCenters[d.specialization].x
            : width / 2,
        )
        .strength(0.12),
    )
    .force(
      "y",
      d3
        .forceY((d) =>
          d.group === "course" && clusterCenters[d.specialization]
            ? clusterCenters[d.specialization].y
            : height / 2,
        )
        .strength(0.12),
    );

  const link = d3Group
    .append("g")
    .attr("class", "links-layer")
    .selectAll("line")
    .data(links)
    .join("line")
    .attr("stroke", (d) => (d.type === "prerequisite" ? "#3b82f6" : "#475569"))
    .attr("stroke-opacity", (d) => (d.type === "prerequisite" ? 0.7 : 0.4))
    .attr("stroke-width", 1.5)
    .attr("stroke-dasharray", (d) => (d.type === "prerequisite" ? "5,5" : "0"));

  const node = d3Group
    .append("g")
    .attr("class", "nodes-layer")
    .attr("stroke", "#fff")
    .attr("stroke-width", 1.5)
    .selectAll("circle")
    .data(nodes)
    .join("circle")
    .attr("r", (d) => (d.group === "course" ? 14 : 7))
    .attr("fill", (d) =>
      d.group === "skill"
        ? "#f59e0b"
        : colorMap[d.specialization] || colorMap.default,
    )
    .attr("cursor", "pointer")
    .call(drag(simulation));

  const labels = d3Group
    .append("g")
    .attr("class", "labels-layer")
    .selectAll("text")
    .data(nodes)
    .join("text")
    .text((d) => d.id)
    .attr("font-size", (d) => (d.group === "course" ? "12px" : "10px"))
    .attr("fill", "#e2e8f0")
    .attr("dx", 18)
    .attr("dy", 4)
    .style("pointer-events", "none")
    .style("font-weight", (d) => (d.group === "course" ? "600" : "400"));

  node.on("click", (event, d) => emit("nodeClicked", d));

  simulation.on("tick", () => {
    link
      .attr("x1", (d) => d.source.x)
      .attr("y1", (d) => d.source.y)
      .attr("x2", (d) => d.target.x)
      .attr("y2", (d) => d.target.y);
    node.attr("cx", (d) => d.x).attr("cy", (d) => d.y);
    labels.attr("x", (d) => d.x).attr("y", (d) => d.y);
  });

  applyFilter(props.selectedTrack);
};

const applyFilter = (track) => {
  if (!d3Group) return;
  d3Group
    .selectAll("circle")
    .transition()
    .duration(400)
    .attr("opacity", (d) => (!track || d.tracks.has(track) ? 1 : 0.1));
  d3Group
    .selectAll("text")
    .transition()
    .duration(400)
    .attr("opacity", (d) => (!track || d.tracks.has(track) ? 1 : 0.1));
  d3Group
    .selectAll("line")
    .transition()
    .duration(400)
    .attr("opacity", (d) => (!track || d.tracks.has(track) ? 0.5 : 0.02));
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
watch(
  () => props.courses,
  (newCourses) => {
    if (newCourses) renderGraph();
  },
  { deep: true },
);
watch(
  () => props.selectedTrack,
  (newTrack) => {
    applyFilter(newTrack);
  },
);
watch(
  () => props.showSkills,
  () => {
    renderGraph();
  },
);
</script>

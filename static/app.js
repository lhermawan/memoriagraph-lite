/**
 * app.js — Interactive Graph Visualizer & Cockpit Controller for MemoriaGraph Lite.
 * Integrates Vis-Network physics canvas with REST API backend.
 */

let network = null;
let nodesDataSet = new vis.DataSet([]);
let edgesDataSet = new vis.DataSet([]);
let rawEpisodes = {};
let activeEpisodeId = null;

// DOM Elements
const graphContainer = document.getElementById("graph-container");
const emptyStateOverlay = document.getElementById("empty-state");
const inspectorDrawer = document.getElementById("inspector-drawer");
const drawerCloseBtn = document.getElementById("drawer-close");
const searchInput = document.getElementById("search-input");
const clearSearchBtn = document.getElementById("clear-search");
const nodeCountEl = document.getElementById("node-count");
const edgeCountEl = document.getElementById("edge-count");
const toastEl = document.getElementById("toast");

// Action Buttons
const btnSeed = document.getElementById("btn-seed");
const btnTeach = document.getElementById("btn-teach");
const btnEmptySeed = document.getElementById("btn-empty-seed");
const btnEmptyTeach = document.getElementById("btn-empty-teach");
const btnCopySolution = document.getElementById("btn-copy-solution");
const btnDeleteEpisode = document.getElementById("btn-delete-episode");

// Modal Elements
const modalTeach = document.getElementById("modal-teach");
const modalCloseBtn = document.getElementById("modal-close");
const btnModalCancel = document.getElementById("btn-modal-cancel");
const formTeach = document.getElementById("form-teach");

// Initialize Vis-Network
function initNetwork() {
  const data = {
    nodes: nodesDataSet,
    edges: edgesDataSet,
  };

  const options = {
    nodes: {
      borderWidth: 2,
      shadow: {
        enabled: true,
        color: "rgba(0, 0, 0, 0.6)",
        size: 10,
        x: 0,
        y: 4,
      },
      font: {
        color: "#f8fafc",
        face: "Inter, sans-serif",
        size: 12,
        strokeWidth: 2,
        strokeColor: "#0a0d14",
      },
    },
    edges: {
      color: {
        color: "#334155",
        highlight: "#38bdf8",
        hover: "#38bdf8",
      },
      width: 1.5,
      smooth: {
        type: "continuous",
        roundness: 0.2,
      },
      font: {
        color: "#64748b",
        size: 9,
        face: "Fira Code",
        align: "middle",
        strokeWidth: 2,
        strokeColor: "#0a0d14",
      },
    },
    groups: {
      episode: {
        shape: "dot",
        size: 26,
        color: {
          background: "#6366f1",
          border: "#818cf8",
          highlight: { background: "#4f46e5", border: "#a5b4fc" },
        },
      },
      problem: {
        shape: "dot",
        size: 17,
        color: {
          background: "#f59e0b",
          border: "#fbbf24",
          highlight: { background: "#d97706", border: "#fde68a" },
        },
      },
      mitigation: {
        shape: "dot",
        size: 17,
        color: {
          background: "#06b6d4",
          border: "#38bdf8",
          highlight: { background: "#0891b2", border: "#7dd3fc" },
        },
      },
      solution: {
        shape: "dot",
        size: 19,
        color: {
          background: "#10b981",
          border: "#34d399",
          highlight: { background: "#059669", border: "#6ee7b7" },
        },
      },
      tag: {
        shape: "box",
        margin: 6,
        color: {
          background: "#182234",
          border: "#334155",
          highlight: { background: "#1e293b", border: "#38bdf8" },
        },
        font: {
          color: "#94a3b8",
          face: "Fira Code",
          size: 11,
        },
      },
    },
    physics: {
      forceAtlas2Based: {
        gravitationalConstant: -40,
        centralGravity: 0.015,
        springLength: 85,
        springConstant: 0.08,
        damping: 0.4,
      },
      solver: "forceAtlas2Based",
      stabilization: { iterations: 120 },
    },
    interaction: {
      hover: true,
      tooltipDelay: 150,
      zoomView: true,
      dragView: true,
    },
  };

  network = new vis.Network(graphContainer, data, options);

  // Click Handler
  network.on("click", (params) => {
    if (params.nodes.length > 0) {
      const selectedNodeId = params.nodes[0];
      handleNodeSelect(selectedNodeId);
    } else {
      closeDrawer();
    }
  });
}

// Fetch and load graph data from backend
async function loadGraph() {
  try {
    const res = await fetch("/api/graph");
    const data = await res.json();

    const nodes = data.nodes || [];
    const edges = data.edges || [];

    // Cache episodes
    const episodesRes = await fetch("/api/episodes");
    const episodesList = await episodesRes.json();
    rawEpisodes = {};
    episodesList.forEach((ep) => {
      rawEpisodes[ep.id] = ep;
    });

    // Update Counts
    nodeCountEl.textContent = nodes.length;
    edgeCountEl.textContent = edges.length;

    // Toggle Empty State
    if (nodes.length === 0) {
      emptyStateOverlay.classList.remove("hidden");
    } else {
      emptyStateOverlay.classList.add("hidden");
    }

    // Refresh DataSets
    nodesDataSet.clear();
    edgesDataSet.clear();
    nodesDataSet.add(nodes);
    edgesDataSet.add(edges);

    if (network) {
      network.fit();
    }
  } catch (err) {
    showToast("Failed to load graph data from backend", "error");
    console.error(err);
  }
}

// Handle Node Selection & Inspection
function handleNodeSelect(nodeId) {
  const node = nodesDataSet.get(nodeId);
  if (!node) return;

  let ep = null;
  if (node.episode_id && rawEpisodes[node.episode_id]) {
    ep = rawEpisodes[node.episode_id];
  } else if (rawEpisodes[nodeId]) {
    ep = rawEpisodes[nodeId];
  }

  if (ep) {
    openDrawer(ep, node.group);
  }
}

// Open Right Drawer
function openDrawer(ep, groupType = "episode") {
  activeEpisodeId = ep.id;
  document.getElementById("drawer-node-type").textContent = groupType.toUpperCase();
  document.getElementById("drawer-title").textContent = ep.title;
  document.getElementById("drawer-id").textContent = ep.id;
  document.getElementById("drawer-date").textContent = new Date(ep.created_at).toLocaleString();
  document.getElementById("drawer-problem").textContent = ep.problem;
  document.getElementById("drawer-mitigation").textContent = ep.mitigation;
  document.getElementById("drawer-solution").textContent = ep.solution;

  // Render Tags
  const tagsContainer = document.getElementById("drawer-tags");
  tagsContainer.innerHTML = "";
  if (ep.tags) {
    ep.tags.split(",").forEach((t) => {
      const trimmed = t.trim();
      if (trimmed) {
        const chip = document.createElement("span");
        chip.className = "tag-chip";
        chip.textContent = `#${trimmed}`;
        tagsContainer.appendChild(chip);
      }
    });
  } else {
    tagsContainer.innerHTML = "<span class='meta-value'>No tags</span>";
  }

  inspectorDrawer.classList.remove("collapsed");
}

// Close Right Drawer
function closeDrawer() {
  inspectorDrawer.classList.add("collapsed");
  activeEpisodeId = null;
}

// Seed generic sample cases
async function seedSampleCases() {
  try {
    const res = await fetch("/api/seed", { method: "POST" });
    const data = await res.json();
    showToast(data.message || "Loaded 3 sample cases");
    await loadGraph();
  } catch (err) {
    showToast("Failed to seed sample cases", "error");
    console.error(err);
  }
}

// Filter and Search Graph
function filterGraph(query) {
  if (!query || !query.trim()) {
    clearSearchBtn.style.display = "none";
    nodesDataSet.forEach((node) => {
      nodesDataSet.update({ id: node.id, opacity: 1, hidden: false });
    });
    edgesDataSet.forEach((edge) => {
      edgesDataSet.update({ id: edge.id, hidden: false });
    });
    return;
  }

  clearSearchBtn.style.display = "block";
  const lowerQ = query.trim().toLowerCase();
  const matchedNodeIds = new Set();

  nodesDataSet.forEach((node) => {
    let match = false;
    const label = (node.label || "").toLowerCase();
    const title = (node.title || "").toLowerCase();

    if (label.includes(lowerQ) || title.includes(lowerQ)) {
      match = true;
    }

    if (node.episode_id && rawEpisodes[node.episode_id]) {
      const ep = rawEpisodes[node.episode_id];
      if (
        ep.title.toLowerCase().includes(lowerQ) ||
        ep.problem.toLowerCase().includes(lowerQ) ||
        ep.mitigation.toLowerCase().includes(lowerQ) ||
        ep.solution.toLowerCase().includes(lowerQ) ||
        ep.tags.toLowerCase().includes(lowerQ)
      ) {
        match = true;
      }
    }

    if (match) {
      matchedNodeIds.add(node.id);
      nodesDataSet.update({ id: node.id, opacity: 1, hidden: false });
    } else {
      nodesDataSet.update({ id: node.id, opacity: 0.15, hidden: false });
    }
  });

  if (matchedNodeIds.size > 0 && network) {
    network.fit({
      nodes: Array.from(matchedNodeIds),
      animation: { duration: 600, easingFunction: "easeInOutQuad" },
    });
  }
}

// Show Toast Alert
function showToast(message, type = "success") {
  toastEl.textContent = message;
  toastEl.className = `toast ${type}`;
  toastEl.classList.remove("hidden");
  setTimeout(() => {
    toastEl.classList.add("hidden");
  }, 3200);
}

// Copy Solution to Clipboard
btnCopySolution.addEventListener("click", () => {
  const solutionText = document.getElementById("drawer-solution").textContent;
  if (solutionText && solutionText !== "-") {
    navigator.clipboard.writeText(solutionText);
    showToast("Solution copied to clipboard!");
  }
});

// Delete Episode
btnDeleteEpisode.addEventListener("click", async () => {
  if (!activeEpisodeId) return;
  if (!confirm("Are you sure you want to delete this memory episode?")) return;

  try {
    const res = await fetch(`/api/episodes/${activeEpisodeId}`, { method: "DELETE" });
    if (res.ok) {
      showToast("Memory episode deleted");
      closeDrawer();
      await loadGraph();
    } else {
      showToast("Failed to delete memory", "error");
    }
  } catch (err) {
    console.error(err);
  }
});

// Modal Handlers
function openTeachModal() {
  modalTeach.classList.remove("hidden");
  document.getElementById("input-title").focus();
}

function closeTeachModal() {
  modalTeach.classList.add("hidden");
  formTeach.reset();
}

btnTeach.addEventListener("click", openTeachModal);
btnEmptyTeach.addEventListener("click", openTeachModal);
modalCloseBtn.addEventListener("click", closeTeachModal);
btnModalCancel.addEventListener("click", closeTeachModal);

// Teach Form Submission
formTeach.addEventListener("submit", async (e) => {
  e.preventDefault();
  const payload = {
    title: document.getElementById("input-title").value,
    problem: document.getElementById("input-problem").value,
    mitigation: document.getElementById("input-mitigation").value,
    solution: document.getElementById("input-solution").value,
    tags: document.getElementById("input-tags").value,
  };

  try {
    const res = await fetch("/api/episodes", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(payload),
    });

    if (res.ok) {
      const data = await res.json();
      showToast("Memory episode recorded into Second Brain!");
      closeTeachModal();
      await loadGraph();
      if (data.episode) {
        openDrawer(data.episode);
      }
    } else {
      showToast("Failed to save memory episode", "error");
    }
  } catch (err) {
    console.error(err);
    showToast("Error connecting to server", "error");
  }
});

// Seed Button Listeners
btnSeed.addEventListener("click", seedSampleCases);
btnEmptySeed.addEventListener("click", seedSampleCases);

// Search Listeners
searchInput.addEventListener("input", (e) => filterGraph(e.target.value));
clearSearchBtn.addEventListener("click", () => {
  searchInput.value = "";
  filterGraph("");
});

drawerCloseBtn.addEventListener("click", closeDrawer);

// Window Load Initialization
window.addEventListener("DOMContentLoaded", () => {
  initNetwork();
  loadGraph();
});

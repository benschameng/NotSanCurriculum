diff --git a/site/app.js b/site/app.js
new file mode 100644
index 0000000000000000000000000000000000000000..c4113acae2c28ee753b34cf99d84610f1c646bf8
--- /dev/null
+++ b/site/app.js
@@ -0,0 +1,133 @@
+const lernfeldList = document.getElementById("lernfeldList");
+const content = document.getElementById("content");
+const searchInput = document.getElementById("search");
+const generatedAtEl = document.getElementById("generatedAt");
+
+async function loadManifest() {
+  const response = await fetch("manifest.json");
+  if (!response.ok) {
+    throw new Error("manifest.json konnte nicht geladen werden.");
+  }
+  return response.json();
+}
+
+function renderLernfelder(manifest) {
+  lernfeldList.innerHTML = "";
+  generatedAtEl.textContent = new Date(manifest.generatedAt).toLocaleString("de-DE");
+
+  const lfTemplate = document.getElementById("lf-template");
+  const lsTemplate = document.getElementById("ls-template");
+
+  manifest.lernfelder.forEach((lf) => {
+    const lfNode = lfTemplate.content.cloneNode(true);
+    const lfButton = lfNode.querySelector(".lf-title");
+    lfButton.textContent = `${lf.id} – ${lf.title}`;
+    const lsList = lfNode.querySelector(".ls-list");
+
+    lf.situationen.forEach((ls) => {
+      const lsNode = lsTemplate.content.cloneNode(true);
+      const lsButton = lsNode.querySelector(".ls-title");
+      lsButton.textContent = `${ls.id}: ${ls.title}`;
+      lsButton.addEventListener("click", () => renderLernsituation(ls, lf));
+      lsList.appendChild(lsNode);
+    });
+
+    lfButton.addEventListener("click", () => {
+      const expanded = lfButton.getAttribute("aria-expanded") === "true";
+      lfButton.setAttribute("aria-expanded", !expanded);
+      lsList.style.display = expanded ? "none" : "block";
+    });
+
+    lernfeldList.appendChild(lfNode);
+  });
+}
+
+function renderLernsituation(ls, lf) {
+  const card = document.createElement("div");
+  card.className = "card";
+
+  const header = document.createElement("div");
+  header.innerHTML = `
+    <p class="badge">${lf.id} · ${lf.title}</p>
+    <h2>${ls.title}</h2>
+  `;
+  card.appendChild(header);
+
+  if (ls.meta) {
+    const metaWrap = document.createElement("div");
+    metaWrap.className = "meta-chips";
+
+    [
+      ["⏱", ls.meta.hours],
+      ["🎓", ls.meta.year],
+      ["📋", ls.meta.aprv],
+    ].forEach(([icon, value]) => {
+      if (!value) return;
+      const chip = document.createElement("span");
+      chip.className = "chip";
+      chip.innerHTML = `<span class="dot"></span>${icon} ${value}`;
+      metaWrap.appendChild(chip);
+    });
+
+    if (Array.isArray(ls.meta.tags)) {
+      ls.meta.tags.forEach((tag) => {
+        const chip = document.createElement("span");
+        chip.className = "chip tag";
+        chip.textContent = tag;
+        metaWrap.appendChild(chip);
+      });
+    }
+
+    card.appendChild(metaWrap);
+  }
+
+  if (ls.overview) {
+    const overview = document.createElement("p");
+    overview.id = "overview";
+    overview.textContent = ls.overview;
+    card.appendChild(overview);
+  }
+
+  const sectionGrid = document.createElement("div");
+  sectionGrid.className = "section-grid";
+
+  if (ls.sections && ls.sections.length) {
+    ls.sections.forEach((section) => {
+      const sectionEl = document.createElement("div");
+      sectionEl.className = "section";
+      sectionEl.innerHTML = `<h3>${section.title}</h3>${section.html || "<p>Keine Inhalte hinterlegt.</p>"}`;
+      sectionGrid.appendChild(sectionEl);
+    });
+  }
+
+  card.appendChild(sectionGrid);
+
+  const source = document.createElement("p");
+  source.className = "meta";
+  source.innerHTML = `Quelle: <a href="${ls.source}" target="_blank" rel="noopener noreferrer">${ls.source}</a>`;
+  card.appendChild(source);
+
+  content.innerHTML = "";
+  content.appendChild(card);
+  content.scrollTop = 0;
+}
+
+function setupSearch(manifest) {
+  searchInput.addEventListener("input", (event) => {
+    const query = event.target.value.toLowerCase();
+    lernfeldList.querySelectorAll(".ls-title").forEach((button) => {
+      const match = button.textContent.toLowerCase().includes(query);
+      const item = button.closest(".ls");
+      item.style.display = match ? "block" : "none";
+    });
+  });
+}
+
+loadManifest()
+  .then((manifest) => {
+    renderLernfelder(manifest);
+    setupSearch(manifest);
+  })
+  .catch((error) => {
+    content.innerHTML = `<div class="card"><h2>Fehler</h2><p>${error.message}</p></div>`;
+  });

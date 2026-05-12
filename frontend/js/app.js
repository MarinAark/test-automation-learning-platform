/**
 * 测试开发学习平台 — 前端 SPA
 * 通过 API 与服务端交互，实现模块化学习、进度追踪
 */
const API = "/api";
const USER_ID = "learner-" + (localStorage.getItem("learner_id") || (() => {
  const id = Math.random().toString(36).slice(2, 10);
  localStorage.setItem("learner_id", id);
  return id;
})());

// ==================== State ====================
let chapters = [];
let currentModuleId = null;
let completedSet = new Set();
let totalModules = 0;

// ==================== Init ====================
async function init() {
  initTheme();
  await Promise.all([loadChapters(), loadProgress()]);
  renderSidebar();
  // 默认加载第一个模块
  if (chapters.length > 0 && chapters[0].modules.length > 0) {
    loadModule(chapters[0].modules[0].id);
  }
}

// ==================== Theme ====================
function initTheme() {
  const saved = localStorage.getItem("theme");
  const theme = saved || (window.matchMedia("(prefers-color-scheme: light)").matches ? "light" : "dark");
  document.documentElement.setAttribute("data-theme", theme);
  updateThemeIcon(theme);
}

function toggleTheme() {
  const current = document.documentElement.getAttribute("data-theme");
  const next = current === "light" ? "dark" : "light";
  document.documentElement.setAttribute("data-theme", next);
  localStorage.setItem("theme", next);
  updateThemeIcon(next);
}

function updateThemeIcon(theme) {
  const btn = document.getElementById("themeToggle");
  if (btn) btn.textContent = theme === "light" ? "☀️" : "🌙";
}

// ==================== API ====================
async function loadChapters() {
  try {
    const res = await fetch(`${API}/modules/chapters`);
    const data = await res.json();
    chapters = data.chapters;
    totalModules = chapters.reduce((s, c) => s + c.modules.length, 0);
  } catch (e) {
    console.error("加载目录失败:", e);
  }
}

async function loadProgress() {
  try {
    const res = await fetch(`${API}/progress/${USER_ID}`);
    const data = await res.json();
    completedSet = new Set(data.completed_modules);
    updateProgressBar(data.percentage);
    updateSidebarDone();
  } catch (e) {
    console.error("加载进度失败:", e);
  }
}

async function toggleComplete() {
  if (!currentModuleId) return;
  const completed = !completedSet.has(currentModuleId);
  try {
    await fetch(`${API}/progress/${USER_ID}`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ module_id: currentModuleId, completed }),
    });
    if (completed) completedSet.add(currentModuleId);
    else completedSet.delete(currentModuleId);
    updateCompleteButton();
    updateSidebarDone();
    updateProgressBar(completedSet.size / totalModules * 100);
    showToast(completed ? "✅ 已标记完成" : "↩ 已取消标记");
  } catch (e) {
    console.error("更新进度失败:", e);
  }
}

// ==================== Sidebar ====================
function renderSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = `
    <div class="srch"><input type="text" id="searchInput" placeholder="🔍 搜索知识点..." oninput="handleSearch(this.value)"></div>
    ${chapters.map(ch => `
      <div class="mod-group" data-chapter="${ch.id}">
        <div class="mod-header open" onclick="toggleMod(this)">
          <span class="icon">${ch.icon}</span>${ch.title}
          <span class="arrow">▶</span>
        </div>
        <div class="mod-body open">
          ${ch.modules.map(m => `
            <a href="#" data-module="${m.id}" onclick="loadModule('${m.id}');return false;"
               class="${completedSet.has(m.id) ? 'done' : ''}">
              ${m.title}
            </a>`).join("")}
        </div>
      </div>`).join("")}
  `;
}

function updateSidebarDone() {
  document.querySelectorAll(".mod-body a").forEach(a => {
    const mid = a.dataset.module;
    if (completedSet.has(mid)) a.classList.add("done");
    else a.classList.remove("done");
  });
}

function toggleMod(header) {
  header.classList.toggle("open");
  header.nextElementSibling.classList.toggle("open");
}

function handleSearch(q) {
  const kw = q.toLowerCase();
  document.querySelectorAll(".mod-body a").forEach(a => {
    const match = !kw || a.textContent.toLowerCase().includes(kw);
    a.style.display = match ? "" : "none";
  });
  if (kw) {
    document.querySelectorAll(".mod-header").forEach(h => {
      h.classList.add("open");
      h.nextElementSibling?.classList.add("open");
    });
  }
}

// ==================== Content Loading ====================
async function loadModule(moduleId) {
  currentModuleId = moduleId;
  updateBreadcrumb(moduleId);
  const content = document.getElementById("content");
  content.innerHTML = '<div class="loading"><div class="spinner"></div><p>加载中...</p></div>';

  // Sidebar active
  document.querySelectorAll(".mod-body a").forEach(a => a.classList.remove("active"));
  const link = document.querySelector(`[data-module="${moduleId}"]`);
  if (link) link.classList.add("active");

  try {
    const res = await fetch(`${API}/modules/${moduleId}`);
    if (!res.ok) throw new Error("模块不存在");
    const m = await res.json();

    let html = `<div class="sec"><h2>${m.title}</h2></div>`;

    // 依赖行
    if (m.prerequisites.length > 0 || m.leads_to.length > 0) {
      html += '<div class="dep-row"><span class="dep-label">📌 依赖关系：</span>';
      m.prerequisites.forEach(p => {
        const mod = findModuleById(p);
        html += `<span class="dep-tag pre" onclick="loadModule('${p}')">前置：${mod ? mod.title : p}</span>`;
      });
      m.leads_to.forEach(l => {
        const mod = findModuleById(l);
        html += `<span class="dep-tag lead" onclick="loadModule('${l}')">进阶：${mod ? mod.title : l} →</span>`;
      });
      html += '</div>';
    }

    // 标签
    if (m.tags.length > 0) {
      html += '<div style="margin-bottom:12px;">';
      m.tags.forEach(t => {
        html += `<span class="badge b-blue" style="margin-right:6px;">${t}</span>`;
      });
      html += '</div>';
    }

    // 模块内容
    html += m.content_html;

    // 资源链接
    if (m.resources && m.resources.length > 0) {
      html += '<div class="res-section"><h4>📺 视频与资源</h4><div class="res-list">';
      m.resources.forEach(r => {
        const icon = r.type === 'video' ? '<svg viewBox="0 0 24 24" fill="currentColor"><path d="M8 5v14l11-7z"/></svg>' :
                     r.type === 'article' ? '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M4 19.5A2.5 2.5 0 0 1 6.5 17H20"/><path d="M6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5v-15A2.5 2.5 0 0 1 6.5 2z"/></svg>' :
                     '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><circle cx="12" cy="12" r="10"/><line x1="2" y1="12" x2="22" y2="12"/><path d="M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>';
        html += `<a class="res-link" href="${r.url}" target="_blank" rel="noopener">${icon} ${r.title}</a>`;
      });
      html += '</div></div>';
    }

    // 完成按钮
    html += `<button class="complete-btn ${completedSet.has(moduleId) ? 'completed' : ''}"
                    id="completeBtn" onclick="toggleComplete()">
             ${completedSet.has(moduleId) ? '✅ 已完成' : '☐ 标记完成'}
             </button>`;

    content.innerHTML = html;
    addCopyButtons();
  } catch (e) {
    content.innerHTML = `<div class="loading"><p>加载失败: ${e.message}</p></div>`;
  }
}

function findModuleById(id) {
  for (const ch of chapters) {
    for (const m of ch.modules) {
      if (m.id === id) return m;
    }
  }
  return null;
}

function findChapterByModuleId(id) {
  for (const ch of chapters) {
    for (const m of ch.modules) {
      if (m.id === id) return ch;
    }
  }
  return null;
}

function updateBreadcrumb(moduleId) {
  const ch = findChapterByModuleId(moduleId);
  const m = findModuleById(moduleId);
  const bc = document.getElementById("breadcrumb");
  if (ch && m) bc.textContent = `${ch.title} / ${m.title}`;
  else if (m) bc.textContent = m.title;
}

function updateCompleteButton() {
  const btn = document.getElementById("completeBtn");
  if (!btn) return;
  if (completedSet.has(currentModuleId)) {
    btn.classList.add("completed");
    btn.textContent = "✅ 已完成";
  } else {
    btn.classList.remove("completed");
    btn.textContent = "☐ 标记完成";
  }
}

function updateProgressBar(pct) {
  document.getElementById("progressFill").style.width = pct + "%";
  document.getElementById("progressText").textContent = Math.round(pct) + "%";
}

// ==================== Copy Buttons ====================
function addCopyButtons() {
  document.querySelectorAll(".cw").forEach(wrap => {
    if (wrap.querySelector(".copy-btn")) return;
    const btn = document.createElement("button");
    btn.className = "copy-btn";
    btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>复制';
    btn.addEventListener("click", () => {
      const code = wrap.querySelector("pre code") || wrap.querySelector("pre");
      navigator.clipboard.writeText(code ? code.innerText : "").then(() => {
        btn.classList.add("copied");
        btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg>已复制';
        setTimeout(() => {
          btn.classList.remove("copied");
          btn.innerHTML = '<svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg>复制';
        }, 2000);
      });
    });
    wrap.appendChild(btn);
  });
}

// ==================== Toast ====================
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2000);
}

// ==================== Boot ====================
document.addEventListener("DOMContentLoaded", init);

/**
 * AI测试-自动化进阶项目 — 前端 SPA
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
let bookmarkSet = new Set(JSON.parse(localStorage.getItem("bookmarks") || "[]"));
let totalModules = 0;
let searchTimeout = null;

// ==================== Init ====================
async function init() {
  initTheme();
  updateBookmarkIcon();
  await Promise.all([loadChapters(), loadProgress()]);
  renderSidebar();
  if (localStorage.getItem("sidebar_collapsed") === "true") {
    document.getElementById("sidebar")?.classList.add("collapsed");
  }
  if (chapters.length > 0 && chapters[0].modules.length > 0) {
    loadModule(chapters[0].modules[0].id);
  }
}

// ==================== Sidebar Toggle ====================
function toggleSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.classList.toggle("collapsed");
  localStorage.setItem("sidebar_collapsed", sidebar.classList.contains("collapsed"));
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
  // Re-render Mermaid with new theme if present
  if (typeof mermaid !== "undefined" && document.querySelector(".mermaid-wrap")) {
    renderMermaid();
  }
}

function updateThemeIcon(theme) {
  const btn = document.getElementById("themeToggle");
  if (btn) btn.textContent = theme === "light" ? "☀️" : "🌙";
}

// ==================== Bookmark ====================
function toggleBookmark() {
  if (!currentModuleId) return;
  const btn = document.getElementById("bookmarkBtn");
  if (bookmarkSet.has(currentModuleId)) {
    bookmarkSet.delete(currentModuleId);
    btn.classList.remove("bookmarked");
    btn.textContent = "☆";
    showToast("已取消收藏");
  } else {
    bookmarkSet.add(currentModuleId);
    btn.classList.add("bookmarked");
    btn.textContent = "★";
    showToast("★ 已收藏 — " + (findModuleById(currentModuleId)?.title || ""));
  }
  localStorage.setItem("bookmarks", JSON.stringify([...bookmarkSet]));
}

function updateBookmarkIcon() {
  const btn = document.getElementById("bookmarkBtn");
  if (!btn || !currentModuleId) return;
  if (bookmarkSet.has(currentModuleId)) {
    btn.classList.add("bookmarked");
    btn.textContent = "★";
  } else {
    btn.classList.remove("bookmarked");
    btn.textContent = "☆";
  }
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
    if (completed) {
      completedSet.add(currentModuleId);
      // Progress bar flow animation
      const pb = document.getElementById("progressBarWrap");
      if (pb) {
        pb.classList.add("flowing");
        setTimeout(() => pb.classList.remove("flowing"), 800);
      }
    } else {
      completedSet.delete(currentModuleId);
    }
    updateCompleteButton();
    updateSidebarDone();
    updateProgressBar(completedSet.size / totalModules * 100);

    // Complete button pop animation
    if (completed) {
      const btn = document.getElementById("completeBtn");
      if (btn) {
        btn.classList.add("just-completed");
        setTimeout(() => btn.classList.remove("just-completed"), 400);
      }
    }

    showToast(completed ? "✅ 已标记完成" : "↩ 已取消标记");
  } catch (e) {
    console.error("更新进度失败:", e);
  }
}

// ==================== Sidebar ====================
function renderSidebar() {
  const sidebar = document.getElementById("sidebar");
  sidebar.innerHTML = `
    <div class="srch">
      <input type="text" id="searchInput" placeholder="🔍 搜索知识点..."
             oninput="handleSearch(this.value)" onfocus="handleSearch(this.value)" autocomplete="off">
      <span class="kbd-hint">Ctrl+K</span>
      <div class="search-dropdown" id="searchDropdown"></div>
    </div>
    ${chapters.map(ch => `
      <div class="mod-group" data-chapter="${ch.id}">
        <div class="mod-header open" onclick="toggleMod(this)">
          <span class="icon">${ch.icon}</span>${ch.title}
          <span class="arrow">▶</span>
        </div>
        <div class="mod-body open">
          ${ch.modules.map(m => `
            <a href="#" data-module="${m.id}" onclick="loadModule('${m.id}');return false;"
               class="${completedSet.has(m.id) ? 'done' : ''} ${bookmarkSet.has(m.id) ? 'bookmarked-link' : ''}">
              ${bookmarkSet.has(m.id) ? '★ ' : ''}${m.title}
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

async function handleSearch(q) {
  const kw = q.trim();
  const dropdown = document.getElementById("searchDropdown");

  // Local filter for sidebar
  document.querySelectorAll(".mod-body a").forEach(a => {
    const match = !kw || a.textContent.replace('★ ','').toLowerCase().includes(kw.toLowerCase());
    a.style.display = match ? "" : "none";
  });
  if (kw) {
    document.querySelectorAll(".mod-header").forEach(h => {
      h.classList.add("open");
      h.nextElementSibling?.classList.add("open");
    });
  }

  // API search for content-level results
  if (kw.length < 2) { dropdown.classList.remove("show"); return; }
  clearTimeout(searchTimeout);
  searchTimeout = setTimeout(async () => {
    try {
      const res = await fetch(`${API}/modules/?q=${encodeURIComponent(kw)}`);
      const data = await res.json();
      if (data.modules && data.modules.length > 0) {
        dropdown.innerHTML = data.modules.map(m => `
          <a href="#" class="s-item" onclick="loadModule('${m.id}');dropdown.classList.remove('show');return false;">
            ${m.title} <span class="s-chapter">${m.chapter}</span>
          </a>`).join("");
        dropdown.classList.add("show");
      } else {
        dropdown.innerHTML = '<div class="s-item" style="color:var(--text2);">无匹配结果</div>';
        dropdown.classList.add("show");
      }
    } catch(e) { /* ignore */ }
  }, 300);
}

// Hide dropdown on outside click
document.addEventListener("click", (e) => {
  const dd = document.getElementById("searchDropdown");
  const srch = document.getElementById("searchInput");
  if (dd && srch && !srch.contains(e.target) && !dd.contains(e.target)) {
    dd.classList.remove("show");
  }
});

// ==================== Flat Module List ====================
function buildFlatModuleList() {
  const flat = [];
  for (const ch of chapters) {
    for (const m of ch.modules) {
      flat.push(m);
    }
  }
  return flat;
}

// ==================== Content Loading ====================
async function loadModule(moduleId) {
  currentModuleId = moduleId;
  updateBreadcrumb(moduleId);
  updateBookmarkIcon();
  const main = document.getElementById("contentMain");
  main.innerHTML = '<div class="loading"><div class="spinner"></div><p>加载中...</p></div>';
  document.getElementById("tocSidebar").style.display = "none";

  // Sidebar active
  document.querySelectorAll(".mod-body a").forEach(a => a.classList.remove("active"));
  const link = document.querySelector(`[data-module="${moduleId}"]`);
  if (link) {
    link.classList.add("active");
    link.scrollIntoView?.({ block: "nearest" });
  }

  try {
    const res = await fetch(`${API}/modules/${moduleId}`);
    if (!res.ok) throw new Error("模块不存在");
    const m = await res.json();

    let html = `<div class="sec"><h2>${m.title}</h2></div>`;

    // 依赖行
    if (m.prerequisites.length > 0 || m.leads_to.length > 0 || m.tags.length > 0) {
      html += '<div class="dep-row">';
      if (m.prerequisites.length > 0) {
        html += '<span class="dep-label">前置：</span>';
        m.prerequisites.forEach(p => {
          const mod = findModuleById(p);
          html += `<span class="dep-tag pre" onclick="loadModule('${p}')">${mod ? mod.title : p}</span>`;
        });
      }
      if (m.leads_to.length > 0) {
        html += '<span class="dep-label" style="margin-left:4px;">进阶：</span>';
        m.leads_to.forEach(l => {
          const mod = findModuleById(l);
          html += `<span class="dep-tag lead" onclick="loadModule('${l}')">${mod ? mod.title : l} →</span>`;
        });
      }
      if (m.tags.length > 0) {
        m.tags.forEach(t => {
          html += `<span class="badge b-blue" style="margin-left:4px;cursor:pointer;" onclick="document.getElementById('searchInput').value='${t}';handleSearch('${t}');">${t}</span>`;
        });
      }
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

    main.innerHTML = html;
    addCopyButtons();
    addCodeFolding();
    injectLineNumbers();
    renderMermaid();
    buildTOC();
    updatePrevNext();
    refreshNotesUI();
  } catch (e) {
    main.innerHTML = `<div class="loading"><p>加载失败: ${e.message}</p></div>`;
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
  if (!ch || !m) {
    bc.innerHTML = `<a href="#" onclick="loadModule('roadmap');return false;">首页</a>`;
    return;
  }
  bc.innerHTML = `<a href="#" onclick="loadModule('roadmap');return false;">首页</a>`
    + `<span class="bc-sep">/</span>`
    + `<a href="#" onclick="loadModule('${ch.modules[0].id}');return false;">${ch.title}</a>`
    + `<span class="bc-sep">/</span>`
    + `<span>${m.title}</span>`;
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

// ==================== Prev / Next Navigation ====================
function navigatePrev() {
  const flat = buildFlatModuleList();
  const idx = flat.findIndex(m => m.id === currentModuleId);
  if (idx > 0) loadModule(flat[idx - 1].id);
}

function navigateNext() {
  const flat = buildFlatModuleList();
  const idx = flat.findIndex(m => m.id === currentModuleId);
  if (idx < flat.length - 1) loadModule(flat[idx + 1].id);
}

function updatePrevNext() {
  const nav = document.getElementById("prevNextNav");
  if (!currentModuleId) { nav.style.display = "none"; return; }
  const flat = buildFlatModuleList();
  const idx = flat.findIndex(m => m.id === currentModuleId);
  if (idx === -1) { nav.style.display = "none"; return; }

  document.getElementById("pnPrev").style.visibility = idx > 0 ? "visible" : "hidden";
  document.getElementById("pnNext").style.visibility = idx < flat.length - 1 ? "visible" : "hidden";
  nav.style.display = "";
}

// ==================== TOC ====================
function buildTOC() {
  const toc = document.getElementById("tocSidebar");
  const main = document.getElementById("contentMain");
  const headings = main.querySelectorAll("h3");
  if (headings.length < 2) { toc.style.display = "none"; return; }

  let html = '<div class="toc-title">📑 目录</div>';
  headings.forEach((h, i) => {
    const id = h.id || ("toc-" + i);
    h.id = id;
    html += `<a href="#${id}" onclick="highlightTOC(this);return true;">${h.textContent}</a>`;
  });
  toc.innerHTML = html;
  toc.style.display = "";

  // Highlight on scroll
  const links = toc.querySelectorAll("a");
  const observer = new IntersectionObserver(entries => {
    entries.forEach(e => {
      if (e.isIntersecting) {
        links.forEach(l => l.classList.remove("active"));
        const match = toc.querySelector(`a[href="#${e.target.id}"]`);
        if (match) match.classList.add("active");
      }
    });
  }, { rootMargin: "-60px 0px -70% 0px" });
  headings.forEach(h => observer.observe(h));
}

function highlightTOC(link) {
  document.querySelectorAll(".toc-sidebar a").forEach(a => a.classList.remove("active"));
  link.classList.add("active");
}

// ==================== Copy Buttons + Fullscreen ====================
function addCopyButtons() {
  document.querySelectorAll(".cw").forEach(wrap => {
    // Copy button
    if (!wrap.querySelector(".copy-btn")) {
      const btn = document.createElement("button");
      btn.className = "copy-btn";
      btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> 复制代码';
      btn.addEventListener("click", (e) => {
        e.stopPropagation();
        const code = wrap.querySelector("pre code") || wrap.querySelector("pre");
        navigator.clipboard.writeText(code ? code.innerText : "").then(() => {
          btn.classList.add("copied");
          btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><polyline points="20 6 9 17 4 12"/></svg> 已复制';
          setTimeout(() => {
            btn.classList.remove("copied");
            btn.innerHTML = '<svg width="15" height="15" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><rect x="9" y="9" width="13" height="13" rx="2"/><path d="M5 15H4a2 2 0 0 1-2-2V4a2 2 0 0 1 2-2h9a2 2 0 0 1 2 2v1"/></svg> 复制代码';
          }, 2000);
        });
      });
      wrap.appendChild(btn);
    }

    // Fullscreen button in cbar
    const cbar = wrap.querySelector(".cbar");
    if (cbar && !cbar.querySelector(".fullscreen-btn")) {
      const fsBtn = document.createElement("button");
      fsBtn.className = "fullscreen-btn";
      fsBtn.innerHTML = '⛶';
      fsBtn.title = "全屏查看";
      fsBtn.addEventListener("click", (e) => {
        e.stopPropagation();
        const code = wrap.querySelector("pre code") || wrap.querySelector("pre");
        const fname = wrap.querySelector(".fname")?.textContent || "";
        openFullscreenCode(code ? code.textContent : "", fname);
      });
      cbar.appendChild(fsBtn);
    }
  });
}

// ==================== Code Folding ====================
function addCodeFolding() {
  document.querySelectorAll(".cw").forEach(wrap => {
    if (wrap.querySelector(".code-fold")) return;
    const pre = wrap.querySelector("pre");
    if (!pre) return;
    const lines = pre.textContent.split("\n").length;
    if (lines < 20) return;

    wrap.classList.add("folded");
    const fold = document.createElement("div");
    fold.className = "code-fold";
    fold.innerHTML = `<span>展开全部 (${lines} 行) ▼</span>`;
    fold.addEventListener("click", () => {
      if (wrap.classList.contains("folded")) {
        wrap.classList.remove("folded");
        fold.innerHTML = `<span>收起 ▲</span>`;
      } else {
        wrap.classList.add("folded");
        fold.innerHTML = `<span>展开全部 (${lines} 行) ▼</span>`;
      }
    });
    wrap.appendChild(fold);
  });
}

// ==================== Line Numbers ====================
function injectLineNumbers() {
  document.querySelectorAll(".cw").forEach(wrap => {
    wrap.classList.add("ln");
    const code = wrap.querySelector("pre code");
    if (!code || code.querySelector("span")) return;
    const text = code.textContent || "";
    let lines = text.split("\n");
    // Strip leading/trailing empty lines
    while (lines.length && lines[0].trim() === "") lines.shift();
    while (lines.length && lines[lines.length - 1].trim() === "") lines.pop();
    code.innerHTML = lines.map(line => `<span>${escapeHTML(line)}</span>`).join("\n");
  });
}

function escapeHTML(str) {
  return str.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
}

// ==================== Mermaid Diagrams ====================
async function renderMermaid() {
  const charts = document.querySelectorAll(".mermaid, pre code.language-mermaid");
  if (!charts.length) return;
  if (typeof mermaid === "undefined") return;

  const theme = document.documentElement.getAttribute("data-theme") === "light" ? "neutral" : "dark";
  mermaid.initialize({ startOnLoad: false, theme, securityLevel: "loose" });

  for (const el of charts) {
    try {
      const code = el.textContent.trim();
      const id = "mermaid-" + Math.random().toString(36).slice(2, 8);
      const { svg } = await mermaid.render(id, code);
      const wrap = document.createElement("div");
      wrap.className = "mermaid-wrap";
      wrap.innerHTML = svg;
      el.parentElement?.replaceWith?.(wrap) || el.replaceWith(wrap);
    } catch (e) {
      console.error("Mermaid render error:", e);
    }
  }
}

// ==================== Fullscreen Code ====================
function openFullscreenCode(code, fname) {
  document.getElementById("fsFname").textContent = fname || "代码";
  document.getElementById("fsCodeContent").textContent = code;
  document.getElementById("fsCodeMask").classList.add("show");
  document.body.style.overflow = "hidden";
}

function closeFullscreenCode() {
  document.getElementById("fsCodeMask").classList.remove("show");
  document.body.style.overflow = "";
}

// Close fullscreen on Escape
document.addEventListener("keydown", (e) => {
  if (e.key === "Escape" && document.getElementById("fsCodeMask").classList.contains("show")) {
    closeFullscreenCode();
  }
});

// ==================== Toast ====================
function showToast(msg) {
  const t = document.getElementById("toast");
  t.textContent = msg;
  t.classList.add("show");
  setTimeout(() => t.classList.remove("show"), 2000);
}

// ==================== Export ====================
function toggleExportMenu() {
  document.getElementById("exportMenu").classList.toggle("show");
}
document.addEventListener("click", (e) => {
  const menu = document.getElementById("exportMenu");
  const btn = document.getElementById("exportBtn");
  if (menu && btn && !btn.contains(e.target) && !menu.contains(e.target)) {
    menu.classList.remove("show");
  }
});

function exportPDF() {
  document.getElementById("exportMenu").classList.remove("show");
  window.print();
}

function exportMarkdown() {
  document.getElementById("exportMenu").classList.remove("show");
  if (!currentModuleId) return;
  const main = document.getElementById("contentMain");
  const clone = main.cloneNode(true);
  // Remove non-content elements from clone
  clone.querySelectorAll(".copy-btn,.code-fold,.fullscreen-btn,.complete-btn").forEach(el => el.remove());
  // Convert code blocks to markdown fenced blocks
  clone.querySelectorAll(".cw").forEach(cw => {
    const fname = cw.querySelector(".fname")?.textContent || "";
    const code = cw.querySelector("pre code")?.textContent || "";
    const lang = fname.endsWith(".py") ? "python" : fname.endsWith(".yml") || fname.endsWith(".yaml") ? "yaml" : "";
    const md = `\`\`\`${lang}\n${code}\n\`\`\``;
    cw.replaceWith(document.createRange().createContextualFragment(`<pre>${md}</pre>`));
  });
  // Build markdown
  let md = `# ${findModuleById(currentModuleId)?.title || ""}\n\n`;
  md += clone.innerText;
  // Download
  const blob = new Blob([md], { type: "text/markdown" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = `${currentModuleId}.md`; a.click();
  URL.revokeObjectURL(url);
  showToast("📝 Markdown 已下载");
}

// ==================== Notes ====================
let notesStore = JSON.parse(localStorage.getItem("learner_notes") || "{}");
let currentNoteId = null;

// ---- Text selection → new note ----
function handleTextSelection() {
  const sel = window.getSelection();
  const text = sel?.toString().trim();
  if (!text || text.length < 3) {
    document.getElementById("selTip").classList.remove("show");
    return;
  }
  const range = sel.getRangeAt(0);
  const rect = range.getBoundingClientRect();
  const tip = document.getElementById("selTip");
  tip.style.top = (rect.top + window.scrollY - 32) + "px";
  tip.style.left = (rect.left + rect.width / 2) + "px";
  tip.style.transform = "translateX(-50%)";
  tip.classList.add("show");
  tip.dataset.quote = text;
}

document.addEventListener("mouseup", (e) => {
  if (e.target.closest(".sel-tip,.note-popup-mask,.note-popup,.note-highlight,.notes-panel,.notes-section")) return;
  setTimeout(handleTextSelection, 10);
});

// Click on a highlighted note → open edit popup
document.addEventListener("click", (e) => {
  const hl = e.target.closest(".note-highlight");
  if (!hl) return;
  const quote = hl.textContent;
  const modNotes = notesStore[currentModuleId] || [];
  const note = modNotes.find(n => n.quote === quote);
  if (note) openNotePopupByData(note.quote, note.text, note.id);
});

// ---- Popup management ----
function openNotePopup() {
  // Called from selTip — new note from selection
  const tip = document.getElementById("selTip");
  const quote = tip.dataset.quote || "";
  tip.classList.remove("show");
  const modNotes = notesStore[currentModuleId] || [];
  const existing = modNotes.find(n => n.quote === quote);
  openNotePopupByData(quote, existing ? existing.text : "", existing ? existing.id : null);
}

function openNotePopupByData(quote, text, noteId) {
  document.getElementById("npQuote").textContent = quote;
  document.getElementById("npText").value = text;
  currentNoteId = noteId;
  document.getElementById("notePopupMask").classList.add("show");
}

function openNoteById(noteId) {
  if (!notesStore[currentModuleId]) return;
  const n = notesStore[currentModuleId].find(n => n.id === noteId);
  if (n) openNotePopupByData(n.quote, n.text, n.id);
}

function closeNotePopup() {
  document.getElementById("notePopupMask").classList.remove("show");
}

// ---- CRUD ----
function saveNote() {
  const quote = document.getElementById("npQuote").textContent;
  const text = document.getElementById("npText").value.trim();
  if (!text || !quote) return;
  if (!notesStore[currentModuleId]) notesStore[currentModuleId] = [];
  if (currentNoteId) {
    const n = notesStore[currentModuleId].find(n => n.id === currentNoteId);
    if (n) { n.text = text; n.timestamp = new Date().toISOString(); }
  } else {
    notesStore[currentModuleId].push({
      id: Date.now().toString(36),
      quote, text,
      timestamp: new Date().toISOString(),
    });
  }
  persistNotes();
  closeNotePopup();
  refreshNotesUI();
  showToast("📝 笔记已保存");
}

function deleteNote(noteId) {
  const id = noteId || currentNoteId;
  if (!id || !notesStore[currentModuleId]) return;
  notesStore[currentModuleId] = notesStore[currentModuleId].filter(n => n.id !== id);
  if (notesStore[currentModuleId].length === 0) delete notesStore[currentModuleId];
  persistNotes();
  closeNotePopup();
  refreshNotesUI();
  showToast("🗑 笔记已删除");
}

function persistNotes() {
  localStorage.setItem("learner_notes", JSON.stringify(notesStore));
}

function refreshNotesUI() {
  renderNoteHighlights();
  renderNotesPanel();
  renderNotesSidebar();
}

// ---- Highlights in content ----
function renderNoteHighlights() {
  document.querySelectorAll(".note-highlight").forEach(el => {
    const parent = el.parentNode;
    parent.replaceChild(document.createTextNode(el.textContent), el);
    parent.normalize();
  });
  const modNotes = notesStore[currentModuleId] || [];
  if (!modNotes.length) return;
  const main = document.getElementById("contentMain");
  if (!main) return;
  const walker = document.createTreeWalker(main, NodeFilter.SHOW_TEXT);
  const textNodes = [];
  while (walker.nextNode()) {
    if (walker.currentNode.parentElement.closest(".cw,script,style,.np-quote,.note-highlight,.notes-panel")) continue;
    textNodes.push(walker.currentNode);
  }
  for (const note of modNotes) {
    for (const node of textNodes) {
      const idx = node.textContent.indexOf(note.quote);
      if (idx !== -1) {
        const range = document.createRange();
        range.setStart(node, idx);
        range.setEnd(node, idx + note.quote.length);
        const span = document.createElement("span");
        span.className = "note-highlight";
        span.title = note.text;
        try { range.surroundContents(span); } catch(e) { /* skip overlapping highlights */ }
        break;
      }
    }
  }
}

// ---- Notes panel (in-content, current module only) ----
function renderNotesPanel() {
  let panel = document.getElementById("notesPanel");
  const modNotes = notesStore[currentModuleId] || [];
  if (!modNotes.length) {
    if (panel) panel.remove();
    return;
  }
  const main = document.getElementById("contentMain");
  if (!main) return;

  if (!panel) {
    panel = document.createElement("div");
    panel.className = "notes-panel open";
    panel.id = "notesPanel";
    // Insert after the first .sec element (title)
    const sec = main.querySelector(".sec");
    sec ? sec.after(panel) : main.prepend(panel);
  }

  panel.innerHTML = `
    <div class="nph" onclick="this.parentElement.classList.toggle('open')">
      📝 本页笔记 (${modNotes.length})
      <span class="nph-toggle">▼</span>
    </div>
    <div class="npb">
      ${modNotes.map(n => `
        <div class="np-item" data-note-id="${n.id}">
          <div style="flex:1;min-width:0;">
            <div class="np-quote-mini">"${escapeHTML(n.quote.slice(0, 100))}${n.quote.length > 100 ? '...' : ''}"</div>
            <div class="np-text-mini">${escapeHTML(n.text.slice(0, 120))}${n.text.length > 120 ? '...' : ''}</div>
          </div>
          <div class="np-acts">
            <button title="编辑" onclick="event.stopPropagation();openNoteById('${n.id}')">✎</button>
            <button class="np-del" title="删除" onclick="event.stopPropagation();deleteNote('${n.id}')">✕</button>
          </div>
        </div>
      `).join("")}
    </div>`;
}

// ---- Notes in sidebar (all modules) ----
function renderNotesSidebar() {
  let container = document.getElementById("notesSection");
  if (!container) {
    const sidebar = document.getElementById("sidebar");
    container = document.createElement("div");
    container.className = "notes-section";
    container.id = "notesSection";
    sidebar.appendChild(container);
  }
  const allNotes = Object.entries(notesStore).filter(([, notes]) => notes.length > 0);
  if (!allNotes.length) { container.innerHTML = ""; return; }
  let html = `<div class="ns-title">📝 我的笔记 (${allNotes.reduce((s, [,n]) => s + n.length, 0)})</div>`;
  allNotes.forEach(([modId, notes]) => {
    const mod = findModuleById(modId);
    const modTitle = mod?.title || modId;
    notes.forEach(n => {
      const preview = n.quote.slice(0, 25);
      html += `<div class="ns-item">
        <span style="flex:1;min-width:0;overflow:hidden;text-overflow:ellipsis;white-space:nowrap;"
              onclick="loadModule('${modId}');setTimeout(()=>renderNotesPanel(),200)"
              title="${modTitle}: ${escapeHTML(n.text)}">${modTitle}: "${escapeHTML(preview)}..."</span>
        <button class="ns-del" title="删除" onclick="event.stopPropagation();deleteModuleNote('${modId}','${n.id}')">✕</button>
      </div>`;
    });
  });
  container.innerHTML = html;
}

// Sidebar delete helper
function deleteModuleNote(modId, noteId) {
  if (!notesStore[modId]) return;
  notesStore[modId] = notesStore[modId].filter(n => n.id !== noteId);
  if (notesStore[modId].length === 0) delete notesStore[modId];
  persistNotes();
  refreshNotesUI();
  showToast("🗑 笔记已删除");
}

// ==================== Keyboard Shortcuts ====================
document.addEventListener("keydown", (e) => {
  if ((e.ctrlKey || e.metaKey) && e.key === "k") {
    e.preventDefault();
    const input = document.getElementById("searchInput");
    if (input) input.focus();
  }
});

// ==================== Boot ====================
document.addEventListener("DOMContentLoaded", init);

(function () {
  const data = JSON.parse(document.getElementById("brainjob-data").textContent);
  const jobs = data.jobs || [];
  const statsPanel = document.getElementById("stats-panel");
  const jobsPanel = document.getElementById("jobs-panel");
  const detailPanel = document.getElementById("detail-panel");
  const detailContent = document.getElementById("detail-content");
  const generatedAt = document.getElementById("generated-at");

  const filterStatus = document.getElementById("filter-status");
  const filterPriority = document.getElementById("filter-priority");
  const filterOverdue = document.getElementById("filter-overdue");
  const filterArchived = document.getElementById("filter-archived");
  const filterIntegrity = document.getElementById("filter-integrity");
  const filterSearch = document.getElementById("filter-search");
  const sortBy = document.getElementById("sort-by");
  const detailClose = document.getElementById("detail-close");

  generatedAt.textContent = data.generated_at || "unknown";

  function uniqueStatuses() {
    const set = new Set(jobs.map((job) => job.application.status).filter(Boolean));
    return Array.from(set).sort();
  }

  function renderStats() {
    const stats = data.stats || {};
    const byStatus = stats.by_status || {};
    const statusCards = Object.entries(byStatus)
      .map(
        ([status, count]) =>
          `<div class="stat-card"><div class="value">${count}</div><div class="label">${status}</div></div>`
      )
      .join("");

    statsPanel.innerHTML = `
      <div class="stats-grid">
        <div class="stat-card"><div class="value">${stats.total_jobs || 0}</div><div class="label">Total jobs</div></div>
        <div class="stat-card"><div class="value">${stats.overdue_actions || 0}</div><div class="label">Overdue actions</div></div>
        <div class="stat-card"><div class="value">${stats.upcoming_deadlines || 0}</div><div class="label">Upcoming deadlines</div></div>
        ${statusCards}
      </div>`;
  }

  function populateStatusFilter() {
    uniqueStatuses().forEach((status) => {
      const option = document.createElement("option");
      option.value = status;
      option.textContent = status;
      filterStatus.appendChild(option);
    });
  }

  function matchesFilters(job) {
    const status = filterStatus.value;
    const priority = filterPriority.value;
    const overdueOnly = filterOverdue.checked;
    const hideArchived = filterArchived.checked;
    const integrityOnly = filterIntegrity.checked;
    const query = filterSearch.value.trim().toLowerCase();

    if (hideArchived && job.application.status === "archived") return false;
    if (status && job.application.status !== status) return false;
    if (priority && job.classification.priority !== priority) return false;
    if (overdueOnly && !job.application.overdue_action) return false;
    if (integrityOnly && job.integrity.valid) return false;

    if (query) {
      const haystack = [
        job.role.title,
        job.role.company,
        job.location.display,
        (job.classification.tags || []).join(" "),
      ]
        .filter(Boolean)
        .join(" ")
        .toLowerCase();
      if (!haystack.includes(query)) return false;
    }
    return true;
  }

  const PRIORITY_ORDER = { high: 0, medium: 1, low: 2 };

  function sortJobs(list) {
    const key = sortBy.value;
    return [...list].sort((a, b) => {
      if (key === "priority-deadline") {
        const pa = PRIORITY_ORDER[a.classification.priority] ?? 1;
        const pb = PRIORITY_ORDER[b.classification.priority] ?? 1;
        if (pa !== pb) return pa - pb;
        const da = a.dates.deadline || "9999";
        const db = b.dates.deadline || "9999";
        return da < db ? -1 : da > db ? 1 : 0;
      }
      if (key === "deadline") {
        const da = a.dates.deadline || "9999";
        const db = b.dates.deadline || "9999";
        return da < db ? -1 : da > db ? 1 : 0;
      }
      if (key === "status") {
        return (a.application.status || "").localeCompare(b.application.status || "");
      }
      if (key === "company") {
        return (a.role.company || "").localeCompare(b.role.company || "");
      }
      return 0;
    });
  }

  function renderJobCard(job) {
    const priority = job.classification.priority || "medium";
    const overdue = job.application.overdue_action;
    const isArchived = job.application.status === "archived";
    const integrityClass = job.integrity.valid ? "integrity-ok" : "integrity-bad";
    const integrityLabel = job.integrity.valid ? "integrity ok" : "integrity issue";
    const next = job.application.next_action;
    const nextText = next && !next.completed
      ? `Next: ${next.description}${next.due ? " (due " + next.due + ")" : ""}`
      : isArchived
        ? `Outcome: ${escapeHtml(job.application.outcome || "archived")}`
        : "No pending next action";

    return `
      <article class="job-card${isArchived ? " archived" : ""}" data-job-id="${job.id}">
        <h3>${escapeHtml(job.role.title)} @ ${escapeHtml(job.role.company)}</h3>
        <div class="job-meta">
          <span class="badge status">${escapeHtml(job.application.status || "unknown")}</span>
          <span class="badge priority-${priority}">${priority} priority</span>
          ${overdue ? '<span class="badge overdue">overdue action</span>' : ""}
          <span class="badge ${integrityClass}">${integrityLabel}</span>
          <span>${escapeHtml(job.location.display || "")}</span>
          ${job.dates.deadline ? `<span>Deadline: ${escapeHtml(job.dates.deadline)}</span>` : ""}
        </div>
        <p>${escapeHtml(nextText)}</p>
      </article>`;
  }

  function renderJobs() {
    const filtered = sortJobs(jobs.filter(matchesFilters));
    if (!filtered.length) {
      jobsPanel.innerHTML = "<p>No jobs match the current filters.</p>";
      return;
    }
    jobsPanel.innerHTML = `<div class="job-list">${filtered.map(renderJobCard).join("")}</div>`;
    jobsPanel.querySelectorAll(".job-card").forEach((card) => {
      card.addEventListener("click", () => showDetail(card.dataset.jobId));
    });
  }

  function showDetail(jobId) {
    const job = jobs.find((entry) => entry.id === jobId);
    if (!job) return;

    const interviews = (job.application.interviews || [])
      .map((item) => `<li>${escapeHtml(JSON.stringify(item))}</li>`)
      .join("") || "<li>None recorded</li>";

    const assessments = (job.application.assessments || [])
      .map((item) => `<li>${escapeHtml(JSON.stringify(item))}</li>`)
      .join("") || "<li>None recorded</li>";

    const timeline = (job.application.timeline || [])
      .map(
        (event) =>
          `<li><strong>${escapeHtml(event.type)}</strong> — ${escapeHtml(event.timestamp || "")}: ${escapeHtml(event.description || "")}</li>`
      )
      .join("") || "<li>Empty timeline</li>";

    const contacts = (job.contacts || [])
      .map(
        (contact) =>
          `<li>${escapeHtml(contact.name)} (${escapeHtml(contact.role || "contact")}) — ${escapeHtml(contact.organisation || "")}</li>`
      )
      .join("") || "<li>No contacts</li>";

    const notes = (job.notes || [])
      .map(
        (note) =>
          `<li><strong>${escapeHtml(note.author)}</strong> [${escapeHtml(note.category || "general")}]: ${escapeHtml(note.content)}</li>`
      )
      .join("") || "<li>No notes</li>";

    const documents = (job.documents.items || [])
      .map(
        (doc) =>
          `<li>${escapeHtml(doc.type)} v${doc.version} — ${escapeHtml(doc.path)} (${doc.submitted ? "submitted" : "pending"})</li>`
      )
      .join("") || "<li>No documents</li>";

    detailContent.innerHTML = `
      <div class="detail-grid">
        <section class="detail-section">
          <h4>${escapeHtml(job.role.title)} @ ${escapeHtml(job.role.company)}</h4>
          <p>Status: ${escapeHtml(job.application.status)}${job.application.outcome ? " | Outcome: " + escapeHtml(job.application.outcome) : ""} | Saved: ${escapeHtml(job.application.saved_date || "n/a")} | Applied: ${escapeHtml(job.application.applied_date || "n/a")}</p>
          <p>Location: ${escapeHtml(job.location.display || "n/a")} (${escapeHtml(job.location.work_arrangement || "unknown")})</p>
          <p>Compensation: ${formatCompensation(job.compensation)}</p>
          <p>Source: <a href="${escapeAttr(job.source.url)}" target="_blank" rel="noopener">${escapeHtml(job.source.url || "")}</a></p>
          <p>Captured: ${escapeHtml(job.dates.captured || "n/a")} | Verified: ${escapeHtml(job.dates.last_verified || "n/a")}</p>
        </section>
        <section class="detail-section">
          <h4>Original content integrity</h4>
          <p class="integrity ${job.integrity.valid ? "ok" : "bad"}">
            SHA-256: ${escapeHtml(job.integrity.sha256 || "n/a")}<br>
            ${job.integrity.valid ? "Content hash verified." : escapeHtml(job.integrity.error || "Integrity check failed.")}
          </p>
        </section>
        <section class="detail-section">
          <h4>Original job description</h4>
          <div class="description-box">${escapeHtml(job.description_original.content || "")}</div>
        </section>
        <section class="detail-section">
          <h4>Application timeline</h4>
          <ul>${timeline}</ul>
        </section>
        <section class="detail-section">
          <h4>Interviews & assessments</h4>
          <p><strong>Interviews</strong></p>
          <ul>${interviews}</ul>
          <p><strong>Assessments</strong></p>
          <ul>${assessments}</ul>
        </section>
        <section class="detail-section">
          <h4>Contacts</h4>
          <ul>${contacts}</ul>
        </section>
        <section class="detail-section">
          <h4>Notes</h4>
          <ul>${notes}</ul>
        </section>
        <section class="detail-section">
          <h4>Documents (${job.documents.submitted_count} submitted, ${job.documents.pending_count} pending)</h4>
          <ul>${documents}</ul>
        </section>
      </div>`;

    detailPanel.classList.remove("hidden");
    detailPanel.scrollIntoView({ behavior: "smooth", block: "start" });
  }

  function formatCompensation(comp) {
    if (!comp) return "n/a";
    if (comp.display_original) return comp.display_original;
    const min = comp.minimum;
    const max = comp.maximum;
    const currency = comp.currency || "";
    const interval = comp.interval || "";
    if (min == null && max == null) return "Not specified";
    if (min != null && max != null) return `${min}-${max} ${currency} ${interval}`.trim();
    return `${min ?? max} ${currency} ${interval}`.trim();
  }

  function escapeHtml(value) {
    return String(value)
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;");
  }

  function escapeAttr(value) {
    return escapeHtml(value).replaceAll("'", "&#39;");
  }

  [filterStatus, filterPriority, filterOverdue, filterArchived, filterIntegrity, filterSearch, sortBy].forEach((el) => {
    el.addEventListener("input", renderJobs);
    el.addEventListener("change", renderJobs);
  });

  detailClose.addEventListener("click", () => detailPanel.classList.add("hidden"));

  renderStats();
  populateStatusFilter();
  renderJobs();
})();

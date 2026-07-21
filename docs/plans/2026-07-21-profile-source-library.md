# Profile Library — Plane Blueprint & Delivery Breakdown

> **Status:** Blueprint registered in-repo; Phase 1 scaffold not implemented; Plane Epics/Tasks not yet created in Plane (no Plane API in this environment — use section 11 as the create checklist).  
> **Canonical rule:** Plane tracks decisions and implementation work; the repository remains the source of truth for folder structure, file inventory, and source-to-profile mapping.

**Purpose:** Operating blueprint for the standalone `profile/` academic and profile-source library.

**Related:** [Work breakdown §14](../work-breakdown.md) | [Docs index](../README.md)

---

## 1. Outcome and scope

Phase 1 establishes a repository-root `profile/` library beside `brainjob/`, `docs/`, and `skills/`. It creates folders, Markdown templates, naming conventions, intake rules, and repository ignore rules. No application code, schema changes, or job-document linkage is included.

### Locked decisions

| Decision | Choice |
|----------|--------|
| Library root | `profile/` at repository root |
| Phase 1 Brainjob linkage | None |
| Versioned material | Curated and renamed material may be tracked; intake and raw dumps remain ignored |
| Phase 1 change type | Folders and Markdown conventions only |
| Derived outputs | `profile/derived/` holds future CV, portfolio, and excerpt artifacts |
| Deferred follow-on | Brainjob attachment storage, WBS 2.8, remains Planned |

---

## 2. Plane project model

| Plane feature | Use | Guidance |
|---------------|-----|----------|
| Project | Profile Library initiative | Personal project is the implementation home (separate from Brainjob JOBBRAINMI issues). |
| Epic | Phase-level outcomes | One Epic for Phase 1; one deferred Epic for Phase 2. |
| Task | Reviewable implementation steps | Each task has a small, testable acceptance checklist. |
| Page | Canonical rationale, standards, templates, workflow | Keep long-lived specs on a Plane Page (or this doc); do not duplicate across tasks. |
| Labels | Cross-cutting classification | Use sparingly; do not use labels as progress states. |
| Milestone | Phase 1 completion checkpoint | Attach Phase 1 tasks once the milestone feature is available. |
| Views | Operational slices | Active-work, review, and deferred-work views. |

---

## 3. Recommended workflow

Default flow: **Backlog → Todo → In Progress → Done** or **Cancelled**. Add a Review state only if a distinct review handoff becomes necessary.

### Recommended labels

- **Phase:** `phase-1`, `phase-2`
- **Area:** `docs`, `repo-structure`, `templates`, `gitignore`, `intake`
- **Planning:** `deferred`, `decision`

Do not create a label for every folder. Folder-level detail belongs in the repository and the Phase 1 Epic acceptance criteria.

---

## 4. Epic breakdown

### Epic: Phase 1 — Profile Library Scaffold

**Proposed Plane ID:** `PROFILE-E1`  
**Goal:** Create an intake-ready repository structure for academic and profile feedstock without linking anything to Brainjob.  
**Labels:** `phase-1`

| WBS | Proposed Plane ID | Task | Acceptance |
|-----|-------------------|------|------------|
| 14.1 | `PROFILE-1` | Create repository folder scaffold | Prescribed tree exists and is clean in a fresh clone (`profile/_inbox/`, `academic/`, `writing/`, `research/`, `projects/`, `reference/`, `derived/{cv,portfolio,excerpts}/` with placeholders). |
| 14.2 | `PROFILE-2` | Write profile README conventions | Contributor can classify, rename, and place a new file using only `profile/README.md` (purpose, categories, naming, git policy, intake, deferred Brainjob note). |
| 14.3 | `PROFILE-3` | Create inventory template | `profile/INVENTORY.md` exists with columns: original name, proposed path, category, relevance, format status, notes. |
| 14.4 | `PROFILE-4` | Create source-to-profile mapping template | `profile/MAPPING.md` distinguishes direct profile material, feedstock, and skip; contains no job identifiers. |
| 14.5 | `PROFILE-5` | Add repository ignore rules | `profile/_inbox/*` ignored (placeholder kept); `profile/**/raw/` ignored; curated material can still be tracked. |
| 14.6 | `PROFILE-6` | Update work-breakdown documentation | WBS records Phase 1 work; Brainjob WBS 2.8 remains explicitly Planned. |
| 14.7 | `PROFILE-7` | Perform Phase 1 closure review | Templates, naming, ignore rules, and deferred notes agree; scaffold ready for first intake batch. |

**Delivery order:** PROFILE-1 → 2 → 3 → 4 → 5 (3 and 4 can parallelize after 2) → confirm 6 → 7.

**Repo status for PROFILE-6:** Partially Done (plan + WBS §14 exist); refresh when scaffold lands so statuses match reality.

### Epic: Phase 2 — Brainjob Derived-Artifact Wiring (Deferred)

**Proposed Plane ID:** `PROFILE-E2`  
**Status:** Planned, not active. Labels: `phase-2`, `deferred`.  
**Begin only after** usable distilled CV or portfolio artifacts exist under `profile/derived/`.

| Proposed Plane ID | Task |
|-------------------|------|
| `PROFILE-8` | Define readiness criteria for derived artifacts |
| `PROFILE-9` | Design how derived CV/portfolio outputs link into Brainjob document storage |
| `PROFILE-10` | Add any needed path validation and attachment-preview work |
| `PROFILE-11` | Revisit WBS 2.8 and schedule implementation |

---

## 5. Repository specification

```
profile/
├── README.md
├── INVENTORY.md
├── MAPPING.md
├── _inbox/
├── academic/
├── writing/
├── research/
├── projects/
├── reference/
└── derived/
    ├── cv/
    ├── portfolio/
    └── excerpts/
```

### Naming convention

`{doctype}_{subject_or_course}_{topic}_{yyyy}[_v{n}].{ext}`

| Segment | Rule | Examples |
|---------|------|----------|
| doctype | Concise artifact class | syllabus, assignment, paper, project, notes, ref, cv, portfolio, excerpt |
| subject_or_course | Short ASCII slug | eu_governance, climate_policy |
| topic | Short specific slug | final_essay, week03 |
| yyyy | Material or version year | 2024, 2025 |
| v{n} | Optional version suffix | v1, v2 |
| ext | Prefer PDF or Markdown for curated items | pdf, md |

Examples: `syllabus_eu_governance_overview_2024.pdf`; `paper_climate_policy_adaptation_governance_2025_v1.pdf`; `project_food_systems_stakeholder_map_2025.pdf`; `cv_master_2026_v1.pdf`.

---

## 6. Intake workflow

1. Drop incoming external material into `profile/_inbox/`.
2. Record every candidate in `INVENTORY.md`.
3. Classify into academic, writing, research, projects, reference, or skip.
4. Rename and move curated material using the naming convention.
5. Update `MAPPING.md` with the intended profile use.
6. Create a derived artifact only when the source is sufficiently valuable and distilled.

### First-batch priority

1. Syllabi and course overviews → `academic/`
2. Papers and essays → `writing/`
3. Projects and graded outputs → `projects/`
4. Research notes → `research/`
5. Profile-relevant material → mapping before any derived output is created

---

## 7. Definition of done for Phase 1

- Complete `profile/` tree exists with placeholder files as needed.
- README documents categories, naming, git policy, and intake workflow.
- Inventory and mapping templates exist and are ready for use.
- Repository rules protect the inbox and raw material directories.
- Phase 2 remains visibly deferred; no Brainjob document linkage is introduced.
- Implementation is ready to accept the first batch without reorganizing files later.

---

## 8. Suggested operational views

- **Phase 1 Active:** `phase-1` work not yet Done or Cancelled, grouped by state.
- **Review Queue:** work awaiting a review state, if that state is added.
- **Deferred Follow-up:** `phase-2` or `deferred` work, kept separate from active implementation.
- **Documentation and Templates:** `docs` or `templates` labels for quick reference.

---

## 9. Risks and guardrails

- Do not treat Plane as the file inventory; repository templates are canonical.
- Do not create job links, document manifests, or validation logic during Phase 1.
- Do not version unreviewed inbox material or large raw dumps by default.
- Keep tasks outcome-oriented; do not create one work-item per directory.
- Use the mapping template before creating polished CV or portfolio derivatives.

---

## 10. Next actions

1. **In Plane (manual):** Create Project “Profile Library”, Epic `PROFILE-E1` with tasks `PROFILE-1`…`PROFILE-7`, Epic `PROFILE-E2` in Backlog with `deferred` + `phase-2`, apply labels from section 3, optionally attach a Plane Page that links to this file.
2. **In repo:** Implement Phase 1 scaffold (PROFILE-1…7 / WBS 14.1–14.7) when ready to execute.
3. Do **not** start Phase 2 until `profile/derived/` holds usable distilled artifacts.

---

## 11. Plane create checklist (copy-ready)

No Plane MCP/API is available in the agent environment. Create these items in the Plane UI:

**Project:** Profile Library

**Labels:** `phase-1`, `phase-2`, `docs`, `repo-structure`, `templates`, `gitignore`, `intake`, `deferred`, `decision`

**Epic PROFILE-E1 — Phase 1 Profile Library Scaffold** (`phase-1`)

1. PROFILE-1 — Create repository folder scaffold (`repo-structure`)
2. PROFILE-2 — Write profile README conventions (`docs`)
3. PROFILE-3 — Create inventory template (`templates`)
4. PROFILE-4 — Create source-to-profile mapping template (`templates`)
5. PROFILE-5 — Add repository ignore rules (`gitignore`)
6. PROFILE-6 — Update work-breakdown documentation (`docs`) — mark In Progress/Done to match repo
7. PROFILE-7 — Perform Phase 1 closure review (`docs`, `decision`)

**Epic PROFILE-E2 — Phase 2 Brainjob Derived-Artifact Wiring** (`phase-2`, `deferred`, Backlog)

8. PROFILE-8 — Define derived-artifact readiness criteria
9. PROFILE-9 — Design Brainjob document-storage linkage
10. PROFILE-10 — Path validation / attachment preview (as needed)
11. PROFILE-11 — Revisit WBS 2.8 and schedule implementation

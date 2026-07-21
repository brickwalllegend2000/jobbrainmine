# Profile Library

Standalone academic and profile feedstock library at repository root. Material here is curated source content for future CVs, portfolios, and excerpts.

**Not wired to Brainjob.** Document paths, job linkage, and attachment storage (WBS 2.8) are Phase 2 and remain deferred until usable distilled artifacts exist under `derived/`.

## Categories

| Folder | Use for |
|--------|---------|
| `_inbox/` | Unreviewed external drops. Ignored by git except the placeholder. |
| `academic/` | Syllabi, course overviews, lecture materials |
| `writing/` | Papers, essays, long-form writing |
| `research/` | Research notes, lit reviews, working notes |
| `projects/` | Projects, graded outputs, deliverables |
| `reference/` | Stable reference material worth keeping |
| `derived/cv/` | Distilled CV artifacts (create only after mapping) |
| `derived/portfolio/` | Distilled portfolio artifacts |
| `derived/excerpts/` | Short excerpts drawn from curated sources |

Optional `raw/` directories under any category hold large unreviewed dumps and are gitignored.

## Naming convention

```
{doctype}_{subject_or_course}_{topic}_{yyyy}[_v{n}].{ext}
```

| Segment | Rule | Examples |
|---------|------|----------|
| doctype | Concise artifact class | syllabus, assignment, paper, project, notes, ref, cv, portfolio, excerpt |
| subject_or_course | Short ASCII slug | eu_governance, climate_policy |
| topic | Short specific slug | final_essay, week03 |
| yyyy | Material or version year | 2024, 2025 |
| v{n} | Optional version suffix | v1, v2 |
| ext | Prefer PDF or Markdown for curated items | pdf, md |

Examples:

- `syllabus_eu_governance_overview_2024.pdf`
- `paper_climate_policy_adaptation_governance_2025_v1.pdf`
- `project_food_systems_stakeholder_map_2025.pdf`
- `cv_master_2026_v1.pdf`

## Git policy

- **Track:** curated, renamed material under category folders and `derived/`.
- **Ignore:** everything in `_inbox/` except `.gitkeep`; any `**/raw/` under `profile/`.
- Do not commit unreviewed inbox drops or large raw dumps by default.

## Intake workflow

1. Drop incoming external material into `_inbox/`.
2. Record every candidate in [`INVENTORY.md`](./INVENTORY.md).
3. Classify into academic, writing, research, projects, reference, or skip.
4. Rename and move curated material using the naming convention above.
5. Update [`MAPPING.md`](./MAPPING.md) with the intended profile use (direct profile / feedstock / skip).
6. Create a derived artifact under `derived/` only when the source is sufficiently valuable and distilled.

### First-batch priority

1. Syllabi and course overviews → `academic/`
2. Papers and essays → `writing/`
3. Projects and graded outputs → `projects/`
4. Research notes → `research/`
5. Profile-relevant material → map in `MAPPING.md` before any derived CV/portfolio output

## Deferred (Phase 2)

Brainjob document storage, path validation, and wiring of `derived/` outputs into job document manifests are out of scope for Phase 1. See [docs/plans/2026-07-21-profile-source-library.md](../docs/plans/2026-07-21-profile-source-library.md) and WBS §14 / 2.8.

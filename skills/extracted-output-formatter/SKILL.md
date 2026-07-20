---
name: extracted-output-formatter
description: >
  Review, clean, and reformat extracted outputs (from OCR, APIs, web scraping, LLM extraction, or any messy data source) without losing information. Use this whenever the user mentions cleaning up data, tidying output, formatting extracted text, fixing structure, converting messy data to clean format, or wants to export to Markdown, YAML, JSON, CSV, or any structured format. Also useful for data extraction cleanup, post-processing OCR results, normalizing API responses, or preparing data for downstream use.
---

# Extracted Output Formatter

Clean and reformat messy extracted data into structured, usable output formats while preserving all information.

## Core Workflow

1. **Analyze the input** — Identify the source type (OCR, API, scrape, LLM output), current structure, and what's broken (inconsistent spacing, missing delimiters, mixed formats, encoding issues)
2. **Preserve information** — Never remove data unless explicitly requested. Cleaning means restructuring, not deleting.
3. **Normalize structure** — Fix inconsistent spacing, align fields, standardize delimiters, correct encoding issues, remove duplicate headers
4. **Convert to target format** — Apply the requested output format with proper syntax and conventions
5. **Validate output** — Ensure the formatted data parses correctly and all original information is present

## Common Issues and Fixes

### Spacing and Alignment
- Inconsistent indentation → Standardize to 2 or 4 spaces
- Mixed tabs/spaces → Convert all to spaces
- Extra blank lines → Consolidate to single line breaks where appropriate
- Trailing whitespace → Remove

### Structural Problems
- Missing delimiters → Infer from context and add
- Inconsistent headers → Normalize capitalization and naming
- Broken hierarchy → Reconstruct logical nesting
- Malformed dates/numbers → Detect format and standardize (ISO 8601 for dates)

### Data Quality
- Duplicate entries → Flag but don't auto-remove (user decides)
- Mixed data types in columns → Cast to appropriate type or flag inconsistency
- Encoding artifacts (smart quotes, em-dashes) → Normalize to ASCII or preserve UTF-8 intentionally
- OCR errors (l/I, 0/O confusion) → Flag suspicious patterns but don't auto-correct without confidence

### Format-Specific Issues
- **JSON**: Missing commas, unquoted keys, trailing commas, unescaped quotes
- **YAML**: Indentation errors, unquoted colons in values, "NO" interpreted as boolean, mixed flow/block styles
- **CSV**: Unescaped commas in fields, inconsistent quote usage, mixed line endings
- **Markdown**: Broken table alignment, missing pipe delimiters, header/body separator issues

## Output Format Guidelines

### Markdown
- Tables: Align columns, proper header separator (`|---|---|`), escape pipes in cells
- Lists: Consistent bullet style, proper indentation for nesting
- Code blocks: Use fenced blocks with language tags
- Headers: Proper hierarchy (H1 → H2 → H3), no skipping levels

### YAML
- Use block style for readability (not flow style with brackets)
- 2-space indentation (standard convention)
- Quote strings containing: colons, brackets, special chars, leading/trailing spaces
- Use `|` for multiline strings, `>` for folded text
- Avoid bare "NO", "YES", "ON", "OFF" — quote them to prevent boolean interpretation

### JSON
- 2 or 4-space indentation (match project convention or ask)
- No trailing commas
- Quote all keys
- Escape quotes, backslashes, newlines in strings
- Use arrays for lists, objects for key-value pairs

### CSV
- Quote fields containing: commas, quotes, newlines
- Escape quotes by doubling them (`""` inside quoted field)
- Consistent line endings (LF or CRLF, not mixed)
- Header row should match data column count

## Decision Tree

```
Input received
  ↓
Is structure recognizable?
  → YES: Identify format, apply format-specific fixes
  → NO: Ask user for context (source, expected structure)
  ↓
Is target format specified?
  → YES: Convert to that format
  → NO: Suggest best format based on data shape (tabular → CSV/Markdown, nested → JSON/YAML, mixed → Markdown)
  ↓
Are there ambiguous issues?
  → Flag them, suggest fixes, ask for confirmation
  ↓
Output cleaned data + summary of changes made
```

## Examples

### Example 1: OCR-Extracted Table to Markdown

**Input (messy OCR output):**
```
Name    Age   City
John Doe  32  New York
Jane Smith   28 Los Angeles
Bob Jones 45    Chicago
```

**Output (clean Markdown table):**
```markdown
| Name       | Age | City        |
|------------|-----|-------------|
| John Doe   | 32  | New York    |
| Jane Smith | 28  | Los Angeles |
| Bob Jones  | 45  | Chicago     |
```

### Example 2: Messy API Response to YAML

**Input (malformed JSON-ish text):**
```
{name: Product A, price: 29.99, tags: [electronics, sale], description: High quality item: perfect for home}
```

**Output (clean YAML):**
```yaml
name: Product A
price: 29.99
tags:
  - electronics
  - sale
description: "High quality item: perfect for home"
```

### Example 3: Mixed Format Extraction to JSON

**Input (scraped data with inconsistent structure):**
```
Title: Annual Report 2025
Author: Jane Doe
Date: 2025-03-15
Sections: Executive Summary, Financial Data, Projections
Pages: 127
```

**Output (structured JSON):**
```json
{
  "title": "Annual Report 2025",
  "author": "Jane Doe",
  "date": "2025-03-15",
  "sections": [
    "Executive Summary",
    "Financial Data",
    "Projections"
  ],
  "pages": 127
}
```

## Best Practices

**Preserve first, clean second** — Always keep original information unless explicitly told to remove it. Cleaning is about structure, not content reduction.

**Explain changes** — Briefly summarize what was fixed (e.g., "Standardized indentation, added missing delimiters, converted dates to ISO 8601").

**Flag ambiguity** — When the correct interpretation is unclear (e.g., "is this a date or a version number?"), ask rather than guess.

**Validate output** — After formatting, mentally (or actually) parse the output to ensure it's valid for the target format.

**Match conventions** — Use format-specific conventions (2-space YAML, pipe-aligned Markdown tables, quoted CSV fields).

**Handle encoding carefully** — Preserve UTF-8 characters unless the user specifically wants ASCII. Smart quotes and em-dashes are often intentional.

## When to Suggest Alternative Formats

- **Tabular data with no nesting** → CSV or Markdown table
- **Nested/hierarchical data** → JSON or YAML
- **Mixed content (text + data)** → Markdown with embedded code blocks
- **Configuration data** → YAML (human-readable) or JSON (machine-parseable)
- **API payloads** → JSON (standard for REST APIs)
- **Documentation** → Markdown

If the user requests a format that's awkward for their data shape (e.g., deeply nested data in CSV), suggest a better alternative and explain why.
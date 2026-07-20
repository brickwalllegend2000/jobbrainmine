# Format Specifications Reference

Detailed specs for common output formats. Consult when handling edge cases or format-specific validation.

## JSON Specification

### Valid Types
- String: `"text"` (double quotes only, no single quotes)
- Number: `42`, `3.14`, `-7`, `1.5e10` (no leading zeros except `0.x`)
- Boolean: `true`, `false` (lowercase only)
- Null: `null` (lowercase only)
- Array: `[1, 2, 3]`
- Object: `{"key": "value"}`

### Escaping Rules
- `"` → `\"`
- `\` → `\\`
- `/` → `\/` (optional but valid)
- `\b`, `\f`, `\n`, `\r`, `\t` for control characters
- Unicode: `\uXXXX` for characters outside ASCII

### Common Mistakes
- Trailing commas: `[1, 2, 3,]` is INVALID
- Unquoted keys: `{key: "value"}` is INVALID (must be `{"key": "value"}`)
- Single quotes: `{'key': 'value'}` is INVALID
- Comments: NOT allowed in standard JSON (use JSON5 or strip before parsing)

### Best Practices
- Use 2 or 4-space indentation consistently
- Keep arrays/objects on multiple lines when they contain multiple items
- Use arrays for ordered lists, objects for key-value mappings
- Validate with `JSON.parse()` or equivalent before delivering

## YAML Specification

### Block Style (Preferred)
```yaml
key: value
list:
  - item1
  - item2
nested:
  child: value
```

### Flow Style (Compact)
```yaml
key: value
list: [item1, item2]
nested: {child: value}
```

### Indentation Rules
- Use spaces only (tabs are INVALID)
- 2-space indentation is standard
- Child elements must be indented more than parent
- List items (`-`) align with parent key's value

### Quoting Rules
Quote strings when they contain:
- Colons followed by space: `"title: subtitle"`
- Leading/trailing spaces: `" padded "`
- Special characters: `[]{}:>|*&!%@`
- Reserved words: `"yes"`, `"no"`, `"true"`, `"false"`, `"null"`, `"on"`, `"off"`
- Numeric-looking strings: `"123"`, `"3.14"` (if you want them as strings)

### Multiline Strings
- Literal block (preserves newlines): `|`
  ```yaml
  description: |
    Line 1
    Line 2
  ```
- Folded block (folds newlines to spaces): `>`
  ```yaml
  description: >
    This is a long
    paragraph folded
    into one line.
  ```

### Common Mistakes
- Mixed tabs and spaces → Use spaces only
- Inconsistent indentation → Align carefully
- Unquoted colons: `title: Foo: Bar` → `title: "Foo: Bar"`
- Boolean confusion: `country: NO` → `country: "NO"` (Norway, not false)

### Best Practices
- Use block style for readability
- Quote ambiguous values
- Validate with a YAML parser before delivering
- Use `---` document separator for multiple documents in one file

## CSV Specification

### Basic Rules
- Fields separated by commas: `value1,value2,value3`
- First row typically contains headers
- Each row must have same number of fields

### Quoting Rules
Quote fields containing:
- Commas: `"Last, First"`
- Quotes: `"She said ""hello"""`  (double the quotes)
- Newlines: `"Line 1\nLine 2"`
- Leading/trailing spaces: `" padded "`

### Line Endings
- Use LF (`\n`) or CRLF (`\r\n`) consistently
- Don't mix line endings in the same file

### Common Mistakes
- Unescaped commas in fields → Quote the field
- Unescaped quotes → Double them (`""`)
- Inconsistent column counts → Pad with empty fields or fix source
- Missing header row → Add one or clarify with user

### Best Practices
- Always include a header row
- Quote fields liberally (better safe than broken)
- Use UTF-8 encoding (with or without BOM depending on target system)
- Validate row length consistency

## Markdown Tables

### Basic Syntax
```markdown
| Header 1 | Header 2 | Header 3 |
|----------|----------|----------|
| Cell 1   | Cell 2   | Cell 3   |
| Cell 4   | Cell 5   | Cell 6   |
```

### Alignment
- Left: `|:---------|`
- Center: `|:--------:|`
- Right: `|---------:|`

### Rules
- Header separator row required (at least 3 hyphens per column)
- Pipes at start and end are optional but recommended for clarity
- Alignment is cosmetic (extra spaces ignored by parsers)

### Escaping
- Pipes in cells: Use `\|` or HTML entity `&#124;`
- Newlines in cells: Not supported in standard Markdown tables (use `<br>` or split into separate rows)

### Common Mistakes
- Missing separator row → Required after header
- Misaligned pipes → Cosmetic but reduces readability
- Pipes in content → Escape them

### Best Practices
- Align pipes for human readability (even though parsers ignore it)
- Keep tables simple (if complex, consider HTML table or different format)
- Use consistent spacing

## Format Selection Matrix

| Data Shape | Best Format | Why |
|------------|-------------|-----|
| Flat table (no nesting) | CSV or Markdown | Simple, widely supported, human-readable |
| Nested/hierarchical | JSON or YAML | Supports arbitrary nesting |
| Configuration | YAML | Human-friendly, supports comments (in some parsers) |
| API payload | JSON | Standard for REST APIs, strict parsing |
| Mixed content (text + data) | Markdown | Readable, supports embedded code/data blocks |
| Time-series data | CSV | Efficient for large datasets, easy to import |
| Key-value pairs | YAML or JSON | Natural representation |

## Validation Tips

- **JSON**: Use `JSON.parse()` in JavaScript, `json.loads()` in Python
- **YAML**: Use `yaml.safe_load()` in Python, `YAML.parse()` in JavaScript (js-yaml)
- **CSV**: Check row length consistency, validate header presence
- **Markdown**: Render with a Markdown parser (e.g., marked.js, CommonMark) to check for issues

Always validate output before delivering to catch syntax errors early.
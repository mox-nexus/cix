# Diagram-as-Code Gotchas and Debugging

Production issues, platform limitations, and debugging strategies.

## Top 10 Mermaid Gotchas

### 1. Platform Version Lag

**Issue**: GitHub and GitLab use older Mermaid versions than official releases.

| Platform | Version | Impact |
|----------|---------|--------|
| GitHub | ~10.0.2 (2024) | Newer diagram types don't render |
| GitLab | 10.6.0 (Oct 2023) | Some newer types work, some don't |
| Official | 11.x+ | All features available |

**Trap**: Using cutting-edge features like `architecture-beta`, `timeline`, `mindmap`

**Fix**: Test on target platform. Stick to core types for GitHub deployment.

### 2. GitHub Pages Doesn't Work

**Issue**: Jekyll (default GitHub Pages processor) blocks Mermaid with `safe: true` mode.

**Symptoms**: Raw Mermaid code shows instead of diagrams

**Fix**:
- Use GitHub Actions to render to SVG before deployment
- Use Docusaurus, MkDocs, or other static site generators that support Mermaid
- Configure Jekyll plugin (complex)

### 3. iOS GitHub App Shows Raw Code

**Issue**: GitHub mobile app (iOS) doesn't render Mermaid diagrams.

**Fix**:
- Provide rendered image fallback for mobile users
- Accept limitation if desktop-only documentation
- Test on mobile before declaring done

### 4. Silent Parameter Failures

**Issue**: Bad parameters fail silently without error messages.

**Symptoms**: Diagram renders but styling doesn't apply

**Fix**: Use Mermaid Live Editor (mermaid.live) for instant validation

### 5. Arrow Syntax Varies by Diagram Type

**Issue**: Each diagram type has different arrow syntax.

| Diagram Type | Solid | Dotted | Bidirectional |
|--------------|-------|--------|---------------|
| Flowchart | `-->` | `-.->` | `<-->` |
| Sequence | `->>` | `-->>` | `<<->>` |
| Class | `--` | `..` | N/A |
| State | `-->` | N/A | N/A |
| ER | `--` | N/A | N/A |

**Trap**: Using flowchart arrows in sequence diagrams

**Fix**: Check diagram-specific syntax in Mermaid docs

### 6. Typos Break Diagrams Completely

**Issue**: Typos in keywords cause entire diagram to fail without specific error.

**Symptoms**: "Syntax error in text" with no line number

**Fix**:
- Copy-paste keywords from docs
- Use Mermaid Live Editor for validation
- Use mermaid-fixer (AI-driven syntax fixer): github.com/sopaco/mermaid-fixer

### 7. Non-Deterministic Rendering

**Issue**: `architecture-beta` diagrams can render differently on multiple loads.

**Source**: GitHub issue #6024 (November 2024)

**Fix**: Avoid `architecture-beta` for production. Use D2 for architecture diagrams.

### 8. Security Risk with User-Generated Content

**Issue**: HTML characters in Mermaid bypass standard sanitization.

**Fix**:
- Never trust user-generated Mermaid
- Use dedicated Mermaid sanitizer
- Pre-render user diagrams server-side

### 9. GitLab Flicker on Load

**Issue**: GitLab shows plain text briefly before rendering diagram (client-side rendering).

**Fix**: Accept as platform limitation. Not fixable without server-side rendering.

### 10. Limited Styling Control

**Issue**: Can't achieve pixel-perfect layouts or specific brand styling.

**Fix**:
- Use class-based styling for colors: `classDef important fill:#f00`
- Upgrade to D2 for more styling control
- Accept "good enough" for documentation

## Debugging Workflow

### Step 1: Validate Syntax
Copy Mermaid code to Mermaid Live Editor: mermaid.live for instant validation + preview.

### Step 2: Check Version Compatibility
Verify diagram type supported on target platform. GitHub: Core types only.

### Step 3: Verify Arrow Syntax
Each diagram type has different arrow syntax. Check Mermaid docs for diagram-specific syntax.

### Step 4: Check Browser Console
Open browser dev tools. Look for JavaScript errors in console. Mermaid errors often show here.

### Step 5: Simplify Diagram
Remove complex parts one by one. Identify what breaks the diagram. Isolate the problematic syntax.

## Common Error Messages

### "Syntax error in text"
**Cause**: Typo in keyword, mismatched brackets, invalid arrow syntax
**Fix**: Check keywords, verify brackets match, use correct arrows for diagram type

### "Diagram failed to render"
**Cause**: Browser JavaScript error, unsupported feature, version incompatibility
**Fix**: Check browser console, verify platform version, simplify diagram

### Diagram shows as raw code
**Cause**: Platform doesn't support Mermaid, version too old, syntax error
**Fix**: Verify platform support, check version, validate syntax

## Platform-Specific Issues

### GitHub
- Core diagram types work
- Newer types (architecture, timeline, mindmap) may not render
- GitHub Pages requires configuration
- iOS app shows raw code

### GitLab
- Most diagram types work
- Brief flicker on load
- Better version support than GitHub

### Azure DevOps
- Native Mermaid support in wikis
- Good version support

## D2 Gotchas

### ELK Engine Can Crash
ELK layout engine unstable with large diagrams. Use dagre (default) or TALA (paid).

### Dagre Unmaintained
Default layout engine hasn't been updated since 2018. Accept limitation or upgrade to TALA.

### No Gantt/Timeline Support
D2 focused on architecture, lacks timeline diagram types. Use Mermaid for these.

### Build Step Required
Must render before viewing. Use `d2 --watch` for auto-rebuild during development.

## Validation Checklist

Before committing diagrams:
- [ ] Tested in Mermaid Live Editor (mermaid.live)
- [ ] Verified diagram type supported on target platform
- [ ] Used correct arrow syntax for diagram type
- [ ] Added titles and descriptive labels
- [ ] Checked diagram renders on target platform
- [ ] Tested on mobile (if audience uses mobile)
- [ ] Kept diagram focused (one concept, not mega-diagram)
- [ ] Validated security if accepting user input
- [ ] No typos in keywords
- [ ] Brackets/parentheses match

---

**Sources**: Mermaid GitHub issues, GitLab handbook, platform documentation, production debugging experience

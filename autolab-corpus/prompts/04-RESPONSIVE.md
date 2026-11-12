# Prompt 04 — Responsive Refinement

Use after the configuration logic is complete.

```text
Using the AutoLab design corpus, refine the entire application for responsive quality.

Target viewports:
- Desktop: 1440 × 900
- Mobile: 390 × 844
- Intermediate widths must behave gracefully.

Audit and improve:

1. Landing page
2. Studio page
3. Cabin viewer
4. Configuration panel
5. Material selector
6. Colour selector
7. Thread selector
8. Composition selector
9. Trim selector
10. Illumination selector
11. Camera controls
12. Specification summary

Mobile requirements:
- Cabin viewer remains the dominant visual element.
- Configuration controls are compact, touch-friendly, and accessible.
- No horizontal scrolling.
- No cramped selectors.
- No tiny tap targets.
- Preserve legible typography.
- Do not simply stack the desktop layout.

Desktop requirements:
- Cabin viewer occupies approximately two-thirds of the working area.
- Configuration controls occupy a focused right-side panel.
- Material imagery communicates texture clearly.
- Navigation remains compact and unobtrusive.

Do not add new features.
Do not change the information architecture.
Do not introduce backend functionality.

Before coding, identify:
1. Every layout weakness at 1440 × 900.
2. Every layout weakness at 390 × 844.
3. Every touch-target or accessibility issue.
4. Every visual inconsistency.
5. Every generic AI-design pattern that remains.

Then fix only those issues.
```

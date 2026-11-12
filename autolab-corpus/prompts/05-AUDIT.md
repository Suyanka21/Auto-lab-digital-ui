# Prompt 05 — Quality and Anti-Slop Audit

Use after the responsive refinement is complete.

```text
Perform a strict design and implementation audit of the AutoLab Digital Showroom.

Compare the implementation against:

- AGENTS.md
- rules/visual-direction.md
- rules/anti-slop.md
- rules/responsive.md
- rules/content.md
- references/README.md
- patterns/landing-page.md
- patterns/studio-page.md
- patterns/cabin-viewer.md
- patterns/configuration-panel.md
- patterns/specification-summary.md

Identify every violation in these categories:

1. Visual direction
2. Typography
3. Colour usage
4. Layout and spacing
5. Material realism
6. Selected states
7. Motion quality
8. Mobile experience
9. Accessibility
10. Component architecture
11. Configuration-state correctness
12. Specification-summary accuracy
13. Generic AI-design patterns
14. Unsupported claims
15. Fake 3D functionality

For each issue:
- Identify the exact screen or component.
- Describe the problem.
- Explain why it fails the corpus rules.
- Provide the precise correction.

Then implement only the corrections.

Do not add new features.
Do not alter the information architecture.
Do not introduce backend functionality.
Do not claim the prototype is production-ready.
```

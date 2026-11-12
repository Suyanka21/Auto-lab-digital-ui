# Prompt 00 — Setup and Design Foundation

Use this as the first prompt after importing the AutoLab corpus.

```text
You are building the AutoLab Digital Showroom: a premium, frontend-only React + TypeScript + Tailwind prototype for AutoLab Interior Studio, a Nairobi-based automotive interior customization workshop.

First, read and internalize:

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

Do not build the full application yet.

Your first task is to establish the design foundation:

1. Create a clean React + TypeScript + Tailwind project structure.
2. Implement the AutoLab colour tokens exactly:
   - Ivory: #F3F0E9
   - Paper: #FAF8F3
   - Ink: #252425
   - Graphite: #101114
   - Cyan: #72C4E1
   - Cyan Ink: #17596D
   - Muted Grey: #65615B
   - Fine Border: #D2CEC5
3. Create a restrained editorial type scale.
4. Create reusable layout and surface primitives.
5. Create a typed configuration state model for:
   - Material
   - Primary colour
   - Secondary colour
   - Accent thread
   - Composition
   - Cabin trim
   - Ambient illumination
   - Active camera
6. Create the component boundaries listed in AGENTS.md, but do not fully implement every screen yet.
7. Build only the global layout shell, design tokens, typography, and reusable primitives.

Strict rules:
- Do not use generic SaaS dashboard styling.
- Do not use glassmorphism, neon glows, purple-blue gradients, floating decorative elements, or excessive gradients.
- Do not add backend, authentication, payments, database, or external APIs.
- Do not invent prices, testimonials, statistics, availability, or delivery timelines.
- Do not fake 3D functionality.
- Use restrained motion only where it clarifies state or hierarchy.

Before writing code, briefly state:
1. The visual system you will follow.
2. The component architecture.
3. The typed configuration state model.
4. What you will build in this pass.
5. What you will deliberately defer.

Then implement the foundation.
```

# AutoLab Design Corpus

This repository is a **design corpus and execution brief** for building the AutoLab Digital Showroom in Google AI Studio Build.

It is not a generic UI kit. It defines the visual standard, interaction rules, component boundaries, and anti-generic-AI constraints for a premium automotive interior configurator.

## How to use in Google AI Studio

1. Import this repository through **Build mode > Add files > Import from GitHub**, or upload the ZIP / individual files if GitHub import is unavailable.
2. Start with `PROMPTS/00-SETUP.md`.
3. Complete each prompt in order. Do not ask for the whole application in one prompt.
4. After every major build pass, run the relevant audit prompt in `PROMPTS/`.
5. Keep the generated code in a clean React + TypeScript + Tailwind project structure.

## Contents

- `AGENTS.md` — primary instructions for the AI agent.
- `rules/` — visual, motion, responsive, content, and anti-slop rules.
- `references/` — reference-image manifest and how to interpret the images.
- `patterns/` — implementation patterns for each major screen and component.
- `prompts/` — sequential Google AI Studio prompts.
- `assets/` — instructions for imagery and placeholders.
- `handoff/` — future Three.js / React Three Fiber integration contract.

## Non-negotiables

- Editorial Atelier direction: restrained, tactile, premium, automotive.
- No generic AI landing-page patterns.
- No fabricated 3D capability.
- No invented prices, reviews, testimonials, availability, or delivery timelines.
- The viewer must be replaceable by the future AutoLab Three.js/R3F engine.

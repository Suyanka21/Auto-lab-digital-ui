# Prompt 03 — Configuration Logic

Use after the Studio shell is complete.

```text
Using the AutoLab design corpus, implement the configuration functionality for the Studio.

Follow `patterns/configuration-panel.md`, `patterns/specification-summary.md`, and the typed state model already created.

Implement:

1. Material selector
   - Classic
   - Diamond Quilted
   - Perforated

2. Colour selector
   - Exclusive Black
   - Sienna Brown
   - Light Ivory
   - Additional colours only where clearly presented as illustrative

3. Accent thread selector
   - Selectable thread colours
   - Clear selected states

4. Composition selector
   - Single-colour
   - Two-tone
   - Clear explanation of affected surfaces

5. Cabin Trim selector — illustrative preview
   - Carbon Fibre
   - Poplar Wood
   - Walnut Wood
   - Piano Lacquer

6. Ambient Illumination selector — illustrative preview
   - Cyan
   - Amber
   - Rose
   - Ocean
   - Champagne

Requirements:
- Selections must update shared application state.
- Changing any option must update the selected control and specification summary.
- Use clear visual feedback and restrained transitions.
- Provide previous and next step navigation.
- Allow users to edit earlier selections.
- Clearly distinguish illustrative previews from confirmed workshop offerings.
- Do not display prices, availability, delivery timelines, or backend integration.

Material imagery must communicate the actual material:
- Smooth leather for Classic.
- Diamond quilting for Diamond Quilted.
- Perforated leather for Perforated.
- Do not reuse one brown seat photograph for every material selection.
- Label illustrative imagery appropriately.

Before coding, state:
1. The state updates triggered by each selector.
2. The selected-state design.
3. The mobile control layout.
4. The specification-summary updates.
5. The anti-slop checks you will apply.

Then implement the configuration logic and selectors.
```

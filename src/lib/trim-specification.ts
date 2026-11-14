export const DEFAULT_TRIM_ID = 'autolab-twill-carbon';

/** Preview choices are illustrative; they do not approve a supplier sample. */
export function trimSpecification(trim: { id: string; name: string }): string {
  return `${trim.name} (3D preview; confirm physical sample with atelier)`;
}

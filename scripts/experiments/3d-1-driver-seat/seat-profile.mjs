// 3D-1 driver-seat experiment: one smooth displacement field for the backrest.
// Coordinates are glTF metres: +X driver side, +Y up, +Z towards the dashboard.
// Every constant is either measured from the production mesh or a visual estimate
// from Gallery 08/30. None is a vehicle dimension; the result is provisional.

export const SEAT_CENTRE_X = 0.425; // measured: production driver-seat symmetry plane
// Measured: least-squares plane through the production backrest insert, z = a*y + b.
export const INSERT_PLANE = { slope: -0.489, offset: 0.107 };
// Measured: production backrest half-width per height (2 cm steps).
const HALF_WIDTH = [
  [0.60, 0.2484], [0.62, 0.2508], [0.64, 0.2520], [0.66, 0.2545], [0.68, 0.2575], [0.70, 0.2609],
  [0.72, 0.2647], [0.74, 0.2686], [0.76, 0.2726], [0.78, 0.2777], [0.80, 0.2818], [0.82, 0.2846],
  [0.84, 0.2861], [0.86, 0.2863], [0.88, 0.2860], [0.90, 0.2840], [0.92, 0.2770], [0.94, 0.2695],
  [0.96, 0.2596], [0.98, 0.2470], [1.00, 0.2257], [1.02, 0.2085], [1.04, 0.1887], [1.06, 0.1490],
];
// Visual estimate: width ratio that turns the shield outline into near-parallel
// sides with broad rounded shoulders (Gallery 08 and 30).
const WIDTH_RATIO = [
  [0.70, 1.0], [0.80, 0.944], [0.86, 0.936], [0.90, 0.944], [0.94, 0.985], [0.96, 1.015],
  [0.98, 1.05], [1.00, 1.10], [1.02, 1.115], [1.04, 1.10], [1.06, 1.05],
];
// Visual estimate: how much of the bolster crest height above the insert plane is removed.
export const BOLSTER_SOFTEN = 0.15;
const BOLSTER_Y = [0.56, 0.66, 0.94, 1.02]; // fade in / fade out heights
const BOLSTER_LATERAL = [0.15, 0.19]; // starts outside the insert seam

const smoothstep = (a, b, x) => {
  const t = Math.min(1, Math.max(0, (x - a) / (b - a)));
  return t * t * (3 - 2 * t);
};

// Monotone cubic (Fritsch–Carlson) through the table; constant outside it.
function curve(table) {
  const xs = table.map((p) => p[0]), ys = table.map((p) => p[1]), n = xs.length;
  const d = [], m = new Array(n);
  for (let i = 0; i < n - 1; i++) d.push((ys[i + 1] - ys[i]) / (xs[i + 1] - xs[i]));
  m[0] = 0; m[n - 1] = 0;
  for (let i = 1; i < n - 1; i++) m[i] = d[i - 1] * d[i] <= 0 ? 0 : (d[i - 1] + d[i]) / 2;
  for (let i = 0; i < n - 1; i++) {
    if (d[i] === 0) { m[i] = 0; m[i + 1] = 0; continue; }
    const a = m[i] / d[i], b = m[i + 1] / d[i], s = a * a + b * b;
    if (s > 9) { const t = 3 / Math.sqrt(s); m[i] = t * a * d[i]; m[i + 1] = t * b * d[i]; }
  }
  return (x) => {
    if (x <= xs[0]) return ys[0];
    if (x >= xs[n - 1]) return ys[n - 1];
    let i = 0; while (x > xs[i + 1]) i++;
    const h = xs[i + 1] - xs[i], t = (x - xs[i]) / h, t2 = t * t, t3 = t2 * t;
    return (2 * t3 - 3 * t2 + 1) * ys[i] + (t3 - 2 * t2 + t) * h * m[i]
      + (-2 * t3 + 3 * t2) * ys[i + 1] + (t3 - t2) * h * m[i + 1];
  };
}
const halfWidth = curve(HALF_WIDTH);
const widthRatio = curve(WIDTH_RATIO);

/** Maps a production backrest point to the candidate position. */
export function deformBackrest([x, y, z]) {
  const side = x >= SEAT_CENTRE_X ? 1 : -1;
  const a = Math.abs(x - SEAT_CENTRE_X);
  // Lateral reshape: the centre (insert, headrest posts) stays put, the outline moves fully.
  const outer = smoothstep(0.45, 1, a / halfWidth(y));
  const a2 = a * (1 + (widthRatio(y) - 1) * outer);
  // Bolster softening: pull the crest back towards the insert plane.
  const proud = z - (INSERT_PLANE.slope * y + INSERT_PLANE.offset);
  const w = smoothstep(BOLSTER_Y[0], BOLSTER_Y[1], y) * (1 - smoothstep(BOLSTER_Y[2], BOLSTER_Y[3], y))
    * smoothstep(BOLSTER_LATERAL[0], BOLSTER_LATERAL[1], a);
  const z2 = proud > 0 ? z - BOLSTER_SOFTEN * w * proud : z;
  return [SEAT_CENTRE_X + side * a2, y, z2];
}

/** Numeric Jacobian of deformBackrest (columns = d/dx, d/dy, d/dz), row-major 3x3. */
export function jacobian(p, eps = 1e-4) {
  const J = new Array(9);
  for (let c = 0; c < 3; c++) {
    const hi = [...p], lo = [...p]; hi[c] += eps; lo[c] -= eps;
    const A = deformBackrest(hi), B = deformBackrest(lo);
    for (let r = 0; r < 3; r++) J[r * 3 + c] = (A[r] - B[r]) / (2 * eps);
  }
  return J;
}

const normalize = (v) => { const n = Math.hypot(v[0], v[1], v[2]) || 1; return [v[0] / n, v[1] / n, v[2] / n]; };
/** Tangent directions transform with J. */
export const transformDirection = (J, v) => normalize([
  J[0] * v[0] + J[1] * v[1] + J[2] * v[2], J[3] * v[0] + J[4] * v[1] + J[5] * v[2], J[6] * v[0] + J[7] * v[1] + J[8] * v[2]]);
/** Normals transform with the inverse transpose of J (the cofactor matrix, up to scale). */
export function transformNormal(J, n) {
  const [a, b, c, d, e, f, g, h, i] = J;
  const C = [e * i - f * h, f * g - d * i, d * h - e * g, c * h - b * i, a * i - c * g, b * g - a * h, b * f - c * e, c * d - a * f, a * e - b * d];
  return normalize([C[0] * n[0] + C[1] * n[1] + C[2] * n[2], C[3] * n[0] + C[4] * n[1] + C[5] * n[2], C[6] * n[0] + C[7] * n[1] + C[8] * n[2]]);
}

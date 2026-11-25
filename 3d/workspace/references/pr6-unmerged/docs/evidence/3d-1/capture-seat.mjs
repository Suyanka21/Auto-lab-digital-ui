// 3D-1 fixed-camera captures of the real viewer (Driver Hero, Stitch Detail; three treatments; two hide colours).
// Usage from the repository root: node docs/evidence/3d-1/capture-seat.mjs <baseUrl> <outDir>
import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const [base, out] = process.argv.slice(2);
await mkdir(out, { recursive: true });
const browser = await chromium.launch({ headless: true, args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] });
const errors = [];
const TREATMENTS = [['classic', 'Classic'], ['diamond', 'Diamond Quilted'], ['perforated', 'Perforated']];
const CAMERAS = [['driver-hero', 'Driver Hero'], ['stitch-detail', 'Stitch Detail']];
const COLOURS = [['black', 'Exclusive Black'], ['stone', 'Warm Stone']];
try {
  const page = await browser.newPage({ viewport: { width: 1440, height: 900 }, deviceScaleFactor: 1 });
  page.on('pageerror', e => errors.push(e.message));
  await page.goto(base, { waitUntil: 'networkidle', timeout: 60000 });
  await page.getByRole('button', { name: 'Enter the Studio', exact: true }).first().click();
  await page.locator('canvas').first().waitFor({ timeout: 60000 });
  await page.waitForTimeout(6000);
  const step = async (label) => page.getByRole('button', { name: label, exact: true }).click();
  const pick = async (group, label) => page.getByRole('radiogroup', { name: group }).getByRole('radio', { name: label, exact: true }).click();
  await step('03 Accent Thread'); await pick('Accent thread colour', 'Light Ivory');
  const cams = page.getByRole('group', { name: 'Cabin camera viewpoints' });
  for (const [cslug, colour] of COLOURS) {
    await step('02 Colour'); await pick('Primary hide colour', colour);
    for (const [tslug, treatment] of TREATMENTS) {
      await step('01 Material'); await pick('Upholstery material', treatment);
      await page.waitForTimeout(6000);
      for (const [vslug, cam] of CAMERAS) {
        await cams.getByRole('button', { name: new RegExp(cam) }).click();
        await page.waitForTimeout(5000);
        await page.locator('canvas').first().screenshot({ path: `${out}/${tslug}-${cslug}-${vslug}.png` });
        console.log('shot', tslug, cslug, vslug);
      }
    }
  }
  await page.close();
} finally { await browser.close(); await writeFile(`${out}/errors.json`, JSON.stringify(errors)); console.log('errors', JSON.stringify(errors)); }

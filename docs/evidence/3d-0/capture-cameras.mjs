import { chromium } from '@playwright/test';
const out = '/home/ubuntu/scratch/shots';
const browser = await chromium.launch({ headless: true, args: ['--use-angle=swiftshader','--enable-unsafe-swiftshader'] });
const errors = [];
try {
  for (const [w, h, tag] of [[1440, 900, 'desktop'], [390, 844, 'mobile']]) {
    const page = await browser.newPage({ viewport: { width: w, height: h } });
    page.on('pageerror', e => errors.push(e.message));
    await page.goto('http://127.0.0.1:4173/', { waitUntil: 'networkidle', timeout: 60000 });
    await page.getByRole('button', { name: 'Enter the Studio', exact: true }).first().click();
    await page.locator('canvas').first().waitFor({ timeout: 60000 });
    const group = page.getByRole('group', { name: 'Cabin camera viewpoints' });
    const initial = await group.locator('button[aria-pressed="true"]').innerText();
    await page.waitForTimeout(8000);
    for (const label of ['Driver Hero', 'Cabin Pair']) {
      await group.getByRole('button', { name: new RegExp(label) }).click();
      await page.waitForTimeout(5000);
      const slug = label.toLowerCase().replace(' ', '-');
      await page.screenshot({ path: `${out}/${tag}-${slug}.png` });
      await page.locator('canvas').first().screenshot({ path: `${out}/${tag}-${slug}-stage.png` });
    }
    console.log(tag, 'initial camera:', initial.replace(/\s+/g, ' '));
    await page.close();
  }
} finally { await browser.close(); console.log('errors', JSON.stringify(errors)); }

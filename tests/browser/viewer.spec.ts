import { mkdir, writeFile } from 'node:fs/promises';
import { test, expect } from '@playwright/test';
test('real cabin loads behind the existing controls', async ({page})=>{
  await page.goto('/');
  await page.getByRole('button',{name:'Enter the Studio',exact:true}).first().click();
  await expect(page.locator('canvas')).toHaveCount(1,{timeout:15000});
  await expect(page.getByTestId('spike-viewer')).toHaveAttribute('aria-busy','false');
  await expect.poll(()=>page.evaluate(()=>window.__autolab?.snapshot().status)).toBe('success');
  await mkdir('docs/evidence/phase3',{recursive:true});
  await page.screenshot({path:'docs/evidence/phase3/live-driver-hero.png',fullPage:true});
  await writeFile('docs/evidence/phase3/scene.json',JSON.stringify(await page.evaluate(()=>window.__autolab?.snapshot()),null,2));
});

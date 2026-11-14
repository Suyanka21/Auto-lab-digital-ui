import { test, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
for(const width of [1440,390]) {
 test(`Back and reset preserve work until explicitly discarded at ${width}`,async({page})=>{
  test.setTimeout(120000);await page.setViewportSize({width,height:900});await page.goto('/studio');
  const snap=()=>page.evaluate(()=>window.__autolab?.snapshot());
  await expect.poll(async()=>(await snap())?.status,{timeout:60000}).toBe('success');
  await page.getByRole('radio',{name:'Diamond Quilted',exact:true}).click();
  await expect.poll(async()=>(await snap())?.assetUrl).toContain('diamond');
  await expect.poll(async()=>(await snap())?.status,{timeout:60000}).toBe('success');
  await page.getByRole('button',{name:'02 Colour',exact:true}).click();
  await page.getByRole('radio',{name:'Forest Green',exact:true}).click();
  await page.getByRole('button',{name:'Enable Two-tone'}).click();
  await page.getByRole('radiogroup',{name:'Secondary hide colour',exact:true}).getByRole('radio',{name:'Warm Stone',exact:true}).click();
  await page.getByRole('button',{name:'03 Accent Thread',exact:true}).click();
  await page.getByRole('radio',{name:'Atelier Cyan',exact:true}).click();
  await expect.poll(async()=>(await snap())?.materialState?.colors.MAT_Seat_Stitching).toBe('#72c4e1');
  const before=await snap();const canvas=await page.locator('canvas').elementHandle();
  await page.getByRole('button',{name:'Previous step'}).click();
  await expect(page.getByRole('button',{name:'02 Colour',exact:true})).toHaveAttribute('aria-current','step');
  await expect.poll(async()=>(await snap())?.materialState).toEqual(before?.materialState);
  expect.soft((await snap())?.cameraPosition).toEqual(before?.cameraPosition);
  await page.getByRole('button',{name:'Reset configuration',exact:true}).click();
  await expect.soft(page.getByRole('button',{name:'Keep my design',exact:true})).toBeVisible({timeout:3000});
  expect.soft((await snap())?.assetUrl).toEqual(before?.assetUrl);
  if(await page.getByRole('button',{name:'Keep my design',exact:true}).isVisible()) {
   await page.getByRole('button',{name:'Keep my design',exact:true}).click();
   expect((await snap())?.materialState).toEqual(before?.materialState);
   await page.getByRole('button',{name:'Your specification',exact:true}).click();
   await expect(page.locator('[data-component=SpecificationSummary]')).toContainText('Forest Green');
   await expect(page.locator('[data-component=SpecificationSummary]')).toContainText('Warm Stone');
   await page.getByRole('button',{name:'Previous step'}).click();
   expect(await canvas!.evaluate(el=>el.isConnected)).toBe(true);
   await mkdir('docs/evidence/back-fix',{recursive:true});
   await page.screenshot({path:`docs/evidence/back-fix/preserved-${width}.png`});
   await writeFile(`docs/evidence/back-fix/state-${width}.json`,JSON.stringify({before,after:await snap()},null,2));
   await page.getByRole('button',{name:'Reset configuration',exact:true}).click();
   await page.getByRole('button',{name:'Reset all choices',exact:true}).click();
   await expect(page.getByRole('button',{name:'01 Material',exact:true})).toHaveAttribute('aria-current','step');
   await expect(page.getByRole('radio',{name:'Classic',exact:true})).toHaveAttribute('aria-checked','true');
  }
 });
}

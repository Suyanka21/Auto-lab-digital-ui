import { test, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const folder='docs/evidence/atelier';
const colours=[['Oxblood Burgundy','#602c39'],['Forest Green','#294b40'],['Midnight Navy','#293d58'],['Saddle Tan','#ad7950'],['Warm Stone','#95897b']] as const;
for(const width of [1440,390]) {
 test(`atelier imagery and expanded live palette at ${width}`,async({page})=>{
  test.setTimeout(180000);await mkdir(folder,{recursive:true});
  const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
  await page.setViewportSize({width,height:900});await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
  const hero=page.locator('.cover-art img');
  await expect(hero).toHaveAttribute('src',/atelier-workbench/);
  await expect.poll(()=>hero.evaluate(el=>(el as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
  await page.screenshot({path:`${folder}/hero-${width}.png`});
  const invitation=page.locator('.editorial-invitation');await invitation.scrollIntoViewIfNeeded();
  await expect.poll(()=>invitation.locator('img').evaluate(el=>(el as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
  await invitation.screenshot({path:`${folder}/invitation-${width}.png`});
  await invitation.getByRole('button',{name:'Enter the Studio'}).click();
  const snapshot=()=>page.evaluate(()=>window.__autolab?.snapshot());
  await expect.poll(async()=>(await snapshot())?.status,{timeout:60000}).toBe('success');
  await page.getByRole('button',{name:'02 Colour',exact:true}).click();
  const primary=page.getByRole('radiogroup',{name:'Primary hide colour',exact:true});
  await expect(primary.getByRole('radio')).toHaveCount(8);
  for(const [name,hex] of colours) {
   await primary.getByRole('radio',{name,exact:true}).click();
   await expect.poll(async()=>(await snapshot())?.materialState?.colors.MAT_Seat_Primary).toBe(hex);
   await expect.poll(async()=>(await snapshot())?.materialState?.colors.MAT_Seat_Secondary).toBe(hex);
  }
  await primary.getByRole('radio',{name:'Oxblood Burgundy',exact:true}).click();
  await primary.getByRole('radio',{name:'Oxblood Burgundy',exact:true}).press('ArrowRight');
  await expect(primary.getByRole('radio',{name:'Forest Green',exact:true})).toHaveAttribute('aria-checked','true');
  await page.getByRole('button',{name:'Enable Two-tone'}).click();
  const secondary=page.getByRole('radiogroup',{name:'Secondary hide colour',exact:true});
  await expect(secondary.getByRole('radio',{name:'Forest Green',exact:true})).toBeDisabled();
  await secondary.getByRole('radio',{name:'Warm Stone',exact:true}).click();
  await expect.poll(async()=>(await snapshot())?.materialState?.colors.MAT_Seat_Secondary).toBe('#95897b');
  await expect.poll(async()=>(await snapshot())?.materialState?.colors.MAT_Steering_Leather).toBe('#95897b');
  await page.screenshot({path:`${folder}/studio-palette-${width}.png`});
  for(const name of ['Diamond Quilted','Perforated']) {
   await page.getByRole('button',{name:'01 Material',exact:true}).click();
   await page.getByRole('radio',{name,exact:true}).click();
   await expect.poll(async()=>(await snapshot())?.assetUrl).toContain(name==='Perforated'?'perforated':'diamond');
   await expect.poll(async()=>(await snapshot())?.status,{timeout:60000}).toBe('success');
   await expect.poll(async()=>(await snapshot())?.materialState?.colors.MAT_Seat_Primary).toBe('#294b40');
  }
  const box=await page.locator('[data-component=CabinViewer]').boundingBox();
  expect(box!.y).toBeGreaterThanOrEqual(0);expect(box!.y+box!.height).toBeLessThanOrEqual(900);
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
  expect(await page.evaluate(()=>document.documentElement.scrollHeight)).toBeLessThanOrEqual(900);
  await expect(page.locator('canvas')).toHaveCount(1);expect(errors).toEqual([]);
  await writeFile(`${folder}/scene-${width}.json`,JSON.stringify({snapshot:await snapshot(),errors},null,2));
 });
}

test('normal build atelier layout and reduced motion at narrow and intermediate widths',async({page})=>{
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
 for(const width of [320,768,1024]) {
  await page.setViewportSize({width,height:900});
  expect(await page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
  expect(await page.locator('.cover-art img').evaluate(el=>getComputedStyle(el).animationName)).toBe('none');
  await page.locator('.editorial-invitation').scrollIntoViewIfNeeded();
  await expect(page.locator('.editorial-invitation').getByRole('button',{name:'Enter the Studio'})).toBeVisible();
 }
 await expect(page.locator('canvas')).toHaveCount(0);
 await page.locator('.editorial-invitation').getByRole('button',{name:'Enter the Studio'}).click();
 await page.getByRole('button',{name:'02 Colour',exact:true}).click();
 await expect(page.getByRole('radiogroup',{name:'Primary hide colour',exact:true}).getByRole('radio')).toHaveCount(8);
});

import { test, expect, type Page } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const folder='docs/evidence/final';
const snap=(page:Page)=>page.evaluate(()=>window.__autolab?.snapshot());
const ready=async(page:Page)=>expect.poll(async()=>(await snap(page))?.status,{timeout:60000}).toBe('success');
const step=(page:Page,name:string)=>page.getByRole('button',{name:new RegExp('^0[1-6] '+name)}).click();
test('desktop evidence and retained state after leaving Studio',async({page})=>{
 test.setTimeout(120000);await mkdir(folder,{recursive:true});const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 const started=Date.now();await page.goto('/studio');await ready(page);const loadMs=Date.now()-started;
 await page.screenshot({path:`${folder}/desktop-studio.png`,fullPage:true});
 const scene=await snap(page);expect(scene?.renderer?.calls).toBe(24);
 expect(Object.values(scene?.materialState?.textures??{}).every(t=>t.compressed && t.mips>1)).toBe(true);
 await step(page,'Colour');await page.getByRole('radiogroup',{name:'Primary hide colour',exact:true}).getByRole('radio',{name:/Sienna Brown/}).click();
 await page.getByRole('button',{name:'Showroom',exact:true}).first().click();await expect(page.locator('canvas')).toHaveCount(0);
 await page.screenshot({path:`${folder}/desktop-welcome.png`,fullPage:true});
 await page.getByRole('button',{name:'Enter the Studio',exact:true}).first().click();await ready(page);
 await expect.poll(async()=>(await snap(page))?.materialState?.colors.MAT_Seat_Primary).toBe('#7b4a2d');
 await expect(page.locator('canvas')).toHaveCount(1);
 await writeFile(`${folder}/desktop-metrics.json`,JSON.stringify({browser:'Edge headless / SwiftShader',viewport:'1440x900',loadMs,scene,errors},null,2));expect(errors).toEqual([]);
});
test('mobile reduced motion, menu focus and narrow layouts',async({page})=>{
 test.setTimeout(120000);await page.setViewportSize({width:390,height:844});await page.emulateMedia({reducedMotion:'reduce'});
 await page.goto('/studio');await ready(page);await page.screenshot({path:`${folder}/mobile-studio.png`,fullPage:true});
 await page.getByRole('button',{name:'Open navigation menu'}).click();
 const menu=page.getByRole('navigation',{name:'Mobile navigation'});await expect(menu.getByRole('button').first()).toBeFocused();
 await page.keyboard.press('Shift+Tab');await expect(page.getByRole('button',{name:'Close navigation menu'})).toBeFocused();
 await page.keyboard.press('Escape');await expect(page.getByRole('button',{name:'Open navigation menu'})).toBeFocused();await expect(menu).toHaveCount(0);
 await step(page,'Colour');await page.getByRole('radiogroup',{name:'Primary hide colour',exact:true}).getByRole('radio',{name:/Sienna Brown/}).click();
 await expect.poll(async()=>(await snap(page))?.materialState?.colors.MAT_Seat_Primary).toBe('#7b4a2d');
 await page.getByRole('button',{name:'Enable Two-tone'}).click();
 const secondary=page.getByRole('radiogroup',{name:'Secondary hide colour',exact:true});await secondary.getByRole('radio',{checked:true}).focus();await page.keyboard.press('ArrowDown');
 await expect(secondary.getByRole('radio',{name:/Sienna Brown/})).toBeDisabled();
 const widths=[];for(const width of [320,390,768,1024,1440]){await page.setViewportSize({width,height:900});await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);widths.push(width);}
 await page.setViewportSize({width:390,height:844});await step(page,'Composition');await expect(page.getByText(/Primary colour defines seat centres/)).toBeVisible();
 await page.screenshot({path:`${folder}/mobile-two-tone.png`,fullPage:true});
 expect(await page.evaluate(()=>getComputedStyle(document.querySelector('button')!).transitionDuration)).toBe('1e-05s');
 await writeFile(`${folder}/responsive.json`,JSON.stringify({widths,reducedMotion:true,physicalPhone:false,scene:await snap(page)},null,2));
});
test('failed GLB recovers and retains selected colour',async({page})=>{
 test.setTimeout(120000);await page.route('**/interior-l4-classic.glb*',r=>r.fulfill({status:503,body:'intentional test failure'}));
 await page.goto('/studio');await expect(page.getByRole('button',{name:'Retry 3D'})).toBeVisible();
 await step(page,'Colour');await page.getByRole('radiogroup',{name:'Primary hide colour',exact:true}).getByRole('radio',{name:/Light Ivory/}).click();
 await page.screenshot({path:`${folder}/recovery-error.png`,fullPage:true});
 await page.unroute('**/interior-l4-classic.glb*');await page.getByRole('button',{name:'Retry 3D'}).click();await ready(page);
 await expect.poll(async()=>(await snap(page))?.materialState?.colors.MAT_Seat_Primary).toBe('#ddd5c7');
 await page.evaluate(()=>window.__autolab?.loseContext());await expect(page.getByRole('button',{name:'Retry 3D'})).toBeVisible();
 await page.getByRole('button',{name:'Retry 3D'}).click();await ready(page);await expect(page.locator('canvas')).toHaveCount(1);
});
test('WebGL unavailable preserves usable controls and summary',async({page})=>{
 await page.addInitScript(()=>{const original=HTMLCanvasElement.prototype.getContext;HTMLCanvasElement.prototype.getContext=function(...args:Parameters<typeof original>){if(String(args[0]).startsWith('webgl'))return null;return original.apply(this,args);} as typeof original;});
 await page.goto('/studio');await expect(page.getByRole('button',{name:'Retry 3D'})).toBeVisible();
 await page.getByRole('button',{name:'Your specification'}).click();
 await expect(page.locator('[data-component=SpecificationSummary]')).toBeVisible();
 await page.getByRole('button',{name:'01 Material',exact:true}).click();
 await page.getByRole('radio',{name:/^Perforated/}).click();await expect(page.getByRole('radio',{name:/^Perforated/})).toHaveAttribute('aria-checked','true');
});

for (const [label, pattern] of [['KTX2 transcoder', '**/basis/*'], ['trim texture', '**/trim-preview/walnut.ktx2*']] as const) {
 test(`${label} failure is explicit and Retry recovers`, async ({page})=>{
  test.setTimeout(120000); await page.route(pattern,r=>r.fulfill({status:503,body:'intentional dependency failure'}));
  await page.goto('/studio');await expect(page.getByRole('button',{name:'Retry 3D'})).toBeVisible({timeout:60000});
  await expect(page.getByTestId('viewer-status')).toContainText('unavailable');
  await page.unroute(pattern);await page.getByRole('button',{name:'Retry 3D'}).click();await ready(page);
  await expect(page.locator('canvas')).toHaveCount(1);
 });
}

import { test, expect } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
test.use({video:'on'});
for (const viewport of [{width:1440,height:900},{width:390,height:844}]) {
 test(`cabin stays visible through the complete journey at ${viewport.width}px`,async({page})=>{
  test.setTimeout(120000);await page.setViewportSize(viewport);await page.goto('/studio');
  await expect(page.getByTestId('spike-viewer')).toHaveAttribute('aria-busy','false',{timeout:60000});
  await mkdir('docs/evidence/cinematic',{recursive:true});
  await page.screenshot({path:`docs/evidence/cinematic/studio-${viewport.width}.png`});
  const cabin=page.locator('[data-component=CabinViewer]');
  for(const step of ['Material','Colour','Accent Thread','Composition','Cabin Trim','Ambient Light']){
   await page.getByRole('button',{name:new RegExp('^0[1-6] '+step+'$')}).click();
   const options=page.getByRole('radio');await options.last().click();
   if(step==='Colour')await page.screenshot({path:`docs/evidence/cinematic/colour-${viewport.width}.png`});
   const box=await cabin.boundingBox();expect(box).not.toBeNull();expect(box!.y).toBeGreaterThanOrEqual(0);expect(box!.y+box!.height).toBeLessThan(viewport.height);
   expect(await page.evaluate(()=>window.scrollY)).toBe(0);
   expect(await page.evaluate(()=>document.documentElement.scrollHeight)).toBeLessThanOrEqual(viewport.height);
  }
  await page.getByRole('button',{name:'Review Specification',exact:true}).click();
  await expect(page.locator('[data-component=SpecificationSummary]')).toBeVisible();
  await expect(page.locator('canvas')).toHaveCount(1);
  await page.screenshot({path:`docs/evidence/cinematic/review-${viewport.width}.png`});
  await writeFile(`docs/evidence/cinematic/scene-${viewport.width}.json`,JSON.stringify(await page.evaluate(()=>window.__autolab?.snapshot()),null,2));
  const video=page.video();await page.close();await video?.saveAs(`docs/evidence/cinematic/journey-${viewport.width}.webm`);
 });
}

test('swipe, back and reduced motion keep one live stage',async({page})=>{
 test.setTimeout(90000);await page.setViewportSize({width:390,height:844});await page.goto('/studio');
 await expect.poll(()=>page.evaluate(()=>window.__autolab?.snapshot().status),{timeout:60000}).toBe('success');
 const canvas=await page.locator('canvas').elementHandle();
 const header=page.locator('.studio-panel-heading');
 await header.evaluate(el=>{
  const touch=(x:number,y:number)=>new Touch({identifier:1,target:el,clientX:x,clientY:y});
  el.dispatchEvent(new TouchEvent('touchstart',{bubbles:true,touches:[touch(300,500)]}));
  el.dispatchEvent(new TouchEvent('touchend',{bubbles:true,changedTouches:[touch(80,505)]}));
 });
 await expect(page.getByRole('button',{name:'02 Colour',exact:true})).toHaveAttribute('aria-current','step');
 await page.getByRole('button',{name:'Previous step'}).click();
 await expect(page.getByRole('button',{name:'01 Material',exact:true})).toHaveAttribute('aria-current','step');
 await page.emulateMedia({reducedMotion:'reduce'});
 await page.getByRole('button',{name:'03 Accent Thread',exact:true}).click();
 expect(await page.locator('.studio-slide-track').evaluate(el=>getComputedStyle(el).transitionProperty)).toBe('none');
 await page.getByRole('radio',{name:'Warm Ochre',exact:true}).focus();await page.keyboard.press('ArrowRight');
 await expect(page.getByRole('radio',{name:'Atelier Cyan',exact:true})).toHaveAttribute('aria-checked','true');
 expect(await canvas!.evaluate(el=>el.isConnected)).toBe(true);
 await expect.poll(()=>page.evaluate(()=>window.__autolab?.snapshot().cameraPosition?.map(n=>Number(n.toFixed(6))))).toEqual([.68,.85,.45]);
 await page.getByRole('button',{name:'05 Cabin Trim',exact:true}).click();
 await expect.poll(()=>page.evaluate(()=>window.__autolab?.snapshot().cameraPosition?.map(n=>Number(n.toFixed(6))))).toEqual([0,1.25,-1.05]);
 for(const size of [{width:320,height:568},{width:768,height:1024},{width:1024,height:768}]){
  await page.setViewportSize(size);
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(size.width);
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollHeight)).toBeLessThanOrEqual(size.height);
 }
});

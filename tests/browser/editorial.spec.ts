import { test, expect } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
test.use({video:'on'});
for (const width of [1440,390]) {
 test(`editorial presentation and navigation at ${width}`,async({page})=>{
  await mkdir('docs/evidence/editorial',{recursive:true});
  await page.setViewportSize({width,height:900});await page.goto('/');
  await page.screenshot({path:`docs/evidence/editorial/cover-${width}.png`});
  const cover=page.locator('[data-component=EditorialCover]');
  await expect(cover.getByRole('button',{name:'Pause motion'})).toBeVisible({timeout:5000});
  await cover.getByRole('button',{name:'Pause motion'}).click();
  await expect(cover).toHaveAttribute('data-motion','still');
  await cover.getByRole('button',{name:'View study: Diamond Quilted'}).click();
  await expect(cover.getByRole('button',{name:'View study: Diamond Quilted'})).toHaveAttribute('aria-pressed','true');
  await expect(cover).toContainText('AI-generated material studies');
  await expect(page.locator('canvas')).toHaveCount(0);
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
  await page.emulateMedia({reducedMotion:'reduce'});
  expect(await cover.locator('.cover-art img').evaluate(el=>getComputedStyle(el).animationName)).toBe('none');
  await page.screenshot({path:`docs/evidence/editorial/landing-${width}.png`,fullPage:true});
  await cover.getByRole('button',{name:'Enter the Studio',exact:true}).click();
  await expect(page).toHaveURL(/studio$/);
  await expect(page.locator('[data-component=StudioPage]')).toBeVisible();
  const video=page.video();await page.close();await video?.saveAs(`docs/evidence/editorial/presentation-${width}.webm`);
 });
}

test('material gallery keyboard selection and intermediate layouts',async({page})=>{
 const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
 await page.emulateMedia({reducedMotion:'reduce'});await page.goto('/');
 const choices=page.getByRole('radiogroup',{name:'Explore material studies'});
 await choices.getByRole('radio',{name:/Classic/}).click();
 await expect(page.locator('.material-feature img')).toHaveAttribute('src',/classic-study/);
 await choices.getByRole('radio',{name:/Classic/}).press('ArrowRight');
 await expect(choices.getByRole('radio',{name:/Diamond Quilted/})).toHaveAttribute('aria-checked','true');
 await expect.poll(()=>page.locator('.material-feature img').evaluate(el=>(el as HTMLImageElement).naturalWidth)).toBeGreaterThan(0);
 for(const width of [320,768,1024]) {
  await page.setViewportSize({width,height:900});
  await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollWidth)).toBeLessThanOrEqual(width);
  await page.getByRole('heading',{level:1}).scrollIntoViewIfNeeded();
  await page.screenshot({path:`docs/evidence/editorial/cover-${width}.png`});
 }
 expect(errors).toEqual([]);await expect(page.locator('canvas')).toHaveCount(0);
});

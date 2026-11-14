import { test, expect } from '@playwright/test';
import { mkdir } from 'node:fs/promises';
test.use({video:'on'});
for(const width of [1440,390]) {
 test(`tactile selectors retain a visible live cabin at ${width}`,async({page})=>{
  test.setTimeout(150000);await mkdir('docs/evidence/editorial',{recursive:true});
  await page.setViewportSize({width,height:900});await page.goto('/studio');
  const ready=()=>expect(page.getByTestId('spike-viewer')).toHaveAttribute('aria-busy','false',{timeout:60000});await ready();
  const active=page.locator('.studio-slide[aria-hidden="false"]');
  await expect(active.locator('.treatment-study img')).toBeVisible();
  await page.getByRole('radio',{name:'Diamond Quilted',exact:true}).click();await ready();
  await expect(active.locator('.treatment-study img')).toHaveAttribute('src',/diamond-study/);
  await page.screenshot({path:`docs/evidence/editorial/studio-material-${width}.png`});
  await page.getByRole('button',{name:'02 Colour',exact:true}).click();
  await page.getByRole('radio',{name:'Sienna Brown',exact:true}).click();
  await page.getByRole('button',{name:'Enable Two-tone'}).click();
  await page.getByRole('radiogroup',{name:'Secondary hide colour',exact:true}).getByRole('radio',{name:'Light Ivory',exact:true}).click();
  await page.screenshot({path:`docs/evidence/editorial/studio-colour-${width}.png`});
  for(const name of ['03 Accent Thread','04 Composition','05 Cabin Trim','06 Ambient Light']) {
   await page.getByRole('button',{name,exact:true}).click();
   await active.getByRole('radio').last().click();
   await expect(active.getByRole('radio').last()).toHaveAttribute('aria-checked','true');
   const box=await page.locator('[data-component=CabinViewer]').boundingBox();expect(box!.y).toBeGreaterThanOrEqual(0);expect(box!.y+box!.height).toBeLessThanOrEqual(900);
   await expect.poll(()=>page.evaluate(()=>document.documentElement.scrollHeight)).toBeLessThanOrEqual(900);
   await page.screenshot({path:`docs/evidence/editorial/studio-${name.slice(0,2)}-${width}.png`});
  }
  await expect(page.locator('canvas')).toHaveCount(1);
  const video=page.video();await page.close();await video?.saveAs(`docs/evidence/editorial/selectors-${width}.webm`);
 });
}

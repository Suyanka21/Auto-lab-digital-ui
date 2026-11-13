import { test, expect } from '@playwright/test';
import { createHash } from 'node:crypto';
import { writeFile } from 'node:fs/promises';
test.use({video:'on'});
test('normal build has real assets and no test diagnostics',async({page})=>{
 test.setTimeout(150000);const errors:string[]=[];page.on('pageerror',e=>errors.push(e.message));
 const hashes:Record<string,string>={};const pending:Promise<void>[]=[];
 page.on('response',response=>{if(response.url().includes('.glb?'))pending.push(response.body().then(bytes=>{hashes[response.url().split('/').at(-1)!.split('?')[0]]=createHash('sha256').update(bytes).digest('hex');}));});
 await page.goto('/studio');
 const ready=async()=>{await expect(page.getByTestId('spike-viewer')).toHaveAttribute('aria-busy','false',{timeout:60000});await expect(page.getByTestId('viewer-status')).toHaveCount(0);await expect(page.locator('canvas')).toHaveCount(1);};
 await ready();expect(await page.evaluate(()=>window.__autolab)).toBeUndefined();
 await page.screenshot({path:'docs/evidence/final/release-desktop.png',fullPage:true});
 for(const name of ['Diamond Quilted','Perforated','Classic']){await page.getByRole('radio',{name:new RegExp('^'+name)}).click();await ready();}
 await page.getByRole('button',{name:/^02 Colour/}).click();await page.getByRole('radiogroup',{name:'Primary hide colour',exact:true}).getByRole('radio',{name:/Sienna Brown/}).click();
 await page.getByRole('button',{name:'Enable Two-tone'}).click();
 await page.getByRole('button',{name:/^02 Cabin Pair/}).click();
 await page.screenshot({path:'docs/evidence/final/release-console.png',fullPage:true});
 await page.getByRole('button',{name:/^03 Accent Thread/}).click();await page.getByRole('radio',{name:/Atelier Cyan/}).click();
 await page.getByRole('button',{name:/^03 Cockpit & Dash/}).click();
 await page.getByRole('button',{name:/^04 Stitch Detail/}).click();
 await page.getByRole('button',{name:/^01 Driver Hero/}).click();
 await page.getByRole('button',{name:'Your specification'}).click();
 await expect(page.locator('[data-component=SpecificationSummary]')).toContainText('Sienna Brown');
 await Promise.all(pending);
 expect(hashes).toEqual({'interior-l4-classic.glb':'e5bdde016348df34889ec4c0ff0e406caad7e368504308bd5a4f5b725a55c056','interior-l4-diamond.glb':'4c217dd00d86d8bae3925d735beddb63b225d24c5f1bafd60726f501bfcba8ad','interior-l4-perforated.glb':'d53f55546232db473ecadee08be9bff6454b5d3a510ee30e88415f2477ca9f9e'});
 expect(errors).toEqual([]);await writeFile('docs/evidence/final/release-network.json',JSON.stringify({hashes,errors,testDiagnostics:false},null,2));
 const video=page.video();await page.close();await video?.saveAs('docs/evidence/final/showroom-interactions.webm');
});

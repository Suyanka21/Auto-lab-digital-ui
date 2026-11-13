import { chromium } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const folder = 'docs/evidence/baseline';
await mkdir(folder,{recursive:true});
const browser = await chromium.launch({channel:'msedge',headless:true});
try {
  const errors=[];
  for (const [width,height] of [[1440,900],[390,844]]) {
    const page=await browser.newPage({viewport:{width,height}});
    page.on('pageerror',error=>errors.push(error.message));
    await page.goto('http://127.0.0.1:5173/',{waitUntil:'networkidle',timeout:60000});
    await page.screenshot({path:`${folder}/landing-${width}.png`,fullPage:true});
    await page.getByRole('button',{name:'Enter the Studio',exact:true}).first().click();
    await page.locator('[data-component="StudioPage"]').waitFor();
    await page.screenshot({path:`${folder}/studio-${width}.png`,fullPage:true});
    await page.close();
  }
  await writeFile(`${folder}/result.json`,JSON.stringify({errors},null,2));
  if(errors.length)throw new Error(errors.join('\n'));
} finally {await browser.close();}

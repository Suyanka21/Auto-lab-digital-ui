import { test, expect, type Page } from '@playwright/test';
import { mkdir, writeFile } from 'node:fs/promises';
const folder='docs/evidence/interactions';
const snap=(page:Page)=>page.evaluate(()=>window.__autolab?.snapshot());
const step=(page:Page,name:string)=>page.getByRole('button',{name:new RegExp('^0[1-6] '+name)}).click();
async function ready(page:Page){await expect.poll(async()=> (await snap(page))?.status,{timeout:60000}).toBe('success');}
async function colour(page:Page,slot:string,hex:string){await expect.poll(async()=> (await snap(page))?.materialState?.colors[slot]).toBe(hex.toLowerCase());}
test('all real materials, composition, thread, cameras, trim and lights',async({page})=>{
  test.setTimeout(180000);
  const errors:string[]=[];page.on('pageerror',error=>errors.push(error.message));
  await page.goto('/');await page.getByRole('button',{name:'Enter the Studio',exact:true}).first().click();await ready(page);
  await expect(page.locator('canvas')).toHaveCount(1);
  expect((await snap(page))?.cameraPosition?.map(v=>Number(v.toFixed(6)))).toEqual([1.45,1.25,.95]);
  await step(page,'Colour');await page.getByRole('radiogroup',{name:'Primary hide colour',exact:true}).getByRole('radio',{name:/Sienna Brown/}).click();
  await colour(page,'MAT_Seat_Primary','#7B4A2D');await colour(page,'MAT_Seat_Secondary','#7B4A2D');
  await page.getByRole('button',{name:'Enable Two-tone'}).click();
  await page.getByRole('radiogroup',{name:'Secondary hide colour',exact:true}).getByRole('radio',{name:/Light Ivory/}).click();
  await colour(page,'MAT_Seat_Secondary','#DDD5C7');await colour(page,'MAT_Steering_Leather','#DDD5C7');await colour(page,'MAT_Dashboard_Trim','#2A2B2E');
  await step(page,'Accent Thread');await page.getByRole('radio',{name:/Atelier Cyan/}).click();await colour(page,'MAT_Seat_Stitching','#72C4E1');
  await step(page,'Material');await page.getByRole('radio',{name:/Diamond Quilted/}).click();
  await expect.poll(async()=> (await snap(page))?.materialState?.quiltThread).toBe(true);
  await colour(page,'MAT_Seat_Primary','#7B4A2D');await colour(page,'MAT_Seat_Stitching','#72C4E1');
  await mkdir(folder,{recursive:true});await page.screenshot({path:`${folder}/diamond-two-tone.png`,fullPage:true});
  const views=[['Cabin Pair',[0,1.25,-1.05]],['Cockpit & Dash',[1,1.12,.05]],['Stitch Detail',[.68,.85,.45]],['Driver Hero',[1.45,1.25,.95]]] as const;
  for(const [name,position] of views){await page.getByRole('button',{name:new RegExp('0[1-4] '+name)}).click();await expect.poll(async()=> (await snap(page))?.cameraPosition?.map(v=>Number(v.toFixed(6)))).toEqual([...position]);}
  for(const name of ['Perforated','Classic','Diamond Quilted','Classic']){await page.getByRole('radio',{name:new RegExp(name)}).click();await expect.poll(async()=> (await snap(page))?.assetUrl).toContain(name==='Diamond Quilted'?'diamond':name.toLowerCase());await ready(page);await colour(page,'MAT_Seat_Stitching','#72C4E1');}
  await step(page,'Composition');await page.getByRole('radio',{name:/^Single-colour/}).click();await colour(page,'MAT_Seat_Secondary','#7B4A2D');
  await step(page,'Cabin Trim');
  for(const [name,id] of [['Walnut Wood','open-pore-walnut'],['Poplar Wood','open-pore-poplar'],['Piano Lacquer','piano-lacquer-flowing-lines'],['Carbon Fibre','autolab-twill-carbon']]){await page.getByRole('radio',{name:new RegExp(name)}).click();await expect.poll(async()=> (await snap(page))?.materialState?.trim?.id).toBe(id);}
  await step(page,'Ambient Light');
  for(const [name,hex] of [['Amber','#d8964b'],['Rose','#c98986'],['Ocean','#3b6f8a'],['Champagne','#d8c7a8'],['Cyan','#72c4e1']]){await page.getByRole('radio',{name:new RegExp(name)}).click();await expect.poll(async()=> (await snap(page))?.materialState?.ambient).toEqual([hex,hex,hex]);}
  await page.getByRole('button',{name:/02 Cabin Pair/}).click();await page.screenshot({path:`${folder}/cabin-console.png`,fullPage:true});
  await writeFile(`${folder}/actual-scene.json`,JSON.stringify({snapshot:await snap(page),errors},null,2));
  expect(errors).toEqual([]);expect((await snap(page))?.renderer?.calls).toBeLessThanOrEqual(24);
});

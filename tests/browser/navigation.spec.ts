import { test, expect } from '@playwright/test';
test('direct studio URL and browser back/forward', async ({page})=>{
 await page.goto('/studio');
 await expect(page.locator('[data-component=StudioPage]')).toBeVisible({timeout:5000});
 await page.getByRole('button',{name:'Showroom',exact:true}).first().click();
 await expect(page).toHaveURL(/\/$/); await page.goBack();
 await expect(page).toHaveURL(/\/studio$/);
 await expect(page.locator('[data-component=StudioPage]')).toBeVisible();
});
test('material radios support arrow keys',async({page})=>{
 await page.goto('/');await page.getByRole('button',{name:'Enter the Studio',exact:true}).first().click();
 const classic=page.getByRole('radio',{name:/^Classic/}); await classic.focus(); await classic.press('ArrowDown');
 await expect(page.getByRole('radio',{name:/^Diamond Quilted/})).toHaveAttribute('aria-checked','true',{timeout:5000});
});

test('mobile drawer releases background when resized to desktop',async({page})=>{
 await page.setViewportSize({width:390,height:844});await page.goto('/');
 await page.getByRole('button',{name:'Open navigation menu'}).click();
 await expect(page.locator('main')).toHaveAttribute('inert','');
 await page.setViewportSize({width:1024,height:900});
 await expect(page.getByRole('navigation',{name:'Mobile navigation'})).toHaveCount(0);
 await expect(page.locator('main')).not.toHaveAttribute('inert','');
});

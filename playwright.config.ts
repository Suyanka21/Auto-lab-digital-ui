import { defineConfig } from '@playwright/test';

export default defineConfig({
  testDir: 'tests/browser',
  timeout: 90000,
  workers: 1,
  expect: { timeout: 30000 },
  reporter: [['list'], ['json', { outputFile: 'docs/evidence/browser-results.json' }]],
  use: {
    channel: 'msedge',
    viewport: { width: 1440, height: 900 },
    launchOptions: { args: ['--use-angle=swiftshader', '--enable-unsafe-swiftshader'] },
    screenshot: 'only-on-failure',
    trace: 'retain-on-failure',
  },
  projects: [
    { name: 'runtime', testIgnore: '**/release.spec.ts', use: { baseURL: process.env.TEST_URL ?? 'http://127.0.0.1:4174' } },
    { name: 'release', testMatch: '**/release.spec.ts', use: { baseURL: process.env.RELEASE_URL ?? 'http://127.0.0.1:4173' } },
  ],
  outputDir: 'test-results',
});

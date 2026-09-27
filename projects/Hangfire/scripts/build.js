import './check.js';
import { mkdir, cp, writeFile } from 'node:fs/promises';
await mkdir('dist', { recursive: true });
for (const folder of ['server', 'client']) await cp(folder, 'dist/' + folder, { recursive: true });
await writeFile('dist/package.json', JSON.stringify({ private: true, type: 'module' }));
console.log('Build PASS: node dist/server/index.js (no bundler or install required)');

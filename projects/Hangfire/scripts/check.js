import { readdirSync } from 'node:fs';
import { spawnSync } from 'node:child_process';
for (const folder of ['server', 'client', 'scripts', 'test']) {
  for (const name of readdirSync(folder).filter(name => name.endsWith('.js'))) {
    const result = spawnSync(process.execPath, ['--check', folder + '/' + name], { stdio: 'inherit' });
    if (result.status !== 0) process.exit(result.status || 1);
  }
}
console.log('Syntax check PASS');

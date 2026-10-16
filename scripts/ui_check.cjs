// App smoke check (P1-S5/D-064/D-065): renders every role's card and all three detail tabs with the exported data in headless
// Chromium and fails on any page error or any blank colour tag. Run: node scripts/ui_check.cjs  (after `export`)
const path = require('path'), fs = require('fs');
const { chromium } = require(process.env.PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright');
(async () => {
  const root = path.resolve(__dirname, '..'), dir = path.join(root, 'data/state/app_export/jobs'), jobs = {};
  for (const f of fs.readdirSync(dir)) Object.assign(jobs, JSON.parse(fs.readFileSync(path.join(dir, f))).jobs);
  const desc = {}, dd = path.join(root, 'data/state/app_export/desc');
  if (fs.existsSync(dd)) for (const f of fs.readdirSync(dd)) desc[f.replace('.json', '')] = JSON.parse(fs.readFileSync(path.join(dd, f)));
  const cp = path.join(root, 'data/state/app_export/meta/company_profiles.json');
  const cprof = fs.existsSync(cp) ? JSON.parse(fs.readFileSync(cp)).companies : {};
  const b = await chromium.launch(), p = await b.newPage(), errs = [];
  p.on('pageerror', e => errs.push(e.message));
  await p.goto('file://' + path.join(root, 'app/lodestone.html')); await p.waitForTimeout(300);
  const r = await p.evaluate(([jobs, desc, cprof]) => {
    S.jobs = jobs; S.desc = desc; S.cprof = cprof; S.ready = true; S.offline = false; let n = 0; const bad = [];
    for (const j of Object.values(jobs)) {
      try { card(j, 0); for (const t of ['summary', 'jd', 'company']) { S.dtab = t; viewDetail(j) } for (const c of prefChecks(j)) { n++; if (!c.t || !c.t.trim() || !c.why) bad.push(j.id + ' ' + c.k) } }
      catch (e) { bad.push(j.id + ' ' + e.message) }
    }
    return { roles: Object.keys(jobs).length, checks: n, bad: bad.slice(0, 10), nbad: bad.length };
  }, [jobs, desc, cprof]);
  await b.close();
  console.log(JSON.stringify({ ...r, pageErrors: errs.slice(0, 5) }));
  process.exit(r.nbad || errs.length ? 1 : 0);
})();

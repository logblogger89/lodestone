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
  let triage0 = null;
  if (process.env.TRIAGE_DIR) { triage0 = {}; for (const f of fs.readdirSync(process.env.TRIAGE_DIR)) { const d = JSON.parse(fs.readFileSync(path.join(process.env.TRIAGE_DIR, f))); triage0[f.replace('.json', '')] = d.data || d } }
  const r = await p.evaluate(([jobs, desc, cprof, triage0]) => {
    S.jobs = jobs; S.desc = desc; S.cprof = cprof; S.ready = true; S.offline = false; let n = 0; const bad = [];
    for (const j of Object.values(jobs)) {
      try { card(j, 0); for (const t of ['summary', 'jd', 'company']) { S.dtab = t; viewDetail(j) } for (const c of prefChecks(j)) { n++; if (!c.t || !c.t.trim() || !c.why) bad.push(j.id + ' ' + c.k) } }
      catch (e) { bad.push(j.id + ' ' + e.message) }
    }
    // P1-S6: Today list, learning, suggestions and the Profile learning panel, with a made-up triage (or TRIAGE_DIR's real one)
    const ids = Object.values(jobs).filter(j => j.live && fitScore(j) != null).sort((a, b) => fitScore(b) - fitScore(a)).map(j => j.id);
    const tri = triage0 || {};
    if (!triage0) { ids.slice(0, 6).forEach(id => tri[id] = { status: 'interested' }); ids.slice(-6).forEach(id => tri[id] = { status: 'not', reasons: ['Pay too low', 'Company'] }) }
    S.triage = tri; S.triLoaded = true; S.todayLoaded = true; S.today = null; S.likes = triage0 ? {} : { [ids[10]]: { v: 1 } }; S.sig = triage0 ? {} : { [ids[11]]: { read_secs: 90 } };
    let learnInfo = {};
    try {
      S.view = 'digest'; S.show = 'today'; const html = viewDigest(); if (!S.today || !S.today.ids.length) bad.push('today: empty stack');
      if (!html.includes('left today')) bad.push('today: no header');
      S.show = 'todo'; viewDigest(); S.view = 'settings'; viewSettings();
      const sug = suggestionsList(); const m = learnMap(); const adj = Object.values(m).map(x => x.adj);
      for (const j of Object.values(jobs)) { learnLine(j); whyRanked(j); if (m[j.id] && Math.abs(m[j.id].adj) > LEARN_CAP) bad.push('learn cap ' + j.id) }
      const rc = rankingCheck();
      learnInfo = { today: S.today.ids.length, explore: !!S.today.explore, moved: adj.length, up: adj.filter(x => x > 0).length, down: adj.filter(x => x < 0).length, suggestions: sug.map(x => x.text), pairwise: rc.pairwise, learned: rc.learned, top25: rc.top25, pos: rc.pos };
    } catch (e) { bad.push('s6 ' + e.message + ' ' + (e.stack || '').split('\n')[1]) }
    return { roles: Object.keys(jobs).length, checks: n, bad: bad.slice(0, 10), nbad: bad.length, learnInfo };
  }, [jobs, desc, cprof, triage0]);
  await b.close();
  console.log(JSON.stringify({ ...r, pageErrors: errs.slice(0, 5) }));
  process.exit(r.nbad || errs.length ? 1 : 0);
})();

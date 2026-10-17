// Persona journeys (UX testing, D-072): runs the real app in headless Chromium against an in-memory copy of its database,
// seeded with the exported jobs plus each persona's own profile, settings and history, then plays that persona's tasks.
// Each task clicks through the UI like a person would, takes screenshots, and records checks (pass/fail) and UX notes.
//   node scripts/persona_test.cjs                 all personas
//   node scripts/persona_test.cjs priya tomas     some of them
//   OUT=<dir> node scripts/persona_test.cjs        where screenshots and results.json go (default: data/state/persona_runs/)
// Personas live in tests/personas/*.cjs; their stories are in docs/product/ux/PERSONAS.md.
const path = require('path'), fs = require('fs');
const { chromium } = require(process.env.PLAYWRIGHT || '/opt/node22/lib/node_modules/playwright');
const root = path.resolve(__dirname, '..'), exp = path.join(root, 'data/state/app_export');

function loadExport() {
  const db = {};
  for (const coll of ['jobs', 'meta', 'desc']) {
    const d = path.join(exp, coll); if (!fs.existsSync(d)) continue;
    for (const f of fs.readdirSync(d)) db[`${coll}/${f.replace('.json', '')}`] = JSON.parse(fs.readFileSync(path.join(d, f)));
  }
  const rd = path.join(root, 'data/state/reports');
  if (fs.existsSync(rd)) for (const f of fs.readdirSync(rd)) db[`reports/${f.replace('.json', '')}`] = JSON.parse(fs.readFileSync(path.join(rd, f)));
  return db;
}

// The fake database: the same calls the app makes on window.claude.use("db"), backed by a plain object, with live listeners.
const MOCK = `(() => {
  const store = window.__seed || {}; const subs = [];
  const SHARED = /^(jobs|desc|meta|reports)[/]/;   // the user's own docs survive a reload, like the real database
  try { const kept = JSON.parse(sessionStorage.getItem('__userdocs') || 'null'); if (kept) { Object.keys(store).filter(k => !SHARED.test(k)).forEach(k => delete store[k]); Object.assign(store, kept) } } catch (e) {}
  const persist = () => { try { sessionStorage.setItem('__userdocs', JSON.stringify(Object.fromEntries(Object.entries(store).filter(([k]) => !SHARED.test(k))))) } catch (e) {} };
  const clone = x => x == null ? x : JSON.parse(JSON.stringify(x));
  const docsIn = c => Object.keys(store).filter(k => k.startsWith(c + '/') && !k.slice(c.length + 1).includes('/'))
    .map(k => ({ id: k.slice(c.length + 1), exists: true, data: () => clone(store[k]) }));
  const snapDoc = p => ({ id: p.split('/').pop(), exists: p in store, data: () => clone(store[p]) });
  const notify = () => { persist(); setTimeout(() => subs.forEach(s => s()), 0) };
  const writes = window.__writes = [];
  const db = {
    collection: c => ({
      onSnapshot: (cb) => { const f = () => cb({ docs: docsIn(c) }); subs.push(f); setTimeout(f, 5); return () => {} },
      add: async d => { const id = Math.random().toString(16).slice(2, 14); store[c + '/' + id] = clone(d); writes.push(['add', c + '/' + id]); notify(); return { id } },
    }),
    doc: p => ({
      onSnapshot: (cb) => { const f = () => cb(snapDoc(p)); subs.push(f); setTimeout(f, 5); return () => {} },
      get: async () => snapDoc(p),
      set: async d => { store[p] = clone(d); writes.push(['set', p]); notify() },
      delete: async () => { delete store[p]; writes.push(['delete', p]); notify() },
    }),
  };
  window.__store = store;
  document.addEventListener('DOMContentLoaded', () => {   // claude.ai adds this when publishing; the local file has none
    if (!document.querySelector('meta[name=viewport]')) { const m = document.createElement('meta'); m.name = 'viewport'; m.content = 'width=device-width, initial-scale=1'; document.head.appendChild(m) }
  });
  window.claude = { use: async n => n === 'db' ? db : n === 'user' ? { can: async () => true }
    : n === 'assets' ? { upload: async f => { writes.push(['upload', f.name]); return { id: 'asset1', contentType: f.type } } } : null };
})();`;

function helpers(page, persona, out, log) {
  const res = { persona: persona.id, tasks: [] }; let task = null, n = 0;
  const h = {
    page,
    task(name) { task = { name, checks: [], notes: [] }; res.tasks.push(task); },
    async shot(label) { const f = `${persona.id}-${String(++n).padStart(2, '0')}-${label}.png`; await page.screenshot({ path: path.join(out, f), fullPage: false }); task && task.notes.push({ kind: 'shot', file: f }); return f },
    check(ok, what) { task.checks.push({ ok: !!ok, what }); if (!ok) log(`  ✕ ${persona.id}: ${what}`) },
    note(kind, text) { task.notes.push({ kind, text }) },   // kind: works | annoyance | bug | idea
    async click(sel) { await page.locator(sel + ' >> visible=true').first().click({ timeout: 4000 }); await page.waitForTimeout(150) },   // the phone layout hides the side menu
    async tap(text, within = 'body') { await page.locator(within).getByRole('button', { name: text, exact: false }).first().click({ timeout: 4000 }); await page.waitForTimeout(150) },
    async reload() { await page.reload(); await page.waitForFunction(() => typeof S !== "undefined" && S.ready && S.triLoaded && S.todayLoaded, null, { timeout: 8000 }); await page.waitForTimeout(250) },
    async has(text) { return (await page.locator('body').innerText()).includes(text) },
    async text(sel = '#view') { return page.locator(sel).innerText() },
    evalS: fn => page.evaluate(fn),
    store: () => page.evaluate(() => window.__store),
    writes: () => page.evaluate(() => window.__writes),
    wait: ms => page.waitForTimeout(ms),
  };
  return { h, res };
}

(async () => {
  const want = process.argv.slice(2), dir = path.join(root, 'tests/personas');
  const personas = fs.readdirSync(dir).filter(f => /^\d.*\.cjs$/.test(f)).map(f => require(path.join(dir, f)))
    .filter(p => !want.length || want.includes(p.id));
  const out = process.env.OUT || path.join(root, 'data/state/persona_runs'); fs.mkdirSync(out, { recursive: true });
  const base = loadExport(), jobs = Object.assign({}, ...Object.keys(base).filter(k => k.startsWith('jobs/')).map(k => base[k].jobs));
  const b = await chromium.launch(), all = []; let failed = 0;
  for (const p of personas) {
    const ctx = await b.newContext({ viewport: p.viewport || { width: 1280, height: 860 }, hasTouch: !!p.touch, isMobile: !!p.touch });
    const page = await ctx.newPage(), errs = [];
    page.on('pageerror', e => errs.push(e.message));
    const seed = { ...base, ...p.seed(jobs) };   // persona's own docs: profile/main, settings/prefs, triage/<id>, ...
    await page.addInitScript(`window.__seed=${JSON.stringify(seed)};`);
    await page.addInitScript(MOCK);
    if (p.localStorage) await page.addInitScript(`(${JSON.stringify(p.localStorage)}).forEach(([k,v])=>localStorage.setItem('lodestone:'+k,JSON.stringify(v)))`);
    await page.goto('file://' + path.join(root, 'app/lodestone.html'));
    await page.waitForFunction(() => typeof S !== "undefined" && S.ready && S.triLoaded && S.todayLoaded, null, { timeout: 8000 });
    await page.waitForTimeout(200);
    const { h, res } = helpers(page, p, out, console.log);
    console.log(`▶ ${p.id}: ${p.name}`);
    try { await p.run(h, jobs) } catch (e) { h.task('crashed'); h.check(false, 'Journey crashed: ' + e.message.split('\n')[0]) }
    // Invariants checked after every journey (10-17): what any user should be able to rely on, whatever they did.
    try {
      const inv = await page.evaluate(() => {
        if (typeof S === 'undefined' || !S.ready) return null;
        const js = Object.values(S.jobs), todo = js.filter(j => prefOk(j) && inPreferred(j) && isTodo(j)).length, T = S.today;
        return { todo, ids: T && T.ids ? T.ids.length : null, missing: T && T.ids ? T.ids.filter(id => !S.jobs[id]).length : 0,
                 famsOk: myFams().every(f => famById(f)), visibleNoRel: js.filter(j => prefOk(j) && j.rel == null && !j.captured).length };
      });
      if (inv) {
        h.task('Invariants');
        h.check(!errs.length, `No script errors (${errs.slice(0, 1).join('')})`);
        h.check(inv.ids === null || inv.todo === 0 || inv.ids > 0, `Today is never empty while matching roles exist (${inv.todo} matching, ${inv.ids} in Today)`);
        h.check(inv.missing === 0, `Every role in Today still exists (${inv.missing} missing)`);
        h.check(inv.famsOk, 'Saved role types are all known types');
        h.check(inv.visibleNoRel === 0, `Every visible role has a relevance score (${inv.visibleNoRel} without)`);
      }
    } catch (e) { h.task('Invariants'); h.check(false, 'Invariant check failed to run: ' + e.message.split('\n')[0]) }
    res.pageErrors = errs; if (errs.length) failed++;
    res.tasks.forEach(t => t.checks.forEach(c => { if (!c.ok) failed++ }));
    all.push(res); await ctx.close();
  }
  await b.close();
  fs.writeFileSync(path.join(out, 'results.json'), JSON.stringify(all, null, 1));
  for (const r of all) {
    const c = r.tasks.flatMap(t => t.checks), ok = c.filter(x => x.ok).length;
    console.log(`${r.persona}: ${ok}/${c.length} checks pass${r.pageErrors.length ? `, ${r.pageErrors.length} page errors: ${r.pageErrors[0]}` : ''}`);
  }
  console.log(`Screenshots and results: ${out}`);
  process.exit(failed ? 1 : 0);
})();

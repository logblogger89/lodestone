// Lena: design-minded Group PM; audits visual consistency on every screen, size and theme (PERSONAS.md §7, D-074)
const { top, tri } = require('./_common.cjs');
const WIDTHS = [1440, 1024, 768, 390, 320], SHOTS = new Set([1440, 390]);
const SCALE = new Set([0, 1, 2, 3, 4, 5, 6, 8, 10, 12, 14, 16, 18, 20, 24, 28, 32, 36, 40, 44, 48, 56, 64, 96]);

// Runs in the page: measures what Lena would notice on the current screen.
function audit() {
  const W = innerWidth, vis = e => { const r = e.getBoundingClientRect(), c = getComputedStyle(e); return r.width > 0 && r.height > 0 && c.visibility !== 'hidden' && c.display !== 'none' && +c.opacity > 0 };
  const all = [...document.querySelectorAll('#view *, #overlay *, .tabbar *, .rail *')].filter(vis);
  const texty = all.filter(e => [...e.childNodes].some(n => n.nodeType === 3 && n.textContent.trim()));
  const sizes = new Set(), weights = new Set(), fams = new Set(), colors = new Set();
  const rgb = s => (s.match(/[\d.]+/g) || []).map(Number);
  const lum = ([r, g, b]) => { const f = v => (v /= 255) <= .03928 ? v / 12.92 : ((v + .055) / 1.055) ** 2.4; return .2126 * f(r) + .7152 * f(g) + .0722 * f(b) };
  const bgOf = e => { for (let x = e; x; x = x.parentElement) { const c = rgb(getComputedStyle(x).backgroundColor); if (c.length >= 3 && (c[3] == null || c[3] > .5)) return c } return rgb(getComputedStyle(document.body).backgroundColor) };
  const lowContrast = [];
  for (const e of texty) {
    const c = getComputedStyle(e); if (e.closest('.done,[disabled],.ndl')) continue;
    sizes.add(c.fontSize); weights.add(c.fontWeight); fams.add(c.fontFamily.split(',')[0].replace(/"/g, '')); colors.add(c.color);
    const fg = rgb(c.color), bg = bgOf(e), a = fg[3] == null ? 1 : fg[3];
    const mix = fg.slice(0, 3).map((v, i) => v * a + bg[i] * (1 - a)), L1 = lum(mix), L2 = lum(bg);
    const ratio = (Math.max(L1, L2) + .05) / (Math.min(L1, L2) + .05), big = parseFloat(c.fontSize) >= 24 || (parseFloat(c.fontSize) >= 18.6 && +c.fontWeight >= 700);
    if (ratio < (big ? 3 : 4.5)) lowContrast.push(`${e.tagName.toLowerCase()}.${(e.className || '').toString().split(' ')[0]} "${e.textContent.trim().slice(0, 24)}" ${ratio.toFixed(2)}`);
  }
  const offScale = new Set();
  for (const e of all) { const c = getComputedStyle(e); for (const p of ['marginTop', 'marginBottom', 'paddingTop', 'paddingBottom', 'paddingLeft', 'paddingRight', 'rowGap', 'columnGap']) { const v = parseFloat(c[p]); if (v > 0 && !SCALE_.has(Math.round(v))) offScale.add(Math.round(v)) } }
  const scrollers = e => { for (let x = e.parentElement; x; x = x.parentElement) { const o = getComputedStyle(x).overflowX; if (o === 'auto' || o === 'scroll' || o === 'hidden') return true } return false };
  const wide = all.filter(e => e.getBoundingClientRect().right > W + 1 && !scrollers(e)).map(e => e.tagName.toLowerCase() + '.' + (e.className || '').toString().split(' ')[0]);
  const fakeLinks = all.filter(e => getComputedStyle(e).cursor === 'pointer' && !e.closest('button,a,label,summary,select,input,[data-open],[data-act],[data-view],[data-show],[role=tab]')).map(e => e.tagName.toLowerCase() + '.' + (e.className || '').toString().split(' ')[0]);
  const cards = [...document.querySelectorAll('#view .card')].filter(vis).map(c => c.querySelectorAll('.chip,.ck,.flag').length);
  const text = [...document.querySelectorAll('#view, #overlay')].map(e => e.innerText).join('\n');
  return { sizes: [...sizes], weights: [...weights], fams: [...fams], colors: colors.size, lowContrast: [...new Set(lowContrast)].slice(0, 8), nLow: lowContrast.length,
    offScale: [...offScale].sort((a, b) => a - b), wide: [...new Set(wide)].slice(0, 6), hscroll: document.documentElement.scrollWidth - W,
    fakeLinks: [...new Set(fakeLinks)].slice(0, 6), maxTags: Math.max(0, ...cards), text };
}

module.exports = {
  id: 'lena', name: 'Lena, design-minded Group PM, audits every screen, size and theme',
  viewport: { width: 1440, height: 900 },
  seed: jobs => {
    const t = top(jobs, () => true, 6);
    return {
      'profile/main': { version: 2, headline: 'Group PM, design tools', work_status: 'needs_permit', current: { title: 'Group PM', level: 'L7' }, domains: ['Design tools', 'Collaboration'] },
      'settings/prefs': { regions: ['Vancouver', 'Remote-Canada'], other_regions: true, tiers: ['Core', 'Adjacent'], exclude_people_mgmt: false, include_no_pay: true,
        learned: [{ id: 'pay-1', text: 'Raise your pay target to CA$200K', why: 'You said "Pay too low" on 3 roles.', at: new Date().toISOString(), before: {} }] },
      ...tri(t.slice(0, 2), 'interested'), ...tri(t.slice(2, 3), 'interested', { stage: 'Applied' }), ...tri(t.slice(3, 4), 'later'), ...tri(t.slice(4, 5), 'not', { reasons: ['Company'] }),
    };
  },
  async run(h) {
    const p = h.page;
    await p.addScriptTag({ content: `window.SCALE_=new Set(${JSON.stringify([...SCALE])});` });
    const nav = async v => { await p.evaluate(v => { S.open = null; setView(v) }, v); await h.wait(150) };
    const screens = [
      ['today', async () => { await nav('digest'); await p.evaluate(() => { S.show = 'today'; render() }) }],
      ['all-to-triage', async () => { await nav('digest'); await p.evaluate(() => { S.show = 'todo'; render() }) }],
      ['role-summary', async () => { await nav('digest'); await p.evaluate(() => { S.show = 'todo'; S.dtab = 'summary'; render(); S.open = S._order[0].id; render() }) }],
      ['role-description', async () => { await p.evaluate(() => { S.dtab = 'jd'; render() }); await h.wait(150) }],
      ['role-company', async () => { await p.evaluate(() => { S.dtab = 'company'; render() }) }],
      ['pipeline', async () => nav('pipeline')], ['add-job', async () => nav('add')], ['reports', async () => nav('reports')],
      ['companies', async () => nav('companies')], ['profile', async () => nav('settings')],
      ['profile-ranking', async () => { await p.evaluate(() => jumpTo('ps-rank')); await h.wait(500) }],
      ['profile-unsaved', async () => { await p.evaluate(() => { markDirty(); window.scrollTo(0, 0) }); await h.wait(200) }],
      ['setup', async () => { await nav('digest'); await p.evaluate(() => { S._obForce = true; S.ob = null; render() }) }],
      ['setup-status', async () => { await p.evaluate(() => { S.ob.step = 2; S.ob.a.status = 'not_sure'; render() }) }],
      ['empty-search', async () => { await p.evaluate(() => { S._obForce = false; S._obDone = true; S.show = 'all'; S.q = 'zzzzqq'; setView('digest') }) }],
    ];
    const findings = {};
    for (const theme of ['light', 'dark']) {
      await p.emulateMedia({ colorScheme: theme });
      for (const w of WIDTHS) {
        await p.setViewportSize({ width: w, height: w < 500 ? 844 : 900 });
        for (const [name, go] of screens) {
          await go(); await h.wait(120);
          const a = await p.evaluate(audit);
          const key = `${name}@${w}/${theme}`;
          findings[key] = a;
          if (SHOTS.has(w)) await h.shot(`${theme}-${w}-${name}`);
        }
        await p.evaluate(() => { S.q = ''; S._obForce = false; S._obDone = true });
      }
    }
    const every = f => Object.entries(findings).filter(([, a]) => f(a)).map(([k]) => k);
    h.task('Type: one scale');
    const sizes = new Set(Object.values(findings).flatMap(a => a.sizes)), weights = new Set(Object.values(findings).flatMap(a => a.weights)), fams = new Set(Object.values(findings).flatMap(a => a.fams));
    h.note('works', `Font sizes in use: ${[...sizes].sort((a, b) => parseFloat(a) - parseFloat(b)).join(' ')}`);
    h.check(sizes.size <= 8, `At most 8 font sizes across the app (${sizes.size})`);
    h.check(weights.size <= 3, `At most 3 font weights (${[...weights].join(', ')})`);
    h.check(fams.size <= 3, `At most 3 typefaces (${[...fams].join(', ')})`);
    h.task('Layout at every width and theme');
    const scroll = every(a => a.hscroll > 1);
    h.check(!scroll.length, `No sideways scrolling (${scroll.slice(0, 4).join(', ')})`);
    const wide = every(a => a.wide.length); h.check(!wide.length, `Nothing pokes past the screen edge (${wide.slice(0, 3).map(k => k + ': ' + findings[k].wide.join(' ')).join('; ')})`);
    const spacing = new Set(Object.values(findings).flatMap(a => a.offScale));
    h.check(spacing.size <= 2, `Spacing comes from one scale (off-scale values: ${[...spacing].join(', ') || 'none'})`);
    h.task('Contrast in light and dark');
    for (const theme of ['light', 'dark']) {
      const low = Object.entries(findings).filter(([k, a]) => k.endsWith(theme) && a.nLow);
      h.check(!low.length, `Readable text contrast in ${theme} mode (${low.slice(0, 2).map(([k, a]) => k + ': ' + a.lowContrast.slice(0, 3).join(' | ')).join(' ;; ')})`);
    }
    h.task('Cards: calm, not noisy');
    const tags = Math.max(...Object.values(findings).map(a => a.maxTags));
    h.check(tags <= 9, `At most 9 tags on a card (${tags})`);
    const fake = every(a => a.fakeLinks.length); h.check(!fake.length, `Nothing looks clickable that isn't (${fake.slice(0, 2).map(k => findings[k].fakeLinks.join(' ')).join('; ')})`);
    h.task('Words and numbers: one way each');
    const text = Object.values(findings).map(a => a.text).join('\n');
    const lowerK = [...new Set(text.match(/CA\$\d+(\.\d+)?k\b/g) || [])];
    h.check(!lowerK.length, `Money always written CA$148K, never CA$148k (${lowerK.slice(0, 3).join(', ')})`);
    const bare = [...new Set(text.match(/(?<![A-Z]{2})\$\d{2,3}K/g) || [])];
    h.check(!bare.length, `No bare "$" amounts without a currency (${bare.slice(0, 3).join(', ')})`);
    const junk = [...new Set(text.match(/\b(undefined|null|NaN|\[object Object\])\b/g) || [])];
    h.check(!junk.length, `No leftover code words on screen (${junk.join(', ')})`);
    const dbl = (text.match(/\S {2,}\S/g) || []).slice(0, 3);
    h.check(!dbl.length, `No doubled spaces (${dbl.join(' | ')})`);
    h.task('No jumps when things appear');
    await p.emulateMedia({ colorScheme: 'light' }); await p.setViewportSize({ width: 1440, height: 900 });
    await p.evaluate(() => { S.q = ''; S.show = 'todo'; setView('digest'); window.__cls = 0; new PerformanceObserver(l => l.getEntries().forEach(e => { if (!e.hadRecentInput) window.__cls += e.value })).observe({ type: 'layout-shift', buffered: false }) });
    const second = async () => p.evaluate(() => { const c = document.querySelectorAll('#view .card')[1]; return c ? c.getBoundingClientRect().top : 0 });
    const before = await second();
    await p.locator('#view .card:not(.done) [data-tri="later"]').first().click(); await h.wait(400);
    h.check(Math.abs((await second()) - before) < 2, 'Answering a role doesn\'t move the next one');
    await h.wait(300);
    const cls = await p.evaluate(() => window.__cls);
    h.check(cls < 0.1, `Little unexpected movement while using the list (layout shift ${cls.toFixed(3)})`);
    h.task('Focus is always visible');
    await p.evaluate(() => document.activeElement && document.activeElement.blur());
    const noRing = [];
    for (let i = 0; i < 18; i++) {
      await p.keyboard.press('Tab');
      const r = await p.evaluate(() => { const e = document.activeElement; if (!e || e === document.body) return null; const c = getComputedStyle(e); return { ok: (c.outlineStyle !== 'none' && parseFloat(c.outlineWidth) > 0) || c.boxShadow !== 'none', what: e.tagName.toLowerCase() + '.' + (e.className || '').toString().split(' ')[0] + ' ' + (e.textContent || '').trim().slice(0, 16) } });
      if (r && !r.ok) noRing.push(r.what);
    }
    h.check(!noRing.length, `Every focused control shows a focus ring (${[...new Set(noRing)].slice(0, 4).join(', ')})`);
  }
};

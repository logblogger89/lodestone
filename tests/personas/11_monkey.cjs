// Monkey test (10-17): hundreds of random taps across every screen, from three starting points (brand new, a long-time
// user, a phone). Checks after every step that nothing breaks: no script errors, the page renders, Today never empty
// while roles match. Seeded, so a failure can be replayed.
const ravi = require('./10_ravi.cjs');
const SAFE = ['[data-view]', '[data-show]', '[data-tri]', '[data-reason]', '[data-fam]', '[data-open]', '[data-act="close"]', '[data-dtab]',
  '[data-jump]', '[data-ob]', '[data-obf]', '[data-obt]', '[data-act="moretoday"]', '[data-act="restmore"]', '[data-act="nudge-later"]',
  '[data-act="taste"]', '[data-act="reonboard"]', '[data-act="expand"]', '[data-sacc]', '[data-snot]', '[data-like]', '[data-act="addrole"]',
  '[data-act="saveprefs"]', '[data-act="obbanner"]', '[data-nudge-status]', '[data-act="nudge-where"]', '[data-ask]', '[data-ask-no]', '[data-undo]'];
module.exports = {
  id: 'monkey', name: 'Monkey test: 300 random taps from three starting points',
  viewport: { width: 1180, height: 820 },
  seed: jobs => ravi.seed(jobs),
  async run(h) {
    let seed = 20261017; const rnd = () => (seed = (seed * 1103515245 + 12345) % 2147483648) / 2147483648;
    const errs = []; h.page.on('pageerror', e => errs.push(e.message));
    const starts = [['long-time user, laptop', null], ['brand-new user, laptop', 'new'], ['long-time user, phone', 'phone']];
    for (const [label, mode] of starts) {
      h.task(`100 random taps: ${label}`);
      if (mode === 'new') { await h.page.evaluate(() => { sessionStorage.clear(); localStorage.clear() }); await h.page.evaluate(() => { for (const k of Object.keys(window.__store)) if (!/^(jobs|desc|meta|reports)\//.test(k)) delete window.__store[k] }); await h.page.reload(); await h.wait(1200) }
      if (mode === 'phone') { await h.page.setViewportSize({ width: 390, height: 844 }) }
      let bad = [], taps = 0, slow = 0, slowest = '';
      for (let i = 0; i < 100; i++) {
        const els = await h.page.locator(SAFE.map(s => s + ':visible').join(',')).all();
        if (!els.length) { bad.push(`step ${i}: nothing to tap`); break }
        const el = els[Math.floor(rnd() * els.length)];
        const what = (await el.evaluate(e => (e.getAttribute('data-act') || Object.keys(e.dataset)[0] || e.tagName) + ':' + (e.textContent || '').trim().slice(0, 20)).catch(() => '?'));
        const t0 = Date.now(); const landed = await el.click({ timeout: 1500 }).then(() => true, () => false); taps++;   // a button under an open panel can't be tapped: not a delay
        await h.page.evaluate(() => new Promise(r => requestAnimationFrame(r)));   // the app has finished responding
        const took = Date.now() - t0; if (landed && took > slow) { slow = took; slowest = what }
        await h.wait(60);
        const st = await h.page.evaluate(() => {
          if (typeof S === 'undefined') return { ok: false, why: 'app gone' };
          const v = document.querySelector('#view'); if (!v || !v.innerHTML.trim()) return { ok: false, why: 'blank page' };
          if (!S.ready) return { ok: true };
          const todo = Object.values(S.jobs).filter(j => prefOk(j) && inPreferred(j) && isTodo(j)).length, T = S.today;
          if (T && T.ids && !T.ids.length && todo && S.view === 'digest' && S.show === 'today' && !document.querySelector('.ob')) return { ok: false, why: `Today empty with ${todo} matching` };
          return { ok: true };
        }).catch(e => ({ ok: false, why: 'evaluate failed: ' + e.message.slice(0, 60) }));
        if (!st.ok) bad.push(`step ${i} after ${what}: ${st.why}`);
        if (errs.length) { bad.push(`step ${i} after ${what}: script error ${errs[0]}`); errs.length = 0 }
      }
      h.check(!bad.length, `${taps} taps with no breakage (${bad.slice(0, 2).join(' | ')})`);
      h.check(slow < 1600, `Every tap responds within 1.6 s (slowest ${slow} ms: ${slowest})`);
      await h.shot(label.replace(/[^a-z]+/g, '-'));
    }
  }
};

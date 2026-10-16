// Tomás: TPM in Mexico City, phone only, a few minutes at a time, says no a lot (PERSONAS.md §4)
const { top, bottom, tri, daysAgo, live } = require('./_common.cjs');
module.exports = {
  id: 'tomas', name: 'Tomás, TPM, phone only, back after four days',
  viewport: { width: 390, height: 844 }, touch: true,
  seed: jobs => {
    const low = bottom(jobs, () => true, 4), cos = live(jobs).filter(j => j.company === (live(jobs)[0] || {}).company).slice(0, 2);
    return {
      'profile/main': { version: 1, headline: 'Technical program manager', work_status: 'needs_permit', current: { title: 'Senior TPM' } },
      'settings/prefs': { regions: ['GTA', 'Vancouver', 'Remote-Canada'], other_regions: false, tiers: ['Core', 'Adjacent'], exclude_people_mgmt: true, include_no_pay: true },
      ...tri(low.slice(0, 3), 'not', { reasons: ['Pay too low'] }),
      ...tri(cos, 'not', { reasons: ['Company'] }),
      ...tri(top(jobs, () => true, 2), 'later', { updated_at: daysAgo(9) }),            // came back from Later
      'settings/today': { date: '2026-01-01', ids: [] },                                   // stale list from his last visit
    };
  },
  localStorage: [['lastVisit', Date.now() - 4 * 864e5]],
  async run(h) {
    h.task('Back after four days, on the phone');
    await h.shot('open');
    const v = await h.text();
    h.check(/left today/.test(v), 'A fresh Today list, not last visit\'s');
    h.check(/Suggestion/.test(v), 'A suggestion from his "Pay too low" answers is waiting');
    const w = await h.evalS(() => document.documentElement.scrollWidth);
    h.check(w <= 392, `No sideways scrolling on the phone (page is ${w}px wide)`);
    const firstTop = await h.evalS(() => { const c = document.querySelector('#view .card'); return c ? Math.round(c.getBoundingClientRect().top) : 9999 });
    h.check(firstTop < 844 - 200, `A role is on screen without scrolling (first card starts at ${firstTop}px of 844)`);

    h.task('Thumb targets');
    const sizes = await h.page.locator('#view .card .tbtn').evaluateAll(bs => bs.slice(0, 6).map(b => b.getBoundingClientRect().height));
    h.check(sizes.length && Math.min(...sizes) >= 40, `Triage buttons are at least 40px tall (smallest ${Math.round(Math.min(...sizes))}px)`);

    h.task('Say no with a reason');
    await h.page.locator('#view .card [data-tri="not"]').first().click(); await h.wait(250);
    await h.shot('not-reasons');
    const r = h.page.locator('.reasons button').first();
    h.check(await r.count() && await r.isVisible(), 'Reason buttons visible right after Not for me');
    if (await r.count()) { const rh = (await r.boundingBox()).height; h.check(rh >= 36, `Reason buttons are thumb-sized (${Math.round(rh)}px)`) }
    await h.page.getByRole('button', { name: 'Pay too low' }).first().click(); await h.wait(250);

    h.task('Accept the suggestion, then undo it');
    const acc = h.page.locator('[data-sacc]');
    if (await acc.count()) {
      const before = (await h.store())['settings/prefs'] || {};
      await acc.first().click(); await h.wait(300);
      const after = (await h.store())['settings/prefs'];
      h.check(JSON.stringify(after.checks) !== JSON.stringify(before.checks), 'Accepting the suggestion changed his settings');
      await h.shot('accepted');
      await h.click('[data-view="settings"]'); await h.wait(250);
      const undo = h.page.locator('[data-undo]');
      h.check(await undo.count(), 'The accepted change is listed with Undo');
      if (await undo.count()) { await undo.first().click(); await h.wait(300) }
      h.check(!((await h.store())['settings/prefs'].learned || []).length, 'Undo removes it');
      await h.click('[data-view="digest"]'); await h.wait(250);
    } else h.check(false, 'Suggestion banner present');

    h.task('Run out of today\'s list, get more');
    for (let i = 0; i < 12; i++) { const b = h.page.locator('#view .card:not(.done) [data-tri="later"]').first(); if (!(await b.count())) break; await b.click(); await h.wait(120) }
    await h.shot('caught-up');
    const more = h.page.getByRole('button', { name: /Show .* more/ });
    h.check(await more.count(), 'Show more is offered');
    if (await more.count()) { await more.first().click(); await h.wait(250); h.check(await h.page.locator('#view .card').count() > 0, 'More roles appear') }
  }
};

// Tomás: TPM in Mexico City, phone only, a few minutes at a time, says no a lot (PERSONAS.md §4)
const { top, bottom, tri, daysAgo, live } = require('./_common.cjs');
module.exports = {
  id: 'tomas', name: 'Tomás, TPM, phone only, back after four days',
  viewport: { width: 390, height: 844 }, touch: true,
  seed: jobs => {
    const low = bottom(jobs, () => true, 4), cos = live(jobs).filter(j => j.company === (live(jobs)[0] || {}).company).slice(0, 2);
    return {
      'profile/main': { version: 1, headline: 'Technical program manager', work_status: 'needs_permit', current: { title: 'Senior TPM' } },
      'settings/prefs': { regions: ['GTA', 'Vancouver', 'Remote-Canada'], other_regions: false, families: ['program'], families_shown: ['pm', 'project'], exclude_people_mgmt: true, include_no_pay: true },
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

    h.task('His own field: program management, not "PM-adjacent"');
    const page = await h.text();
    h.check(!/PM-adjacent|Core PM/.test(page), 'Nothing calls his roles "PM-adjacent" or "Core PM"');
    const tags = await h.page.locator('#view .card .ck.tier').evaluateAll(xs => xs.map(x => [x.textContent, x.className]));
    const prog = tags.filter(([t]) => /^Program/.test(t));
    h.check(prog.length && prog.every(([, c]) => /t-core/.test(c)), `Program roles carry his field's highlighted tag (${prog.length} on screen)`);
    h.check(tags.filter(([t]) => t === 'Product').every(([, c]) => !/t-core/.test(c)), 'Pure product roles show as related, not as his field');
    const top3 = tags.slice(0, 3).map(([t]) => t);
    h.check(top3.filter(t => /^Program/.test(t)).length >= 2, `His first roles are mostly program roles (${top3.join(', ')})`);
    await h.click('[data-show="todo"]'); await h.wait(250);
    const chips = await h.page.locator('[data-fam]').allInnerTexts();
    h.check(/^All/.test(chips[0] || '') && /^Program/.test(chips[1] || ''), `Role-type filter starts with his field (${chips.join(' | ')})`);
    await h.page.locator('[data-fam="program"]').click(); await h.wait(250);
    const only = await h.page.locator('#view .card .ck.tier').allInnerTexts();
    h.check(only.length && only.every(t => /\bProgram\b/.test(t)), `Filtering to Program shows only program roles (${[...new Set(only)].join(', ')})`);
    await h.shot('program-filter');
    await h.page.locator('[data-fam=""]').click(); await h.wait(250);
    // D-077: a job can be more than one type; Claude read the descriptions
    const also = await h.page.locator('#view .card .ck.tier', { hasText: '· also' }).allInnerTexts();
    h.check(also.length > 0, `Hybrid jobs show both types (${also.slice(0, 3).join(' | ')})`);
    const pmLike = await h.evalS(() => Object.values(S.jobs).filter(j => j.live && j.aff_src === 'read' && j.family !== 'program' && (j.aff.program || 0) >= 50 && prefOk(j)).length);
    h.check(pmLike > 0, `Jobs titled otherwise but with real program work reach his list (${pmLike})`);
    await h.click('[data-show="today"]'); await h.wait(250);

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
      h.task('Jump around the Profile on the phone, change one thing, save');
      h.check(await h.page.locator('.jumpbar').isVisible(), 'A row of "jump to" chips sits at the top of the Profile');
      await h.page.locator('.jumpbar [data-jump="ps-app"]').click(); await h.wait(700);
      const r = await h.evalS(() => { const s = document.getElementById('ps-app').getBoundingClientRect(), b = document.querySelector('.jumpbar').getBoundingClientRect(); return { top: Math.round(s.top), bar: Math.round(b.bottom) } });
      h.check(r.top >= r.bar - 2 && r.top < 200, `Tapping "Lists" lands on that section, not hidden under the chips (section at ${r.top}px, chips end at ${r.bar}px)`);
      h.check(await h.page.locator('.jumpbar').isVisible() && (await h.evalS(() => Math.round(document.querySelector('.jumpbar').getBoundingClientRect().top))) <= 1, 'The chips stay at the top while he scrolls');
      await h.page.fill('#ldays', '5'); await h.wait(150);
      const sb = await h.evalS(() => { const b = document.getElementById('savebar').getBoundingClientRect(), t = document.querySelector('.tabbar').getBoundingClientRect(); return { dirty: document.getElementById('savebar').classList.contains('dirty'), bottom: Math.round(b.bottom), tab: Math.round(t.top), vis: b.top < innerHeight } });
      h.check(sb.dirty && sb.vis && sb.bottom <= sb.tab, `After a change, "Save changes" is on screen just above the tab bar (bar ends ${sb.bottom}px, tabs start ${sb.tab}px)`);
      h.check(/unsaved changes/i.test(await h.text('#savebar')), 'It says he has unsaved changes');
      await h.shot('profile-phone-save');
      await h.page.locator('#savebar [data-act="saveprefs"]').click(); await h.wait(300);
      h.check(((await h.store())['settings/prefs'] || {}).later_days === 5, 'Saving from the bar keeps his change');
      await h.click('[data-view="digest"]'); await h.wait(250);
    } else h.check(false, 'Suggestion banner present');

    h.task('Run out of today\'s list, keep going');
    for (let i = 0; i < 15 && !(await h.has('reviewed your top matches')); i++) { const b = h.page.locator('#view .card:not(.done) [data-tri="later"]').first(); if (!(await b.count())) break; await b.click(); await h.wait(120) }
    await h.shot('after-top-matches');
    h.check(await h.has("You've reviewed your top matches for today"), 'The phone shows the done message');
    h.check(await h.page.locator('#view .card').count() > 0, 'More roles appear without hunting for a button');
    const top = await h.evalS(() => { const c = document.querySelector('#view .card'); return c ? Math.round(c.getBoundingClientRect().top) : 9999 });
    h.check(top < 844 - 150, `The first of the other roles is on screen (${top}px)`);
  }
};

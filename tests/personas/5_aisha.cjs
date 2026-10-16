// Aisha: Principal PM, keyboard and screen reader, privacy-minded (PERSONAS.md §5)
const { top, tri } = require('./_common.cjs');
module.exports = {
  id: 'aisha', name: 'Aisha, Principal PM, keyboard only, privacy-minded',
  viewport: { width: 1280, height: 900 },
  seed: jobs => {
    const t = top(jobs, () => true, 4);
    return {
      'profile/main': { version: 2, headline: 'Principal PM', work_status: 'needs_permit', current: { title: 'Principal PM', level: 'L7' } },
      'settings/prefs': { regions: ['GTA'], other_regions: true, tiers: ['Core'], exclude_people_mgmt: false, include_no_pay: true,
        learned: [{ id: 'people', text: 'Hide roles that manage people', why: 'You said "People management" on 3 roles.', at: new Date().toISOString(), before: { exclude_people_mgmt: false } }] },
      ...tri(t.slice(0, 2), 'interested'),
      ...Object.fromEntries(t.slice(2).map(j => [`signals/${j.id}`, { read_secs: 120, opens: 2, at: new Date().toISOString() }])),
    };
  },
  async run(h) {
    const k = async key => { await h.page.keyboard.press(key); await h.wait(160) };
    const focusName = () => h.evalS(() => { const a = document.activeElement; return a ? (a.getAttribute('aria-label') || a.textContent || a.id || a.tagName).trim().slice(0, 40) : '' });

    h.task('Triage by keyboard');
    h.check(!(await h.has('Get started')) && !(await h.page.locator('.ob').count()), 'An existing user never sees the setup flow');
    await k('j'); await k('j');
    const sel = await h.page.locator('#view .card.sel').count();
    h.check(sel === 1, 'J moves the highlighted role');
    await k('i');
    h.check((await h.writes()).some(x => x[1].startsWith('triage/')), 'I marks the highlighted role Interested');
    await k('Enter');
    h.check(await h.page.locator('.drawer').count(), 'Enter opens the role');
    const f1 = await focusName();
    h.check(await h.evalS(() => !!document.activeElement.closest('.drawer')), `Focus moves into the opened role (focus on: "${f1}")`);
    await h.shot('opened-by-keyboard');

    h.task('Tabs with arrow keys, close with Escape');
    await h.page.focus('#dt-summary'); await k('ArrowRight');
    h.check(await h.evalS(() => document.activeElement.id === 'dt-jd'), 'Right arrow moves to the Job description tab');
    await k('Escape');
    h.check(!(await h.page.locator('.drawer').count()), 'Escape closes the role');
    const back = await h.evalS(() => !!document.activeElement.closest('.card'));
    h.check(back, 'Focus returns to the role she came from');

    h.task('Names a screen reader can say');
    const unnamed = await h.evalS(() => [...document.querySelectorAll('button,a,input,select,textarea')].filter(e => e.offsetParent !== null)
      .filter(e => !(e.getAttribute('aria-label') || e.textContent.trim() || e.labels?.length || e.title || e.placeholder)).map(e => e.outerHTML.slice(0, 60)));
    h.check(!unnamed.length, `Every control has a name (${unnamed.length} without: ${unnamed.slice(0, 2).join(' ')})`);
    const ring = await h.evalS(() => { const c = document.querySelector('#view .card'); return getComputedStyle(c).outlineStyle + '/' + c.getAttribute('tabindex') });
    h.note('works', 'Card focusability: ' + ring);
    h.check(await h.evalS(() => document.querySelector('#view .card').tabIndex >= 0), 'Cards can be reached with Tab');

    h.task('Learning controls: stop reading-time learning, delete reading data');
    await h.click('[data-view="settings"]'); await h.wait(250);
    await h.page.locator('#lread').uncheck();
    await h.click('[data-act="saveprefs"]'); await h.wait(300);
    h.check((await h.store())['settings/prefs'].learn_reading === false, 'Reading-time learning switched off and saved');
    h.check(((await h.store())['settings/prefs'].learned || []).length === 1, 'Saving the Profile keeps what Lodestone learned');
    await h.click('[data-act="delreading"]'); await h.wait(300);
    const sig = Object.keys(await h.store()).filter(k => k.startsWith('signals/'));
    h.check(!sig.length, `Reading data deleted (${sig.length} left)`);
    await h.shot('privacy');
    const p = await h.text();
    h.check(/only you/i.test(p), 'The Profile says who can see her data');
  }
};

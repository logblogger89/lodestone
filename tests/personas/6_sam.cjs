// Sam: skips everything. Wants to look around first, on a phone, and is wary of questions (PERSONAS.md §6, P1-S7)
module.exports = {
  id: 'sam', name: 'Sam, skips every question, browses on a phone',
  viewport: { width: 390, height: 844 }, touch: true,
  seed: () => ({}),
  async run(h) {
    h.task('Skip setup on the first screen');
    await h.shot('welcome');
    h.check(await h.has('Skip and browse'), 'A way to skip is on the first screen');
    await h.tap('Skip and browse'); await h.wait(500);
    const v = await h.text();
    h.check(/left today/.test(v), 'Skipping lands on a real list straight away');
    h.check(/Based on default settings/.test(v), 'The list says it is based on default settings');
    h.check(await h.page.locator('#view .card').count() >= 5, 'At least five roles to look at');
    const top = await h.evalS(() => { const c = document.querySelector('#view .card'); return c ? Math.round(c.getBoundingClientRect().top) : 9999 });
    h.check(top < 844 - 200, `A role is on screen without scrolling (${top}px)`);
    await h.shot('list');

    h.task('Come back later: no setup again');
    await h.reload();
    h.check(!(await h.has('Get started')), 'Setup does not come back after a reload');
    h.check(/left today/.test(await h.text()), 'He goes straight to his list');

    h.task('Dismiss the banner; skip questions mid-flow');
    const got = h.page.getByRole('button', { name: 'Got it' });
    if (await got.count()) { await got.click(); await h.wait(200); h.check(!(await h.has('Your first list')), '"Got it" dismisses the first-list banner') }
    await h.click('[data-view="settings"]'); await h.wait(250);
    const p = await h.text();
    h.check(/Level 0 of 4/i.test(p), 'Profile shows match quality level 0');
    h.check(/Run the quick setup again/.test(p), 'Setup can be started from the Profile later');
    await h.shot('profile');
    await h.click('[data-act="reonboard"]'); await h.wait(250);
    h.check(/Step 1 of 3/.test(await h.text()), 'Running setup again starts at the first question (role type)');
    await h.tap('Answer 2 more quick questions');                                  // skips the role question
    await h.page.locator('.obnav [data-ob="next"].link').click(); await h.wait(150); // skips where
    h.check(/Step 3 of 3/.test(await h.text()), 'Skipping each question still moves forward');
    await h.page.locator('.obnav [data-ob="finish"].link').click(); await h.wait(400); // skips work status
    h.check(/left today/.test(await h.text()), 'Skipping the last question lands on the list');
    const st = await h.store(), pr = st['profile/main'] || {};
    h.check(pr.work_status === 'unknown', 'Work status stays "not set", not guessed');
    h.check(!(await h.page.locator('#view .card .ck-bad', { hasText: 'No sponsorship' }).count()), 'With no work status, work-permit tags are never red');
    const w = await h.evalS(() => document.documentElement.scrollWidth);
    h.check(w <= 392, `No sideways scrolling (${w}px)`);
  }
};

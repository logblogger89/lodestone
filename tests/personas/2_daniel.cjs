// Daniel: product marketer arriving in Calgary on an open work permit, no resume, first visit (PERSONAS.md §2)
// P1-S7: the full onboarding journey, then profile without a resume, the match-quality meter and one-tap questions.
module.exports = {
  id: 'daniel', name: 'Daniel, product marketer, first visit, open work permit, no resume',
  viewport: { width: 1366, height: 768 },
  seed: () => ({}),          // brand new: no profile, no settings, no history
  async run(h) {
    h.task('First visit: the promise, privacy, and a way in');
    const v = await h.text();
    await h.shot('welcome');
    h.check(/Find the jobs that fit you/.test(v), 'The first screen says what Lodestone does, in one line');
    h.check(/private to you/i.test(v), 'The first screen says his answers stay private');
    h.check(/No resume needed/i.test(v), 'It says no resume is needed');
    h.check(!(await h.page.locator('#view .card').count()), 'No ranked list before he has said anything');
    await h.tap('Get started');

    h.task('Where: Calgary');
    h.check(/Step 1 of 4/.test(await h.text()), 'Progress shows step 1 of 4');
    await h.page.locator('[data-obf="city"][data-v="Calgary"]').click(); await h.wait(150);
    h.check((await h.page.locator('[data-obf="city"][data-v="Calgary"]').getAttribute('aria-pressed')) === 'true', 'Calgary is selected');
    await h.shot('where');
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(150);

    h.task('Work status: not sure at first, then open permit');
    await h.page.locator('[data-obf="status"][data-v="not_sure"]').click(); await h.wait(150);
    h.check(/not immigration advice/i.test(await h.text()), '"Not sure" shows a short plain explainer, with the not-advice line');
    await h.shot('status-not-sure');
    await h.page.locator('[data-obf="status"][data-v="open_permit"]').click(); await h.wait(150);
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(150);

    h.task('Role: in his own words plus two role types');
    await h.page.fill('#ob-role', 'product marketing or product manager, fintech, 6 years');
    await h.page.locator('[data-obf="fam"][data-v="pmm"]').click(); await h.wait(100);
    await h.page.locator('[data-obf="fam"][data-v="pm"]').click(); await h.wait(100);
    h.check((await h.page.inputValue('#ob-role')).includes('fintech'), 'His typed words survive tapping role cards');
    await h.shot('role');
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(200);

    h.task('Taste test: eight real roles, then his list');
    const tc = await h.page.locator('.tcard').count();
    h.check(tc >= 6 && tc <= 8, `Taste test shows up to 8 roles (${tc})`);
    const metas = await h.page.locator('.tcard .tmeta').allInnerTexts();
    h.check(metas.filter(m => /Calgary|Anywhere|Remote/i.test(m)).length >= Math.min(3, tc), 'Taste-test roles are in Calgary');
    const btns = h.page.locator('.tcard [data-obt="1"]');
    for (let i = 0; i < Math.min(3, tc); i++) { await btns.nth(i).click(); await h.wait(80) }
    await h.page.locator('.tcard [data-obt="-1"]').nth(Math.min(4, tc - 1)).click(); await h.wait(80);
    h.check(/4 of \d+ answered/.test(await h.text()), 'A counter shows how many he answered');
    await h.shot('taste');
    await h.page.getByRole('button', { name: 'See my list' }).click(); await h.wait(500);
    const st = await h.store();
    h.check(st['profile/main'] && st['profile/main'].onboarded_at, 'Finishing saves that he has been set up');
    h.check(st['profile/main'] && st['profile/main'].work_status === 'open_permit', 'Open work permit saved');
    h.check(st['settings/prefs'] && (st['settings/prefs'].regions || []).join() === 'Calgary', 'Calgary saved as his city');
    h.check(Object.keys(st).filter(k => k.startsWith('likes/')).length === 4, 'His 4 taste-test taps are saved and train the ranking');
    const list = await h.text();
    h.check(/left today/.test(list), 'He lands on his Today list');
    h.check(/personal fit scores arrive at the next update/i.test(list), 'It says honestly when his personal scores arrive');
    const cards = await h.page.locator('#view .card .meta').allInnerTexts();
    h.check(cards.length && cards.filter(m => /calgary|remote/i.test(m)).length / cards.length >= 0.5, `Today leans to Calgary (${cards.filter(m => /calgary|remote/i.test(m)).length} of ${cards.length})`);
    h.check(!/Sponsorship unknown|Hires from abroad/.test(list), 'No sponsorship tags for someone with an open permit');
    await h.shot('first-list');

    h.task('Paste a LinkedIn link');
    await h.click('[data-view="add"]'); await h.wait(200);
    await h.page.fill('#paste', 'https://www.linkedin.com/jobs/view/1234567890');
    await h.click('[data-act="addjob"]'); await h.wait(300);
    h.check((await h.writes()).some(x => x[0] === 'add' && x[1].startsWith('inbox/')), 'Pasted link saved to the inbox');
    h.check(/linkedin\.com\/jobs/i.test(await h.text()), 'The inbox shows what he pasted');

    h.task('Understand role types and levels');
    await h.click('[data-view="digest"]'); await h.wait(200);
    await h.page.locator('details.legend summary').click(); await h.wait(150);
    const legend = await h.text('details.legend');
    h.check(/PM-adjacent/.test(legend) && /Stretch/.test(legend), 'Legend explains the role types');
    h.check(/L5|L6|level/i.test(legend), 'Legend explains the levels shown on cards');
  }
};

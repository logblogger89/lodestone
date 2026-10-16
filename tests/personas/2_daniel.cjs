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
    await h.page.fill('#ob-role', 'fintech product marketing, 6 years'); await h.wait(100);
    h.check((await h.page.locator('[data-obf="fam"][data-v="pmm"]').getAttribute('aria-pressed')) === 'true', 'Typing "product marketing" lights up that card');
    await h.page.locator('[data-obf="fam"][data-v="pm"]').click(); await h.wait(100);   // and he's open to product manager roles too
    h.check((await h.page.locator('[data-obf="fam"][aria-pressed="true"]').count()) === 2, 'Tapping Product manager adds it; product marketing stays picked');
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
    h.check(st['settings/prefs'] && (st['settings/prefs'].regions || []).join() === 'Calgary,Remote-Canada', 'Calgary (plus remote in Canada) saved as his cities');
    h.check(Object.keys(st).filter(k => k.startsWith('likes/')).length === 4, 'His 4 taste-test taps are saved and train the ranking');
    const list = await h.text();
    h.check(/left today/.test(list), 'He lands on his Today list');
    h.check(/personal fit scores arrive at the next update/i.test(list), 'It says honestly when his personal scores arrive');
    const cards = await h.page.locator('#view .card .meta').allInnerTexts();
    h.check(cards.length && cards.filter(m => /calgary|remote/i.test(m)).length / cards.length >= 0.5, `Today leans to Calgary (${cards.filter(m => /calgary|remote/i.test(m)).length} of ${cards.length})`);
    h.check(!/Sponsorship unknown|Hires from abroad/.test(list), 'No sponsorship tags for someone with an open permit');
    await h.shot('first-list');

    h.task('One-tap questions while triaging');
    await h.page.locator('#view .card:not(.done) [data-tri="not"]').first().click(); await h.wait(250);
    await h.page.locator('#view .card.done .reasons button', { hasText: 'Pay too low' }).first().click(); await h.wait(300);
    const ask = h.page.locator('[data-ask="minpay"]');
    h.check(await ask.count(), 'Saying "Pay too low" asks once for his lowest acceptable base pay');
    await h.shot('ask-minpay');
    if (await ask.count()) { await h.page.locator('[data-ask="minpay"][data-v="140000"]').click(); await h.wait(300) }
    const ck = ((await h.store())['settings/prefs'] || {}).checks || {};
    h.check(ck.pay_yellow === 140000, 'His minimum (CA$140K) is saved as the point where pay turns red');
    h.check(!(await h.page.locator('[data-ask="minpay"]').count()), 'The question is not asked again');
    const tor = h.page.locator('#view .card:not(.done)', { hasText: /Toronto|Waterloo|Vancouver|Ottawa|Montreal/ }).first();
    if (await tor.count()) {
      await tor.locator('[data-tri="interested"]').click(); await h.wait(300);
      h.check(await h.page.locator('[data-ask="city"]').count(), 'Shortlisting a role outside Calgary asks whether to add that city');
      await h.page.locator('.ask [data-ask-no]').first().click(); await h.wait(250);
      h.check(!(await h.page.locator('[data-ask="city"]').count()), '"No thanks" closes it for good');
    } else h.note('annoyance', 'No role outside Calgary in today\'s list to test the city question');
    await h.page.locator('#view .card:not(.done) [data-tri="later"]').first().click(); await h.wait(250);
    await h.page.locator('#view .card:not(.done) [data-tri="interested"]').first().click(); await h.wait(250);

    h.task('After three answers: sharper matches, without a resume');
    await h.click('[data-show="todo"]'); await h.click('[data-show="today"]'); await h.wait(250);
    h.check(/Want sharper matches/.test(await h.text()), 'After a few answers, Lodestone offers to add his experience');
    await h.shot('nudge');
    await h.tap('Build it with me'); await h.wait(300);
    h.check(await h.page.locator('#b-role').isVisible(), '"Build it with me" opens five short questions');
    await h.page.fill('#b-role', 'Senior product marketing manager');
    await h.page.fill('#b-years', '6');
    await h.page.fill('#b-win', 'Launched a savings product that reached 400,000 users in a year');
    await h.page.fill('#b-domains', 'fintech, payments, consumer apps');
    await h.page.fill('#b-tools', 'SQL, Amplitude, A/B testing');
    await h.shot('builder');
    await h.click('[data-act="savebuild"]'); await h.wait(300);
    const pr = (await h.store())['profile/main'] || {};
    h.check(pr.builder && pr.builder.status === 'new', 'His answers are saved for the next run to build his profile');
    h.check((pr.domains || []).includes('fintech') && (pr.current || {}).title, 'Domains and title fill in straight away');
    const prof = await h.text();
    h.check(/next update \(within about 6 hours\)/.test(prof), 'It says when the profile will be built');
    h.check(/How well Lodestone knows you.*Level [0-4] of 4/i.test(prof), 'The match-quality meter shows his level');
    h.check(/Next:/.test(prof), 'The meter names the one next step');
    h.check(/never sent to employers/i.test(prof), 'Privacy promise next to his experience');
    await h.shot('profile-after-builder');

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
    h.check(/your field \([^)]*Product management/.test(legend) && /your field \([^)]*Product marketing/.test(legend), `Legend names his own field in his words (${legend.match(/Role type:[^\n]*/)})`);
    h.check(!/PM-adjacent|Core PM/.test(await h.text()), 'Nothing calls his roles "PM-adjacent" or "Core PM"');
    h.check(/L5|L6|level/i.test(legend), 'Legend explains the levels shown on cards');
    const pmm = h.page.locator('#view .ck.tier', { hasText: 'Product marketing' });
    h.check(await pmm.count() && /t-core/.test(await pmm.first().getAttribute('class')), 'Product marketing roles carry his field\'s highlighted tag');
  }
};

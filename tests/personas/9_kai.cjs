// Kai: project manager in Halifax, curious, answers one question and wants to see jobs now (PERSONAS.md §9, D-077)
const STRIP = jobs => {   // brand new: nothing has been scored for Kai yet
  const all = {}; Object.values(jobs).forEach(j => { const c = { ...j }; delete c.fit; all[j.id] = c });
  const out = { 'jobs/b0': { jobs: all } }; for (let i = 1; i < 16; i++) out[`jobs/b${i}`] = { jobs: {} };
  return out;
};
module.exports = {
  id: 'kai', name: 'Kai, project manager, one question then straight to the jobs',
  viewport: { width: 1280, height: 860 },
  seed: jobs => STRIP(jobs),
  async run(h) {
    h.task('One question, then the jobs');
    h.check(/One question to start/.test(await h.text()), 'The welcome says it is one question to start');
    await h.tap('Get started');
    h.check(/What kind of role/.test(await h.text()), 'The first question is the role type');
    await h.page.locator('[data-obf="fam"][data-v="project"]').click(); await h.wait(120);
    await h.shot('role');
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(500);
    const st = await h.store(), prefs = st['settings/prefs'] || {}, prof = st['profile/main'] || {};
    h.check((prefs.families || []).join() === 'project', 'Project management saved as Kai\'s field');
    h.check((prof.onboarding || {}).where_set === false && prof.work_status === 'unknown', 'Where and work status are left unanswered, not guessed');
    h.check((prefs.regions || []).length >= 8, `With no cities picked, all of Canada counts (${(prefs.regions || []).length} regions)`);
    const v = await h.text();
    h.check(/left today/.test(v), 'Kai lands on a real list');
    h.check(/Ranked by role type only/.test(v), 'The banner says the list is ranked by role type only');
    const tags = await h.page.locator('#view .card .ck.tier').allInnerTexts();
    h.check(tags.length >= 5 && tags.filter(t => /^Project/.test(t)).length >= Math.ceil(tags.length * 0.7), `Today is mostly project roles (${tags.join(', ')})`);
    h.check(!(await h.page.locator('#view .card .ck-bad', { hasText: 'No sponsorship' }).count()), 'No red work-permit tags while work status is unknown');
    h.check(!(await h.page.locator('.sbanner.nudge').count()), 'No nudge before Kai has done anything');
    await h.shot('list');

    h.task('A gentle nudge after a few answers, at most once a day');
    for (let i = 0; i < 3; i++) { await h.page.locator('#view .card:not(.done) [data-tri="later"]').first().click(); await h.wait(150) }
    await h.click('[data-show="todo"]'); await h.click('[data-show="today"]'); await h.wait(250);
    const n1 = h.page.locator('.sbanner.nudge');
    h.check(await n1.count() === 1, 'After three answers, one small card appears in the list (not a pop-up)');
    h.check(/Where do you want to work/.test(await n1.first().innerText()), 'It asks the next most useful thing: where');
    await h.shot('nudge-where');
    await h.tap('Not now'); await h.wait(200);
    h.check(!(await h.page.locator('.sbanner.nudge').count()), '"Not now" hides it');
    await h.reload();
    h.check(!(await h.page.locator('.sbanner.nudge').count()), 'and it stays hidden for the rest of the day');

    h.task('Next day: answer where, from the nudge');
    await h.page.evaluate(() => localStorage.setItem('lodestone:nudgeDay', JSON.stringify('2000-01-01'))); await h.reload();
    h.check(await h.page.locator('.sbanner.nudge').count() === 1, 'The nudge comes back the next day');
    await h.tap('Choose cities'); await h.wait(250);
    h.check(/Where do you want to work/.test(await h.text()) && !(await h.page.locator('[data-obf="city"][aria-pressed="true"]').count()), 'It opens the where question, nothing pre-ticked');
    await h.page.locator('[data-obf="city"][data-v="Vancouver"]').click(); await h.wait(100);
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(150);
    await h.page.locator('[data-obf="status"][data-v="needs_permit"]').click(); await h.wait(100);
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(500);
    const st2 = await h.store(), p2 = st2['settings/prefs'] || {}, pr2 = st2['profile/main'] || {};
    h.check((p2.regions || []).join() === 'Vancouver,Remote-Canada', 'Vancouver (plus remote) saved');
    h.check(pr2.work_status === 'needs_permit' && (pr2.onboarding || {}).where_set === true, 'Work status and where are now known');
    h.check((p2.families || []).join() === 'project', 'Kai\'s role type is kept');
    h.check(!(await h.page.locator('.sbanner.nudge').count()), 'No second nudge the same day');

    h.task('The meter shows what is done and what is next');
    await h.click('[data-view="settings"]'); await h.wait(250);
    const p = await h.text();
    h.check(/Level 2 of 4/.test(p), 'Role type and where & work status: level 2 of 4');
    h.check(/Next:.*experience/i.test(p), 'The next step is adding experience');
    await h.shot('meter');
  }
};

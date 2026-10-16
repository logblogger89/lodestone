// Priya: Staff PM, needs sponsorship, Toronto/Waterloo, methodical ten-minute mornings (docs/product/ux/PERSONAS.md §1)
const { top, bottom, tri } = require('./_common.cjs');
module.exports = {
  id: 'priya', name: 'Priya, Staff PM, Seattle to Toronto, needs sponsorship',
  viewport: { width: 1280, height: 860 },
  seed: jobs => ({
    'profile/main': { version: 3, headline: 'Staff PM, payments platform', current: { employer: 'Contoso Pay', title: 'Staff Product Manager', level: 'L6' },
      work_status: 'needs_permit', domains: ['Payments', 'Platform', 'AI'], preferences: { domains_wanted: 'payments, platform, AI agents' } },
    'settings/prefs': { regions: ['GTA', 'Waterloo Region'], other_regions: false, tiers: ['Core', 'Adjacent'], exclude_people_mgmt: false, include_no_pay: true,
      checks: { green_regions: ['GTA', 'Waterloo Region'], pay_green: 200000, pay_yellow: 170000, level_green: 6, level_yellow: 5, fresh_green: 14, fresh_yellow: 30 } },
    ...tri(top(jobs, j => /platform|ai/i.test(j.title), 3), 'interested'),
    ...tri(bottom(jobs, () => true, 3), 'not', { reasons: ['Not my domain'] }),
  }),
  async run(h) {
    h.task('Morning: open the app and see today\'s list');
    h.check(!(await h.has('Get started')) && !(await h.page.locator('.ob').count()), 'An existing user never sees the setup flow');
    const v = await h.text();
    h.check(/left today/.test(v), 'Today list is the first thing she sees');
    h.check(/picked at \d/.test(v), 'The list says what time it was picked');
    const cards = await h.page.locator('#view .card').count();
    h.check(cards >= 5 && cards <= 10, `Today shows a short list (${cards} roles)`);
    await h.shot('today');
    // D-076: her settings predate role families (tiers Core + Adjacent): she keeps exactly what she had
    const tags = await h.page.locator('#view .card .ck.tier').evaluateAll(xs => xs.map(x => [x.textContent, /t-core/.test(x.className)]));
    h.check(tags.every(([t, core]) => (t === 'Product') === core), `Product roles are highlighted as her field, others plain (${[...new Set(tags.map(t => t[0]))].join(', ')})`);
    h.check(!tags.some(([t]) => /analytics|Business analysis|Project|marketing|Solutions/.test(t)), 'No stretch or new families appear (she had Stretch off)');

    h.task('Triage two fast, then ask for more without finishing the list');
    await h.page.locator('#view .card [data-tri="interested"]').first().click(); await h.wait(250);
    await h.page.locator('#view .card [data-tri="not"]').first().click(); await h.wait(250);
    await h.shot('after-two');
    const reasonsVisible = await h.page.locator('.reasons').count();
    h.check(reasonsVisible > 0, '"Why not?" reasons stay visible after Not for me');
    const more = h.page.getByRole('button', { name: /more/i });
    h.check(await more.count() > 0 && await more.first().isVisible(), 'A way to see more roles is on screen before finishing today\'s list');

    h.task('Open the best role: why ranked, description, pay');
    await h.page.locator('#view .card h3').first().click(); await h.wait(300);
    h.check(await h.has('Ranked #'), '"Why it\'s ranked here" line in the Summary tab');
    await h.shot('detail-summary');
    await h.click('#dt-jd'); await h.wait(300);
    const jd = await h.text('#dpanel');
    h.check(jd.length > 400, 'Job description loads');
    await h.shot('detail-jd');
    await h.click('#dt-summary');

    h.task('Interested → next steps → Applied');
    const btn = h.page.locator('.drawer [data-tri="interested"]');
    if ((await btn.getAttribute('aria-pressed')) !== 'true') { await btn.click(); await h.wait(250) }
    h.check(await h.has('Next steps'), 'Next steps appear after Interested');
    await h.page.locator('.drawer [data-act="mreq"]').first().click(); await h.wait(250);
    const w = await h.writes();
    h.check(w.some(x => x[1].startsWith('market_req/')), 'Market check request saved');
    await h.page.selectOption('#stage', 'Applied'); await h.wait(250);
    h.check((await h.writes()).filter(x => x[1].startsWith('triage/')).length >= 3, 'Stage change saved');
    await h.page.locator('.drawer [data-like="1"]').click(); await h.wait(250);
    h.check((await h.writes()).some(x => x[1].startsWith('likes/')), '"More like this" saved');
    await h.shot('detail-after-actions');
    await h.page.keyboard.press('Escape'); await h.wait(200);

    h.task('Pipeline shows the applied role');
    await h.click('[data-view="pipeline"]'); await h.wait(250);
    h.check(/Applied/.test(await h.text()), 'Pipeline has an Applied column with her role');
    await h.shot('pipeline');

    h.task('Finish the list: the rest of the matches follow straight away');
    await h.click('[data-view="digest"]'); await h.wait(200);
    for (let i = 0; i < 15 && !(await h.has('reviewed your top matches')); i++) { const b = h.page.locator('#view .card:not(.done) [data-tri="later"]').first(); if (!(await b.count())) break; await b.click(); await h.wait(150) }
    h.check(await h.has("You've reviewed your top matches for today"), 'A message says today\'s top matches are done');
    const rest = await h.page.locator('#view .card').count();
    h.check(rest >= 5, `Other matches show straight away, no extra tap (${rest})`);
    h.check(!(await h.has('All caught up')), 'No dead-end "All caught up" screen');
    await h.shot('after-top-matches');
  }
};

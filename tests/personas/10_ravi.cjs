// Ravi: long-time user, senior PM, set up before role types existed (PERSONAS.md §10). Mirrors the owner's real state
// on 10-17 (no field saved, older settings, resume-read roles, an empty Today list saved for today), all fictional.
const { top, bottom, tri } = require('./_common.cjs');
const today = () => { const d = new Date(); return d.getFullYear() + '-' + String(d.getMonth() + 1).padStart(2, '0') + '-' + String(d.getDate()).padStart(2, '0') };
module.exports = {
  id: 'ravi', name: 'Ravi, long-time PM user, re-runs setup and the taste test',
  viewport: { width: 1180, height: 820 },
  seed: jobs => ({
    'profile/main': { version: 4, headline: 'Senior PM, enterprise AI platforms', summary: 'Eight years in product.', work_status: 'needs_permit',
      current: { employer: 'Northwind', title: 'Senior Product Manager', level: 'L5' }, domains: ['Enterprise AI', 'Risk'], skills: ['SQL'],
      roles: [{ title: 'Senior Product Manager', company: 'Northwind', years: '2022-present', focus: 'AI platform governance' },
              { title: 'Product Manager', company: 'Northwind', years: '2019-2022', focus: 'Ads safety policy' },
              { title: 'Business Analyst', company: 'Contoso', years: '2015-2019', focus: 'Analytics and forecasting' }],
      education: ['MBA, Example University (2019)'], experience_years: { total: 11, product_management: 6 },
      preferences: { domains_wanted: 'enterprise AI, risk', target_level: 'L6' } },
    'settings/prefs': { regions: ['GTA', 'Waterloo Region', 'Remote-Canada'], other_regions: false, tiers: ['Core', 'Adjacent', 'Stretch'], exclude_people_mgmt: false, include_no_pay: true,
      checks: { green_regions: ['GTA', 'Waterloo Region', 'Remote-Canada'], pay_green: 200000, pay_yellow: 170000, level_green: 6, level_yellow: 5, fresh_green: 14, fresh_yellow: 30 } },
    'settings/today': { date: today(), ids: [], explore: null, built_at: new Date().toISOString() },   // the broken state Ayush hit
    ...tri(top(jobs, j => /product/i.test(j.title), 4), 'interested'),
    ...tri(bottom(jobs, () => true, 4), 'not', { reasons: ['Not my domain'] }),
  }),
  async run(h) {
    h.task('An empty Today list repairs itself');
    const n0 = await h.page.locator('#view .card').count();
    h.check(n0 >= 5, `Today shows roles even though an empty list was saved earlier today (${n0})`);
    h.check(((await h.store())['settings/today'].ids || []).length >= 5, 'The repaired list is saved');
    await h.shot('today-healed');

    h.task('Profile shows his roles, and he can edit them');
    await h.click('[data-view="settings"]'); await h.wait(300);
    const rows = await h.page.locator('#rolelist .rolerow').count();
    h.check(rows === 3, `His 3 past roles are listed (${rows})`);
    h.check(/Years of experience in total/.test(await h.text()) && (await h.page.inputValue('#pf-yrs')) === '11', 'Years of experience are shown');
    h.check(/Example University/.test(await h.page.inputValue('#pf-edu')), 'Education is shown');
    const pm = await h.page.locator('[data-myfam="pm"]').isChecked();
    h.check(pm, 'Product management shows as his field');
    await h.shot('profile-roles');
    await h.page.fill('#rr-t-0', 'Staff Product Manager');
    await h.click('[data-act="addrole"]'); await h.wait(100);
    const last = h.page.locator('#rolelist .rolerow').last();
    await last.locator('[data-rr="title"]').fill('Intern'); await last.locator('[data-rr="company"]').fill('Fabrikam');
    await h.page.locator('#rolelist .rolerow').nth(2).locator('[data-act="rmrole"]').click(); await h.wait(100);
    h.check(/unsaved changes/i.test(await h.text('#savebar')), 'Editing roles shows the unsaved-changes bar');
    await h.click('[data-act="saveprefs"]'); await h.wait(400);
    const r1 = ((await h.store())['profile/main'] || {}).roles || [];
    h.check(r1.length === 3 && r1[0].title === 'Staff Product Manager' && r1[0].focus === 'AI platform governance', 'Edits keep the rest of each role');
    h.check(r1.some(r => r.company === 'Fabrikam') && !r1.some(r => r.company === 'Contoso'), 'Added and removed roles are saved');

    h.task('Run setup again: his field is pre-selected and nothing he set is lost');
    await h.click('[data-act="reonboard"]'); await h.wait(300);
    h.check((await h.page.locator('[data-obf="fam"][data-v="pm"]').getAttribute('aria-pressed')) === 'true', 'Product manager is already selected');
    await h.tap('Answer 2 more quick questions');
    const cities = await h.page.locator('[data-obf="city"][aria-pressed="true"]').allInnerTexts();
    h.check(cities.length === 2, `His cities are pre-selected (${cities.join(', ')})`);
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(150);
    h.check((await h.page.locator('[data-obf="status"][aria-checked="true"]').count()) === 1, 'His work status is pre-selected');
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(600);
    const p = (await h.store())['settings/prefs'] || {};
    h.check((p.families || []).join() === 'pm', 'His field is now saved explicitly');
    h.check((p.checks || {}).pay_green === 200000 && (p.checks || {}).pay_yellow === 170000, 'His own pay targets are kept (not reset to defaults)');
    h.check(p.other_regions === false, '"Rest of Canada" stays off, as he had it');
    h.check((p.families_shown || []).includes('pmm') && (p.families_shown || []).includes('program'), `The other types he saw are kept (${(p.families_shown || []).join(', ')})`);
    const n1 = await h.page.locator('#view .card').count();
    h.check(n1 >= 5, `His list is there after setup (${n1})`);

    h.task('Taste test: mostly his field, nothing he already answered');
    await h.page.getByRole('button', { name: 'Take the 20-second taste test' }).click(); await h.wait(400);
    const metas = await h.page.locator('.tcard .tmeta').allInnerTexts();
    const kinds = metas.map(m => (m.split('\n')[2] || '').split(' · ')[0].trim());
    h.check(metas.length >= 6, `Eight real roles (${metas.length})`);
    h.check(kinds.filter(k => k === 'Product').length >= 6, `At least 6 are product management (${kinds.join(', ')})`);
    const ids = await h.page.locator('.tcard [data-obt="1"]').evaluateAll(b => b.map(x => x.dataset.id));
    const triaged = Object.keys(await h.store()).filter(k => k.startsWith('triage/')).map(k => k.slice(7));
    h.check(!ids.some(i => triaged.includes(i)), 'None of them are roles he already answered');
    await h.shot('taste');
    const nots = h.page.locator('.tcard [data-obt="-1"]');
    for (let i = 0; i < 6; i++) { await nots.nth(i).click(); await h.wait(60) }
    await h.page.locator('.tcard [data-obt="1"]').last().click(); await h.wait(60);
    await h.page.getByRole('button', { name: 'See my list' }).click(); await h.wait(800);
    const n2 = await h.page.locator('#view .card').count();
    h.check(n2 >= 5, `After the taste test his Digest still has a full list (${n2})`);
    h.check(((await h.store())['settings/today'].ids || []).length >= 5, 'and it is saved');
    await h.shot('after-taste');
    await h.reload();
    h.check(await h.page.locator('#view .card').count() >= 5, 'Still there after a reload');
    await h.click('[data-show="todo"]'); await h.wait(250);
    h.check(await h.page.locator('#view .card').count() >= 5, 'All to triage has roles too');
  }
};

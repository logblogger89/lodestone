// Mei: AI product lead, permanent resident in Montreal, exploring the market, not applying (PERSONAS.md §3)
module.exports = {
  id: 'mei', name: 'Mei, AI PM, permanent resident, exploring pay and companies',
  viewport: { width: 1440, height: 900 },
  seed: () => ({
    'profile/main': { version: 2, headline: 'AI product lead', current: { employer: 'Northwind AI', title: 'Lead PM, AI', level: 'L6' },
      work_status: 'needs_permit', domains: ['AI', 'ML platform'] },
    'settings/prefs': { regions: ['Montreal', 'Remote-Canada'], other_regions: true, tiers: ['Core', 'Adjacent', 'Stretch'], exclude_people_mgmt: false, include_no_pay: true },
  }),
  async run(h) {
    h.task('Browse all of Canada sorted by pay');
    await h.click('[data-show="all"]'); await h.wait(200);
    await h.page.selectOption('#region', 'all'); await h.page.selectOption('#sort', 'pay'); await h.wait(300);
    const pays = (await h.page.locator('#view .card').allInnerTexts()).map(t => (t.match(/CA\$[\d.,]+K?[–-][\d.,]+K?( est\.)?/) || [''])[0]).filter(Boolean);
    h.check(pays.length >= 5, `Pay shown on the top cards (${pays.length})`);
    h.note('works', 'Top pay tags: ' + pays.slice(0, 4).join(' | '));
    await h.shot('all-by-pay');

    h.task('Search "AI" and look at one company');
    await h.page.fill('#q', 'AI'); await h.wait(300);
    const n = await h.page.locator('#view .card').count();
    h.check(n > 0, `Search for AI finds roles (${n})`);
    await h.page.locator('#view .card h3').first().click(); await h.wait(250);
    await h.click('#dt-company'); await h.wait(300);
    await h.shot('company-tab');
    const see = h.page.locator('[data-cofilter]');
    if (await see.count()) { await see.first().click(); await h.wait(250); h.check((await h.page.inputValue('#q')).length > 0, 'See all roles at the company filters the list') }
    else h.note('annoyance', 'This company has one role, so no "See all"');

    h.task('Companies page and the daily report');
    await h.click('[data-view="companies"]'); await h.wait(250);
    h.check((await h.page.locator('#view').innerText()).length > 300, 'Companies page lists companies');
    await h.shot('companies');
    await h.click('[data-view="reports"]'); await h.wait(250);
    await h.shot('reports');

    h.task('Tell the app she doesn\'t need a work permit');
    await h.click('[data-view="settings"]'); await h.wait(250);
    const opts = await h.page.locator('#pf-work option').allInnerTexts();
    h.note('works', 'Work-permit options: ' + opts.join(' / '));
    h.check(opts.some(o => /citizen|permanent resident|don't need/i.test(o)), 'There is a "citizen or permanent resident" option');
    await h.page.selectOption('#pf-work', 'no_permit');
    await h.click('[data-act="saveprefs"]'); await h.wait(300);
    await h.click('[data-view="digest"]'); await h.click('[data-show="all"]'); await h.wait(250);
    const v = await h.text();
    h.check(!/Hires from abroad|Sponsorship unknown|Sponsors sometimes/.test(v), 'Sponsorship tags are gone once she says she\'s a permanent resident');
    await h.page.locator('#view .card h3').first().click(); await h.wait(250);
    await h.click('#dt-summary');
    h.check(!/Work-permit pathway/i.test(await h.text('#dpanel')), 'The role view drops the work-permit table for her');
    await h.shot('pr-detail');
    await h.page.keyboard.press('Escape');
  }
};

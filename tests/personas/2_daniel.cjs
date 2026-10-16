// Daniel: product marketer arriving in Calgary on an open work permit, no resume, first visit (PERSONAS.md §2)
module.exports = {
  id: 'daniel', name: 'Daniel, product marketer, first visit, open work permit, no resume',
  viewport: { width: 1366, height: 768 },
  seed: () => ({}),          // brand new: no profile, no settings, no history
  async run(h) {
    h.task('First visit with nothing set up');
    const v = await h.text();
    await h.shot('first-screen');
    h.check(/welcome|new here|get started|set up/i.test(v), 'The first screen says what Lodestone is and how to start');
    h.check(!/left today/.test(v) || /profile/i.test(v), 'A first-timer is pointed to the Profile before a ranked list built for someone else\'s defaults');
    const firstCard = (await h.page.locator('#view .card .meta').first().innerText().catch(() => ''));
    h.note('works', 'First card: ' + firstCard.slice(0, 80));

    h.task('Set open work permit and Calgary in the Profile');
    await h.click('[data-view="settings"]'); await h.wait(250);
    await h.shot('profile-empty');
    await h.page.selectOption('#pf-work', 'open_permit');
    for (const r of ['GTA', 'Waterloo Region', 'Remote-Canada']) { const c = h.page.locator(`[data-region="${r}"]`); if (await c.isChecked()) await c.uncheck() }
    await h.page.locator('[data-region="Calgary"]').check();
    await h.page.locator('[data-ptier="Stretch"]').check().catch(() => {});
    await h.click('[data-act="saveprefs"]'); await h.wait(400);
    const st = await h.store();
    h.check(st['settings/prefs'] && st['settings/prefs'].regions.includes('Calgary'), 'Calgary saved as his region');
    h.check(st['profile/main'] && st['profile/main'].work_status === 'open_permit', 'Open work permit saved');

    h.task('Back to the list: does it reflect Calgary?');
    await h.click('[data-view="digest"]'); await h.wait(300);
    const metas = await h.page.locator('#view .card .meta').allInnerTexts();
    const calgary = metas.filter(m => /calgary|remote/i.test(m)).length;
    h.check(metas.length && calgary / metas.length >= 0.5, `Today's list leans to Calgary after he set it (${calgary} of ${metas.length})`);
    await h.shot('list-after-profile');
    const v2 = await h.text();
    h.check(!/Sponsorship unknown/.test(v2) || /open work permit/i.test(v2), 'Sponsorship tags step back for someone with an open work permit');

    h.task('Understand role types and jargon');
    await h.page.locator('details.legend summary').click(); await h.wait(150);
    const legend = await h.text('details.legend');
    h.check(/PM-adjacent/.test(legend) && /Stretch/.test(legend), 'Legend explains the role types');
    h.check(/L5|L6|level/i.test(legend), 'Legend explains the Google levels (L5, L6) shown on cards');
    await h.shot('legend');

    h.task('Paste a LinkedIn link');
    await h.click('[data-view="add"]'); await h.wait(200);
    await h.page.fill('#paste', 'https://www.linkedin.com/jobs/view/1234567890');
    await h.click('[data-act="addjob"]'); await h.wait(300);
    h.check((await h.writes()).some(x => x[0] === 'add' && x[1].startsWith('inbox/')), 'Pasted link saved to the inbox');
    h.check(/linkedin\.com\/jobs/i.test(await h.text()), 'The inbox shows what he pasted');
    await h.shot('add-job');

    h.task('No finished resume: can he still describe himself?');
    await h.click('[data-view="settings"]'); await h.wait(250);
    const p = await h.text();
    h.check(/paste/i.test(p), 'He can paste rough text instead of uploading a file');
    h.check(/rough|draft|don't have|no resume|without a resume/i.test(p), 'The Profile reassures him a rough draft or no resume is fine');
  }
};

// Omar: senior business analyst in Toronto banking, moving into tech; permanent resident; first visit on a laptop (PERSONAS.md §8)
// D-076: role types that make sense for someone who isn't a product manager.
const STRIP = jobs => {   // a brand-new person: nothing has been scored for him yet, so the list is provisional
  const all = {}; Object.values(jobs).forEach(j => { const c = { ...j }; delete c.fit; all[j.id] = c });
  const out = { 'jobs/b0': { jobs: all } }; for (let i = 1; i < 16; i++) out[`jobs/b${i}`] = { jobs: {} };
  return out;
};
module.exports = {
  id: 'omar', name: 'Omar, senior business analyst, Toronto, new to Lodestone',
  viewport: { width: 1280, height: 860 },
  seed: jobs => STRIP(jobs),
  async run(h) {
    h.task('Setup in his own words');
    await h.tap('Get started');
    await h.page.locator('[data-obf="city"][data-v="GTA"]').click(); await h.wait(120);
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(150);
    await h.page.locator('[data-obf="status"][data-v="no_permit"]').click(); await h.wait(120);
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(150);
    const cards = await h.page.locator('.obfams .obopt b').allInnerTexts();
    h.check(cards.some(c => /business or systems analyst/i.test(c)), `The role cards include business analysts (${cards.length} cards)`);
    h.check(cards.some(c => /project/i.test(c)) && cards.some(c => /data or BI analyst/i.test(c)), 'and project managers and data analysts');
    await h.page.fill('#ob-role', 'senior business analyst, banking and payments, 9 years'); await h.wait(150);
    const heard = await h.text('#ob-heard');
    h.check(/Business analysis/.test(heard), `Typing "business analyst" is understood without tapping a card ("${heard.trim()}")`);
    h.check(!/covers product and nearby roles/i.test(await h.text()), 'He is not told his role isn\'t covered');
    h.check((await h.page.locator('[data-obf="fam"][data-v="ba"]').getAttribute('aria-pressed')) === 'true', 'The business analyst card lights up as he types');
    await h.shot('role-typed');
    await h.page.locator('.obnav .btn.primary').click(); await h.wait(250);

    h.task('Taste test: his kind of work, not product management');
    const metas = await h.page.locator('.tcard .tmeta').allInnerTexts();
    const fam = m => (m.split('\n')[2] || '').split(' · ')[0].trim();
    const kinds = metas.map(fam);
    h.check(metas.length >= 6, `Taste test shows real roles (${metas.length})`);
    const near = kinds.filter(k => /Business analysis|analytics|Project|Strategy/.test(k)).length;
    h.check(near >= Math.min(6, metas.length), `Taste-test roles are business analysis or close to it (${kinds.join(', ')})`);
    h.check(!kinds.some(k => k === 'Product'), 'No product manager roles in his taste test');
    await h.shot('taste');
    const b = h.page.locator('.tcard [data-obt="1"]');
    for (let i = 0; i < 3; i++) { await b.nth(i).click(); await h.wait(80) }
    await h.page.getByRole('button', { name: 'See my list' }).click(); await h.wait(500);

    h.task('His list speaks his language');
    const st = await h.store(), prefs = st['settings/prefs'] || {}, prof = st['profile/main'] || {};
    h.check((prefs.families || []).join() === 'ba', `His field is saved as business analysis (${(prefs.families || []).join()})`);
    h.check((prefs.families_shown || []).includes('analytics') && (prefs.families_shown || []).includes('project'), `Related fields are shown too (${(prefs.families_shown || []).join(', ')})`);
    h.check(((prof.preferences || {}).families || []).join() === 'ba', 'The profile the scorer reads knows his field');
    h.check((prefs.checks || {}).pay_green === 120000, `Pay targets fit a business analyst (green from CA$${((prefs.checks || {}).pay_green || 0) / 1000}K)`);
    const list = await h.text();
    const pmw = (list.match(/.{0,40}(PM-adjacent|Core PM|(?<!\d\d? ?)\bPM\b).{0,20}/g) || []);
    h.check(!pmw.length, `No "PM" wording anywhere on his list (${pmw.slice(0, 2).join(' | ')})`);
    const tags = await h.page.locator('#view .card .ck.tier').evaluateAll(xs => xs.map(x => [x.textContent, x.className, x.title]));
    const ba = tags.filter(([t]) => t === 'Business analysis');
    h.check(ba.length >= 3, `Most of today's roles are business analysis (${ba.length} of ${tags.length})`);
    h.check(ba.every(([, c]) => /t-core/.test(c)), 'Business analysis roles carry the highlighted "your field" tag');
    h.check(ba.length && /your field/.test(ba[0][2]), `Hovering the tag says what it means ("${ba[0] && ba[0][2]}")`);
    h.check(tags.slice(0, 3).every(([t]) => t === 'Business analysis'), `His field comes first (${tags.slice(0, 3).map(t => t[0]).join(', ')})`);
    const reds = await h.page.locator('#view .card .ck-bad').allInnerTexts();
    h.check(!reds.some(r => /CA\$1[0-2]\dK/.test(r)), `Ordinary BA pay isn't marked red (${reds.filter(r => /CA\$/.test(r)).slice(0, 3).join(', ') || 'none'})`);
    await h.shot('first-list');

    h.task('Understand the role types');
    await h.page.locator('details.legend summary').click(); await h.wait(150);
    const legend = await h.text('details.legend');
    h.check(/your field \(Business analysis\)/.test(legend), 'The legend names his field');
    h.check(/Data analytics/.test(legend) && /Project management/.test(legend), 'and the related fields he also sees');

    h.task('Fine-tune: stop seeing analytics roles');
    await h.click('[data-view="settings"]'); await h.wait(250);
    const mine = await h.page.locator('[data-myfam]:checked').evaluateAll(xs => xs.map(x => x.dataset.myfam));
    h.check(mine.join() === 'ba', 'Profile shows "What you do: Business analysis"');
    const also = await h.page.locator('.famset').nth(1).innerText();
    h.check(/Data analytics · related/.test(also), 'Also-show list marks which fields are related');
    await h.page.locator('#pf-subnav [data-jump="ps-want"]').click(); await h.wait(700);
    await h.shot('profile-families');
    await h.page.locator('[data-alsofam="analytics"]').uncheck(); await h.wait(100);
    await h.click('[data-act="saveprefs"]'); await h.wait(300);
    h.check(!((await h.store())['settings/prefs'].families_shown || []).includes('analytics'), 'Unticking analytics is saved');
    await h.click('[data-view="digest"]'); await h.click('[data-show="todo"]'); await h.wait(250);
    const after = await h.page.locator('#view .card .ck.tier').allInnerTexts();
    h.check(after.length && !after.includes('Data analytics'), `No analytics roles after that (${[...new Set(after)].join(', ')})`);
    const chips = await h.page.locator('[data-fam]').allInnerTexts();
    h.check(chips.length >= 2 && /^Business analysis/.test(chips[1]), `The role-type filter lists his field first, with counts (${chips.join(' | ')})`);
    await h.shot('all-to-triage');
  }
};

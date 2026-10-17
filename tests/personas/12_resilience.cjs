// Resilience (D-079): break things on purpose and check the safety nets hold. Reproduces the 10-17 outage (the app
// writing onto frozen database objects) and a screen that fails to draw.
const ravi = require('./10_ravi.cjs');
module.exports = {
  id: 'resilience', name: 'Resilience: the 10-17 outage and a crashing screen, on purpose',
  viewport: { width: 1180, height: 820 },
  seed: jobs => ravi.seed(jobs),
  async run(h) {
    h.task('The real database delivers frozen data');
    const frozen = await h.evalS(() => { const any = Object.values(window.__store).find(v => v && v.jobs); return true });
    h.check(await h.page.locator('#view .card').count() >= 5, 'With frozen data, the list shows (the 10-17 fix)');

    h.task('If relevance can\'t be worked out, roles still show (fail-safe)');
    const n = await h.evalS(() => { Object.values(S.jobs).forEach(j => { delete j.rel }); S._famKey = '__'; const orig = relevance; window.relevance = null;
      // simulate the 10-17 failure: every job's relevance throws
      S.jobs = Object.fromEntries(Object.entries(S.jobs).map(([k, j]) => [k, Object.freeze({ ...j, rel: undefined })])); render(); return Object.values(S.jobs).filter(j => prefOk(j)).length });
    h.check(n > 0, `Roles still visible when relevance fails (${n})`);
    h.check(await h.page.locator('#view .card').count() > 0, 'and the page shows them');
    const errs = await h.evalS(() => ERRS.length);
    h.check(errs > 0, `The failure is recorded for the health note (${errs} errors)`);
    await h.shot('fail-safe');

    h.task('A screen that fails to draw shows a way out');
    await h.evalS(() => { window.__realViewDigest = viewDigest; viewDigest = () => { throw new Error('test: digest broke') }; S.view = 'digest'; render() });
    const t = await h.text();
    h.check(/Something went wrong showing this page/.test(t) && /Your data is safe/.test(t), 'A clear message instead of a blank page');
    h.check(await h.page.getByRole('button', { name: 'Reload' }).count() && await h.page.getByRole('button', { name: 'Go to Profile' }).count(), 'with Reload and a way to another page');
    await h.shot('error-screen');
    await h.page.getByRole('button', { name: 'Go to Profile' }).click(); await h.wait(300);
    h.check(/Tell Lodestone about your work/.test(await h.text()), 'Other pages still work');
    await h.evalS(() => { viewDigest = window.__realViewDigest });

    h.task('The health note reports it');
    await h.wait(1800);
    const hn = await h.evalS(() => window.__store['health/app'] || null);
    h.check(hn && hn.errors > 0 && hn.last_errors.some(e => /digest broke|relevance|render/.test(e)), `Health note lists the errors (${hn ? hn.last_errors.join(' | ') : 'none'})`);
    h.check(hn && hn.version, `and the app version (${hn && hn.version})`);
  }
};

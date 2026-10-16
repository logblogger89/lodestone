// Shared helpers for persona journeys (scripts/persona_test.cjs).
const live = jobs => Object.values(jobs).filter(j => j.live && j.fit && j.fit.subs);
const avg = j => { const s = j.fit.subs; return Object.values(s).reduce((a, b) => a + b, 0) / Object.keys(s).length };
const top = (jobs, f = () => true, n = 5) => live(jobs).filter(f).sort((a, b) => avg(b) - avg(a)).slice(0, n);
const bottom = (jobs, f = () => true, n = 5) => live(jobs).filter(f).sort((a, b) => avg(a) - avg(b)).slice(0, n);
const tri = (list, status, extra = {}) => Object.fromEntries(list.map(j => [`triage/${j.id}`,
  { status, title: j.title, company: j.company, updated_at: new Date().toISOString(), ...(status === 'interested' ? { stage: 'Shortlisted' } : {}), ...extra }]));
const daysAgo = d => new Date(Date.now() - d * 864e5).toISOString();
module.exports = { live, top, bottom, tri, daysAgo };

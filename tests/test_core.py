import json
import pathlib
import unittest

from lodestone import dedup
from lodestone.adapters import ADAPTERS
from lodestone.geo import classify
from lodestone.models import Posting
from lodestone.rules import classify_title
from lodestone.text import html_to_text, slug_candidates

FIX = pathlib.Path(__file__).parent / "fixtures"


def P(loc, country=None, remote=None, title="Product Manager"):
    return Posting(source="t", company="Acme", slug="acme", source_job_id="1", title=title, url="u",
                   location_raw=loc, country_hint=country, remote_hint=remote)


class TestText(unittest.TestCase):
    def test_html(self):
        self.assertEqual(html_to_text("&lt;p&gt;Hi &amp;amp; bye&lt;/p&gt;"), "Hi & bye")

    def test_slugs(self):
        self.assertEqual(slug_candidates("Wealthsimple")[0], "wealthsimple")
        self.assertIn("cohere", slug_candidates("Cohere AI"))
        self.assertIn("block", slug_candidates("Block (Square / Cash App)"))


class TestGeo(unittest.TestCase):
    def test_canada(self):
        self.assertEqual(classify(P("Toronto, ON")).region, "GTA")
        self.assertEqual(classify(P("Kitchener, Ontario, Canada")).region, "Waterloo Region")
        self.assertEqual(classify(P("Remote", country="CA")).region, "Remote-Canada")
        self.assertTrue(classify(P("Vancouver, BC")).in_canada)

    def test_not_canada(self):
        self.assertFalse(classify(P("Amsterdam, NL", country="nl")).in_canada)
        for loc in ("Waterloo, Iowa", "London, UK", "San Francisco, CA", "Remote - US", "New York, NY"):
            self.assertFalse(classify(P(loc)).in_canada, loc)


class TestRules(unittest.TestCase):
    def test_tiers(self):
        self.assertEqual(classify_title("Sr. Product Manager, Payments").tier, "Core")
        self.assertEqual(classify_title("Technical Program Manager II").tier, "Adjacent")
        self.assertEqual(classify_title("Trust & Safety Program Lead").tier, "Adjacent")
        self.assertEqual(classify_title("Product Marketing Manager").tier, "Stretch")
        self.assertIsNone(classify_title("Software Engineer").tier)

    def test_families_are_absolute_and_closeness_is_relative(self):
        from lodestone.rules import closeness
        fam = lambda t: classify_title(t).family
        self.assertEqual(fam("Senior Business Analyst"), "ba")
        self.assertEqual(fam("Business Systems Analyst II"), "ba")
        self.assertEqual(fam("Technical Program Manager"), "program")
        self.assertEqual(fam("IT Project Manager"), "project")
        self.assertEqual(fam("Senior Data Analyst"), "analytics")
        self.assertEqual(fam("Program Manager, Trust & Safety"), "program")
        self.assertEqual(fam("Chief of Staff to the CTO"), "strategy")
        self.assertEqual(fam("Senior Product Manager, Payments"), "pm")
        self.assertEqual(classify_title("Senior Business Analyst").tier, "Other")   # stored, though not near the default families
        self.assertEqual(closeness("program", ["program"]), "Core")
        self.assertEqual(closeness("pm", ["program"]), "Adjacent")
        self.assertEqual(closeness("ba", ["program"]), "Stretch")
        self.assertEqual(closeness("analytics", ["ba"]), "Adjacent")
        self.assertEqual(fam("Senior Product Analyst"), "prodanalytics")
        self.assertIsNone(closeness("analytics", ["pm"]))          # data analysts don't join a product manager's list
        self.assertIsNone(closeness("solutions", ["ba"]))
        self.assertTrue(classify_title("Junior Business Analyst").excluded)

    def test_excluded_and_people(self):
        self.assertTrue(classify_title("Associate Product Manager").excluded)
        self.assertTrue(classify_title("Product Manager Intern").excluded)
        self.assertTrue(classify_title("Director of Product").people_mgmt_hint)


class TestAdapters(unittest.TestCase):
    def test_greenhouse_parse(self):
        ps = ADAPTERS["greenhouse"].parse(json.loads((FIX / "greenhouse_jobs.json").read_text()), "Acme", "acme")
        self.assertEqual(len(ps), 4)
        self.assertEqual(ps[0].url, "https://boards.greenhouse.io/acme/jobs/101")
        self.assertEqual(ps[0].canonical_key, "greenhouse:acme:101")
        self.assertIn("fraud", ps[0].description)
        kept = [p for p in ps if classify(p).in_canada and classify_title(p.title).tier
                and not classify_title(p.title).excluded]
        self.assertEqual([p.source_job_id for p in kept], ["101"])

    def test_lever_parse(self):
        ps = ADAPTERS["lever"].parse(json.loads((FIX / "lever_postings.json").read_text()), "Acme", "acme")
        p = ps[0]
        self.assertEqual(p.url, "https://jobs.lever.co/acme/abc-1")
        self.assertEqual(p.pay["min"], 150000)
        self.assertEqual(classify(p).region, "Waterloo Region")


class TestDedup(unittest.TestCase):
    def rec(self, key, source, title="Senior Product Manager", company="Acme Inc."):
        return {"key": key, "source": source, "url": f"https://{source}/{key}", "seen_at": "t0",
                "group": dedup.group_key(company, title, "GTA"), "company": company, "title": title}

    def test_exact_and_cross_source(self):
        jobs = {}
        a = dedup.merge(jobs, self.rec("greenhouse:acme:1", "greenhouse"))
        self.assertEqual(dedup.merge(jobs, self.rec("greenhouse:acme:1", "greenhouse")), a)
        b = dedup.merge(jobs, self.rec("linkedin:acme:9", "linkedin", title="Sr Product Manager", company="Acme"))
        self.assertEqual(a, b)
        self.assertEqual(len(jobs[a]["sightings"]), 2)

    def test_same_source_different_ids_kept(self):
        jobs = {}
        dedup.merge(jobs, self.rec("greenhouse:acme:1", "greenhouse"))
        dedup.merge(jobs, self.rec("greenhouse:acme:2", "greenhouse"))
        self.assertEqual(len(jobs), 2)


if __name__ == "__main__":
    unittest.main()

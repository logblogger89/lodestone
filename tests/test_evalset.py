import unittest

from lodestone import evalset

NOW = 1792000000.0


def job(i, subs, live=True, company="A"):
    return {"id": i, "company": company, "title": i, "live": live, "posted_at": None, "first_seen": None,
            "pathway": {"score": 45, "signals": []}, "pay": None, "fit": {"subs": subs}}


S_HI = {"role": 90, "level": 90, "domain": 90, "pathway": 45, "pay": 50, "skills": 90}
S_LO = {"role": 50, "level": 40, "domain": 50, "pathway": 45, "pay": 50, "skills": 50}


class TestRanking(unittest.TestCase):
    def test_interested_above_later_is_perfect(self):
        jobs = {"a": job("a", S_HI), "b": job("b", S_LO)}
        r = evalset.ranking({"a": {"status": "interested"}, "b": {"status": "later"}}, jobs, now=NOW)
        self.assertEqual((r["pairwise"], r["interested_in_top25"], r["labels"]["later"]), (1.0, 1, 1))
        self.assertFalse(r["enough_labels"])

    def test_current_employer_is_an_internal_transfer(self):
        j = job("g", S_LO, company="Google")
        self.assertEqual(evalset.pathway(j, {"current": {"employer": "Google"}}), 95)
        self.assertEqual(evalset.pathway(j, {"work_status": "open_permit"}), 95)
        self.assertEqual(evalset.pathway(j, {}), 45)

    def test_relative_dates_count_from_when_read(self):
        read = NOW - 10 * 86400
        self.assertAlmostEqual(evalset._when("Posted 5 Days Ago", read), read - 5 * 86400)


if __name__ == "__main__":
    unittest.main()

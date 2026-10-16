import unittest

from lodestone import jdsections as js

POSTING = """Stripe is a financial infrastructure platform for businesses. Millions of companies use Stripe to accept payments and grow their revenue.

About the team
The Payments Risk team protects Stripe and its users from fraud while keeping good payments flowing, using machine learning and rules.

What you'll do
- Own the roadmap for risk decisioning
- Work with engineering and data science

Equal Employment Opportunity
Stripe is an equal opportunity employer and considers all applicants without regard to protected status.
"""


class TestSections(unittest.TestCase):
    def test_company_team_and_body(self):
        self.assertTrue(js.company_about(POSTING, "Stripe").startswith("Stripe is a financial"))
        head, text = js.team_about(POSTING)
        self.assertEqual(head, "About the team")
        self.assertIn("Payments Risk team", text)
        app = js.for_app(POSTING)
        self.assertIn("## What you'll do", app["text"])
        self.assertNotIn("equal opportunity employer", app["text"])     # legal notices left to the original
        self.assertTrue(app["legal"])

    def test_no_sections_and_best_about(self):
        self.assertIsNone(js.team_about("Build things. Ship things."))
        best = js.best_company_about(["We've won awards.", "Acme is a payments company.", "We've won awards."], "Acme")
        self.assertEqual(best, "Acme is a payments company.")


if __name__ == "__main__":
    unittest.main()

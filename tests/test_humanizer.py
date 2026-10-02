import unittest
from humanizer import humanize, score, analyze, DEFAULT_PROFILE


class T(unittest.TestCase):
    def h(self, s, **kw):
        return humanize(s, DEFAULT_PROFILE, seed=1, **kw)

    def test_vocab(self):
        out = self.h("We delve into a robust, pivotal plan.")
        for bad in ("delve", "robust", "pivotal"):
            self.assertNotIn(bad, out.lower())

    def test_articles_kept(self):
        self.assertIn("has a ", self.h("It boasts a view."))
        self.assertIn("a guide", self.h("It serves as a guide."))

    def test_chatbot_residue(self):
        out = self.h("Great question! The sky is blue. I hope this helps!")
        self.assertEqual(out.strip(), "The sky is blue.")

    def test_ing_tail(self):
        out = self.h("The firm grew in 2020, highlighting its pivotal role in the market.")
        self.assertEqual(out.strip(), "The firm grew in 2020.")

    def test_negative_parallelism(self):
        self.assertRegex(self.h("It’s not just a bug, it’s a mess."), r"It(’|.)?s? ?(is )?a mess")

    def test_code_untouched(self):
        src = "Intro\n\n```\nrobust = leverage(delve)\n```\n"
        self.assertIn("robust = leverage(delve)", self.h(src))

    def test_score_drops(self):
        s = "In today's fast-paced world, it's crucial to leverage robust, seamless, and comprehensive tools."
        self.assertLess(score(self.h(s))["score"], score(s)["score"])

    def test_profile(self):
        p = analyze("I don't know... it's fine, really. But I'd go anyway. So yeah." * 5)
        self.assertGreater(p["contractions_per_100w"], 0)
        self.assertGreater(p["ellipses_per_100w"], 0)

    def test_own_phrases_kept(self):
        prof = {**DEFAULT_PROFILE, "own_phrases": ["at the end of the day"]}
        out = humanize("At the end of the day, we left.", prof, seed=1)
        self.assertIn("At the end of the day", out)

    def test_curly_quotes_kept_and_dash_style(self):
        prof = {**DEFAULT_PROFILE, "curly_quote_rate": 1.0, "em_dashes_per_100w": 0.0}
        out = humanize("It’s “fine” — really.", prof, seed=1)
        self.assertIn("“fine”", out)
        self.assertNotIn("—", out)

    def test_own_writing_barely_changes(self):
        src = "I never wanted to be anyone’s first choice --- as people would call it --- but here we are."
        self.assertEqual(humanize(src, DEFAULT_PROFILE, seed=1).strip(), src)


if __name__ == "__main__":
    unittest.main()

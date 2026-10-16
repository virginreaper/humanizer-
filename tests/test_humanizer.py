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


class SecondPass(unittest.TestCase):
    def h(self, s, **kw):
        return humanize(s, DEFAULT_PROFILE, seed=1, **kw)

    def test_markup_leaks_removed(self):
        out = self.h("The school opened in 1990.citeturn0search1 See :contentReference[oaicite:3]{index=3} now.")
        for bad in ("turn0", "oaicite", "contentReference"):
            self.assertNotIn(bad, out)
        self.assertIn("The school opened in 1990.", out)

    def test_image_markup_keeps_real_words(self):
        out = self.h("Also iturn0image0turn0image1 end. I turn left.")
        self.assertNotIn("turn0", out)
        self.assertIn("I turn left", out)

    def test_utm_stripped_from_urls(self):
        out = self.h("See https://x.com/a?utm_source=chatgpt.com&b=1 and https://y.com/p?utm_source=openai.")
        self.assertIn("https://x.com/a?b=1", out)
        self.assertNotIn("utm_source", out)

    def test_cutoff_and_flattery(self):
        out = self.h("You're absolutely right! As of my last knowledge update in January 2022, the plan works.")
        self.assertEqual(out.strip(), "The plan works.")

    def test_staged_runups_and_closers(self):
        out = self.h("Here's the thing: the plan works. Read that again. Would you like me to expand on it?")
        self.assertEqual(out.strip(), "The plan works.")

    def test_hedge_stack(self):
        self.assertIn("could work", self.h("It could potentially work."))

    def test_new_vocab(self):
        out = self.h("We streamline a burgeoning paradigm.").lower()
        for bad in ("streamline", "burgeoning", "paradigm"):
            self.assertNotIn(bad, out)

    def test_emoji_lead_stripped(self):
        out = self.h("- \U0001F680 Launch phase starts.\n\n\U0001F9E0 Insight: users like it.")
        self.assertNotIn("\U0001F680", out)
        self.assertNotIn("\U0001F9E0", out)
        self.assertIn("Launch phase starts", out)

    def test_own_phrase_survives_new_patterns(self):
        prof = {**DEFAULT_PROFILE, "own_phrases": ["genuinely"]}
        self.assertIn("genuinely", humanize("I genuinely care.", prof, seed=1))

    def test_flag_only_tells_are_reported_not_rewritten(self):
        src = "Despite these challenges, the town continues to thrive."
        self.assertIn("continues to thrive", self.h(src))
        cats = {f["category"] for f in score(src)["findings"]}
        self.assertIn("significance-inflation", cats)

    def test_detector_new_categories(self):
        src = ("## Strategic Negotiations And Global Partnerships\n\n- **Speed:** fast.\n- **Safety:** safe.\n\n"
               "She ran. She hid. She slept. Hi [Entertainer's Name]. It is not widely documented.citeturn0search0")
        cats = {f["category"] for f in score(src)["findings"]}
        for c in ("title-case-headings", "inline-header-lists", "repeated-openers", "placeholder",
                  "cutoff-disclaimer", "markup-leak"):
            self.assertIn(c, cats)

    def test_sentence_case_headings_not_flagged(self):
        self.assertNotIn("title-case-headings",
                         {f["category"] for f in score("## How the six options compare\n\nText.")["findings"]})

    def test_no_facts_added(self):
        src = "Notably, the firm earned 12 million in 2020, genuinely beating its 2019 total."
        out = self.h(src)
        import re
        self.assertEqual(re.findall(r"\d+", out), re.findall(r"\d+", src))
        self.assertTrue(set(re.findall(r"[a-z]+", out.lower())) <= set(re.findall(r"[a-z]+", src.lower())))


if __name__ == "__main__":
    unittest.main()

class Regressions(unittest.TestCase):
    def h(self, s, **kw):
        return humanize(s, DEFAULT_PROFILE, seed=1, **kw)

    def test_serve_as_not_mangled(self):
        out = self.h("He acts as if nothing happened. She stands as high as the wall.")
        self.assertIn("acts as if", out)
        self.assertIn("stands as high as", out)
        self.assertNotIn("will are", self.h("The firm will serve as a guide."))
        self.assertIn("will be a guide", self.h("The firm will serve as a guide."))

    def test_article_agrees_with_swapped_word(self):
        self.assertIn("An important vote", self.h("A crucial vote."))

    def test_inflected_ai_words(self):
        out = self.h("He delved into the files and was delving again.").lower()
        self.assertNotIn("delv", out)

    def test_ing_tail_survives_decimal(self):
        self.assertEqual(self.h("Costs rose, highlighting a 2.5% rise for firms.").strip(), "Costs rose.")

    def test_real_claims_after_ing_kept(self):
        s = "The judge ruled early, ensuring the trial finished on time."
        self.assertIn("finished on time", self.h(s))

    def test_have_not_contracted_as_main_verb(self):
        p = {**DEFAULT_PROFILE, "contractions_per_100w": 5}
        out = humanize("I have a dog. We have to go. I have been there.", p, seed=1)
        self.assertIn("I have a dog", out)
        self.assertIn("We have to go", out)
        self.assertIn("I’ve been", out.replace("'", "’"))

    def test_negative_parallelism_keeps_about_and_clausal_form(self):
        self.assertIn("about trust", self.h("It is not about money, but about trust."))
        s = "It is not that I don’t care, it is that I can’t."
        self.assertRegex(self.h(s), r"(?:not|n.t) that I don")

    def test_year_range_stays_a_range(self):
        self.assertIn("2020–2024", self.h("The years 2020—2024 were hard."))

    def test_detector_ignores_plain_not_but(self):
        s = "The judgment was not unanimous, but the majority held firm."
        names = {f["category"] for f in score(s)["findings"]}
        self.assertNotIn("negative-parallelism", names)

    def test_isnt_just_framing(self):
        out = self.h("This isn't just a technological shift, it's a cultural transformation.")
        self.assertIn("a cultural transformation", out)
        self.assertNotIn("just a technological", out)

    def test_role_in_gerund(self):
        out = self.h("Media plays a pivotal role in shaping opinion.")
        self.assertIn("is central to shaping", out)

    def test_empower_keeps_to(self):
        out = self.h("Tools empowering users to decide.")
        self.assertIn("enabling users to decide", out)

    def test_paradigm_shift(self):
        self.assertNotIn("model shift", self.h("It is a paradigm shift in law."))

    def test_title_case_heading_sentence_cased_but_names_kept(self):
        out = self.h("# The Rise Of Apple In India\n\nApple grew fast in India last year, said Mr Rao.\n")
        self.assertIn("# The rise of Apple in India", out)

    def test_not_merely_framing(self):
        out = self.h("This phenomenon is not merely a trend; it is a profound shift.")
        self.assertNotIn("merely", out)
        self.assertIn("a deep shift", out)

    def test_detector_gives_examples(self):
        f = score("Studies show that it works. Experts say so.")["findings"]
        self.assertTrue(any(x.get("examples") for x in f))

    def test_filler_sentence_removed(self):
        out = self.h("The law changed. However, it would be remiss not to acknowledge the cost. Prices rose.")
        self.assertNotIn("remiss", out)
        self.assertIn("Prices rose", out)

    def test_despite_lead_in_dropped_claim_kept(self):
        out = self.h("Despite these challenges, the regime continues to grow.")
        self.assertEqual(out.strip(), "The regime continues to grow.")

    def test_two_word_heading(self):
        out = self.h("## Key Benefits\n\nThe benefits are clear.\n")
        self.assertIn("## Key benefits", out)

    def test_corpus_stays_clean(self):
        from tests.eval import run, LIMIT
        rows, worst = run()
        self.assertLessEqual(worst, LIMIT, rows)


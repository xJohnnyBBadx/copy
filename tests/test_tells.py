"""Unit tests for the COPY tells linter. Run: python -m unittest discover -s tests"""

import importlib.util
import json
import pathlib
import subprocess
import sys
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "skills" / "copy" / "scripts" / "tells.py"
FIXTURES = ROOT / "evals" / "fixtures"

spec = importlib.util.spec_from_file_location("tells", SCRIPT)
tells = importlib.util.module_from_spec(spec)
spec.loader.exec_module(tells)


def families(result):
    return {f["family"] for f in result["findings"]}


def fixture_text(name):
    raw = (FIXTURES / name).read_text(encoding="utf-8")
    return raw.split("-->", 1)[1]


class PhraseFamilies(unittest.TestCase):
    def test_stock_vocab_and_puffery(self):
        r = tells.run("Unlock your team's full potential with our seamless, world-class platform.")
        self.assertIn("vocab", families(r))
        self.assertIn("puffery", families(r))

    def test_residue(self):
        r = tells.run("Certainly! Here is a revised version of your copy for [Your Company].")
        self.assertIn("residue", families(r))

    def test_reveal_construction(self):
        r = tells.run("Nimbus isn't just software. It's a new way of working.")
        self.assertIn("reveal", families(r))
        r = tells.run("It's not a tool, it's a movement.")
        self.assertIn("reveal", families(r))

    def test_attribution(self):
        r = tells.run("Studies show that teams are happier. Experts agree.")
        self.assertIn("attribution", families(r))

    def test_literal_navigate_not_flagged(self):
        r = tells.run("Navigate to Settings and select Verify.")
        self.assertNotIn("vocab", families(r))

    def test_allow_list(self):
        r = tells.run("Our robust test suite runs nightly.", allow=["robust"])
        self.assertNotIn("vocab", families(r))

    def test_avoid_list(self):
        r = tells.run("Experience our premium artisan blend.", avoid=["premium", "artisan"])
        self.assertIn("brand-avoid", families(r))

    def test_claim_candidates(self):
        r = tells.run(fixture_text("f10-misleading-focus-app.md"))
        claims = [f for f in r["findings"] if f["family"] == "claim"]
        self.assertGreaterEqual(len(claims), 5)
        r = tells.run(fixture_text("f12-misleading-green-claims.md"))
        self.assertIn("claim", families(r))

    def test_ordinary_first_not_a_claim(self):
        r = tells.run("He told me the first night I rode up with him.")
        self.assertNotIn("claim", families(r))

    def test_html_comments_ignored(self):
        r = tells.run("<!-- seamless synergy -->\nSetup takes fifteen minutes.")
        self.assertEqual(r["findings"], [])

    def test_smart_quotes_normalized(self):
        r = tells.run("Here’s the thing: it’s worth noting.")
        self.assertIn("throat", families(r))


class Metrics(unittest.TestCase):
    def test_dramatic_fragments(self):
        r = tells.run("We rebuilt everything. Simple. Fast. Secure. That is the product.")
        self.assertIn("rhythm", families(r))

    def test_dash_density_reported_not_banned(self):
        one = tells.run("A person will read it — usually me. " + "This is filler text for length. " * 20)
        self.assertNotIn("format", families(one))
        many = tells.run("It works — fast — always — every time — no matter what.")
        self.assertIn("format", families(many))

    def test_uniform_sentence_length(self):
        text = " ".join(["We make good tools for teams."] * 8)
        r = tells.run(text)
        self.assertIn("rhythm", families(r))

    def test_bold_label_bullets(self):
        text = "- **Speed:** fast\n- **Scale:** big\n- **Safety:** safe\n"
        self.assertIn("format", families(tells.run(text)))


class Context(unittest.TestCase):
    def test_script_suppresses_throat_and_rhythm(self):
        text = "Here's the thing. Simple. Fast. Done. When it comes to receipts, we help."
        r = tells.run(text, context="10")
        self.assertNotIn("throat", families(r))
        self.assertNotIn("rhythm", families(r))
        self.assertIn("throat", r["suppressed"])


class FixtureCalibration(unittest.TestCase):
    """Generic copy should produce many hits; strong copy should produce few."""

    def count(self, name, context=None):
        return len(tells.run(fixture_text(name), context=context)["findings"])

    def test_generic_landing_is_noisy(self):
        self.assertGreaterEqual(self.count("f01-generic-saas-landing.md", "3"), 10)

    def test_strong_pieces_are_quiet(self):
        self.assertLessEqual(self.count("f04-strong-manifesto.md", "2"), 1)
        self.assertLessEqual(self.count("f15-unchanged-docs.md", "12"), 1)
        self.assertLessEqual(self.count("f17-unchanged-price-increase.md", "6"), 1)
        self.assertLessEqual(self.count("f19-strong-longform.md", "13"), 0)
        self.assertLessEqual(self.count("f16-unchanged-hero.md", "3"), 0)


class Cli(unittest.TestCase):
    def test_json_and_exit_codes(self):
        p = subprocess.run([sys.executable, str(SCRIPT), "--json", "-"],
                           input="Unlock seamless synergy.".encode("utf-8"), capture_output=True)
        self.assertEqual(p.returncode, 2)
        data = json.loads(p.stdout.decode("utf-8"))
        self.assertEqual(data["tool"], "copy-tells")
        p = subprocess.run([sys.executable, str(SCRIPT), "-"],
                           input="Setup takes about fifteen minutes.".encode("utf-8"), capture_output=True)
        self.assertEqual(p.returncode, 0)


class HeadingStacks(unittest.TestCase):
    def test_repeat_across_eyebrow_title_subtitle(self):
        r = tells.run("SCOPE / FEE / SCHEDULE\nScope, fee and schedule\nOne fixed fee for all six RFP deliverables.\n")
        hits = [f for f in r["findings"] if f["family"] == "stack"]
        self.assertEqual(len(hits), 1)
        self.assertIn("scope", hits[0]["note"])
        self.assertIn("fee", hits[0]["note"])

    def test_boilerplate_eyebrow_prefix_not_flagged(self):
        deck = "\n\n".join([
            "ACME SYSTEMS / APPROACH\nOne system for three kits\nThe vehicle sits at the centre.",
            "ACME SYSTEMS / COMMERCIALS\nScope, fee and schedule\nThree kits in ten days.",
            "ACME SYSTEMS / NEXT STEPS\nRequired to start\nWe begin when we receive these items.",
            "ACME SYSTEMS / COMPLIANCE\nRFP requirements\nHow we meet each one."])
        r = tells.run(deck)
        self.assertNotIn("stack", families(r))

    def test_distinct_stack_is_quiet(self):
        r = tells.run("ACME / COMMERCIALS\nScope, fee and schedule\nThree kits in 10 business days, at one fixed price.\n")
        self.assertNotIn("stack", families(r))

    def test_regressions_from_a_real_deck_are_flagged(self):
        # Both shapes slipped past a polish pass on a client deck (anonymised).
        for stack, word in [("ACME / COMMERCIALS\nScope, fee and schedule\nThree kits in 10 business days, for one fixed fee.\n", "fee"),
                            ("ACME / NEXT STEPS\nRequired to start\nWork starts when the studio receives these items.\n", "start")]:
            hits = [f for f in tells.run(stack)["findings"] if f["family"] == "stack"]
            self.assertEqual(len(hits), 1, stack)
            self.assertIn(word, hits[0]["note"])

    def test_prose_paragraphs_are_not_stacks(self):
        r = tells.run("We built the first version of this tool over a long winter and learned a great deal about it along the way.\nThe tool now ships to every team.\n")
        self.assertNotIn("stack", families(r))

    def test_card_figure_then_list_not_flagged(self):
        r = tells.run("SCHEDULE\nDAY 10\nCheck-in, day 2: Kit A direction.\nCheck-in, day 5: system and layouts.\n")
        self.assertNotIn("stack", families(r))

    def test_label_then_list_items_not_flagged(self):
        r = tells.run("PROGRAM\nOne system for 15+ shows a year.\nKit B is ready for the late-January show.\n")
        self.assertNotIn("stack", families(r))

    def test_allow_list_suppresses_brand_word(self):
        r = tells.run("Acme approach\nWhy Acme builds kits\n", allow=["acme"])
        self.assertNotIn("stack", families(r))


if __name__ == "__main__":
    unittest.main()


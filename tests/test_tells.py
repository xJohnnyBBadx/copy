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


if __name__ == "__main__":
    unittest.main()

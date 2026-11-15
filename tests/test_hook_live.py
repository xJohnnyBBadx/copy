"""Tests for the COPY hook and live server. Run: python -m unittest discover -s tests"""

import json
import pathlib
import subprocess
import sys
import tempfile
import threading
import unittest
import urllib.error
import urllib.request

ROOT = pathlib.Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "skills" / "copy" / "scripts"
sys.path.insert(0, str(SCRIPTS))
import live  # noqa: E402

GENERIC = "Certainly! Our seamless platform is clinically proven to double revenue. Studies show it works.\n"
CLEAN = "Setup takes about fifteen minutes. Ask your web person to add the records.\n"


def hook(event, payload):
    p = subprocess.run([sys.executable, str(SCRIPTS / "hook.py"), event],
                       input=json.dumps(payload).encode("utf-8"), capture_output=True, timeout=30)
    assert p.returncode == 0, p.stderr
    out = p.stdout.decode("utf-8").strip()
    return json.loads(out) if out else None


class Hook(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = pathlib.Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def edit(self, rel, text, session="s1"):
        path = self.root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
        return hook("post", {"session_id": session, "cwd": str(self.root),
                             "tool_name": "Write", "tool_input": {"file_path": str(path)}})

    def test_off_without_opt_in(self):
        self.assertIsNone(self.edit("page.md", GENERIC))

    def test_immediate_tier_when_brand_present(self):
        (self.root / "BRAND.md").write_text("# Brand\n", encoding="utf-8")
        out = self.edit("content/page.md", GENERIC)
        ctx = out["hookSpecificOutput"]["additionalContext"]
        self.assertIn("[residue]", ctx)
        self.assertIn("[claim]", ctx)
        self.assertIn("[attribution]", ctx)
        self.assertNotIn("[vocab]", ctx)  # vocab is deferred to the Stop deep pass

    def test_repeat_edit_does_not_repeat_findings(self):
        (self.root / ".copy").mkdir()
        self.assertIsNotNone(self.edit("page.md", GENERIC))
        self.assertIsNone(self.edit("page.md", GENERIC))

    def test_excluded_and_non_copy_files(self):
        (self.root / ".copy").mkdir()
        self.assertIsNone(self.edit("CLAUDE.md", GENERIC))
        self.assertIsNone(self.edit("app.py", GENERIC))
        self.assertIsNone(self.edit("node_modules/x/readme.md", GENERIC))

    def test_explicit_disable(self):
        (self.root / ".copy").mkdir()
        (self.root / ".copy" / "config.json").write_text('{"hook": {"enabled": false}}', encoding="utf-8")
        self.assertIsNone(self.edit("page.md", GENERIC))

    def test_stop_deep_pass_once(self):
        (self.root / ".copy").mkdir()
        self.edit("page.md", GENERIC)
        out = hook("stop", {"session_id": "s1", "cwd": str(self.root)})
        self.assertEqual(out["decision"], "block")
        self.assertIn("[vocab]", out["reason"])
        self.assertIsNone(hook("stop", {"session_id": "s1", "cwd": str(self.root)}))

    def test_stop_respects_stop_hook_active(self):
        (self.root / ".copy").mkdir()
        self.edit("page.md", GENERIC)
        self.assertIsNone(hook("stop", {"session_id": "s1", "cwd": str(self.root), "stop_hook_active": True}))

    def test_clean_file_is_silent(self):
        (self.root / ".copy").mkdir()
        self.assertIsNone(self.edit("page.md", CLEAN))
        self.assertIsNone(hook("stop", {"session_id": "s1", "cwd": str(self.root)}))

    def test_brand_avoid_words(self):
        (self.root / "BRAND.md").write_text(
            "## 6. Language\n| Use | Instead of | Why |\n|---|---|---|\n| coffee | ritual, journey | plain |\n",
            encoding="utf-8")
        out = self.edit("page.md", "Start your morning ritual.\n")
        self.assertIn("[brand-avoid]", out["hookSpecificOutput"]["additionalContext"])

    def test_bad_input_never_fails(self):
        p = subprocess.run([sys.executable, str(SCRIPTS / "hook.py"), "post"], input=b"not json", capture_output=True)
        self.assertEqual(p.returncode, 0)


class Live(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        cls.file = pathlib.Path(cls.tmp.name) / "page.md"
        cls.file.write_text(GENERIC, encoding="utf-8")
        cls.state = live.State(cls.file, "3", None, None)
        cls.server = live.ThreadingHTTPServer(("127.0.0.1", 0), live.make_handler(cls.state))
        cls.base = "http://127.0.0.1:%d" % cls.server.server_address[1]
        threading.Thread(target=cls.server.serve_forever, daemon=True).start()

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.tmp.cleanup()

    def call(self, path, body=None, token=True):
        req = urllib.request.Request(self.base + path, data=json.dumps(body).encode() if body is not None else None,
                                     headers={"X-Copy-Token": self.state.token if token else "nope",
                                              "Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status, r.read().decode("utf-8")
        except urllib.error.HTTPError as e:
            return e.code, e.read().decode("utf-8")

    def test_token_required(self):
        self.assertEqual(self.call("/api/state", token=False)[0], 403)

    def test_page_and_state(self):
        code, html = self.call("/?t=" + self.state.token)
        self.assertEqual(code, 200)
        self.assertIn("COPY", html)
        self.assertNotIn("__TOKEN__", html)
        code, body = self.call("/api/state")
        data = json.loads(body)
        self.assertEqual(data["context"], "3")
        spans = [f for f in data["findings"] if f["start"] is not None]
        self.assertTrue(spans)
        for f in spans:
            self.assertEqual(data["text"][f["start"]:f["end"]].lower(), f["match"].lower())

    def test_apply_single_occurrence(self):
        self.file.write_text(GENERIC, encoding="utf-8")
        code, _ = self.call("/api/apply", {"old": "Studies show it works.", "new": "It works for us."})
        self.assertEqual(code, 200)
        self.assertIn("It works for us.", self.file.read_text(encoding="utf-8"))
        code, _ = self.call("/api/apply", {"old": "not in file", "new": "x"})
        self.assertEqual(code, 409)

    def test_context_validation(self):
        self.assertEqual(self.call("/api/context", {"context": "99"})[0], 400)
        self.assertEqual(self.call("/api/context", {"context": "12"})[0], 200)
        self.call("/api/context", {"context": "3"})


if __name__ == "__main__":
    unittest.main()

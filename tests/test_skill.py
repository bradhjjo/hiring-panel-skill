import json
import os
import re
import unittest

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
NUMBER_WORDS = {"seven": 7, "eight": 8, "nine": 9, "ten": 10, "eleven": 11}


def read(*parts):
    with open(os.path.join(ROOT, *parts), encoding="utf-8") as f:
        return f.read()


def frontmatter(text):
    """Return (top-level keys, metadata keys) from the SKILL.md frontmatter."""
    match = re.match(r"---\n(.*?)\n---\n", text, re.S)
    if not match:
        raise AssertionError("SKILL.md has no frontmatter block")
    top, meta, in_meta = {}, {}, False
    for line in match.group(1).splitlines():
        if not line.strip():
            continue
        if line.startswith("  ") and in_meta:
            key, _, value = line.strip().partition(":")
            meta[key] = value.strip().strip('"')
            continue
        if line.startswith("  "):
            continue  # folded description continuation
        key, _, value = line.partition(":")
        top[key] = value.strip().strip('"')
        in_meta = key == "metadata"
    return top, meta


def section(text, number):
    """Return the body of the '## <number>. ...' section."""
    match = re.search(rf"^## {number}\. .*?$(.*?)(?=^## |\Z)", text, re.M | re.S)
    if not match:
        raise AssertionError(f"SKILL.md has no section {number}")
    return match.group(1)


class SkillTest(unittest.TestCase):
    def setUp(self):
        self.text = read("skills", "hiring-panel", "SKILL.md")
        self.top, self.meta = frontmatter(self.text)
        self.readers = re.findall(r"^\d\. \*\*([^*]+?)\.\*\*", section(self.text, 4), re.M)

    def test_frontmatter(self):
        self.assertEqual(self.top.get("name"), "hiring-panel")
        self.assertEqual(self.top.get("license"), "MIT")
        self.assertTrue(self.top.get("argument-hint"))
        self.assertIn("description", self.top)
        self.assertRegex(self.meta.get("version", ""), r"^\d+\.\d+\.\d+$")

    def test_five_distinct_readers(self):
        self.assertEqual(len(self.readers), 5, self.readers)
        lowered = [r.lower() for r in self.readers]
        self.assertEqual(len(set(lowered)), 5, f"duplicate reader: {self.readers}")
        # The readers must not repeat the two reviewers that run before them.
        for earlier in ("the automated screen", "the hiring manager"):
            self.assertNotIn(earlier, lowered)
        self.assertIn("Start five sub-agents at once", self.text)

    def test_seven_reviewers(self):
        self.assertIn("## 2. The automated screen", self.text)
        self.assertIn("## 3. The hiring manager", self.text)
        self.assertEqual(2 + len(self.readers), 7)

    def test_rebuild_keeps_format(self):
        rebuild = section(self.text, 6)
        for fmt in (".docx", "LaTeX", "Markdown"):
            self.assertIn(fmt, rebuild)
        self.assertIn("RESUME-IMPROVED.<ext>", section(self.text, 7))

    def test_rescreen_runs_screen_and_hiring_manager(self):
        rebuild = section(self.text, 6)
        self.assertIn("automated-screen and hiring-manager sub-agents once more", rebuild)
        self.assertIn("before and after verdict", rebuild)

    def test_output_path_is_defined(self):
        result = section(self.text, 7)
        self.assertIn(".hiring-panel/<date>-<role>/", result)
        self.assertIn("YYYY-MM-DD", result)

    def test_never_invents(self):
        self.assertIn("Never invent employers, titles, dates, numbers or skills", self.text)

    def test_credit_line(self):
        self.assertIn("Made with /hiring-panel by Alex Chen (@nocodealex) · chen.media", self.text)


class PackagingTest(unittest.TestCase):
    def setUp(self):
        self.plugin = json.loads(read(".claude-plugin", "plugin.json"))
        self.market = json.loads(read(".claude-plugin", "marketplace.json"))
        self.readme = read("README.md")
        _, self.meta = frontmatter(read("skills", "hiring-panel", "SKILL.md"))

    def test_versions_match(self):
        citation = re.search(r'^version: "([^"]+)"', read("CITATION.cff"), re.M).group(1)
        self.assertEqual(self.plugin["version"], self.meta["version"])
        self.assertEqual(self.plugin["version"], citation)

    def test_marketplace_lists_plugin(self):
        names = [p["name"] for p in self.market["plugins"]]
        self.assertIn(self.plugin["name"], names)
        install = f"/plugin install {self.plugin['name']}@{self.market['name']}"
        self.assertIn(install, self.readme)

    def test_readme_sub_agent_count(self):
        # 1 screen + 1 hiring manager + 5 readers + 2 re-screens.
        word = re.search(r"One run is (\w+) sub-agent calls", self.readme).group(1)
        self.assertEqual(NUMBER_WORDS.get(word), 9)

    def test_readme_readers_match_skill(self):
        self.assertIn("the team lead (can you do the job on day one?)", self.readme)
        self.assertNotIn("the hiring manager (can you do the job on day one?)", self.readme)


if __name__ == "__main__":
    unittest.main()

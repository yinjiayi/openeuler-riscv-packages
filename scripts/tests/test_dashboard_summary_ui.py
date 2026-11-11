# SPDX-License-Identifier: Apache-2.0
"""Execute the actual summary renderer in Node with an inert DOM fixture."""
import json
import pathlib
import shutil
import subprocess
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[2]
NODE = shutil.which("node")
HARNESS = r'''
const fs = require('node:fs');
const vm = require('node:vm');
const input = JSON.parse(fs.readFileSync(0, 'utf8'));
class Element {
  constructor(tag) { this.tag = tag; this.children = []; this.textContent = ''; }
  replaceChildren(...items) { this.children = items; }
  append(...items) { this.children.push(...items); }
}
const elements = new Map();
const document = {
  createElement: tag => new Element(tag),
  querySelector: key => { if (!elements.has(key)) elements.set(key, new Element('div')); return elements.get(key); },
};
const context = vm.createContext({document, Intl, Date, URL, Map, window: {location: {href: 'https://example.org/'}}, fetch: () => new Promise(() => {})});
vm.runInContext(fs.readFileSync(input.app, 'utf8'), context);
vm.runInContext('dashboard = ' + JSON.stringify({packages: [], build_history: input.history}) + '; inventory = {entries: [], status_counts: {}}; renderSummary();', context);
const cards = elements.get('#summary').children.map(card => ({label: card.children[1].textContent, value: card.children[0].textContent}));
process.stdout.write(JSON.stringify({cards, coverage: elements.get('#history-coverage').textContent, gaps: elements.get('#coverage-gap-summary').textContent}));
'''


@unittest.skipUnless(NODE, "Node required for actual JavaScript summary renderer")
class DashboardSummaryUITests(unittest.TestCase):
    def render(self, **changes):
        history = {"source_generated_at": "2026-10-09T00:00:00Z", "coverage_complete": True, "lower_bound": False,
                   "current_pr_source_generated_at": "2026-10-09T00:00:00Z", "current_pr_source_available": True,
                   "current_pr_source_complete": True, "current_pr_selection_gaps": [],
                   "metrics": {"cumulative_success_packages": 9, "current_main_success_packages": 3, "current_pr_success_packages": 2, "published_packages": 1}}
        history.update(changes)
        result = subprocess.run([NODE, "-e", HARNESS], input=json.dumps({"app": str(ROOT / "dashboard/app.js"), "history": history}), capture_output=True, text=True, check=True, timeout=15)
        output = json.loads(result.stdout)
        return {row["label"]: row["value"] for row in output["cards"]}, output

    def test_complete_current_selection_has_exact_value(self):
        cards, output = self.render()
        self.assertEqual(cards["Current open PR success"], "2")
        self.assertIn("current-check selection complete", output["coverage"])

    def test_selection_gap_has_independent_lower_bound_and_visible_reason(self):
        cards, output = self.render(current_pr_source_complete=False, current_pr_selection_gaps=[{"pr": 1, "head_sha": "a" * 40, "reason": "unverified current checks"}])
        self.assertEqual(cards["Current open PR success"], "≥ 2 (partial)")
        self.assertEqual(cards["Cumulative build + smoke success"], "9")
        self.assertIn("partial current-check selection; count is a lower bound", output["coverage"])
        self.assertIn("Current PR selection gap records 1", output["gaps"])
        self.assertIn("unverified current checks: 1", output["gaps"])

    def test_missing_legacy_selection_completeness_is_not_exact(self):
        cards, output = self.render(current_pr_source_complete=None)
        self.assertEqual(cards["Current open PR success"], "≥ 2 (partial)")
        self.assertIn("partial current-check selection", output["coverage"])

    def test_unavailable_current_snapshot_remains_unknown(self):
        cards, output = self.render(current_pr_source_available=False, current_pr_source_complete=False)
        self.assertEqual(cards["Current open PR success"], "unknown")
        self.assertIn("unavailable / incomplete; count unknown", output["coverage"])

    def test_partial_history_does_not_claim_complete_count(self):
        cards, _ = self.render(lower_bound=True, coverage_complete=False)
        self.assertEqual(cards["Current open PR success"], "≥ 2")
        self.assertEqual(cards["Cumulative build + smoke success"], "≥ 9")

    def test_missing_history_source_withholds_current_count(self):
        cards, _ = self.render(source_generated_at=None)
        self.assertEqual(cards["Current open PR success"], "unknown")


if __name__ == "__main__":
    unittest.main()

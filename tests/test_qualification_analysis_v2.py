import copy
import json
import hashlib
from pathlib import Path
import sys
import unittest
from jsonschema import Draft202012Validator

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import qualification_analysis_v2 as a  # noqa: E402


class AnalysisV2Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.inputs = a.read_inputs()
        cls.value = a.generate(**cls.inputs)

    def test_deterministic_and_complete(self):
        self.assertEqual(self.value, a.generate(**self.inputs))
        self.assertEqual(self.value["counts"]["assertions"], 5808)
        self.assertEqual(self.value["counts"]["reported_events"], 74)
        self.assertEqual(
            self.value,
            json.loads((ROOT / "reports/analysis-v2/analysis.json").read_text()),
        )

    def test_mixed_candidate_rejected(self):
        value = copy.deepcopy(self.value)
        value["assertions"][0]["candidate_manifest_sha256"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            a.validate(value)

    def test_duplicate_rejected(self):
        value = copy.deepcopy(self.value)
        value["assertions"].append(value["assertions"][0])
        with self.assertRaises(ValueError):
            a.validate(value)

    def test_wrong_applicability_rejected(self):
        inputs = copy.deepcopy(self.inputs)
        inputs["catalog"]["scenarios"][0]["applicable_components"] = []
        with self.assertRaises(ValueError):
            a.generate(**inputs)

    def test_diagnostic_credit_rejected(self):
        value = copy.deepcopy(self.value)
        value["chronology"][0]["qualification_credit"] = 1
        with self.assertRaises(Exception):
            a.validate(value)

    def test_inferred_causality_rejected(self):
        value = copy.deepcopy(self.value)
        value["chronology"][0]["causal_status"] = "ESTABLISHED"
        with self.assertRaises(Exception):
            a.validate(value)

    def test_private_dimension_rejected(self):
        value = copy.deepcopy(self.value)
        value["assertions"][0]["runtime"] = "/Users/private"
        with self.assertRaises(Exception):
            a.validate(value)

    def test_wrong_group_denominator_detected(self):
        value = copy.deepcopy(self.value)
        value["comparisons"][0]["denominator"] = 1
        with self.assertRaises(ValueError):
            a.check_exact(value)

    def test_register_rebind_rejected(self):
        inputs = copy.deepcopy(self.inputs)
        inputs["registers"][0]["sha256"] = "sha256:" + "0" * 64
        with self.assertRaises(ValueError):
            a.generate(**inputs)

    def test_chronology_unknowns(self):
        self.assertTrue(
            all(
                x["execution_at"] is None and x["causal_status"] == "UNKNOWN"
                for x in self.value["chronology"]
            )
        )
        self.assertFalse(self.value["historical_inventory_complete"])
        self.assertTrue(
            all(
                x["raw_output_equivalence"] == "NOT_ESTABLISHED"
                for x in self.value["comparisons"]
            )
        )

    def test_manifest_member_hashes(self):
        root = ROOT / "reports/analysis-v2"
        manifest = json.loads((root / "manifest.json").read_text())
        actual = {str(p.relative_to(root)) for p in root.rglob("*") if p.is_file()} - {
            "manifest.json"
        }
        self.assertEqual(actual, set(manifest["members"]))
        for name, value in manifest["members"].items():
            data = (root / name).read_bytes()
            self.assertEqual(value["bytes"], len(data))
            self.assertEqual(
                value["sha256"], "sha256:" + hashlib.sha256(data).hexdigest()
            )

    def test_dmsc_no_claim_promotion(self):
        schema = json.loads(
            (ROOT / "schemas/analysis-v2-dmsc-association.json").read_text()
        )
        data = json.loads(
            (ROOT / "reports/analysis-v2/dmsc-association.json").read_text()
        )
        Draft202012Validator(schema).validate(data)
        self.assertEqual(len(data["sources"]), 51)
        self.assertEqual(len(data["mapping"]), 27)
        data["mapping"][0]["status"] = "INTEROPERABLE"
        with self.assertRaises(Exception):
            Draft202012Validator(schema).validate(data)


if __name__ == "__main__":
    unittest.main()

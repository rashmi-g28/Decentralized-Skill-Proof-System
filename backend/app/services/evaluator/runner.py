import json
import os
import subprocess
import sys
import tempfile
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Tuple


@dataclass
class TestCase:
	name: str
	input: Any
	expected: Any


@dataclass
class EvaluationResult:
	skill: str
	total: int
	passed: int
	score: int
	passed_overall: bool
	details: List[Dict[str, Any]]


class CodeEvaluator:
	"""
	Simple evaluator that executes user-submitted Python function files in a separate process.
	Assumes the user's file defines a function named `solve(input_value)` that returns the expected output.
	Testcases are provided as JSON files with fields: name, input, expected.
	"""

	def __init__(self, testcases_dir: str) -> None:
		self.testcases_dir = Path(testcases_dir)

	def _load_testcases(self, skill: str) -> List[TestCase]:
		path = self.testcases_dir / f"{skill}.json"
		if not path.exists():
			raise FileNotFoundError(f"No testcases found for skill '{skill}' at {path}")
		data = json.loads(path.read_text())
		cases: List[TestCase] = []
		for item in data.get("cases", []):
			cases.append(TestCase(name=item["name"], input=item["input"], expected=item["expected"]))
		return cases

	def _run_case(self, user_code_path: str, case: TestCase, timeout_seconds: int = 2) -> Tuple[bool, Any, str]:
		"""
		Run a single test case by executing a tiny harness that imports the user's code file as a module,
		calls solve(input) and prints the result as JSON to stdout.
		"""
		user_code_abs = str(Path(user_code_path).resolve())
		with tempfile.TemporaryDirectory() as tmpdir:
			# Create a harness script
			harness_path = Path(tmpdir) / "harness.py"
			harness_code = f"""
import importlib.util
import json
import os
import sys
from types import ModuleType

module_path = r"{user_code_abs}"
spec = importlib.util.spec_from_file_location("user_module", module_path)
mod = importlib.util.module_from_spec(spec)
spec.loader.exec_module(mod)  # type: ignore

if not hasattr(mod, "solve"):
	print(json.dumps({{"error": "solve function not found"}}))
	sys.exit(0)

inp = json.loads({json.dumps(json.dumps(case.input))})
try:
	res = mod.solve(inp)
	print(json.dumps({{"result": res}}))
except Exception as e:
	print(json.dumps({{"error": str(e)}}))
	"""
			
			harness_path.write_text(harness_code)
			# Run harness in isolated Python subprocess
			proc = subprocess.run(
				[sys.executable, str(harness_path)],
				stdout=subprocess.PIPE,
				stderr=subprocess.PIPE,
				timeout=timeout_seconds,
				check=False,
			)
			stdout = proc.stdout.decode("utf-8", errors="ignore").strip()
			stderr = proc.stderr.decode("utf-8", errors="ignore").strip()
			try:
				payload = json.loads(stdout) if stdout else {}
			except Exception:
				payload = {"error": f"Invalid JSON output: {stdout}"}
			if "error" in payload:
				return False, None, payload["error"]
			return True, payload.get("result"), stderr

	def evaluate(self, skill: str, user_code_path: str) -> EvaluationResult:
		cases = self._load_testcases(skill)
		passed_count = 0
		details: List[Dict[str, Any]] = []
		for case in cases:
			ok, value, err = self._run_case(user_code_path, case)
			is_pass = ok and (value == case.expected)
			passed_count += 1 if is_pass else 0
			details.append({
				"case": case.name,
				"input": case.input,
				"expected": case.expected,
				"got": value,
				"error": None if ok else err,
				"pass": is_pass,
			})

		total = len(cases)
		score = int((passed_count / total) * 100) if total else 0
		return EvaluationResult(
			skill=skill,
			total=total,
			passed=passed_count,
			score=score,
			passed_overall=passed_count == total and total > 0,
			details=details,
		)
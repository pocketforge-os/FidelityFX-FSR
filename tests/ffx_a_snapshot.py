#!/usr/bin/env python3

import hashlib
import tempfile
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
HEADER = ROOT / "ffx-fsr" / "ffx_a.h"
EXPECTED_SHA256 = "b95d8bd7c98ae44e78c1178d707171048e0d7e361efef3d72c385866144e1ecc"
RETURN_TYPES = ("AD", "AF", "AL", "AU")


def validate_header(path):
	contents = path.read_bytes()
	if hashlib.sha256(contents).hexdigest() != EXPECTED_SHA256:
		raise ValueError("ffx_a.h does not match the admitted source snapshot")
	text = contents.decode("utf-8")
	if "#define A_STATIC static inline" not in text:
		raise ValueError("CPU helper functions are not static inline")
	for scalar in RETURN_TYPES:
		for width in (2, 3, 4):
			macro = f"#define ret{scalar}{width} {scalar}1 *"
			if macro not in text:
				raise ValueError(f"missing unrestricted return macro {macro}")
			if f"{macro}A_RESTRICT" in text:
				raise ValueError(f"return macro ret{scalar}{width} is restrict-qualified")
	if "#define inAF4 AF1 *A_RESTRICT" not in text:
		raise ValueError("input pointer restrict qualification was lost")


class FfxASnapshotTests(unittest.TestCase):
	def test_repository_header_matches_admitted_snapshot(self):
		validate_header(HEADER)

	def test_modified_snapshot_is_rejected(self):
		with tempfile.TemporaryDirectory() as temp_dir:
			modified = Path(temp_dir) / "ffx_a.h"
			modified.write_bytes(HEADER.read_bytes() + b"\n")
			with self.assertRaises(ValueError):
				validate_header(modified)


if __name__ == "__main__":
	unittest.main(verbosity=2)

"""CLI: risolve una istanza con il PLI (amplpy + HiGHS). Stampa su stdout
un JSON {"status": ..., "cmax": ...} sull'ultima riga. Pensato per essere
lanciato come subprocess isolato da run_with_limits.run_solver.
"""
import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent.parent))

from solvers.pli_solver import LicenseLimitExceeded, solve_pli  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("instance_path")
    args = parser.parse_args()

    inst = json.loads(Path(args.instance_path).read_text())
    try:
        cmax = solve_pli(inst["n"], inst["m"], inst["p"])
        print(json.dumps({"status": "OK", "cmax": cmax}))
    except LicenseLimitExceeded as e:
        print(json.dumps({"status": "LICENSE_LIMIT", "cmax": None, "error": str(e)}))
    except Exception as e:  # noqa: BLE001 - propagare qualunque errore al padre
        print(json.dumps({"status": "ERROR", "cmax": None, "error": str(e)}))
        sys.exit(1)


if __name__ == "__main__":
    main()

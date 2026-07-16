"""Risoluzione di P_m||C_max come PLI via amplpy + modello model_pmcmax.mod.

Solver: HiGHS (open-source, incluso nella AMPL Community Edition gratuita).

Nota storica: con una licenza AMPL CE non attivata, i problemi lineari sono
limitati a 2000 variabili/vincoli dopo il presolve. Questo modulo conteneva
un controllo esplicito (n*m > 2000 -> LicenseLimitExceeded) per distinguere
questo limite artificiale da un vero fallimento del solver. Rimosso dopo
l'attivazione di una licenza CE gratuita (ampl.com/ce), che elimina il
limite. runner_pli.py mantiene comunque il except LicenseLimitExceeded per
compatibilita' con eventuali esecuzioni future senza licenza attivata.
"""
from pathlib import Path

from amplpy import AMPL

MODEL_PATH = Path(__file__).parent / "model_pmcmax.mod"


class LicenseLimitExceeded(Exception):
    """Il solve ha fallito per il tetto di variabili/vincoli di una licenza
    AMPL CE non attivata (rilevato dal messaggio d'errore di AMPL stesso)."""


def solve_pli(n: int, m: int, p: list[int]) -> int:
    """Risolve P_m||C_max via PLI. Ritorna C*_max ottimo (int)."""
    ampl = AMPL()
    try:
        ampl.read(str(MODEL_PATH))
        ampl.set["J"] = list(range(1, n + 1))
        ampl.set["M"] = list(range(1, m + 1))
        ampl.param["p"] = {j + 1: p[j] for j in range(n)}

        ampl.option["solver"] = "highs"
        try:
            ampl.solve()
        except Exception as e:
            if "demo license" in str(e).lower():
                raise LicenseLimitExceeded(str(e)) from e
            raise

        solve_result = ampl.get_value("solve_result")
        if solve_result != "solved":
            raise RuntimeError(f"Solve non ottimale: solve_result={solve_result}")

        cmax = ampl.get_value("Cmax")
        return round(cmax)
    finally:
        ampl.close()


if __name__ == "__main__":
    assert solve_pli(3, 2, [3, 3, 3]) == 6
    assert solve_pli(3, 1, [3, 3, 3]) == 9
    print("pli_solver: sanity checks OK")

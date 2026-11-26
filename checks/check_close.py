"""Offline check of the original synthetic May close, not a general ledger."""
from collections import Counter, deque
from datetime import date
from fractions import Fraction
import json
from pathlib import Path
import unittest

DATA = Path(__file__).resolve().parents[1] / "data" / "may-close.json"


def fifo(receipts, issued):
    lots = deque([r["units"], r["unit_cost"]] for r in receipts)
    if not 0 <= issued <= sum(n for n, _ in lots):
        raise ValueError("issued quantity outside available stock")
    used = 0
    while issued:
        n, cost = lots.popleft()
        take = min(n, issued)
        used += take * cost
        issued -= take
        if n > take:
            lots.appendleft([n - take, cost])
    return used, sum(n * cost for n, cost in lots), sum(n for n, _ in lots)


def close(d, premature=False):
    b = Counter()
    journal = []

    def post(debit, credit, amount):
        if amount < 0:
            raise ValueError("use a reversing entry for negative amounts")
        b[debit] += amount
        b[credit] -= amount
        journal.append((debit, credit, amount))

    opening = d["opening"]
    post("cash", "equity", opening["cash"])
    post("equipment", "equity", opening["equipment"])
    post("equity", "accumulated_depreciation", opening["accumulated_depreciation"])
    if b["equity"] != -opening["equity"]:
        raise ValueError("opening assets net of depreciation do not explain equity")
    end = date.fromisoformat(d["period_end"])
    cov = d["coverage"]
    post("prepaid", "cash", cov["cash_paid"])
    post("coverage_expense", "prepaid", Fraction(cov["cash_paid"] * cov["months_used"], cov["months"]))
    cash_parts = 0
    for r in d["part_receipts"]:
        total = r["units"] * r["unit_cost"]
        post("inventory", "accounts_payable" if r["on_account"] else "cash", total)
        if not r["on_account"]:
            cash_parts += total
    used, stock_cost, units = fifo(d["part_receipts"], d["part_units_issued"])
    if units != d["part_units_counted"]:
        raise ValueError("inventory count difference needs investigation")
    post("parts_expense", "inventory", used)
    post("cash", "loan", d["loan_received"])
    post("cash", "revenue", d["completed_cash_service"])
    post("receivable", "revenue", d["completed_billed_service"])
    post("cash", "receivable", d["cash_collected_on_invoice"])
    done, flagged, collections = [], [], 0
    seen = set()
    for a in d["advances"]:
        if a["job"] in seen:
            raise ValueError("duplicate advance ID")
        seen.add(a["job"])
        if date.fromisoformat(a["received"]) > end:
            continue
        post("cash", "advances", a["amount"])
        collections += a["amount"]
        if a["accepted"] and date.fromisoformat(a["accepted"]) <= end:
            done.append(a["job"])
            post("advances", "revenue", a["amount"])
        else:
            flagged.append(a["job"])
            if premature:
                post("advances", "revenue", a["amount"])
    post("wage_expense", "cash", d["wages_paid"])
    post("wage_expense", "wages_payable", d["wages_owed"])
    old = d["existing_equipment"]
    dep = Fraction(old["cost"] - old["residual"], old["life_months"])
    post("depreciation_expense", "accumulated_depreciation", dep)
    new = d["new_equipment"]
    if date.fromisoformat(new["in_service"]) <= end:
        raise ValueError("new equipment needs its own May depreciation schedule")
    post("equipment", "cash", new["cost"])
    if sum(b.values()) or b["inventory"] != stock_cost:
        raise ValueError("postings or inventory valuation do not reconcile")

    income = -b["revenue"] - sum(v for k, v in b.items() if k.endswith("_expense"))
    assets = sum(b[k] for k in ("cash", "receivable", "inventory", "prepaid", "equipment",
                                "accumulated_depreciation"))
    liabilities = -sum(b[k] for k in ("accounts_payable", "advances", "wages_payable", "loan"))
    equity = -b["equity"] + income
    direct = (d["completed_cash_service"] + d["cash_collected_on_invoice"] + collections
              - cov["cash_paid"] - cash_parts - d["wages_paid"])
    indirect = (income + dep - b["receivable"] - b["inventory"] - b["prepaid"]
                - b["accounts_payable"] - b["advances"] - b["wages_payable"])
    return dict(journal=journal, balances=b, income=income, assets=assets, liabilities=liabilities,
                equity=equity, direct=direct, indirect=indirect, cash=b["cash"],
                cash_change=direct-new["cost"]+d["loan_received"], done=done, flagged=flagged,
                trial=sum(v for v in b.values() if v > 0))


class CloseTests(unittest.TestCase):
    def setUp(self):
        self.data = json.loads(DATA.read_text())
        self.good = close(self.data)
        self.bad = close(self.data, premature=True)

    def test_inventory_methods(self):
        receipts = self.data["part_receipts"]
        self.assertEqual(fifo(receipts, 7), (145, 75, 3))
        self.assertEqual(fifo(receipts, 5), (100, 120, 5))
        average = Fraction(220, 10)
        self.assertEqual((average * 7, average * 3), (154, 66))
        with self.assertRaises(ValueError):
            fifo(receipts, 11)

    def test_count_mismatch_is_not_plugged(self):
        self.data["part_units_counted"] = 2
        with self.assertRaisesRegex(ValueError, "count"):
            close(self.data)

    def test_trial_balances_hold_even_when_wrong(self):
        for outcome in (self.good, self.bad):
            self.assertEqual(sum(outcome["balances"].values()), 0)
            self.assertEqual(outcome["trial"], 2670)
            self.assertEqual(outcome["assets"], outcome["liabilities"]+outcome["equity"])

    def test_correct_income_and_position(self):
        self.assertEqual(tuple(self.good[k] for k in ("income","assets","liabilities","equity")),
                         (185, 2185, 520, 1665))
        self.assertEqual(self.good["balances"]["receivable"], 70)
        self.assertEqual(self.good["balances"]["prepaid"], 60)
        self.assertEqual(self.good["balances"]["equipment"], 840)
        self.assertEqual(self.good["balances"]["accumulated_depreciation"], -150)

    def test_cash_cannot_detect_cutoff_error(self):
        for outcome in (self.good, self.bad):
            self.assertEqual((outcome["direct"], outcome["indirect"]), (230, 230))
            self.assertEqual(outcome["cash_change"], 290)
            self.assertEqual(outcome["cash"], 1000 + outcome["cash_change"])

    def test_cutoff_and_exact_correction(self):
        self.assertEqual(self.good["done"], ["A", "B"])
        self.assertEqual(self.good["flagged"], ["C"])
        self.assertEqual(tuple(self.bad[k] for k in ("income","assets","liabilities","equity")),
                         (285, 2185, 420, 1765))
        fixed = self.bad["balances"].copy()
        fixed["revenue"] += 100
        fixed["advances"] -= 100
        self.assertEqual(fixed, self.good["balances"])

    def test_missing_acceptance_does_not_release_advance(self):
        self.data["advances"][2]["accepted"] = None
        self.assertEqual(close(self.data)["flagged"], ["C"])
        self.assertEqual(close(self.data)["income"], 185)

    def test_collection_deferral(self):
        self.data["cash_collected_on_invoice"] = 0
        result = close(self.data)
        self.assertEqual((result["income"], result["cash"], result["balances"]["receivable"],
                          result["direct"], result["indirect"], result["assets"]),
                         (185, 1220, 140, 160, 160, 2185))

    def test_duplicate_advance_rejected(self):
        self.data["advances"].append(self.data["advances"][0].copy())
        with self.assertRaisesRegex(ValueError, "duplicate"):
            close(self.data)

    def test_small_ledger(self):
        for payment, cash, payable, total in ((40,435,60,535),(55,420,45,520)):
            self.assertEqual((400+75-payment,100-payment), (cash,payable))
            self.assertEqual(cash+100,total)
            self.assertEqual(payable+400+75,total)


if __name__ == "__main__":
    unittest.main(verbosity=2)

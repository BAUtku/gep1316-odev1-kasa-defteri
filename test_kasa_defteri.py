import os
import tempfile
import unittest

from kasa_defteri import (
    add_transaction,
    calculate_balance,
    save_transactions_csv,
    validate_amount,
    validate_date,
)


class KasaDefteriTests(unittest.TestCase):
    def test_validate_amount_accepts_decimal(self):
        self.assertEqual(validate_amount("1250,50"), 1250.5)

    def test_validate_amount_rejects_negative(self):
        with self.assertRaises(ValueError):
            validate_amount("-25")

    def test_validate_date_accepts_common_formats(self):
        self.assertEqual(validate_date("2026-11-15"), "2026-11-15")
        self.assertEqual(validate_date("15.11.2026"), "2026-11-15")

    def test_add_transaction_creates_income_record(self):
        transactions = []
        item = add_transaction(transactions, "gelir", "satış", "Müşteri ödemesi", "2500", "2026-11-04")
        self.assertEqual(item["type"], "gelir")
        self.assertEqual(item["amount"], 2500.0)
        self.assertEqual(len(transactions), 1)

    def test_add_transaction_rejects_invalid_type(self):
        transactions = []
        with self.assertRaises(ValueError):
            add_transaction(transactions, "maaş", "satış", "Hatalı işlem", "1000", "2026-11-04")

    def test_calculate_balance_sums_income_and_expense(self):
        transactions = [
            {"type": "gelir", "amount": 5000},
            {"type": "gelir", "amount": 1500},
            {"type": "gider", "amount": 2200},
            {"type": "gider", "amount": 600},
        ]
        summary = calculate_balance(transactions)
        self.assertEqual(summary["toplam_gelir"], 6500.0)
        self.assertEqual(summary["toplam_gider"], 2800.0)
        self.assertEqual(summary["bakiye"], 3700.0)

    def test_save_transactions_csv_creates_file(self):
        transactions = [
            {"id": 1, "type": "gelir", "category": "satış", "description": "Kasa", "amount": 300, "date": "2026-11-09"},
            {"id": 2, "type": "gider", "category": "kira", "description": "Dükkan kira", "amount": 150, "date": "2026-11-10"},
        ]

        with tempfile.TemporaryDirectory() as tmp_dir:
            path = os.path.join(tmp_dir, "test_transactions.csv")
            saved_path = save_transactions_csv(transactions, path)
            self.assertTrue(os.path.exists(saved_path))
            with open(saved_path, "r", encoding="utf-8") as file:
                content = file.read()
            self.assertIn("type,category,description,amount,date", content)
            self.assertIn("gelir", content)


if __name__ == "__main__":
    unittest.main()

from __future__ import annotations

import csv
from datetime import datetime
from pathlib import Path

DATA_FILE = Path(__file__).with_name("transactions.csv")
TRANSACTION_TYPES = ("gelir", "gider")
CATEGORY_MAP = {
    "gelir": ["satış", "hizmet", "diğer"],
    "gider": ["malzeme", "personel", "kira", "elektrik", "internet", "diğer"],
}


def validate_amount(amount_text: str) -> float:
    """Miktarı doğrular ve float değere çevirir."""
    try:
        amount = float(amount_text.replace(",", "."))
    except ValueError as exc:
        raise ValueError("Tutar sayısal olmalıdır. Örnek: 1250.50") from exc

    if amount <= 0:
        raise ValueError("Tutar 0'dan büyük olmalıdır.")
    return round(amount, 2)


def validate_date(date_text: str) -> str:
    """Tarih formatını kontrol eder ve standart formata çevirir."""
    if not date_text.strip():
        raise ValueError("Tarih boş olamaz.")

    for fmt in ("%Y-%m-%d", "%d.%m.%Y", "%d/%m/%Y"):
        try:
            parsed = datetime.strptime(date_text.strip(), fmt)
            return parsed.strftime("%Y-%m-%d")
        except ValueError:
            continue

    raise ValueError("Tarih formatı geçersiz. Örnek: 2026-11-15 veya 15.11.2026")


def validate_category(category: str, transaction_type: str) -> str:
    """Kategori seçimini kontrol eder."""
    cleaned = category.strip().lower()
    if not cleaned:
        raise ValueError("Kategori boş olamaz.")

    valid = CATEGORY_MAP.get(transaction_type)
    if valid and cleaned not in valid:
        allowed = ", ".join(valid)
        raise ValueError(f"Geçersiz kategori. Seçenekler: {allowed}")

    return cleaned


def add_transaction(transactions: list[dict], transaction_type: str, category: str, description: str, amount: str | float, date: str) -> dict:
    """Yeni işlem ekler ve doğrulama yapar."""
    normalized_type = transaction_type.strip().lower()
    if normalized_type not in TRANSACTION_TYPES:
        raise ValueError("İşlem tipi 'gelir' veya 'gider' olmalıdır.")

    clean_category = validate_category(category, normalized_type)
    clean_description = description.strip()
    if not clean_description:
        raise ValueError("Açıklama boş olamaz.")

    clean_amount = validate_amount(str(amount)) if isinstance(amount, str) else validate_amount(str(float(amount)))
    clean_date = validate_date(date)

    new_transaction = {
        "id": len(transactions) + 1,
        "type": normalized_type,
        "category": clean_category,
        "description": clean_description,
        "amount": round(clean_amount, 2),
        "date": clean_date,
    }
    transactions.append(new_transaction)
    return new_transaction


def calculate_balance(transactions: list[dict]) -> dict:
    """Toplam gelir, gider ve bakiyeyi hesaplar."""
    toplam_gelir = sum(item["amount"] for item in transactions if item["type"] == "gelir")
    toplam_gider = sum(item["amount"] for item in transactions if item["type"] == "gider")
    bakiye = toplam_gelir - toplam_gider
    return {
        "toplam_gelir": round(toplam_gelir, 2),
        "toplam_gider": round(toplam_gider, 2),
        "bakiye": round(bakiye, 2),
    }


def format_money(value: float) -> str:
    return f"{value:,.2f} TL"


def print_transactions(transactions: list[dict]) -> None:
    if not transactions:
        print("\nKayıtlı işlem yok.")
        return

    print("\n--- KASA KAYITLARI ---")
    print(f"{'ID':<4} {'Tarih':<12} {'Tip':<8} {'Kategori':<12} {'Tutar':>12} {'Açıklama'}")
    print("-" * 80)
    for item in transactions:
        print(
            f"{item['id']:<4} "
            f"{item['date']:<12} "
            f"{item['type']:<8} "
            f"{item['category']:<12} "
            f"{format_money(item['amount']):>14} "
            f"{item['description']}"
        )


def print_balance_summary(transactions: list[dict]) -> None:
    summary = calculate_balance(transactions)
    print("\n--- BAKİYE ÖZETİ ---")
    print(f"Toplam gelir: {format_money(summary['toplam_gelir'])}")
    print(f"Toplam gider: {format_money(summary['toplam_gider'])}")
    print(f"Mevcut bakiye: {format_money(summary['bakiye'])}")


def save_transactions_csv(transactions: list[dict], file_path: str | Path = DATA_FILE) -> str:
    output_path = Path(file_path)
    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["id", "type", "category", "description", "amount", "date"])
        writer.writeheader()
        writer.writerows(transactions)
    return str(output_path)


def load_transactions_csv(file_path: str | Path = DATA_FILE) -> list[dict]:
    input_path = Path(file_path)
    if not input_path.exists():
        return []

    rows: list[dict] = []
    with input_path.open("r", newline="", encoding="utf-8") as csv_file:
        reader = csv.DictReader(csv_file)
        for row in reader:
            rows.append(
                {
                    "id": int(row["id"]),
                    "type": row["type"],
                    "category": row["category"],
                    "description": row["description"],
                    "amount": float(row["amount"]),
                    "date": row["date"],
                }
            )
    return rows


def show_menu() -> None:
    print("\n=== KÜÇÜK İŞLETME KASA DEFTERİ ===")
    print("1. Gelir ekle")
    print("2. Gider ekle")
    print("3. Kayıtları göster")
    print("4. Bakiye özeti")
    print("5. CSV'ye kaydet")
    print("6. Çıkış")


def collect_transaction(transactions: list[dict], transaction_type: str) -> dict:
    valid_categories = ", ".join(CATEGORY_MAP[transaction_type])

    print(f"\n{transaction_type.upper()} KAYDI")
    print(f"Kategori seçenekleri: {valid_categories}")
    category = input("Kategori: ").strip()
    description = input("Açıklama: ").strip()
    amount = input("Tutar (TL): ").strip()
    date = input("Tarih (YYYY-MM-DD veya 15.11.2026): ").strip()

    return add_transaction(transactions, transaction_type, category, description, amount, date)


def main() -> None:
    transactions = load_transactions_csv(DATA_FILE)

    while True:
        show_menu()
        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            try:
                entry = collect_transaction(transactions, "gelir")
                print(f"Gelir kaydı eklendi: {entry['description']} - {format_money(entry['amount'])}")
            except ValueError as exc:
                print(f"Hata: {exc}")

        elif choice == "2":
            try:
                entry = collect_transaction(transactions, "gider")
                print(f"Gider kaydı eklendi: {entry['description']} - {format_money(entry['amount'])}")
            except ValueError as exc:
                print(f"Hata: {exc}")

        elif choice == "3":
            print_transactions(transactions)

        elif choice == "4":
            print_balance_summary(transactions)

        elif choice == "5":
            try:
                saved_path = save_transactions_csv(transactions, DATA_FILE)
                print(f"Kayıtlar CSV dosyasına kaydedildi: {saved_path}")
            except OSError as exc:
                print(f"Dosya kaydedilemedi: {exc}")

        elif choice == "6":
            print("Program kapatıldı. İyi günler!")
            break

        else:
            print("Geçersiz seçenek. Lütfen 1-6 arasında seçim yapın.")


if __name__ == "__main__":
    main()

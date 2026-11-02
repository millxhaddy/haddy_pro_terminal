"""Source-backed balance-sheet calculations without account-specific defaults."""

import pandas as pd

from pipeline_cleaner import clean_currency


def get_holistic_balance_sheet(
    stock_portfolio_val=None,
    cash_reserve=None,
    vault_data=None,
):
    """Return only supplied or Sheets-backed amounts; omit incomplete net-worth claims."""
    assets = []
    if stock_portfolio_val is not None:
        assets.append(
            {
                "Kategori": "Pegangan saham",
                "Institusi": "Nilai daripada aplikasi",
                "Nilai_MYR": float(stock_portfolio_val),
                "Likuiditi": "Tidak dinilai",
            }
        )
    if cash_reserve is not None:
        assets.append(
            {
                "Kategori": "Tunai",
                "Institusi": "Nilai dibekalkan",
                "Nilai_MYR": float(cash_reserve),
                "Likuiditi": "Tidak dinilai",
            }
        )
    df_assets = pd.DataFrame(
        assets, columns=["Kategori", "Institusi", "Nilai_MYR", "Likuiditi"]
    )

    source = (vault_data or {}).get("ccris_facilities")
    if not isinstance(source, pd.DataFrame) or source.empty:
        source = (vault_data or {}).get("10_Lejar Liabiliti")
    if isinstance(source, pd.DataFrame) and not source.empty:
        df_liabilities = source.copy()
    else:
        df_liabilities = pd.DataFrame()

    balance_col = next(
        (
            column
            for column in df_liabilities.columns
            if any(
                term in str(column).lower()
                for term in ("baki semasa", "outstanding balance", "current balance")
            )
        ),
        None,
    )
    monthly_col = next(
        (
            column
            for column in df_liabilities.columns
            if any(term in str(column).lower() for term in ("ansuran", "monthly payment"))
        ),
        None,
    )
    def sum_valid_amounts(column):
        if column is None:
            return None
        raw_values = df_liabilities[column]
        valid = (
            raw_values.notna()
            & raw_values.astype(str).str.strip().str.contains(r"\d", regex=True)
            & ~raw_values.astype(str).str.strip().str.startswith("#")
        )
        amounts = raw_values.map(clean_currency).where(valid)
        total = amounts.sum(min_count=1)
        return float(total) if pd.notna(total) else None

    if balance_col:
        df_liabilities["Baki_Semasa_MYR"] = df_liabilities[balance_col].map(clean_currency)
    if monthly_col:
        df_liabilities["Ansuran_Bulanan_MYR"] = df_liabilities[monthly_col].map(clean_currency)
    total_liabilities = sum_valid_amounts(balance_col)
    monthly_commitment = sum_valid_amounts(monthly_col)

    total_assets = float(df_assets["Nilai_MYR"].sum()) if not df_assets.empty else None
    return {
        "df_assets": df_assets,
        "df_liabilities": df_liabilities,
        "total_assets": total_assets,
        "total_liabilities": total_liabilities,
        "total_monthly_commitment": monthly_commitment,
        "net_worth": None,
        "solvency_ratio": None,
        "dmp_monthly_savings": None,
    }

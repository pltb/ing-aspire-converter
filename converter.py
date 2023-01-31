#!/usr/bin/env python3

import pandas as pd
from numpy import nan


def convert_transactions(data, account_name) -> pd.DataFrame:
    result = pd.DataFrame()
    data["Betrag"].astype(int)
    for _, row in data.iterrows():
        new_line = {
            "DATE": row["Buchung"],
            "OUTFLOW": -row["Betrag"] if row["Betrag"] < 0 else nan,
            "INFLOW": row["Betrag"] if row["Betrag"] > 0 else nan,
            "CATEGORY": "",
            "ACCOUNT": account_name,
            "MEMO": f"{row['Auftraggeber/Empfänger']} – {row['Verwendungszweck']}",
            "STATUS": "✅",
        }
        result = result.append(new_line, ignore_index=True)
    return result


if __name__ == "__main__":
    checking = convert_transactions(
        pd.read_csv(
            "girokonto.csv",
            dayfirst=True,
            delimiter=";",
            encoding="iso-8859-1",
            thousands=".",
            decimal=",",
            parse_dates=["Buchung", "Valuta"],
        ),
        "Checking",
    )
    savings = convert_transactions(
        pd.read_csv(
            "sparkonto.csv",
            dayfirst=True,
            delimiter=";",
            encoding="iso-8859-1",
            thousands=".",
            decimal=",",
            parse_dates=["Buchung", "Valuta"],
        ),
        "Savings",
    )

    result = checking.append(savings, ignore_index=True)
    result.sort_values("DATE", inplace=True, ascending=False)
    result.to_csv(
        "result.csv",
        index=False,
        header=False,
        decimal=",",
        sep=";",
        date_format="%d/%m/%Y",
    )

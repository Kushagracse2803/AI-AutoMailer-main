import os
import pandas as pd

HISTORY_FILE = "data/sent_history.csv"


def load_history():

    os.makedirs("data", exist_ok=True)

    if not os.path.exists(HISTORY_FILE):

        pd.DataFrame(
            columns=["Email"]
        ).to_csv(
            HISTORY_FILE,
            index=False
        )

    history = pd.read_csv(HISTORY_FILE)

    return set(
        history["Email"]
        .astype(str)
        .str.lower()
        .str.strip()
    )


def save_history(history):

    pd.DataFrame(
        {
            "Email": sorted(history)
        }
    ).to_csv(
        HISTORY_FILE,
        index=False
    )
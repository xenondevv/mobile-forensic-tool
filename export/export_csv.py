import pandas as pd
import os

def export_to_csv(data, filename):
    if not os.path.exists("output"):
        os.makedirs("output")
    df = pd.DataFrame(data)
    df.to_csv(f"output/{filename}.csv", index=False)

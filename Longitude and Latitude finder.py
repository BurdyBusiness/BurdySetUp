import pandas as pd
import time

FILE_PATH = r"C:\Users\user\OneDrive\Documents\Business\ONSPD_FEB_2025_UK.csv"

print("Loading ONS Postcode Directory… this may take up to a minute.")

start = time.time()

df = pd.read_csv(
    FILE_PATH,
    usecols=["pcds", "lat", "long"],
    dtype={"pcds": "string", "lat": "float32", "long": "float32"}
)

df["pcds_clean"] = df["pcds"].str.replace(" ", "").str.upper()
df = df.set_index("pcds_clean")

print(f"Loaded {len(df):,} postcodes in {time.time() - start:.1f} seconds.\n")

while True:
    postcode = input("Enter postcode (or 'exit'): ").strip()

    if postcode.lower() == "exit":
        break

    key = postcode.replace(" ", "").upper()

    if key in df.index:
        lat = df.loc[key, "lat"]
        lon = df.loc[key, "long"]
        print(f"Latitude: {lat}, Longitude: {lon}\n")
    else:
        print("Postcode not found.\n")

import pandas as pd
import os
from pymongo import MongoClient

def seed_mongo():
    try:
        # MongoDB connection
        uri = os.getenv("MONGO_URL")
        client = MongoClient(uri, serverSelectionTimeoutMS=3000)

        db = client[os.getenv("DB_NAME", "HealthcareDB")]
        patients = db[os.getenv("PATIENT_COLLECTION", "StrokeData")]
        markers = db["SeedMarkers"]

        # Try pinging Mongo first
        try:
            client.admin.command("ping")
        except Exception:
            print("Mongo unreachable. Skipping seeding")
            return

        # Check marker
        if markers.find_one({"name": "stroke_seed_done"}):
            print("Seed skipped (already done).")
            return

        # Load CSV
        try:
            df = pd.read_csv("healthcare-dataset-stroke-data.csv")
        except Exception:
            print("CSV missing or unreadable. Skipping seeding.")
            return

        # Minimal cleaning
        df["bmi"] = pd.to_numeric(df["bmi"], errors="coerce").fillna(0)

        records = df.to_dict("records")

        # Insert records to mongo
        try:
            patients.delete_many({})
            if records:
                patients.insert_many(records)
        except Exception:
            print("Database insert failed. Skipping seeding.....")
            return

        #  marker to confirm the db has already been seeded
        markers.insert_one({"name": "stroke_seed_done"})

        print(f"Seed complete. Inserted {len(records)} records.")

    except Exception as e:
        # NEVER let the app break
        print("Unexpected error during seeding, but continuing:", e)

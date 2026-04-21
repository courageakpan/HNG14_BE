import json
from app import create_app
from extensions import db
from models import Profile
from uuid6 import uuid7
from datetime import datetime

app = create_app()
def seed():
    with app.app_context():

        # ✅ Load JSON file
        with open('data.json') as f:
            data = json.load(f)

        # 🔥 IMPORTANT: if your JSON is wrapped like {"profiles": [...]}
        if isinstance(data, dict) and "profiles" in data:
            data = data["profiles"]

        inserted = 0

        for item in data:
            try:
                # ✅ Extract name safely
                name = item.get("name", "").lower().strip()

                if not name:
                    continue

                # ✅ Prevent duplicates (VERY IMPORTANT)
                exists = Profile.query.filter_by(name=name).first()
                if exists:
                    continue

                # ✅ Create profile directly from JSON
                profile = Profile(
                    id=str(uuid7()),
                    name=name,
                    gender=item.get("gender"),
                    gender_probability=item.get("gender_probability"),
                    sample_size=None,  # not in dataset, safe to leave None
                    age=item.get("age"),
                    age_group=item.get("age_group"),
                    country_id=item.get("country_id"),
                    country_name=item.get("country_name"),
                    country_probability=item.get("country_probability"),
                    created_at=datetime.utcnow()
                )

                db.session.add(profile)
                inserted += 1

                # ✅ Optional: batch commit every 100 (better performance)
                if inserted % 100 == 0:
                    db.session.commit()
                    print(f"{inserted} profiles inserted...")

            except Exception as e:
                print(f"Error processing item: {e}")
                continue

        # ✅ Final commit
        db.session.commit()

        print(f"Seeding complete. Total inserted: {inserted}")


if __name__ == "__main__":
    seed()
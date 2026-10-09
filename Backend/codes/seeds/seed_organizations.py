from sqlalchemy import select
from sqlalchemy.orm import Session

from codes.database import SessionLocal
from codes.models.organizations.organization import Organization


ISP_ORGANIZATIONS = [
    {
        "name": "WorldLink Communications",
        "code": "WORLDLINK",
    },
    {
        "name": "Vianet Communications",
        "code": "VIANET",
    },
    {
        "name": "Subisu Cablenet",
        "code": "SUBISU",
    },
    {
        "name": "DishHome Fibernet",
        "code": "DISHHOME",
    },
    {
        "name": "Classic Tech",
        "code": "CLASSICTECH",
    },
]


def seed_organizations(db: Session) -> None:
    existing_codes = set(
        db.scalars(
            select(Organization.code)
        ).all()
    )

    created = 0
    skipped = 0

    for isp in ISP_ORGANIZATIONS:
        if isp["code"] in existing_codes:
            print(f"Skipped (already exists): {isp['name']}")
            skipped += 1
            continue

        organization = Organization(
            name=isp["name"],
            code=isp["code"],
            is_active=True,
        )

        db.add(organization)
        existing_codes.add(isp["code"])

        print(f"Added: {isp['name']}")
        created += 1

    db.commit()

    print("\nOrganization seeding completed.")
    print(f"Created: {created}")
    print(f"Skipped: {skipped}")


def main() -> None:
    with SessionLocal() as db:
        try:
            seed_organizations(db)
        except Exception:
            db.rollback()
            raise


if __name__ == "__main__":
    main()
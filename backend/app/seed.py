from app.db.session import SessionLocal
from app.db.models.users import Role, User
from app.db.models.inventory import Location
from app.core.security import hash_password

db = SessionLocal()
# Create minimal roles and admin if not exists
try:
    if not db.query(Role).filter(Role.role_name=="System Administrator").first():
        db.add(Role(role_name="System Administrator"))
    if not db.query(Role).filter(Role.role_name=="Warehouse Manager").first():
        db.add(Role(role_name="Warehouse Manager"))
    db.commit()
except Exception as e:
    print("Seed roles error (tables may not exist):", e)

# create admin user if not exists
try:
    if not db.query(User).filter(User.username=="admin").first():
        db.add(User(username="admin", email="admin@example.com", password_hash=hash_password("admin123")))
        db.commit()
except Exception as e:
    print("Seed user error:", e)

# create example 'Online' location and a sample location
try:
    if not db.query(Location).filter(Location.location_name=="Online").first():
        db.add(Location(location_name="Online", location_type="Online"))
    if not db.query(Location).filter(Location.location_name=="Warehouse").first():
        db.add(Location(location_name="Warehouse", location_type="Warehouse"))
    db.commit()
except Exception as e:
    print("Seed location error:", e)

print("Seed completed (errors printed if any).")

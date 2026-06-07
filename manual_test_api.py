import urllib.request
import json

BASE = "http://127.0.0.1:8000/api"

# Step 1: Login
login_data = json.dumps({
    "email": "testuser@gmail.com",
    "password": "test1234"
}).encode()

req = urllib.request.Request(
    f"{BASE}/auth/login/",
    data=login_data,
    headers={"Content-Type": "application/json"},
    method="POST"
)
with urllib.request.urlopen(req) as res:
    tokens = json.loads(res.read())

access = tokens["access"]
print(f"✅ Login OK — token: {access[:40]}...")

# Step 2: Create application
app_data = json.dumps({
    "company_name": "Google",
    "role_title": "Python Developer",
    "status": "Applied",
    "location": "Pune",
    "salary_range": "8-12 LPA"
}).encode()

req = urllib.request.Request(
    f"{BASE}/applications/",
    data=app_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access}"
    },
    method="POST"
)
with urllib.request.urlopen(req) as res:
    app = json.loads(res.read())

app_id = app["id"]
print(f"✅ Application created — id: {app_id}")

# Step 3: Add a note
note_data = json.dumps({
    "content": "Applied via LinkedIn. HR name is Priya."
}).encode()

req = urllib.request.Request(
    f"{BASE}/applications/{app_id}/notes/",
    data=note_data,
    headers={
        "Content-Type": "application/json",
        "Authorization": f"Bearer {access}"
    },
    method="POST"
)
with urllib.request.urlopen(req) as res:
    note = json.loads(res.read())

print(f"✅ Note created — id: {note['id']}")

# Step 4: List applications
req = urllib.request.Request(
    f"{BASE}/applications/",
    headers={"Authorization": f"Bearer {access}"},
    method="GET"
)
with urllib.request.urlopen(req) as res:
    apps = json.loads(res.read())

# Step 5: Dashboard summary
req = urllib.request.Request(
    f"{BASE}/dashboard/summary/",
    headers={"Authorization": f"Bearer {access}"},
    method="GET"
)
with urllib.request.urlopen(req) as res:
    dashboard = json.loads(res.read())

print(f"✅ Dashboard — total: {dashboard['total']}, by status: {dashboard['by_status']}")

print(f"✅ List applications — total: {len(apps['results']) if 'results' in apps else len(apps)}")

print("\n🎉 All 4 tests passed!")
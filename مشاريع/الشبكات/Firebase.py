from firebase_rest import FirebaseREST

fb = FirebaseREST(
    project_id="your-project-id",
    api_key="your-firebase-web-api-key",
    service_account_path="serviceAccountKey.json"  # optional for secure calls
)

# 1️⃣ Firestore
fb.add_document("users", {"name": "Ali", "age": 25}, "ali123")
print(fb.get_document("users", "ali123"))

# 2️⃣ Realtime Database
fb.db_set("users/ali", {"name": "Ali", "active": True})
print(fb.db_get("users/ali"))

# 3️⃣ Auth
user = fb.sign_up("ali@example.com", "12345678")
print("New user:", user)

# 4️⃣ Storage
print(fb.upload_file("photo.png", "uploads/photo.png"))


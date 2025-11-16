
"""
firebase_rest.py
Mini Firebase SDK using REST APIs (Python)
"""

import requests
from google.oauth2 import service_account
import google.auth.transport.requests


class FirebaseREST:
    def init(self, project_id: str, api_key: str, service_account_path: str = None):
        """
        project_id: Firebase project ID
        api_key: Firebase Web API key (from project settings)
        service_account_path: path to service account JSON (optional, for server-to-server auth)
        """
        self.project_id = project_id
        self.api_key = api_key
        self.base_firestore = f"https://firestore.googleapis.com/v1/projects/{project_id}/databases/(default)/documents"
        self.base_db = f"https://{project_id}.firebaseio.com"
        self.base_auth = "https://identitytoolkit.googleapis.com/v1"
        self.base_storage = f"https://firebasestorage.googleapis.com/v0/b/{project_id}.appspot.com/o"

        self.token = None
        if service_account_path:
            self.token = self._get_service_account_token(service_account_path)

    # ======================================================
    # 🔑 AUTH HELPERS
    # ======================================================
    def _get_service_account_token(self, path: str):
        """Generate OAuth 2.0 access token from service account"""
        creds = service_account.Credentials.from_service_account_file(path)
        creds = creds.with_scopes(["https://www.googleapis.com/auth/cloud-platform"])
        auth_req = google.auth.transport.requests.Request()
        creds.refresh(auth_req)
        return creds.token

    def _headers(self):
        if self.token:
            return {"Authorization": f"Bearer {self.token}"}
        return {}

    # ======================================================
    # 🔥 FIRESTORE REST API
    # ======================================================
    def get_document(self, collection: str, doc_id: str):
        url = f"{self.base_firestore}/{collection}/{doc_id}"
        res = requests.get(url, headers=self._headers())
        return res.json()

    def add_document(self, collection: str, data: dict, doc_id: str = None):
        if doc_id:
            url = f"{self.base_firestore}/{collection}/{doc_id}"
            res = requests.patch(url, json={"fields": self._encode_fields(data)}, headers=self._headers())
        else:
            url = f"{self.base_firestore}/{collection}"
            res = requests.post(url, json={"fields": self._encode_fields(data)}, headers=self._headers())
        return res.json()

    def _encode_fields(self, data: dict):
        """Convert Python dict -> Firestore REST field format"""
        def encode_value(value):
            if isinstance(value, bool):
                return {"booleanValue": value}
            elif isinstance(value, int):
                return {"integerValue": str(value)}
            elif isinstance(value, float):
                return {"doubleValue": value}
            else:
                return {"stringValue": str(value)}

        return {k: encode_value(v) for k, v in data.items()}

    # ======================================================
    # 💾 REALTIME DATABASE REST API
    # ======================================================
    def db_get(self, path: str):
        url = f"{self.base_db}/{path}.json"
        res = requests.get(url, headers=self._headers())
        return res.json()

    def db_set(self, path: str, data: dict):
        url = f"{self.base_db}/{path}.json"
        res = requests.put(url, json=data, headers=self._headers())
        return res.json()

    # ======================================================
    # 👤 AUTH REST API
    # ======================================================
    def sign_up(self, email: str, password: str):
        url = f"{self.base_auth}/accounts:signUp?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        return requests.post(url, json=payload).json()


def sign_in(self, email: str, password: str):
        url = f"{self.base_auth}/accounts:signInWithPassword?key={self.api_key}"
        payload = {"email": email, "password": password, "returnSecureToken": True}
        return requests.post(url, json=payload).json()

    # ======================================================
    # ☁️ STORAGE REST API
    # ======================================================
    def upload_file(self, local_path: str, remote_name: str):
        files = {"file": open(local_path, "rb")}
        url = f"{self.base_storage}?uploadType=media&name={remote_name}"
        res = requests.post(url, files=files, headers=self._headers())
        return res.json()

    def download_file(self, remote_name: str, local_path: str):
        url = f"{self.base_storage}/{remote_name}?alt=media"
        res = requests.get(url, headers=self._headers())
        with open(local_path, "wb") as f:
            f.write(res.content)
        return local_path

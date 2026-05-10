import firebase_admin
from firebase_admin import credentials, auth, firestore
import json
import os

firebase_creds_json = os.getenv("FIREBASE_CREDENTIALS_JSON")
if firebase_creds_json:
    cred = credentials.Certificate(json.loads(firebase_creds_json))
else:
    cred = credentials.Certificate("firebase-credentials.json")

firebase_admin.initialize_app(cred)
db = firestore.client()


def verify_token(id_token: str) -> str | None:
    try:
        decoded = auth.verify_id_token(id_token)
        return decoded["uid"]
    except Exception as e:
        print(f"[verify_token error] {e}")
        return None


def get_active_partida(uid: str, partida_id: str) -> dict | None:
    try:
        doc = (
            db.collection("partidas")
            .document(uid)
            .collection("partidas")
            .document(partida_id)
            .get()
        )
        if doc.exists:
            return doc.to_dict()
        return None
    except Exception:
        return None

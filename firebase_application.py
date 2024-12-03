import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import json

cred = credentials.Certificate("./serviceAccount.json")
firebase_admin.initialize_app(
    cred,
    {"databaseURL": "https://auto-question-gen-default-rtdb.firebaseio.com/"},
)


def get_source_list():
    source_ref = firebase_admin.db.reference("/question-gen-sources")
    snapshot = source_ref.order_by_child("id").get()
    return snapshot


question_ref = firebase_admin.db.reference("/generated-question-list")


def add_question_gen_data(data):
    new_data = {
        **data,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime(
            "%Y-%m-%dT%H:%M:%SZ"
        ),
        "state": "PENDING",  # PENDING | DRAFT | PUBLISHED
        "review": [],
    }
    question_ref.child("question-" + str(data["index"])).set(new_data)
    # question_ref.push().set(new_data)

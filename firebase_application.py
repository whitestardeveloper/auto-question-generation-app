import firebase_admin
from firebase_admin import credentials
import os

# download serviceAccount.json file
cred = credentials.Certificate("./serviceAccount.json")
firebase_admin.initialize_app(
    cred,
    {"databaseURL": os.environ.get("FIREBASE_DB_URL")},
)


def get_source_list():
    source_ref = firebase_admin.db.reference("/question-gen-sources")
    snapshot = source_ref.order_by_child("id").get()
    return snapshot


def get_generated_question_list():
    source_ref = firebase_admin.db.reference("/generated-question-list")
    snapshot = source_ref.order_by_child("index").get()
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



def add_question_ai_reviewer(rates_array, question_key):
    try:
        # Reference to the database location
        data_ref = firebase_admin.db.reference("/generated-question-list/{}/review".format(question_key))
        # Prepare reviewer data
        reviewer_data = {
            'reviewer_name': 'GEMMA2 27B',
            'reviwer_mail': '',
            'reviewer_type': 'ai', # ai, manual
            'description': '',
            "created_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime(
                "%Y-%m-%dT%H:%M:%SZ"
            ),
            'is_valid_question': True,
            'question_rates': rates_array
        }
        updated_reviewer_list = [reviewer_data]
        data_ref.set(updated_reviewer_list)
    except Exception as e:
        print(f"An error occurred: {e}")
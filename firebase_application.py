import firebase_admin
from firebase_admin import credentials
from firebase_admin import db
import datetime
import json

# Fetch the service account key JSON file contents
cred = credentials.Certificate('./serviceAccount.json')

# Initialize the app with a service account, granting admin privileges
default_app = firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://automatic-question-creator-default-rtdb.firebaseio.com/'
})

ref = firebase_admin.db.reference('/question-gen-sources')
# def add_question_source_data_item(data):
#     new_data={
#         **data,
#         "created_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
#         "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
#     }

#     # update_time, city_ref = db.collection("question-generation-pool").add(data1)

#     ref.child('source-row-' + str(data['id'])).set(new_data)
    # ref.push().set(new_data)

# add_question_gen_data(None)

# print(ref.get())


def get_source_list():
    # snapshot = ref.order_by_key().get()
    snapshot = ref.order_by_child('id').get()
    return snapshot



def add_question_gen_data(data):
    question_ref = firebase_admin.db.reference('/generated-question-list')

    new_data={
        **data,
        "created_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "updated_at": datetime.datetime.now(tz=datetime.timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ'),
        "state": "PENDING", # PENDING | DRAFT | PUBLISHED
        "review": {
            "reviewer_user": { "mail": "", "full_name": ""},
            "description": "",
            "rating": 0, # None | 0 - 5 stars
        }
    }

    # update_time, city_ref = db.collection("question-generation-pool").add(data1)
    # ref.push().set(data1)


    question_ref.push().set(new_data)
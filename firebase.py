import firebase_admin
from firebase_admin import credentials , firestore

credential = credentials.Certificate('datahackru-firebase-adminsdk-4xarf-e0251e8577.json')
firebase_admin.initialize_app(credential)

database = firestore.client()

def update_database(name , password , aim_data , goal_data):
    object = {
        'username' : name,
        'password' : password,
        'aim_data' : aim_data,
        'goal_data' : goal_data,
    }
    #add to database
    doc_ref = database.collection(u'Users').document(object['username'])
    doc_ref.set(object)


def get_aim_data(username):
    users_ref = database.collection(u'Users')
    documents = users_ref.stream()
    for doc in documents:
        if(doc.id == username):
            doc = doc.to_dict()
            aim_data = doc['aim_data']
            return aim_data


def get_goal_data(username):
    users_ref = database.collection(u'Users')
    documents = users_ref.stream()
    for doc in documents:
        if(doc.id == username):
            doc = doc.to_dict()
            goal_data = doc['goal_data']
            return goal_data

#returns true if the username and password match
def login(username , password):
    users_ref = database.collection(u'Users')
    documents = users_ref.stream()
    for doc in documents:
        if(doc.id == username and doc.to_dict()['password'] == password):
            return True
    return False

#returns false if username already exists
def isUsername(username):
    users_ref = database.collection(u'Users')
    documents = users_ref.stream()
    for doc in documents:
        if(doc.id == username):
            return False
    return True

valid_user = None
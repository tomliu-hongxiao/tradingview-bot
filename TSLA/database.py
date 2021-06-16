import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class DataBase:
    def __init__(self, cred):
        self.cred = credentials.Certificate(cred)
        firebase_admin.initialize_app(self.cred)
        self.db = firestore.client()

    def get_signal(self):
        doc_ref = self.db.collection(u'messages').document(u'signal')
        doc = doc_ref.get()
        if doc.exists:
            text = doc.to_dict()['text']
            text = text.split(',')
            result = {'order_action': text[1], 'order_position': int(text[0]), 'time': int(text[2][-6:-4])}
            return result
        else:
            return None


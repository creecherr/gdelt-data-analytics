from firebase_admin import firestore


class Firebase:
    def __init__(self):
        self.store = firestore.client()
        self.doc_ref = self.store.collection(u'data')
        self.index_ref = self.store.collection(u'index')

    def get_data(self):
        data = []
        docs = self.doc_ref.stream()
        for doc in docs:
            data.append(doc.to_dict())
        return data

    def add_document(self, data, id):
        self.doc_ref.document(f"u'{id}'").set(data)

    def get_index(self):
        doc_ref = self.index_ref.document(u'index')
        doc = doc_ref.get()
        data = doc._data
        return data['index']

    def update_index(self, index):
        self.index_ref.document(u'index').update({'index': index})

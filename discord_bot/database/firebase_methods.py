import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


cred = credentials.Certificate("database/pixiebot-aea70-firebase-adminsdk-7verr-0e8da3dbfc.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

def add_data(user_id,level,username,xp):
    doc_ref = db.collection("users").document(str(user_id))
    
    data = {
        "display_name":username,
        "id":user_id,
        "level":level,
        "xp":xp,
    }
    doc_ref.set(data)
    print("veri başarıyla yazdırıldı!")
    
def get_data(user_id,message):
    doc_ref = db.collection("users").document(str(user_id))
    doc = doc_ref.get()
    
    if doc.exists:
        return doc.to_dict()
    else:
        print("çalıştı!!")
        return {"xp":0,"level":1,"message":message}
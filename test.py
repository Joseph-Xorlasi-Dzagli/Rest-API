import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://webtech-1b839-default-rtdb.firebaseio.com/"})
ref = db.reference('py/')
voter_ref = ref.child('voter')
election_ref = ref.child('election')

# Set Data
voter_ref.set({"1":{
    "name": "kwame",
     "email": "j@m.com", 
     "yeargroup": "2024", 
     "contact": "0206252066", 
     "major": "Business"
     }, 
     "2":{
    "name": "Joseph",
     "email": "j@m.com", 
     "yeargroup": "2024", 
     "contact": "0206252066", 
     "major": "Science"}
})


# Update Data
newVoter_ref = voter_ref.child("1")
newVoter_ref.update({"name":"Joshua"})

# read data
handle = db.reference('py/voter_ref/1')

# Read data at the posts reference (this is a blocking operation)
print(ref.get())

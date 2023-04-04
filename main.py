import json
from flask import Flask, request, jsonify

import firebase_admin
from firebase_admin import credentials, db

cred = credentials.Certificate("key.json")
firebase_admin.initialize_app(cred, {"databaseURL": "https://webtech-1b839-default-rtdb.firebaseio.com/"})
ref = db.reference('py/')
voter_ref = ref.child('voter')
election_ref = ref.child('election')
voter_ref.set({})
election_ref.set({})



app = Flask(__name__)

@app.route("/")
def index():
    return "<h1>Welcome<h1>"

# 1. Registering a student as a voter.
# a. It will be necessary for new students to be registered to vote.
@app.route("/register", methods = ['GET', 'POST'])
def register():
    voterId = request.args.get('voterId')
    name = request.args.get('name')
    email = request.args.get('email')
    yeargroup =  request.args.get('yeargroup')
    contact = request.args.get('contact')
    major = request.args.get('major')



    voter_ref.child(voterId).set({
    "name": name,
     "email": email, 
     "yeargroup": yeargroup, 
     "contact": contact, 
     "major": major
     })
        
    return jsonify({'status': '200 Ok'})

# 2. De-registering a student as a voter.
# a. A student may need to be de-registered once they leave campus.
@app.route("/deregister", methods = ['GET', 'DELETE'])
def delete():
    voterId = request.args.get('voterId')
    voter_ref.child(voterId).delete()    
    return jsonify({'status': '200 Ok'})


    
# 3. Updating a registered voter’s information.
# a. A student’s year group, major or other information might change.
@app.route('/edit-voter', methods=['GET', 'PUT'])
def update_data():
    voterId = request.args.get('voterId')
    major = request.args.get('major')
    contact = request.args.get('contact')

    voter_ref.child(voterId).update({
        "major": major,
        "contact": contact
    })
    # Return the updated object as a JSON response
    return jsonify(voter_ref.child(voterId).get())

    



# 4. Retrieving a registered voter.
@app.route('/view-voter', methods=['GET'])
def view_voter():  
    voterId = request.args.get('voterId')
    voter_ref.child(voterId).get() 
    return jsonify(voter_ref.child(voterId).get())


# 5. Creating an election.
@app.route('/new-election', methods=['GET', 'POST'])
def create_election():  
    ElectionId = request.args.get("ElectionId")
    Election = request.args.get("Election")
    Year = request.args.get("Year")
    Position = request.args.get("Position")
    Candidate = request.args.get("Candidate")
    count = request.args.get("count")
   

    election_ref.child(ElectionId).set({
                    "Election" : Election,
                    "Year" : Year,
                    "Position" : Position,
                    "Candidate" : Candidate,
                    "count" : count
                })    
    return jsonify({'status': '200 Ok'})


# 6. Retrieving an election (with its details).
@app.route('/view-election', methods=['GET'])
def view_election():  
    ElectionId = request.args.get('ElectionId')
    election_ref.child(ElectionId).get()    
    return jsonify(election_ref.child(ElectionId).get())

# 7. Deleting an election.
@app.route("/delete-election", methods = ['GET', 'DELETE'])
def delete_election():
    ElectionId = request.args.get('ElectionId')
    election_ref.child(ElectionId).delete()    
    return jsonify({'status': '200 Ok'})


# 8. Voting in an election.
@app.route("/vote", methods = ['GET', 'PUT'])
def vote():
    ElectionId = request.args.get('ElectionId')
    # Candidate = request.args.get('Candidate')
    # count = db.reference('py/election_ref/'+ ElectionId + '/count')
    count = election_ref.child(ElectionId).child("count").get()

    election_ref.child(ElectionId).update({
        "count": str(int(count)+1)
    })    # Return the updated object as a JSON response
    return jsonify(election_ref.child(ElectionId).get())

if __name__ == '__main__':
    app.debug = True
    app.run()


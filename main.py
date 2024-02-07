import pandas as pd
import os
from flask import Flask, request, jsonify
import pandas as pd
import os

app = Flask(__name__)


class DB:
    def __init__(self, filename='user_data.csv'):
        self.filename = filename
        self.users = self.load_users()
        if(filename not in os.listdir()):
            if filename not in os.listdir():
                # Initialize a DataFrame with the specified columns
                self.users = pd.DataFrame(columns=['username', 'password', 'summary'])
                # Save the DataFrame as a CSV file
                self.users.to_csv(filename, index=False)
            
    def load_users(self):
        if os.path.exists(self.filename):
            return pd.read_csv(self.filename)
        else:
            return pd.DataFrame(columns=['user', 'password', 'summary'])

    def add_user(self, usr, pwd, summary):
        if usr not in self.users['user'].values:
            new_user = pd.DataFrame([[usr, pwd, summary]], columns=['user', 'password', 'summary'])
            self.users = pd.concat([self.users, new_user], ignore_index=True)
            self.users.to_csv(self.filename, index=False)

    def get_user(self, usr, pwd):
        user_data = self.users[self.users['user'] == usr]
        if not user_data.empty:
            if pwd == user_data.iloc[0]['password']:
                return user_data.iloc[0]['summary']
        return None

@app.route('/get_summary', methods=['POST'])
def get_summary():
    # Extract username and password from the request
    data = request.get_json()
    usr = data.get('username')
    pwd = data.get('password')
    
    if not usr or not pwd:
        return jsonify({'error': 'Missing username or password'}), 400
    
    db = DB()
    summary = db.get_user(usr, pwd)
    
    if summary:
        return jsonify({'username': usr, 'summary': summary})
    else:
        return jsonify({'error': 'User not found or incorrect password.'}), 404

if __name__ == '__main__':
    app.run(debug=True)
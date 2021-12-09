from logging import debug
from flask import Flask, request
import os
import psycopg2
import uuid
import json
from flask_cors import CORS

app = Flask(__name__)
# https://stackoverflow.com/a/64657739
CORS(app, support_credentials=True)
# https://devcenter.heroku.com/articles/heroku-postgresql#connecting-in-python

DATABASE_URL = os.environ['DATABASE_URL']
conn = psycopg2.connect(DATABASE_URL, sslmode='require')
# https://stackoverflow.com/a/43634941
conn.autocommit = True

cursor = conn.cursor()
try:
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS time_taken_per_screen_2 (
        screen varchar(256),
        timeTaken integer
    );
    ''')
except psycopg2.Error:
    print('Error occurred while creating table')


@app.route('/health-check')
def health_check():
    return {'status': 200}

@app.route('/time-on-screen', methods=['POST'])
def create_entry():
    # https://stackoverflow.com/a/67461897
    data = request.get_json()
    screen = data['screen']
    timeTaken = int(data['timeTaken'])
    query = '''
        INSERT INTO time_taken_per_screen_2 (screen, timeTaken)
        VALUES (%s, 
    '''
    query = query + str(timeTaken) + ')'

    print("Running", query)

    cursor.execute(query, [screen])
    
    return {'status': 201}

# https://www.youtube.com/watch?v=4eQqcfQIWXw
if __name__ == '__main__':
    port = os.environ.get('PORT', 5000)
    app.run(debug=True, host='0.0.0.0', port=port)
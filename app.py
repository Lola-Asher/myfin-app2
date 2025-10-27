import redis
from flask import Flask, session, request
import psycopg2

app = Flask(__name__)
app.secret_key = 'supersecret'

# Connect to Redis
r = redis.Redis(host='redis', port=6379, db=0)

# Connect to Postgres
conn = psycopg2.connect(
    dbname="bank", user="postgres", password="password", host="db"
)

@app.route('/action', methods=['POST'])
def action():
    user = session.get('user_id')
    action_data = request.json['action']
    # Save to database
    with conn.cursor() as cur:
        cur.execute("INSERT INTO logs (user_id, action) VALUES (%s, %s)", (user, action_data))
        conn.commit()
    # Save session state to Redis
    r.set(f"user:{user}:state", "last_action")
    return "Action saved!"

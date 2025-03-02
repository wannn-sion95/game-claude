from flask import Flask, render_template, request, jsonify
from game_logic import process_command

app = Flask(__name__)

# Inisialisasi game_state dengan current_location
game_state = {"current_location": "start"}  
world = {"start": {"description": "You are in a dark room."}}  # Tambahkan lokasi awal
items = {}
npcs = {}
enemies_dict = {}

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/command', methods=['POST'])
def command():
    data = request.json
    user_input = data.get("command", "")
    
    response = process_command(user_input, game_state, world, items, npcs, enemies_dict)
    
    return jsonify({"response": response})

if __name__ == '__main__':
    app.run(debug=True)

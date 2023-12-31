from flask import Flask, request, render_template, jsonify
from uuid import uuid4

from boggle import BoggleGame

from flask_debugtoolbar import DebugToolbarExtension


app = Flask(__name__)
app.config["SECRET_KEY"] = "this-is-secret"
debug = DebugToolbarExtension(app)

# The boggle games created, keyed by game id
games = {}


@app.get("/")
def homepage():
    """Show board."""

    return render_template("index.html")


@app.post("/api/new-game")
def new_game():
    """Start a new game and return JSON: {game_id, board}."""

    # get a unique string id for the board we're creating
    game_id = str(uuid4())
    game = BoggleGame()
    games[game_id] = game

    return jsonify({"gameId": game_id, "board": game.board})


@app.post("/api/score-word")
def valid_word():
    """Takes JSON: {'gameId', 'word'} Determine if valid word and return JSON:
    {"result": "not-word" or "not-on-board" or "ok" } """

    data = request.json
    word = data["word"]
    game = games[data['gameId']]

    if not game.is_word_in_word_list(word):
        return jsonify({"result": "not-word"})
    elif not game.check_word_on_board(word):
        return jsonify({"result": "not-on-board"})

    return jsonify({"result": "ok"})

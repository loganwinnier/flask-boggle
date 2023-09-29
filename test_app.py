from unittest import TestCase

from app import app, games

# Make Flask errors be real errors, not HTML pages with error info
app.config['TESTING'] = True

# This is a bit of hack, but don't use Flask DebugToolbar
app.config['DEBUG_TB_HOSTS'] = ['dont-show-debug-toolbar']


class BoggleAppTestCase(TestCase):
    """Test flask app of Boggle."""

    def setUp(self):
        """Stuff to do before every test."""

        app.config['TESTING'] = True

    def test_homepage(self):
        """Make sure information is in the session and HTML is displayed"""

        with app.test_client() as client:
            response = client.get('/')
            html = response.get_data(as_text=True)

            self.assertEqual(response.status_code, 200)
            self.assertIn('<!-- Homepage Template - used in test -->', html)

    def test_api_new_game(self):
        """Test starting a new game."""

        with app.test_client() as client:
            resp = client.post('/api/new-game')
            data = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIsInstance(data['gameId'], str)
            self.assertIsInstance(data['board'], list)
            self.assertIsInstance(data['board'][0], list)
            self.assertIn(data["gameId"], games)

    def test_api_score_word_not_word(self):
        """Test word for not a valid word"""

        with app.test_client() as client:
            resp_new_game = client.post('/api/new-game')
            new_game_data = resp_new_game.get_json()

            game = games[new_game_data['gameId']]
            game.board = [
                ["C", "A", "T"],
                ["O", "X", "X"],
                ["X", "G", "X"]]

            resp = client.post(
                '/api/score-word',
                json={'gameId': new_game_data["gameId"], 'word': "XGX"})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({"result": "not-word"}, resp.get_json())

    def test_api_score_word_ok(self):
        """Test for valid word"""

        with app.test_client() as client:
            resp_new_game = client.post('/api/new-game')
            new_game_data = resp_new_game.get_json()

            game = games[new_game_data['gameId']]
            game.board = [
                ["C", "A", "T"],
                ["O", "X", "X"],
                ["X", "G", "X"]]

            resp = client.post(
                '/api/score-word',
                json={'gameId': new_game_data["gameId"], 'word': "CAT"})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({"result": "ok"}, resp.get_json())

    def test_api_score_word_not_on_board(self):
        """Test for word not on board"""

        with app.test_client() as client:
            resp_new_game = client.post('/api/new-game')
            new_game_data = resp_new_game.get_json()

            game = games[new_game_data['gameId']]
            game.board = [
                ["C", "A", "T"],
                ["O", "X", "X"],
                ["X", "G", "X"]]

            resp = client.post(
                '/api/score-word',
                json={'gameId': new_game_data["gameId"], 'word': "DOG"})

            self.assertEqual(resp.status_code, 200)
            self.assertEqual({"result": "not-on-board"}, resp.get_json())

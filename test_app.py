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
            json = resp.get_json()

            self.assertEqual(resp.status_code, 200)
            self.assertIn('gameId', json)
            self.assertIn('board', json)
            self.assertIn(json["gameId"], games)

    def test_api_score_word(self):
        """Test validation of word."""

        with app.test_client() as client:
            resp_new_game = client.post('/api/new-game')
            new_game_data = resp_new_game.get_json()

            games[f"{new_game_data['gameId']}"].board = ["C", "A", "T"], [
                "O", "X", "X"], ["X", "G", "X"]

            def _test_word(word):
                resp = client.post(
                    '/api/score-word',
                    json={'gameId': f'{new_game_data["gameId"]}', 'word': word})
                self.assertEqual(resp.status_code, 200)
                return resp.get_json()

            self.assertEqual({"result": "not-word"}, _test_word("XGX"))
            self.assertEqual({"result": "not-on-board"}, _test_word("DOG"))
            self.assertEqual({"result": "ok"}, _test_word("CAT"))

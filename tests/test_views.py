from unittest.mock import patch

from django.test import TestCase
from django.http import HttpResponse, JsonResponse

from libs.google_actions import TestUtils as GoogleUtils
from libs.google_actions.tests.mocks import MockRequest

from apps.video_player.views import index


class TestViews(TestCase):
    def test_hello_world_if_not_json(self):
        result = index(MockRequest(body='NOT JSON'))
        self.assertIs(type(result), HttpResponse)
        self.assertIn("Hello world", str(result.content))

    def test_asks_what_would_you_like_to_play(self):
        result = index(MockRequest(text=''))
        self.assertIs(type(result), JsonResponse)
        self.assertEqual("What would you like to play?",
                         GoogleUtils.get_text_from_google_response(result))

    def test_says_i_dont_know_how(self):
        result = index(MockRequest(text='dance'))
        self.assertIs(type(result), JsonResponse)
        self.assertIn("I don't know how to dance",
                      GoogleUtils.get_text_from_google_response(result))

    def test_tell_response_for_blue_planet(self):
        with patch('apps.video_player.views.Messenger') as messenger:
            result = index(MockRequest(text='Blue Planet'))
        self.assertEqual(messenger.open_website.call_count, 1)
        self.assertIn(
            "Opening Blue Planet",
            GoogleUtils.get_text_from_google_response(result))

    def test_pause(self):
        with patch('apps.video_player.views.Messenger') as messenger:
            result = index(MockRequest(text='play'))
        self.assertEqual(messenger.play_pause_video.call_count, 1)
        self.assertEqual(
            "On it!",
            GoogleUtils.get_text_from_google_response(result))

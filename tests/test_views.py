from unittest.mock import patch

from django.test import TestCase
from django.http import HttpResponse, JsonResponse

from libs.google_actions import Util as GoogleUtil
from libs.google_actions.tests.mocks import MockRequest

from apps.video_player.views import index


class TestViews(TestCase):
    def test_hello_world_if_not_json(self):
        result = index(MockRequest(body='NOT JSON'))
        self.assertIs(type(result), HttpResponse)
        self.assertIn("Hello world", str(result.content))

    def test_asks_what_would_you_like_to_play(self):
        result = index(MockRequest(argument_text_value=None))
        self.assertIs(type(result), JsonResponse)
        self.assertEqual("What would you like to play?",
                         GoogleUtil.get_text_from_google_response(result))

    def test_says_i_dont_know_how(self):
        result = index(MockRequest(argument_text_value='dance'))
        self.assertIs(type(result), JsonResponse)
        self.assertIn("I don't know how to dance",
                      GoogleUtil.get_text_from_google_response(result))

    def test_tell_response_for_blue_planet(self):
        with patch('apps.video_player.views.Messenger') as messenger:
            result = index(MockRequest(argument_text_value='Blue Planet'))
        self.assertEqual(messenger.open_website.call_count, 1)
        self.assertIn(
            "Opening Blue Planet",
            GoogleUtil.get_text_from_google_response(result))

import json
from unittest.mock import patch

from django.test import TestCase
from django.http import HttpResponse, JsonResponse

from libs.google_actions import Util as GoogleUtil

from apps.video_player.views import index


class TestViews(TestCase):
    def test_hello_world_if_not_json(self):
        result = index(MockRequest(raise_json_decode=True))
        assert type(result) is HttpResponse
        assert "Hello world" in str(result.content)

    def test_asks_what_would_you_like_to_play(self):
        result = index(MockRequest(argument_text_value=None))
        assert type(result) is JsonResponse
        self.assertEqual(
            "What would you like to play?",
            GoogleUtil.get_text_from_google_response(result),
        )

    def test_tell_response_for_blue_planet(self):
        with patch('apps.video_player.views.Messenger') as messenger:
            result = index(MockRequest(argument_text_value='Blue Planet'))
        assert messenger.open_website.call_count == 1
        assert "Opening Blue Planet" in GoogleUtil.get_text_from_google_response(result)


class MockRequest(object):
    def __init__(self, argument_text_value=None, raise_json_decode=False):
        self.argument_text_value = argument_text_value
        self.raise_json_decode = raise_json_decode

    @property
    def body(self):
        if self.raise_json_decode:
            json.loads('NOT_JSON')  # raises JSONDecodeError

        if not self.argument_text_value:
            input_dict = {}
        else:
            input_dict = {'arguments': [{'textValue': self.argument_text_value}]}
        return json.dumps({'inputs': [input_dict]}).encode('utf-8')

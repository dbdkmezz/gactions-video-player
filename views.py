import json
import pprint
import logging

from django.http import HttpResponse

from libs.google_actions import ask, tell

from .models import VideoFolder
from .messenger import Messenger


logger = logging.getLogger('django')


def index(request):
    try:
        input = json.loads(request.body.decode('utf-8'))['inputs'][0]
    except json.JSONDecodeError:
        logger.warn("Unable to decode json")
        return HttpResponse("Hello world. You're at the video_player index.")

    logger.info("Input: %s", pprint.pformat(input))
    if 'arguments' not in input:
        return ask("What would you like to play?")
    else:
        query = input['arguments'][0]['textValue'].lower()
        video = VideoFolder.get_next_video_matching_query(query)
        if video:
            video.play()
            return tell("OK! Playing {}".format(video.name))
        if any(s in query for s in ('play', 'pause', 'resume')):
            Messenger.play_pause_video()
            return tell("On it!")
        if 'blue' in query:
            Messenger.open_website('https://www.bbc.co.uk/iplayer/episodes/p04tjbtx')
            return tell("OK! Opening Blue Planet, on iPlayer.")
        return ask("Sorry. I don't know how to {}. What would you like to play?".format(query))

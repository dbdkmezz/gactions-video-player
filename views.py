import logging

from django.http import HttpResponse

from libs.google_actions import GoogleActions, GoogleRequest, NoJsonException

from .models import VideoFolder
from .messenger import Messenger


logger = logging.getLogger('django')
google_actions = GoogleActions(logger)


def index(request):
    try:
        google_request = GoogleRequest(request, logger)
    except NoJsonException:
        return HttpResponse("Hello world. You're at the video_player index.")

    query = google_request.text
    if not query:
        return google_actions.ask("What would you like to play?")
    else:
        query = query.lower()
        video = VideoFolder.get_next_video_matching_query(query)
        if video:
            video.play()
            return google_actions.tell("OK! Playing {}".format(video.name))
        if any(s in query for s in ('play', 'pause', 'resume')):
            Messenger.play_pause_video()
            return google_actions.tell("On it!")
        if 'blue' in query:
            Messenger.open_website('https://www.bbc.co.uk/iplayer/episodes/p04tjbtx')
            return google_actions.tell("OK! Opening Blue Planet, on iPlayer.")
        return google_actions.ask("Sorry. I don't know how to {}. What would you like to play?".format(query))

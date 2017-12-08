import logging

from django.http import HttpResponse, JsonResponse

from libs.google_actions import AppResponse, AppRequest, NoJsonException

from .models import VideoFolder
from .messenger import Messenger


logger = logging.getLogger(__name__)


def index(request):
    try:
        google_request = AppRequest(request)
    except NoJsonException:
        return HttpResponse("Hello world. You're at the video_player index.")

    query = google_request.text
    if not query:
        return JsonResponse(AppResponse().ask("What would you like to play?"))

    query = query.lower()

    video = VideoFolder.get_next_video_matching_query(query)
    if video:
        video.play()
        return JsonResponse(AppResponse().tell("OK! Playing {}".format(video.name)))

    if any(s in query for s in ('play', 'pause', 'resume')):
        Messenger.play_pause_video()
        return JsonResponse(AppResponse().tell("On it!"))

    if 'blue' in query:
        Messenger.open_website(
            'https://www.bbc.co.uk/iplayer/episodes/p04tjbtx')
        return JsonResponse(AppResponse().tell("OK! Opening Blue Planet, on iPlayer."))

    return JsonResponse(AppResponse().ask(
        "Sorry. I don't know how to {}. What would you like to play?".format(query))
    )

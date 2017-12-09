import string

from factory import DjangoModelFactory, fuzzy, SubFactory

from apps.video_player.models import Video, VideoFolder


class VideoFolderFactory(DjangoModelFactory):
    class Meta:
        model = VideoFolder

    path = fuzzy.FuzzyText(length=100)
    full_name = fuzzy.FuzzyText(length=100)
    aliases = fuzzy.FuzzyText(length=100, chars="{},".format(string.ascii_letters))
    priority = fuzzy.FuzzyInteger(low=0)


class VideoFactory(DjangoModelFactory):
    class Meta:
        model = Video

    folder = SubFactory(VideoFolderFactory)
    file_name = fuzzy.FuzzyText(length=100)

import random
import string

import factory

from apps.video_player.models import Video, VideoFolder


def random_string(length=10, characters=string.ascii_letters):
    return u''.join(random.choice(characters) for x in range(length))


def random_int(min=0, max=1000):
    return random.randrange(min, max)


class VideoFolderFactory(factory.DjangoModelFactory):
    class Meta:
        model = VideoFolder

    path = factory.LazyAttribute(lambda t: random_string())
    full_name = factory.LazyAttribute(lambda t: random_string())
    aliases = factory.LazyAttribute(lambda t: random_string(
        characters="{},".format(string.ascii_letters)))
    priority = factory.LazyAttribute(lambda t: random_int())


class VideoFactory(factory.DjangoModelFactory):
    class Meta:
        model = Video

    folder = factory.SubFactory(VideoFolderFactory)
    file_name = factory.LazyAttribute(lambda t: random_string())

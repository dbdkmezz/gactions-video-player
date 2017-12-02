import os
import logging
import datetime

from django.db import models

from .messenger import Messenger
from .exceptions import AliasesContainSpaces, FolderContainsNoVideos, InvalidPath


logger = logging.getLogger('django')


class VideoFolder(models.Model):
    path = models.CharField(max_length=1024, unique=True)
    full_name = models.CharField(max_length=128)
    aliases = models.CharField(max_length=512)
    priority = models.PositiveIntegerField(default=100)

    def save(self, *args, **kwargs):
        if self.pk:  # video folder is not being created for the first time
            super(VideoFolder, self).save(*args, **kwargs)
            return

        if ' ' in self.aliases:
            raise AliasesContainSpaces("Aliases should be a comma separated list, with no spaces.")

        videos = list(self.paths_of_videos_in_folder())
        if not videos:
            raise FolderContainsNoVideos("{} contains no video files".format(self.path))

        # need to save it now so it has an id, then we can add the videos
        super(VideoFolder, self).save(*args, **kwargs)
        for v in videos:
            Video.objects.create(folder=self, file_name=v)

    def __str__(self):
        return "{}. Priority: {}, Aliases: [{}], Path:{}, {} Files".format(
            self.full_name,
            self.priority,
            self.aliases,
            self.path,
            Video.objects.filter(folder__id=self.id).count(),
        )

    @staticmethod
    def get_next_video_matching_query(query):
        for folder in VideoFolder.objects.all().order_by('-priority'):
            print(folder)
            for name in folder.aliases.split(','):
                if name.lower() in query.lower():
                    video = Video.objects.filter(folder__id=folder.id, last_played=None).order_by('file_name').first()
                    return video

    def paths_of_videos_in_folder(self):
        if not os.path.isdir(self.path):
            raise InvalidPath("{} is not a valid path".format(self.path))
        for f in os.listdir(self.path):
            if Video.is_video_file(f):
                yield f


class Video(models.Model):
    folder = models.ForeignKey('VideoFolder', on_delete=models.CASCADE)
    file_name = models.CharField(max_length=256)
    last_played = models.DateTimeField(null=True, blank=True)

    class Meta:
        unique_together = (("folder", "file_name"),)
        ordering = ['file_name']

    def __str__(self):
        return "{} - {} ({})".format(
            self.folder.full_name,
            self.file_name,
            self.last_played,
        )

    @staticmethod
    def is_video_file(filename):
        ENDINGS = ['mp4', 'mkv', 'avi']
        return any(filename.lower().endswith(".{}".format(e)) for e in ENDINGS)

    def play(self):
        self.last_played = datetime.datetime.now()
        self.save()
        Messenger.open_video(os.path.join(self.folder.path, self.file_name))

    @property
    def name(self):
        return self.folder.full_name

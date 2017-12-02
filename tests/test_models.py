import pytest
from unittest.mock import patch

from django.test import TestCase

from apps.video_player.models import Video, VideoFolder
from apps.video_player.exceptions import AliasesContainSpaces, InvalidPath
from .factories import VideoFolderFactory


@pytest.mark.django_db
class TestVideoFolderModel(TestCase):
    def test_raises_if_spaces_in_aliases(self):
            with self.assertRaises(AliasesContainSpaces):
                VideoFolderFactory(aliases='test testy')

    def test_raises_if_invalid_path(self):
        with patch('apps.video_player.models.os.path.isdir', return_value=False):
            with self.assertRaises(InvalidPath):
                VideoFolderFactory()

    def test_creates_videos(self):
        with patch('apps.video_player.models.os.path.isdir', return_value=True):
            with patch('apps.video_player.models.os.listdir', return_value=['test.avi', 'readme.txt', 'test2.mp4']):
                folder = VideoFolderFactory()
                videos = Video.objects.filter(folder=folder)
                assert videos.count() == 2
                assert videos.filter(last_played=None).count() == 2
                assert set(v.file_name for v in videos) == set(['test.avi', 'test2.mp4'])

    def test_gets_next_video(self):
        with patch('apps.video_player.models.os.path.isdir', return_value=True):
            with patch('apps.video_player.models.os.listdir', return_value=['video.avi']):
                correctFolder = VideoFolderFactory(aliases='hello,other', priority=50)
                VideoFolderFactory(aliases='hello,word', priority=20)
                VideoFolderFactory(aliases='nope', priority=100)

        result = VideoFolder.get_next_video_matching_query('hello')
        assert result.folder == correctFolder


class TestVideoModel(TestCase):
    def test_is_video_file(self):
        assert Video.is_video_file("test.mp4")
        assert Video.is_video_file("test.MP4")
        assert Video.is_video_file("test.avi")
        assert not Video.is_video_file("test.txt")
        assert not Video.is_video_file("testavi")

    def test_play_sets_datetime(self):
        with patch('apps.video_player.models.os.path.isdir', return_value=True):
            with patch('apps.video_player.models.os.listdir', return_value=['video.avi']):
                VideoFolderFactory()
        video = Video.objects.get()
        assert not video.last_played
        with patch('apps.video_player.models.Messenger'):
            video.play()
        assert video.last_played

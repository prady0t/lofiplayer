import sys
from types import SimpleNamespace


def _fake_yt_dlp_module(info):
    class FakeYDL:
        def __init__(self, opts):
            self.opts = opts

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            return False

        def extract_info(self, url, download=False):
            return info

    return SimpleNamespace(YoutubeDL=FakeYDL)


def test_resolve_urls_returns_single_video_url(monkeypatch):
    sys.modules["yt_dlp"] = _fake_yt_dlp_module({"url": "https://cdn.example/video.mp4"})
    from lofiplayer.player.yt import resolve_urls

    assert resolve_urls("https://youtu.be/example") == ["https://cdn.example/video.mp4"]


def test_resolve_urls_returns_playlist_urls(monkeypatch):
    sys.modules["yt_dlp"] = _fake_yt_dlp_module(
        {"entries": [{"url": "https://cdn.example/1.mp4"}, {"url": "https://cdn.example/2.mp4"}]}
    )
    from lofiplayer.player.yt import resolve_urls

    assert resolve_urls("https://www.youtube.com/playlist?list=example") == [
        "https://cdn.example/1.mp4",
        "https://cdn.example/2.mp4",
    ]

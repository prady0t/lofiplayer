import yt_dlp


def resolve_urls(url):
    ydl_opts = {
        "format": "best",
        "quiet": True,
        "no_warnings": True,
        "ignoreerrors": True,
    }

    urls = []

    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info = ydl.extract_info(url, download=False)

        # Playlist
        if info and "entries" in info:
            for entry in info["entries"]:
                if entry is None:
                    continue

                stream_url = entry.get("url")
                if stream_url:
                    urls.append(stream_url)

            return urls

        # Single video
        if info and info.get("url"):
            return [info["url"]]

    return []
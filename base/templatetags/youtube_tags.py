# base/templatetags/youtube_tags.py
from django import template
import re
from urllib.parse import urlparse, parse_qs

register = template.Library()

@register.filter
def youtube_embed2(url):
    """
    Convert a YouTube URL into an embeddable iframe URL.
    Example:
      Input: https://www.youtube.com/watch?v=dQw4w9WgXcQ
      Output: https://www.youtube.com/embed/dQw4w9WgXcQ
    """
    if not url:
        return ""

    video_id = None
    parsed_url = urlparse(url)

    # Case 1: Standard YouTube watch link
    if parsed_url.hostname in ["www.youtube.com", "youtube.com"]:
        query = parse_qs(parsed_url.query)
        video_id = query.get("v", [None])[0]

    # Case 2: Short youtu.be link
    elif parsed_url.hostname == "youtu.be":
        video_id = parsed_url.path.lstrip("/")

    # Case 3: Embed link already
    elif "embed" in parsed_url.path:
        return url

    if video_id:
        return f"https://www.youtube.com/embed/{video_id}"

    return url  # fallback


YOUTUBE_REGEX = re.compile(
        r'(?P<url>(https?://)?((www\.)|(m\.))?(youtube\.com/watch\?v=|youtu\.be/)(?P<id>[\w-]{11})([^\S]*\b))'
        )

def youtube_embed(match):
    #YOUTUBE_REGEX.sub(embed_youtube, content)
    video_id = match.group("id")
    embed_url = f"https://www.youtube.com/embed/{video_id}"
    return embed_url

@register.filter(name='embed_youtube')
def embed_youtube_filter(value):
    if not value:
        return ''
    content = YOUTUBE_REGEX.sub(youtube_embed, value)
    return content

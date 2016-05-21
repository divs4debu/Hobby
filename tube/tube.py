"""
Download youtube clips.
"""
import sys
from io import StringIO
from six.moves import input  # pylint: disable=redefined-builtin
from pytube import YouTube
from lxml import html
import requests


def fetch_url_content(url):
    """
    Fetch the URL html content.

    :param url: URL that you are getting the content from.
    :type url: :class:`str`
    :raises requests.HTTPError: Raised if there was a problem getting the
        content of the provided url.
    :returns: HTML content for the given url.
    :rtype: :class:`file`
    """
    response = requests.get(url)
    response.raise_for_status()
    return StringIO(response.text)


def fetch_video_links(content, base_url=None, class_name="yt-uix-sessionlink"):
    """
    Fetch all the links from the html content provided.

    :param content: Fetch all the links from the URL content. Content
        can be any object that support `file` like operations.
    :type content: :class:`file`
    :param base_url: Resolve all links to the base url. If omitted then this
        step will be skipped.
    :type base_url: :class:`str` or :obj:`None`
    :param class_name: Extract all links that have a the given class name.
    :type class_name: :class:`str`
    :returns: All the links extracted from the url content.
    :rtype: iterable of :class:`str`
    """
    links = set()
    parsed = html.parse(content)
    root = parsed.getroot()

    if base_url is not None:
        root.make_links_absolute(base_url)

    for element in root.find_class(class_name):
        for elem, _, link, _ in element.iterlinks():
            # skip over images and etc..
            if elem.tag == "a":
                links.add(link)

    return links


def fetch_video_qualtiy(url):
    """
    Fetch a list of available video qualities.

    :param url: Url to fetch available video options.
    :type url: :class:`str`
    :returns: Iterable of available video options.
    :rtype: Iterable of :class:`str`
    """
    youtube = YouTube(url)
    for element in youtube.get_videos():
        yield element


def user_select(options):
    """
    Prompt the user for the video quality they desire.

    :param options: List of available options.
    :type options: :class:`str`
    :returns: The selected video quality.
    :rtype: :class:`int`
    """
    for count, element in enumerate(options, 1):
        sys.stdout.write("{}. {}\n".format(count, element))

    selected = None
    while selected is None or selected > len(options):
        try:
            selected = int(input('select one of the above: '))
        except Exception:  # pylint: disable=broad-except
            continue
    return selected


def run():
    """
    Test runner
    """
    base_url = "http://www.youtube.com"
    url = base_url + '/watch?v=Ik-RsDGPI5Y'

    content = fetch_url_content(url)
    links = fetch_video_links(content, base_url)

    qual = list(fetch_video_qualtiy(links))
    selected = user_select(qual)
    sys.stdout.write("{}".format(selected))
    # import re
    # print(str(qual[0]))
    # value = re.search("(- \d{4,4}[p] -)",str( qual[4]))
    # print(str(qual[4])[value.span()[0]+2:value.span()[1]-2])

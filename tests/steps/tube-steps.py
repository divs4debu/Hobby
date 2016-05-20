from assertpy import assert_that
from behave import given, then, when
from tube import tube
import requests_mock
from requests import RequestException
from StringIO import StringIO
import mock


@when("we fetch the content from a url with status code 200")
def fetch_content(context):
    context.html = """
     <html>
        <a href='watch?v=cdMEMGLr9xE'></a>
     </html>
    """
    context.url = "mock://www.youtube.com/watch?v=Ik-RsDGPI5Y"
    with requests_mock.Mocker() as mock_response:
        mock_response.get(context.url, text=context.html)
        context.html_content = tube.fetch_url_content(context.url)


@when("we fetch the content from a url with status code 404")
def fetch_content(context):
    context.url = "mock://www.youtube.com/watch?SayWhat"
    with requests_mock.Mocker() as mock_response:
        mock_response.get(context.url, status_code=404)
        try:
            context.html_content = tube.fetch_url_content(context.url)
        except Exception as err:
            context.html_content = err


@then("we return the html content in a file type object")
def check_fetch_content_return(context):
    assert_that(hasattr(context.html_content, "read")).is_true()
    assert_that(context.html_content.read()).is_equal_to(context.html)


@then("we raise an HTTPError")
def check_fetch_content_return(context):
    assert_that(context.html_content).is_instance_of(RequestException)


@given("we have a file like object with the content")
def make_a_content_file_obj(context):
    context.html_content = StringIO(context.text)


@when("we extract the links using http://www.youtube.com as the base url")
def extract_links(context):
    base_url = "http://www.youtube.com"
    context.links = tube.fetch_video_links(context.html_content, base_url)


@then("we will have a set with 1 absolute link")
def check_fetch_link_results(context):
    assert_that(context.links).is_length(1)


@then("the link will be http://www.youtube.com/watch?v=gaSyeDxBlug")
def check_fetch_link_results(context):
    assert_that(context.links.pop()).is_equal_to(
        "http://www.youtube.com/watch?v=gaSyeDxBlug"
    )

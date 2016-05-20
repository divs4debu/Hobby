Feature: Download youtube clips

        @valid
        Scenario: Get content from a valid url
            When we fetch the content from a url with status code 200
            Then we return the html content in a file type object

        @invalid
        Scenario: Get content from a invalid url
            When we fetch the content from a url with status code 404
            Then we raise an HTTPError

        @links
        Scenario: Get all the links from HTML content
        Given we have a file like object with the content
        """
        <html>
          <li class="watch-meta-item yt-uix-expander-body">
            <h4 class="title">Movie</h4>
            <ul class="content watch-info-tag-list">
              <li>
                <a href="/watch?v=gaSyeDxBlug" class="yt-uix-sessionlink spf-link " data-sessionlink="ei=6Oo-V8vFJcXt4QLT7oXgBg&amp;feature=s2l" >Pulp fiction</a>
              </li>
            </ul>
          </li>
        </html>
        """
        When we extract the links using http://www.youtube.com as the base url
        Then we will have a set with 1 absolute link
        And the link will be http://www.youtube.com/watch?v=gaSyeDxBlug

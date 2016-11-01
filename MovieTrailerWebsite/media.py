import webbrowser
class Movie(object):
    """Class that contains info about a movie, including title,storyline,poster and trailer"""
    def __init__(self, movie_title,movie_storyline,poster_image,trailer_youtube):
        self.title=movie_title
        self.storyline=movie_storyline
        self.poster_image_url=poster_image
        self.trailer_youtube_url=trailer_youtube
    #Opens the default webbrowser and plays the movie trailer
    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)


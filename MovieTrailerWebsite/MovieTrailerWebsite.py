import media
import fresh_tomatoes
#Ceate several movie objects and pass them as list to the fresh_tomatoes.open_movies_page, 
#which constructs a movie website displaying the movie object
toy_story=media.Movie("Toy Story",
                      "Story aout a boy",
                      "http://upload.wikimedia.org/wikipedia/en/1/13/Toy_Story.jpg",
                      "https://www.youtube.com/watch?v=vwyZH85NQC4")
children_of_men=media.Movie("Children of men",
                            "Women stop to have babies,in a dystopian, not so distant future",
                            "http://cdn1.ssninsider.com/wp-content/uploads/2013/04/Children-of-Men-Poster.jpg",
                            "https://www.youtube.com/watch?v=2VT2apoX90o")
apocalypse_now=media.Movie("Apocalypse Now",
                           "Dystopian road-trip through the Vietnam war",
                           "http://www.oscars.org/sites/oscars/files/movie_poster.jpg",
                           "https://www.youtube.com/watch?v=snDR7XsSkB4")
das_boot=media.Movie("Das Boot", 
                     "The adventures of a submarine crew in WWII",
                     "http://img.goldposter.com/2015/04/Das-Boot_poster_goldposter_com_7.jpg",
                     "https://www.youtube.com/watch?v=FRKXemPhtYI")
spinal_tap=media.Movie("This is Spinal Tap",
                       "Mockumentary about a stereotypical metal band",
                       "https://www.movieposter.com/posters/archive/main/152/MPW-76100",
                       "https://www.youtube.com/watch?v=N63XSUpe-0o")
paradise_lost=media.Movie("Paradies Lost",
                          "Disturbing documentary about a triple infanticide and a subsequent miscarriage of justice",
                          "http://posting.arktimes.com/images/blogimages/2013/03/14/1363289932-paradiselost_poster.jpg",
                          "https://www.youtube.com/watch?v=_QkUJtt61ps")
movies=[toy_story,children_of_men,apocalypse_now,das_boot,spinal_tap,paradise_lost]
fresh_tomatoes.open_movies_page(movies)

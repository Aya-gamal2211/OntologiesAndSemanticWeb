from rdflib import Graph, URIRef

gr = Graph()
gr.parse("F:/PythonProjects/OntologiesPart3/mm.ttl", format="ttl")

print(f"Graph has {len(gr)} statements.")

def get_actors(g):
    query1 = """
    SELECT ?actor WHERE {
    ?actor a :Actor.
    }
    """

    # Execute the first query
    print("Movies and their genres:")
    myList = []
    for row in g.query(query1):
        # Extracting the local name from the URIs
        my_actor = row.actor.split('#')[-1]  # Split the URI by '#' and take the last part
        print(f"Actor: {my_actor}")
        myList.append(my_actor)
    return myList

def writers():
    query3 = """
        SELECT ?writer WHERE {
        ?writer a :Writer.
        }
        """
    print("Wrtiers of movies")
    for row in g.query(query3):
        my_writer = row.writer.split("#")[-1]
        print(f"Writer: {my_writer}")

def get_directors(g):
    query="""
    SELECT ?director WHERE {
      ?director a :Director.
    }
    """
    print("Directors of movies")
    myList = []
    for row in g.query(query):
        my_director = row.director.split("#")[-1]
        print(f"Director: {my_director}")
        myList.append(my_director)
    return myList

def get_genres(g):
    query="""
    SELECT ?genre WHERE {
      ?genre a :Genre
    }
    """
    print("Genres Available")
    myList = []
    for row in g.query(query):
        my_genre = row.genre.split("#")[-1]
        print(f"Genre: {my_genre}")
        myList.append(my_genre)
    return myList

def ThrillerMoviesDirectors():
    query="""
    SELECT ?movie ?director WHERE {
      ?movie a :Movie;
            :hasGenre :Thriller;
            :hasDirector ?director.
    }
    """
    print("Thriller Movies and Thier directors")
    for row in g.query(query):
        my_movie = row.movie.split("#")[-1]
        my_director = row.director.split("#")[-1]
        print(f"Movie: {my_movie}",f"Director: {my_director}")

def crime_thriller_movies():
    query = """
    SELECT ?movie WHERE {
      ?movie a :Movie;
             :hasGenre :Crime, :Thriller.
    }
    """
    print("Crime and Thriller Movies:")
    for row in g.query(query):
        movie_name = row.movie.split('#')[-1]
        print(f"Movie: {movie_name}")

def male_actors_of_movie(movie_uri):    
    query = f"""
    SELECT ?actor WHERE {{
      :{movie_uri} a :Movie;
             :hasActor ?actor.
      ?actor :Gender "Male".
    }}
      """  
    print(f"Male actors of the movie {movie_uri}:")
    for row in g.query(query):
        actor_name = row.actor.split('#')[-1] if '#' in row.actor else row.actor.split('/')[-1]
        print(f"Actor: {actor_name}")

def count_action_thriller_movies():
    # This query assumes that a movie can have multiple genres and counts movies that include both genres.
    query = """
    SELECT (COUNT(DISTINCT ?movie) as ?movieCount) WHERE {
      ?movie a :Movie.
      ?movie :hasGenre :Action.
      ?movie :hasGenre :Thriller.
    }
    """
    result = g.query(query)
    # Access the count from the query results
    for row in result:
        # The count result can be accessed using row.movieCount in RDFlib
        print("Count of Action and Thriller Movies:", row.movieCount)

def movies_by_writer(writer_uri):
    query = f"""
    SELECT ?movie WHERE {{
      ?movie a :Movie;
             :hasWriter :{writer_uri}.
    }}
    """
    print(f"Movies written by {writer_uri.split('#')[-1]}:")
    for row in g.query(query):
        movie_name = row.movie.split('#')[-1]
        print(f"Movie: {movie_name}")

def movies_by_language(language):
    query = f"""
    SELECT ?movie WHERE {{
      ?movie a :Movie;
             :Language "{language}".
    }}
    """
    print(f"Movies in {language}:")
    for row in g.query(query):
        movie_name = row.movie.split('#')[-1]
        print(f"Movie: {movie_name}")

def actors_by_age(min_age):
    query = f"""
    SELECT ?actor WHERE {{
      ?actor a :Actor;
             :Age ?age.
      FILTER(?age > {min_age})
    }}
    """
    print(f"Actors older than {min_age} years:")
    for row in g.query(query):
        actor_name = row.actor.split('#')[-1]
        print(f"Actor: {actor_name}")

def actors_and_their_movies():
    query = """
    SELECT ?actor ?movie WHERE {
      ?movie a :Movie;
             :hasActor ?actor.
      ?actor a :Actor.
    }
    """
    print("Actors and their movies:")
    for row in g.query(query):
        actor_name = row.actor.split('#')[-1]
        movie_name = row.movie.split('#')[-1]
        print(f"Actor: {actor_name}, Movie: {movie_name}")

def count_movies_by_directors():
    query = """
    SELECT ?director (COUNT(?movie) as ?numberOfMovies) WHERE {
      ?movie a :Movie;
              :hasDirector ?director.
      ?director a :Director;
    } GROUP BY ?director
    """
    print("Number of movies directed by each director:")
    for row in g.query(query):
        director_name = row.director.split('#')[-1]
        print(f"Director: {director_name}, Number of Movies: {row.numberOfMovies}")

def directors_who_act_and_direct():
    query = """
    SELECT ?movie ?director WHERE {
      ?movie a :Movie;
              :hasDirector ?director.
      ?director a :Director.
      ?director a :Actor.
    }
    """
    print("Movies directed and acted in by the same director:")
    for row in g.query(query):
        director_name = row.director.split('#')[-1]
        movie_name = row.movie.split('#')[-1]
        print(f"Director: {director_name}, Movie: {movie_name}")

def directors_who_never_acted():
    query = """
    SELECT ?director WHERE {
      ?director a :Director.
      FILTER NOT EXISTS {
        ?movie :hasActor ?director.
      }
    }
    """
    print("Directors who have never acted in any movie:")
    for row in g.query(query):
        director_name = row.director.split('#')[-1]
        print(f"Director: {director_name}")

def actors_in_drama():
    query = """
    SELECT DISTINCT ?actor WHERE {
      ?movie a :Movie;
            :hasActor ?actor.
      ?actor a :Actor.
      ?movie :hasGenre :Drama.
    }
    """
    print("Actors who have acted in Drama movies:")
    for row in g.query(query):
        actor_name = row.actor.split('#')[-1]  # Assuming URI ends with '#'
        print(f"Actor: {actor_name}")

def query_movies_with_optional_info():

    query = """
    SELECT ?movie ?director ?writer WHERE {
      ?movie a :Movie.
      OPTIONAL {
        ?movie :hasDirector ?director.
        ?director a :Director.
      }
      OPTIONAL {
        ?movie :hasWriter ?writer.
        ?writer a :Writer.
      }
    }
    """
    print("Movies with their optional director and writer info:")
    for row in g.query(query):
        movie_name = row.movie.split('#')[-1] if '#' in row.movie else row.movie.split('/')[-1]
        director_name = row.director.split('#')[-1] if row.director is not None else "No director"
        writer_name = row.writer.split('#')[-1] if row.writer is not None else "No writer"
        print(f"Movie: {movie_name}, Director: {director_name}, Writer: {writer_name}")

def query_people_by_roles_and_genres():
    query = """
    SELECT ?person ?role ?genre WHERE {
      {
        ?movie a :Movie;
                :hasDirected ?person.
        ?person a :Director;
                :hasDirected ?movie.
        BIND("Director" AS ?role).
      } UNION {
        ?movie a :Movie;
                :hasActor ?person.
        BIND("Writer" AS ?role).
      }
      ?movie :hasGenre ?genre.
      FILTER(?genre IN (:Thriller, :Drama))
    }
    """
    print("People and their roles in Thriller or Drama movies:")
    for row in g.query(query):
        person_name = row.person.split('#')[-1] if '#' in row.person else row.person.split('/')[-1]
        role = row.role
        genre = row.genre.split('#')[-1] if '#' in row.genre else row.genre.split('/')[-1]
        print(f"Person: {person_name}, Role: {role}, Genre: {genre}")

def construct_roles_graph():
    query = """
    SELECT ?person ?movie ?role WHERE {
      {
        ?movie :hasDirector ?person.
        ?person a :Director.
        BIND("Director" AS ?role).
      } UNION {
        ?movie :hasWriter ?person.
        ?person a :Writer.
        BIND("Writer" AS ?role).
      } UNION {
        ?movie :hasActor ?person.
        ?person a :Actor.
        BIND("Actor" AS ?role).
      }
    }
    """
    # Execute the query
    print("People and their roles in movies:")
    for row in g.query(query):
        person_name = row.person.split('#')[-1] if '#' in row.person else row.person.split('/')[-1]
        movie_name = row.movie.split('#')[-1] if '#' in row.movie else row.movie.split('/')[-1]
        role = row.role
        print(f"Person: {person_name}, Movie: {movie_name}, Role: {role}")

def check_for_thriller_with_female_director():
    query = """
    ASK {
      ?movie a :Movie;
             :hasGenre :Thriller;
             :hasDirector ?director.
      ?director a :Director;
                :gender :Female.
    }
    """
    # Execute the ASK query
    result = g.query(query)
    
    # Result is a boolean, so we check if it's True or False
    if result:
        print("Yes, there is at least one thriller movie directed by a female director.")
    else:
        print("No, there are no thriller movies directed by a female director.")

def describe_movie(title):
    # Properly formatted SPARQL query with title as a string literal
    query = f"""
    DESCRIBE ?movie
    WHERE {{
      ?movie a :Movie;
             :Name "{title}".
    }}
    """
    # Execute the DESCRIBE query
    described_graph = g.query(query).graph
    
    # Output the results, extracting local names after '#'
    print(f"Description of the movie '{title}':")
    for s, p, o in described_graph:
        subject_local = s.split('#')[-1] if '#' in str(s) else str(s)
        predicate_local = p.split('#')[-1] if '#' in str(p) else str(p)
        object_local = o.split('#')[-1] if isinstance(o, URIRef) and '#' in str(o) else str(o)
        print(f"Subject: {subject_local}, Predicate: {predicate_local}, Object: {object_local}")

def list_movies_with_multiple_genres(g):
    query = """
    SELECT ?movie (COUNT(?genre) AS ?genresCount) WHERE {
      ?movie a :Movie;
             :hasGenre ?genre.
    } GROUP BY ?movie
      HAVING(COUNT(?genre) >= 3)
    """
    # Execute the query
    results = g.query(query)
    
    # Output the results
    print("Movies with at least three different genres:")
    for row in results:
        movie_uri = row.movie
        movie_name = movie_uri.split('#')[-1] if '#' in str(movie_uri) else str(movie_uri)
        genres_count = row.genresCount
        print(f"Movie: {movie_name}, Genres Count: {genres_count}")

def list_movies_by_director_actors(g):
    query = """
    SELECT DISTINCT ?movie WHERE {
      ?movie a :Movie;
             :hasDirector ?director.
      ?director a :Director.
      ?director a :Actor.
    }
    """
    # Execute the query
    try:
        results = g.query(query)
        # Output the results
        print("Movies directed by directors who also acted in movies:")
        for row in results:
            movie_uri = row.movie
            movie_name = movie_uri.split('#')[-1] if '#' in str(movie_uri) else str(movie_uri)
            print(f"Movie: {movie_name}")
    except Exception as e:
        print(f"An error occurred: {e}")

def find_actors_in_multiple_genres(g):
    query = """
    SELECT ?actor ?movie ?genre WHERE {
      ?movie a :Movie;
              :hasActor ?actor.
      ?actor a :Actor;
             :Age ?age.
      ?movie :hasGenre ?genre.
      FILTER(?age > 50)
    }
    """
    # Execute the query
    results = g.query(query)
    
    # Process the results to count distinct genres per actor
    from collections import defaultdict
    actor_genres = defaultdict(set)  # Use a set to keep genres unique
    
    for row in results:
        actor_uri = row.actor
        genre = row.genre
        actor_genres[actor_uri].add(genre)

    # Output actors who have acted in at least two different genres
    print("Actors over 50 who have acted in at least two different genres:")
    for actor, genres in actor_genres.items():
        if len(genres) >= 2:
            actor_name = actor.split('#')[-1] if '#' in str(actor) else str(actor)
            print(f"Actor: {actor_name}, Genres Count: {len(genres)}")


def list_movies_with_triple_roles(g):
    query = """
    SELECT ?movie WHERE {
      ?movie a :Movie;
             :hasActor ?person;
             :hasDirector ?person;
             :hasWriter ?person.
      ?person a :Person.
    }
    """
    # Execute the query
    results = g.query(query)
    
    # Output the results
    print("Movies where the same person is an actor, director, and writer:")
    for row in results:
        movie_uri = row.movie
        movie_name = movie_uri.split('#')[-1] if '#' in str(movie_uri) else str(movie_uri)
        print(f"Movie: {movie_name}")

def list_directors_with_no_thriller_movies(g):
    query = """
    SELECT DISTINCT ?director WHERE {
      ?director a :Director.
      FILTER NOT EXISTS {
        ?movie a :Movie;
                :hasDirector ?director;
                :hasGenre :Thriller.
      }
    }
    """
    # Execute the query
    results = g.query(query)
    
    # Output the results
    print("Directors who have never directed a Thriller movie:")
    for row in results:
        director_uri = row.director
        director_name = director_uri.split('#')[-1] if '#' in str(director_uri) else str(director_uri)
        print(f"Director: {director_name}")


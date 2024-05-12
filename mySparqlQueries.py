from rdflib import Graph, URIRef


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

def get_writers(g):
    query3 = """
        SELECT ?writer WHERE {
        ?writer a :Writer.
        }
        """
    print("Wrtiers of movies")
    myList = []
    for row in g.query(query3):
        my_writer = row.writer.split("#")[-1]
        print(f"Writer: {my_writer}")
        myList.append(my_writer)
    return myList

def get_general(g, actors=None, directors=None, genres=None):
    conditions = []
    
    if actors:
        actor_placeholders = ', '.join(f':{actor}' for actor in actors)
        conditions.append(f"?movie :hasActor {actor_placeholders}")

    if directors:
        director_placeholders = ', '.join(f':{director}' for director in directors)
        conditions.append(f"?movie :hasDirector {director_placeholders}")

    if genres:
        genre_placeholders = ', '.join(f':{genre}' for genre in genres)
        conditions.append(f"?movie :hasGenre {genre_placeholders}")

    combined_conditions = " .\n".join(conditions)
    
    query = f"""
        SELECT DISTINCT ?movie WHERE {{
            ?movie a :Movie.
            {combined_conditions}
        }}
    """
    print("Querying for specific movie characteristics:")
    myList = []
    try:
        for row in g.query(query):
            my_movie = row.movie.split("#")[-1]
            print(f"Movie: {my_movie}")
            myList.append(my_movie)
    except Exception as e:
        print(f"An error occurred: {e}")
    return myList

if __name__ == "__main__":
    gr = Graph()
    gr.parse("F:/PythonProjects/OntologiesPart3/mm.ttl", format="ttl")
    movies = get_general(gr, actors=["Tom_Hanks"],directors=["Robert_Zemeckis"], genres=["Comedy"])
    print(movies)
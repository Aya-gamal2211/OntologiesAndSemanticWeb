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

def get_general(g, writers):
    # Use map to handle escaping quotes outside of the f-string
    placeholder = ', '.join(writers)
    print(placeholder)
    query = f"""
        SELECT ?movie WHERE {{
            ?movie a :Movie.
            ?movie :hasActor ?actor.
            ?actor a :Tom_Hanks.
        }}
    """
    print("Querying for specific writers:")
    myList = []
    try:
        for row in g.query(query):
            my_writer = row.movie.split("#")[-1]
            print(f"movie: {my_writer}")
            myList.append(my_writer)
    except Exception as e:
        print(f"An error occurred: {e}")
    return myList



gr = Graph()
gr.parse("F:/PythonProjects/OntologiesPart3/mm.ttl", format="ttl")

print(f"Graph has {len(gr)} statements.")
get_actors(gr)
get_general(gr, ["David_Stassen", "Ike_Barinholtz"])
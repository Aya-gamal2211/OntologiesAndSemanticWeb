

@app.route("/jena5", methods=["GET"])
def jena5():

    global graph

    # Load the OWL rule file
    rule_file = "rdf/rules.ttl"
    rule_graph = Graph()
    rule_graph.parse(rule_file, format="ttl")

    # Print the content of the rule graph before merging
    print("Rule Graph Content Before Merging:")
    print(rule_graph.serialize(format="turtle"))

    # Merge the rule graph with the main graph
    graph = graph + rule_graph

    # Apply OWL reasoning
    owlrl.OWLRL_Semantics(graph, axioms=True, daxioms=True)
    DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    # Query to find individuals who are both actors and directors
    query = """
    PREFIX : <http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/>
    SELECT DISTINCT ?person_name
    WHERE {
        ?person rdf:type :ActorDirector ;
                rdfs:label ?person_name .
    }
    """
    try:
        results = graph.query(query)
    except Exception as e:
        flash("Could not run that query.")
        flash("RDFLIB Error: {}".format(e))
        sparql_validate(query)
        return jena5()
    return show_result(results=results, template="jena5.html")


@app.route("/jena6_1", methods=["GET"])
def jena6_1():
    owlrl.OWLRL_Semantics(graph,axioms=True, daxioms=True)
    onto = rdflib.Namespace("http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/")

    # Rule 1: ActorDirector
    graph.add((onto.ActorDirector, RDF.type, OWL.Class))
    graph.add((onto.ActorDirector, RDFS.subClassOf, onto.Person))

    # Create a blank node for intersection and ensure the intersection is properly constructed
    intersection = rdflib.BNode()
    list_actor = rdflib.BNode()
    list_director = rdflib.BNode()

    graph.add((intersection, RDF.type, OWL.Class))
    graph.add((intersection, OWL.intersectionOf, list_actor))
    graph.add((list_actor, RDF.first, onto.Actor))
    graph.add((list_actor, RDF.rest, list_director))
    graph.add((list_director, RDF.first, onto.Director))
    graph.add((list_director, RDF.rest, RDF.nil))

    graph.add((onto.ActorDirector, OWL.equivalentClass, intersection))

    # Apply reasoning
    owlrl.DeductiveClosure(owlrl.OWLRL_Semantics, datatype_axioms=False).expand(graph)

    query = """prefix : <http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/>  
SELECT ?person_name 
WHERE { 
  ?person rdf:type :ActorDirector. 
  ?person rdfs:label ?person_name. 
} """
    return run_query(query=query, template="jena6_1.html")

@app.route("/jena6_2", methods=["GET"])
def jena6_2():
    owlrl.OWLRL_Semantics(graph,axioms=True, daxioms=True)
    onto = rdflib.Namespace("http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/")

    #Rule 2: MultiGenreMovies
    graph.add((onto.hasMultipleGenres, RDF.type, OWL.DatatypeProperty))
    graph.add((onto.MultiGenreMovies, RDF.type, OWL.Class))
    graph.add((onto.MultiGenreMovies, RDFS.subClassOf, onto.Movie))
    graph.add((onto.MultiGenreMovies, OWL.equivalentClass, rdflib.BNode()))
    graph.add((onto.MultiGenreMovies, RDF.type, OWL.Restriction))
    graph.add((onto.MultiGenreMovies, OWL.onProperty, onto.hasMultipleGenres))
    graph.add((onto.MultiGenreMovies, OWL.hasValue, rdflib.Literal(True)))

        # Preprocess and mark multi-genre movies
    for movie in graph.subjects(RDF.type, onto.Movie):
        genres = set(graph.objects(movie, onto.hasGenre))
        if len(genres) > 1:
            graph.add((movie, onto.hasMultipleGenres, rdflib.Literal(True)))

    DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    query = """prefix : <http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/>  
SELECT ?movie_name 
WHERE { 
  ?movie rdf:type :MultiGenreMovies. 
  ?movie rdfs:label ?movie_name. 
} """
    return run_query(query=query, template="jena6_2.html")

@app.route("/jena6_3", methods=["GET"])
def jena6_3():
    owlrl.OWLRL_Semantics(graph,axioms=True, daxioms=True)
    onto = rdflib.Namespace("http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/")

    #Rule 3: Old Movies
    graph.add((onto.isOld, RDF.type, OWL.DatatypeProperty))
    graph.add((onto.OldMovies, RDF.type, OWL.Class))
    graph.add((onto.OldMovies, RDFS.subClassOf, onto.Movie))
    graph.add((onto.OldMovies, OWL.equivalentClass, rdflib.BNode()))
    graph.add((onto.OldMovies, RDF.type, OWL.Restriction))
    graph.add((onto.OldMovies, OWL.onProperty, onto.isOld))
    graph.add((onto.OldMovies, OWL.hasValue, rdflib.Literal(True)))

    # Process each movie and check its release year
    for movie in graph.subjects(RDF.type, onto.Movie):
        release_year = graph.value(movie, onto.Year)
        if release_year and int(release_year) < 2000:
            graph.add((movie, onto.isOld, rdflib.Literal(True)))
        else:
            graph.add((movie, onto.isOld, rdflib.Literal(False)))

    DeductiveClosure(owlrl.OWLRL_Semantics).expand(graph)

    query = """prefix : <http://www.semanticweb.org/adham/ontologies/2024/4/untitled-ontology-6/>  
SELECT ?movie_name 
WHERE { 
  ?movie rdf:type :OldMovies. 
  ?movie rdfs:label ?movie_name. 
} """
    return run_query(query=query, template="jena6_3.html")

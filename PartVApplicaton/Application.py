import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from rdflib import Graph, URIRef
from SparqlQueries.mySparqlQueries import get_actors, get_directors, get_genres, get_general, get_writers

# Sample hierarchical data for the tree view
hierarchy = {
    'Actors': [
        # 'Leonardo DiCaprio', 'Tom Hardy', 'Christian Bale', 'Heath Ledger', 'John Travolta', 'Samuel L. Jackson'
    ],
    'Directors': [
        # 'Christopher Nolan', 'Quentin Tarantino'
    ],
    'Genres': [
        # 'Sci-Fi', 'Action', 'Crime'
    ],
    'Writers': []
}


def filter_films():
    include_actors = selected_films['Actors']
    include_directors = selected_films['Directors']
    include_genres = selected_films['Genres']
    include_writers = selected_films['Writers']

    movies = get_general(graph, include_actors, include_directors, include_writers, include_genres)
    update_listbox(result_display, movies)
    print(f"movies : {movies}")


# Dictionary to store selected films by genre
selected_films = {key: [] for key in hierarchy}


def populate_tree(tree, node, children):
    if isinstance(children, list):
        for child in children:
            tree.insert(node, 'end', text=child)
    elif isinstance(children, dict):
        for key, value in children.items():
            sub_node = tree.insert(node, 'end', text=key)
            populate_tree(tree, sub_node, value)


def refresh_tree(tree, hierarchy):
    """ Clears the current treeview and repopulates it with updated hierarchy. """
    for i in tree.get_children():
        tree.delete(i)  # Remove all existing nodes
    root_node = tree.insert('', 'end', text="Film Genres")
    populate_tree(tree, root_node, hierarchy)


def import_films():
    filepath = filedialog.askopenfilename(filetypes=[("Turtle Files", "*.ttl")])
    g = Graph()
    g.parse(filepath, format="ttl")
    hierarchy['Actors'] = get_actors(g)
    hierarchy['Directors'] = get_directors(g)
    hierarchy['Genres'] = get_genres(g)
    hierarchy['Writers'] = get_writers(g)

    refresh_tree(tree, hierarchy)
    global graph
    graph = g


def update_listbox(listbox, items):
    listbox.delete(0, tk.END)
    for item in items:
        listbox.insert(tk.END, item)


def item_selected(event):
    tree = event.widget
    selected_item = tree.focus()
    item = tree.item(selected_item, 'text')
    parent_id = tree.parent(selected_item)
    genre = tree.item(parent_id, 'text') if parent_id else None

    # Append the film under the correct genre
    if genre != "Film Genres":
        if genre and item not in selected_films[genre]:
            selected_films[genre].append(item)
        else:
            selected_films[genre].remove(item)

    # perform a refresh to show items again
    if genre == 'Actors':
        update_listbox(actor_listbox, selected_films[genre])
    elif genre == 'Directors':
        update_listbox(director_listbox, selected_films[genre])
    elif genre == 'Genres':
        update_listbox(genre_listbox, selected_films[genre])
    elif genre == 'Writers':
        update_listbox(writers_listbox, selected_films[genre])


def create_tree_panel(parent, hierarchy):
    tree = ttk.Treeview(parent)
    root_node = tree.insert('', 'end', text="Films")
    populate_tree(tree, root_node, hierarchy)
    tree.bind('<Double-1>', item_selected)  # Bind double-click event
    tree.pack(expand=True, fill='both')
    return tree


window = tk.Tk()
window.title("Film Finder")

# Layout Configuration
left_frame = tk.Frame(window, width=200, bg='grey')
left_frame.pack(side='left', fill='y')

main_frame = tk.Frame(window)
main_frame.pack(expand=True, fill='both')

# Treeview Panel
tree = create_tree_panel(left_frame, hierarchy)


# Actor input as a Combobox
def create_scrollable_listbox(parent, items):
    frame = tk.Frame(parent)
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL)
    listbox = tk.Listbox(frame, yscrollcommand=scrollbar.set, selectmode=tk.MULTIPLE, height=5)
    scrollbar.config(command=listbox.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
    listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    for item in items:
        listbox.insert(tk.END, item)
    frame.pack(fill=tk.BOTH, expand=True)
    return listbox


# Actor
tk.Label(main_frame, text="Include Actors:").pack()
actor_listbox = create_scrollable_listbox(main_frame, selected_films['Actors'])
actor_listbox.pack()

# Director
tk.Label(main_frame, text="Include Directors:").pack()
director_listbox = create_scrollable_listbox(main_frame, selected_films['Directors'])
director_listbox.pack()

# Writers
tk.Label(main_frame, text="Include Writers:").pack()
writers_listbox = create_scrollable_listbox(main_frame, selected_films['Writers'])
writers_listbox.pack()

# Genre
tk.Label(main_frame, text="Include Genres:").pack()
genre_listbox = create_scrollable_listbox(main_frame, selected_films['Genres'])
genre_listbox.pack()

# Import button
import_button = tk.Button(main_frame, text="Import Films (.ttl)", command=lambda: import_films())
import_button.pack()

# Filter button
filter_button = tk.Button(main_frame, text="Filter Films", command=lambda: filter_films())
filter_button.pack()

# Result display
results = []
result_display = create_scrollable_listbox(main_frame, results)
result_display.pack()

# padding
tk.Label(main_frame, text="").pack()

# result_display.configure(state='disabled')
window.geometry('800x600')
window.mainloop()

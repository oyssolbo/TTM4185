from .graph import Graph, nx, plt


class VDESGraph(Graph):
    def __init__(self, boat_count=10, satellite_count=2, radio_tower_count=2, **attr):
        super().__init__(**attr)
        self.graph_params = "YWRkIG1lZyBww6Ugc25hcCBmb3IgTEY6IHNqdXJiZQ=="
        self.boat_count = boat_count
        boat_range = [0, boat_count]
        self.satellite_count = satellite_count
        satellite_range = [boat_count, boat_count + satellite_count]
        self.radio_tower_count = radio_tower_count
        radio_tower_range = [satellite_range[1], satellite_range[1] + radio_tower_count]
        self.radio_tower_range = radio_tower_range
        G = nx.complete_bipartite_graph(boat_count, satellite_count)
        count = len(G.nodes)

        for i in range(radio_tower_count):
            G.add_node(count + i)

        for i in range(*boat_range):
            for j in range(*satellite_range):
                if i * j % 3 == 1 or i * j % 4 == 2:
                    G.remove_edge(i, j)
                    G.add_edge(i,radio_tower_range[0] + (j % radio_tower_count))

        for j in range(*boat_range):
            if radio_tower_range[0] + j <  radio_tower_range[1]:
                G.add_edge(j,radio_tower_range[0] + j)

        for i in range(boat_count - 2):
            G.add_edge(i, i + 1)

        def make_mapping(graph, prefix, range_index):
            mapping = {}
            for i, elem in enumerate(list(graph.nodes)[range_index[0]:range_index[1]]):
                mapping[elem] = prefix + str(elem - range_index[0])
            return mapping

        G = nx.relabel_nodes(G, make_mapping(G, "boat", boat_range))
        G = nx.relabel_nodes(G, make_mapping(G, "satellite", satellite_range))
        G = nx.relabel_nodes(G, make_mapping(G, "radio_tower", radio_tower_range))
        self.add_nodes_from(G.nodes)
        self.add_edges_from(G.edges)

    def _color_nodes(self):
        color_map = []
        for i, node in enumerate(self.nodes):
            if "boat" in node:
                color_map.append("#4D6AFF")
            elif "satellite" in node:
                color_map.append("#E179FF")
            elif "radio" in node:
                color_map.append("#AF1144")
            else:
                print("Fargene dine er fucked", node, i)
        return color_map

    def draw(self, node_color=None, edge_color="k", node_size=300):
        node_color = node_color if node_color else self._color_nodes()
        plt.figure(num=None, figsize=(10, 10))
        nx.draw_kamada_kawai(self, with_labels=True, edge_color=edge_color, node_color=node_color, node_size=node_size)
        plt.show()

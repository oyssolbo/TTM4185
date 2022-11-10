from .graph import Graph, nx, plt


class ConstructedGraph(Graph):
    def __init__(self, expanded=False, **attr):
        super().__init__(**attr)
        grid_size = 3
        G = nx.grid_2d_graph(grid_size, grid_size)
        F = nx.cycle_graph(5)

        def create_mapping(grid_size):
            mapping = {(0, 0): "a0", (0, 2): "b0", (2, 0): "c0", (1, 2): "d0"}
            for i in range(grid_size):
                for j in range(grid_size):
                    if not (i, j) in mapping:
                        mapping[(i, j)] = "core" + str(i * 3 + j)
            return mapping

        mapping = create_mapping(grid_size)
        G = nx.relabel_nodes(G, mapping)

        def make_mapping(graph, prefix):
            mapping = {}
            for i, elem in enumerate(graph.nodes):
                mapping[elem] = prefix + str(elem)
            return mapping

        stars = "abcd"
        star_form_list = []
        for letter in stars:
            F_ = nx.relabel_nodes(F, make_mapping(F, letter))
            star_form_list.append(F_)

        access_net_size = 5
        A = nx.star_graph(access_net_size)
        access_net_list = []
        cnt = 0
        for i, letter in enumerate(stars):
            A_ = nx.relabel_nodes(A, make_mapping(A, stars[0] + letter))
            access_net_list.append(A_)

        for i, letter in enumerate(stars):
            A_ = nx.relabel_nodes(A, make_mapping(A, stars[1] + letter))
            access_net_list.append(A_)

        for i, net in enumerate(access_net_list):
            if (i < len(access_net_list) // 2):
                access_net_list[i] = nx.relabel_nodes(net, {list(net.nodes)[1]: list(net.nodes)[2][1:]})
            else:
                access_net_list[i] = nx.relabel_nodes(net, {list(net.nodes)[1]: list(net.nodes)[3][1:]})

        for graph in star_form_list:
            G = nx.compose(G, graph)

        for graph in access_net_list:
            G = nx.compose(G, graph)

        if expanded:
            # adding last part of access nett
            access_sub_net_size = 2
            A_sub = nx.star_graph(access_sub_net_size)
            access_sub_net_list = []
            cnt = 0
            for i, graph in enumerate(access_net_list):
                for j, node in enumerate(list(graph.nodes)[2:]):
                    mapping = make_mapping(A_sub, node)
                    mapping[0] = node
                    A_sub_ = nx.relabel_nodes(A_sub, mapping=mapping)
                    access_sub_net_list.append(A_sub_)

            for graph in access_sub_net_list:
                G = nx.compose(G, graph)

        self.add_nodes_from(G.nodes)
        self.add_edges_from(G.edges)

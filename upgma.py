"""
Module 3 - Part 2: UPGMA Clustering (Ancestry Tree Construction)
====================================================================
"""


class ClusterNode:
    def __init__(self, name, left=None, right=None, height=0.0):
        self.name = name
        self.left = left
        self.right = right
        self.height = height

    def is_leaf(self):
        return self.left is None and self.right is None

    def get_leaf_names(self):
        if self.is_leaf():
            return [self.name]
        return self.left.get_leaf_names() + self.right.get_leaf_names()


def upgma(names, distance_matrix):
    clusters = {name: ClusterNode(name) for name in names}
    dist = dict(distance_matrix)
    cluster_sizes = {name: 1 for name in names}
    active = list(names)
    merge_counter = 0

    while len(active) > 1:
        min_pair = None
        min_dist = float("inf")
        for i in range(len(active)):
            for j in range(i + 1, len(active)):
                a, b = active[i], active[j]
                d = dist[(a, b)]
                if d < min_dist:
                    min_dist = d
                    min_pair = (a, b)

        a, b = min_pair

        merge_counter += 1
        new_name = f"Cluster_{merge_counter}"
        new_node = ClusterNode(new_name, left=clusters[a], right=clusters[b], height=min_dist)
        clusters[new_name] = new_node

        size_a, size_b = cluster_sizes[a], cluster_sizes[b]
        cluster_sizes[new_name] = size_a + size_b

        for k in active:
            if k == a or k == b:
                continue
            d_new_k = (size_a * dist[(a, k)] + size_b * dist[(b, k)]) / (size_a + size_b)
            dist[(new_name, k)] = d_new_k
            dist[(k, new_name)] = d_new_k

        active.remove(a)
        active.remove(b)
        active.append(new_name)

    root_name = active[0]
    return clusters[root_name]


def print_tree(node, indent=""):
    if node.is_leaf():
        print(f"{indent}- {node.name}")
    else:
        print(f"{indent}Merged at distance {node.height:.2f}:")
        print_tree(node.left, indent + "    ")
        print_tree(node.right, indent + "    ")
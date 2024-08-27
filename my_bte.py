import bte
import itertools
import matplotlib.pyplot as plt
import numpy as np

tree = bte.MATree("public-2021-05-25.all.masked.pb.gz")

# Counting leaves
count = tree.count_leaves()
print(count)

def between_distance(pos1, pos2, genome_length):
    ''' distance formula'''
    distance = abs(pos2 - pos1)
    circular_distance = genome_length - distance
    return min(distance, circular_distance)

def calculate_closest_distance(mutation_tuples, genome_length):
    '''calculate the cloeset distance'''
    min_distances = []
    positions = [pos for pos, _, _ in mutation_tuples]
    for i in range(len(positions)):
        min_distance = float('inf')
        for j in range(len(positions)):
            # dont compare to itself
            if i != j:
                distance = between_distance(positions[i], positions[j], genome_length)
                if distance < min_distance:
                    min_distance = distance
        min_distances.append(min_distance)
    return min_distances

def out_tree(node, genome_length):
    '''Traverse the tree and print out tuples (position, mutation, type, distance)'''
    if node is not None and len(node.mutations) > 2:
        print("Mutations:", node.mutations)
        print('hello')
        
        mutation_list = []
        
        mutation_tuples = []

        # Extract position, mutation, and mutation type
        # Ex: A1234B, type: AB, positon: 1234
        for mutation in node.mutations:
            char1 = mutation[0]
            char2 = mutation[-1]
            mutation_type = char1 + char2
            # add mutation type to list to store for later
            mutation_type.append(mutation_type)
            
            position = int(mutation[1:-1])
            mutation_tuples.append((position, mutation, mutation_type))
        
        # Calculate closest distances
        closest_distances = calculate_closest_distance(mutation_tuples, genome_length)
        
        # Print original distances
        print("Original: ")
        for i in range(len(mutation_tuples)):
            position, mutation, mutation_type = mutation_tuples[i]
            min_distance = closest_distances[i]
            print(f"Position: {position}, Mutation: {mutation}, Type: {mutation_type}, Closest Distance: {min_distance}")
            
        # Permutations
        permutations = list(itertools.permutations(mutation_tuples))
        print("Permutations: ")
        for perm in permutations:
            print("Permutation:")
            min_distances = calculate_closest_distance(perm, genome_length)
            for i in range(len(perm)):
                position, mutation, mutation_type = perm[i]
                min_distance = min_distances[i]
                print(f"Position: {position}, Mutation: {mutation}, Type: {mutation_type}, Closest Distance: {min_distance}")
    
    # Recursive call to process child nodes
    for child in node.children:
        out_tree(child, genome_length)

def traverse(tree, genome_length):
    if tree and tree.root:
        out_tree(tree.root, genome_length)

def main():
    genome_length = count
    traverse(tree, genome_length)

if __name__ == "__main__":
    main()

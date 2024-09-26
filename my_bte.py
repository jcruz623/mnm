import bte
import random

tree = bte.MATree("public-2021-05-25.all.masked.pb.gz")

# Counting leaves
count = tree.count_leaves()
print(f"Number of leaves: {count}")

def between_distance(pos1, pos2, genome_length):
    '''Distance formula considering circular genome.'''
    distance = abs(pos2 - pos1)
    circular_distance = genome_length - distance
    return min(distance, circular_distance)

def calculate_closest_distance(mutation_tuples, genome_length):
    '''Calculate the closest distance for each mutation.'''
    min_distances = []
    positions = [pos for pos, _, _ in mutation_tuples]
    for i in range(len(positions)):
        min_distance = float('inf')
        for j in range(len(positions)):
            if i != j:
                distance = between_distance(positions[i], positions[j], genome_length)
                if distance < min_distance:
                    min_distance = distance
        min_distances.append(min_distance)
    return min_distances

def out_tree(node, genome_length):
    '''Traverse the tree and handle mutations.'''
    if node is not None and len(node.mutations) > 2:
        print(f"Node {node.id} Original Mutations:", node.mutations)

        mutation_tuples = []
        mutation_list = []

        # Extract mutation information
        for mutation in node.mutations:
            char1 = mutation[0]
            char2 = mutation[-1]
            mutation_type = char1 + char2
            position = int(mutation[1:-1])
            mutation_tuples.append((position, mutation, mutation_type))
            mutation_list.append(mutation)
        
        # Original distances
        original_distances = calculate_closest_distance(mutation_tuples, genome_length)
        print("Original Distances:")
        for i in range(len(mutation_tuples)):
            position, mutation, mutation_type = mutation_tuples[i]
            min_distance = original_distances[i]
            print(f"Position: {position}, Mutation: {mutation}, Type: {mutation_type}, Closest Distance: {min_distance}")
        
        # Collect all mutations from the entire tree
        all_mutations = []
        def collect_all_mutations(node):
            if node is not None and len(node.mutations) > 2:
                for mutation in node.mutations:
                    all_mutations.append(mutation)
            for child in node.children:
                collect_all_mutations(child)
        collect_all_mutations(tree.root)
        
        # Shuffle the entire mutation list
        random.shuffle(all_mutations)
        #print("Shuffled Mutations:", all_mutations)
        
        # Reassign mutations to branches
        branch_mutations_count = [len(node.mutations)]  # Use the original count
        branch_new_mutations = []
        
        start_index = 0
        for count in branch_mutations_count:
            branch = all_mutations[start_index:start_index + count]
            branch_new_mutations.append(branch)
            start_index += count
        
        # new mutations
        print("New Mutations for Branches:")
        for idx, branch in enumerate(branch_new_mutations):
            print(f"New Mutations:", branch)
        
        # Calculate new distances
        new_mutation_tuples = []
        for branch in branch_new_mutations:
            for mutation in branch:
                char1 = mutation[0]
                char2 = mutation[-1]
                mutation_type = char1 + char2
                position = int(mutation[1:-1])
                new_mutation_tuples.append((position, mutation, mutation_type))
        
        new_distances = calculate_closest_distance(new_mutation_tuples, genome_length)
        print("New Distances:")
        for i in range(len(new_mutation_tuples)):
            position, mutation, mutation_type = new_mutation_tuples[i]
            min_distance = new_distances[i]
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

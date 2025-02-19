import random
import time
# import matplotlib.pyplot as plt
from tests import test_cases

class AhoCorasick:
    def __init__(self):
        """
        Initialize the Aho-Corasick automaton.
        
        Data structures:
        - trie: Stores the go-to transitions between states
        - fail: Stores failure links for each state
        - output: Stores the patterns matched at each state
        """
        # Remember: Root state is always at index 0
        self.trie = [{}]
        # Failure links point to the longest suffix state
        self.fail = [0]
        # Output set for each state containing matched patterns
        self.output = [set()]

    def add_pattern(self, pattern):
        """
        Adds a pattern to the trie data structure.
        Input: The pattern to add to the automaton
        """
        node = 0
        for char in pattern:
            # If the current character transition doesn't exist, create a new state
            if char not in self.trie[node]:
                # Create a new state and add it to the trie
                self.trie[node][char] = len(self.trie)
                
                # Initialize new state's data structures
                self.trie.append({})
                self.fail.append(0)
                self.output.append(set())
            
            # Move to the next state
            node = self.trie[node][char]
        
        # Mark the end state with the full pattern
        self.output[node].add(pattern)

    def build_automaton(self):
        """
        Construct failure links for the Aho-Corasick automaton.
        
        This method builds the failure function which allows:
        1. Handling mismatches efficiently
        2. Finding all pattern matches in a single pass -> O(n+z)
        """
        # We need a queue for breadth first traversal of trie states
        queue = []
        
        # Process first-level states (direct children of root)
        for char, next_node in self.trie[0].items():
            # First-level states fail back to root
            self.fail[next_node] = 0
            queue.append(next_node)
        
        # BFS to construct failure links
        while queue:
            current = queue.pop(0)
            
            # Explore all transitions from the current state
            for char, next_node in self.trie[current].items():
                # Find the appropriate failure link
                fail_node = self.fail[current]
                
                # Traverse up failure links until a matching transition is found
                while fail_node > 0 and char not in self.trie[fail_node]:
                    fail_node = self.fail[fail_node]
                
                # Set failure link for the current transition
                self.fail[next_node] = self.trie[fail_node].get(char, 0)
                
                # Combine outputs from failure link state
                self.output[next_node].update(self.output[self.fail[next_node]])
                
                # Add to queue for further processing
                queue.append(next_node)

    def search(self, text):
        """
        Search for all patterns in the given text using the automaton.
        
        Input: The text to search for patterns
        Returns: A list of tuples (start_index, end_index, matched_pattern)
        """
        # Start at root state
        node = 0
        matches = []
        
        # Iterate thru each character in the text
        for i, char in enumerate(text):
            # Follow failure links when no matching transition exists
            while node > 0 and char not in self.trie[node]:
                node = self.fail[node]
            
            # Move to the next state with the go-to transition
            node = self.trie[node].get(char, 0)
            
            # Check for matches at the current state
            for pattern in self.output[node]:
                # Calculate the start & end index of the match
                start_index = i - len(pattern) + 1
                end_index = i
                matches.append((start_index, i, pattern))
                
        # Sort matches to ensure consistent order
        matches.sort()
        return matches

## TESTS ##
def test_correctness():
    for i, (dna_sequence, test_patterns, expected) in enumerate(test_cases):
        print(f"Test Case {i + 1}:")
        print(f"DNA Sequence: {dna_sequence}")
        print(f"Patterns: {test_patterns}")

        # Initialize Aho-Corasick automaton
        ac = AhoCorasick()
        for pattern in test_patterns:
            ac.add_pattern(pattern)
        ac.build_automaton()

        # Perform the search
        matches = ac.search(dna_sequence)

        print("Expected Matches:")
        print(expected)
        print("Actual Matches:")
        print(matches)

        assert matches == expected, f"Test Case {i + 1} failed: Expected {expected}, got {matches}"
        print("\n")

    print("All correctness test cases passed!\n")

def test_runtime():
    def generate_random_dna(length):
        return ''.join(random.choices("ACGT", k=length))

    def measure_runtime(patterns, sequence, num_trials=10):
        automaton = AhoCorasick()
        for pattern in patterns:
            automaton.add_pattern(pattern)
        automaton.build_automaton()

        total_time = 0
        for _ in range(num_trials):
            start_time = time.perf_counter()
            _ = automaton.search(sequence)
            total_time += time.perf_counter() - start_time

        return total_time / num_trials

    pattern_sets = [
        ["ATG"],
        ["ATG", "TGA"],
        ["ATG", "TGA", "CAT", "GTA", "ACT"],
        ["ATG", "TGA", "CAT", "GTA", "ACT", "GCT", "TAC", "GAG", "CCA", "TTG"]
    ]

    sequence_lengths = [100, 500, 1000, 5000, 10000, 20000]

    # Simulate and Collect Runtime Analysis Data
    runtime_data = {}
    for patterns in pattern_sets:
        runtimes = []
        for length in sequence_lengths:
            dna_sequence = generate_random_dna(length)
            runtime = measure_runtime(patterns, dna_sequence, num_trials=10)
            runtimes.append(runtime)
        runtime_data[tuple(patterns)] = runtimes

    # Output runtime results to terminal
    print("\nRun Time Analysis Results:\n")
    for patterns, runtimes in runtime_data.items():
        print(f"Patterns: {patterns}")
        for length, runtime in zip(sequence_lengths, runtimes):
            print(f"Sequence Length: {length}, Runtime: {runtime:.6f} seconds")
        print("\n")

    # Plot runtime results [This is only if you have MatPlotLib Installed]
    # plt.figure(figsize=(10, 6))
    # for patterns, runtimes in runtime_data.items():
    #     plt.plot(sequence_lengths, runtimes, marker='o', label=f'{len(patterns)} patterns')

    # plt.xlabel("Sequence Length")
    # plt.ylabel("Runtime (seconds)")
    # plt.title("Aho-Corasick Runtime vs. Sequence Length")
    # plt.legend()
    # plt.grid()
    # plt.show()  

# Run Tests
test_correctness()
test_runtime()
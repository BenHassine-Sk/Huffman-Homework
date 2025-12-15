# Exercise 1 – Character frequencies

def frequency(text):
    freqs = {}
    text = text.lower()
    for c in text:
        if c in freqs:
            freqs[c] += 1
        else:
            freqs[c] = 1
    return freqs


# Exercise 2 – Huffman tree node

class Node:
    def __init__(self, characters, frequency):
        self.characters = characters
        self.frequency = frequency
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.frequency < other.frequency


# Exercise 3 – Building the Huffman tree

from heapq import heapify, heappop, heappush

def huffman_tree(freqs):
    heap = []

    for char, freq in freqs.items():
        heap.append(Node(char, freq))

    heapify(heap)

    while len(heap) > 1:
        n1 = heappop(heap)
        n2 = heappop(heap)

        merged = Node(n1.characters + n2.characters,
                      n1.frequency + n2.frequency)
        merged.left = n1
        merged.right = n2

        heappush(heap, merged)

    return heap[0]


# Exercise 4 – Code of a single character

def get_code(tree, char):
    if char not in tree.characters:
        raise ValueError("Character not in tree")

    if tree.left is None and tree.right is None:
        return ""

    if tree.left and char in tree.left.characters:
        return "0" + get_code(tree.left, char)
    else:
        return "1" + get_code(tree.right, char)


# Exercise 5 – Listing all codes

def show_all_codes(tree):
    for char in tree.characters:
        code = get_code(tree, char)
        print("Character:", char, "Code:", code)


# Exercise 6 – Encoding and decoding

# 6.1 Encoding

def huffman_encode(text, tree):
    text = text.lower()
    encoded = ""
    for c in text:
        encoded += get_code(tree, c)
    return encoded


# 6.2 Decoding

def huffman_decode(encoded_text, tree):
    decoded = ""
    node = tree

    for bit in encoded_text:
        if bit == "0":
            node = node.left
        else:
            node = node.right

        if node.left is None and node.right is None:
            decoded += node.characters
            node = tree

    return decoded

# Exercise 7 – Universal Huffman tree

freqs_english = {
    " ": 18.0,
    "e": 12.02, "t": 9.10, "a": 8.12, "o": 7.68, "i": 7.31, "n": 6.95,
    "s": 6.28, "r": 6.02, "h": 5.92, "d": 4.32, "l": 3.98, "u": 2.88,
    "c": 2.71, "m": 2.61, "f": 2.30, "y": 2.11, "w": 2.09, "g": 2.03,
    "p": 1.82, "b": 1.49, "v": 1.11, "k": 0.69, "x": 0.17, "q": 0.11,
    "j": 0.10, "z": 0.07
}

english_tree = huffman_tree(freqs_english)

# Note: I removed punctuation because it is not present
# in the English frequency dictionary
text = "Huffman coding is a data compression algorithm"
text = text.lower()

encoded = huffman_encode(text, english_tree)
decoded = huffman_decode(encoded, english_tree)

print("Decoded text:", decoded)

original_bits = len(text) * 8
encoded_bits = len(encoded)

print("Original length (bits):", original_bits)
print("Encoded length (bits):", encoded_bits)
print("Compression ratio:", encoded_bits / original_bits)


class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''

    def __init__(self, name, number):
        self.name = name
        self.number = number

    def __str__(self):
        return f"{self.name}: {self.number}"


class Node:
    '''
    Node class to represent a single entry in the hash table.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node): Pointer to the next node in case of a collision.
    '''

    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table.
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, value): Inserts a new contact into the hash table.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''

    def __init__(self, size):
        self.size = size
        self.data = [None] * size

    def hash_function(self, key):
        total = 0
        for char in key:
            total += ord(char)
        return total % self.size

    def insert(self, key, value):
        index = self.hash_function(key)
        new_contact = Contact(key, value)
        new_node = Node(key, new_contact)

        # If no collision
        if self.data[index] is None:
            self.data[index] = new_node
            return

        # Collision handling (separate chaining)
        current = self.data[index]
        while current:
            # Update if duplicate key
            if current.key == key:
                current.value.number = value
                return
            if current.next is None:
                break
            current = current.next

        current.next = new_node

    def search(self, key):
        index = self.hash_function(key)
        current = self.data[index]

        while current:
            if current.key == key:
                return current.value
            current = current.next

        return None

    def print_table(self):
        for i in range(self.size):
            print(f"Index {i}:", end=" ")
            current = self.data[i]

            if current is None:
                print("Empty")
            else:
                while current:
                    print(f"- {current.value}", end=" ")
                    current = current.next
                print()

# Testing the HashTable

table = HashTable(10)

print("Initial Table:")
table.print_table()

# Insert contacts
table.insert("John", "909-876-1234")
table.insert("Rebecca", "111-555-0002")

print("\nAfter Adding John and Rebecca:")
table.print_table()

# Search
contact = table.search("John")
print("\nSearch result:", contact)

# Test collisions
table.insert("Amy", "111-222-3333")
table.insert("May", "222-333-1111")

print("\nAfter Testing Collisions:")
table.print_table()

# Test duplicate update
table.insert("Rebecca", "999-444-9999")

print("\nAfter Updating Rebecca:")
table.print_table()

# Search for non-existent contact
print("\nSearch for Chris:", table.search("Chris"))


"""
Design Memo

A hash table is the right structure for fast lookups because it provides average O(1) time complexity 
for insertions and searches. Instead of scanning through every contact like a list would require, 
the hash function converts a contacts name into an index in the underlying array. This allows the 
program to jump directly to the location where the contact should be stored, making lookups extremely fast 
even with hundreds of entries.

To handle collisions, I used separate chaining with linked lists. When two names produce the same index, 
the new contact is added to the linked list at that index instead of overwriting the existing data. 
During insertion, the linked list is traversed to check if the key already exists. If it does, the 
contacts number is updated. If not, a new node is added to the end of the chain. This keeps all 
colliding entries organized while preserving fast average performance.

An engineer might choose a hash table over a list when fast search speed is critical, especially when 
working with large datasets. Compared to trees, hash tables are typically simpler to implement and 
offer faster average lookups when ordering is not required. However, if sorted data or range queries 
are needed, a tree structure may be more appropriate.
"""

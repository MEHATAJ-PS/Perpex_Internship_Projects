class LRUCache:
    def __init__(self, capacity: int):
        self.capacity = capacity
        self.cache = {}  # key → value
        self.order = []  # keeps track of usage order

    def get(self, key):
        """Retrieve value and mark as recently used"""
        if key not in self.cache:
            return -1
        # Move key to the end (most recently used)
        self.order.remove(key)
        self.order.append(key)
        return self.cache[key]

    def put(self, key, value):
        """Insert or update a value in the cache"""
        if key in self.cache:
            # Update and mark as recently used
            self.cache[key] = value
            self.order.remove(key)
            self.order.append(key)
        else:
            if len(self.cache) >= self.capacity:
                # Evict least recently used key
                lru_key = self.order.pop(0)
                del self.cache[lru_key]
                print(f"Evicted: {lru_key}")
            self.cache[key] = value
            self.order.append(key)

    def display(self):
        """Show current cache state"""
        print("Cache:", {k: self.cache[k] for k in self.order})


# Example usage
if __name__ == "__main__":
    cache = LRUCache(3)

    cache.put(1, "A")
    cache.put(2, "B")
    cache.put(3, "C")
    cache.display()

    cache.get(1)  # Access key 1 (recently used)
    cache.put(4, "D")  # This will evict key 2
    cache.display()

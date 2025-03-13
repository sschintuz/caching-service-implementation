# Caching Service Implementation

An in-memory caching service with **LRU eviction** and **database synchronization** for efficient data retrieval.

## FEATURES:
- Set max cache size during initialization.
- Automatically evicts the least recently used (LRU) items when the cache exceeds the size limit.
- Fetches from cache first; if not found, retrieves from the database.
- Clears cache without affecting the database.
- Evicted data is persisted to the database.
- The **Entity** class has a unique identifier, accessible via the `getId()` method, which returns the unique ID of the object.
- Logs all actions (add, remove, eviction, retrieval) for transparency and debugging.
- Follows industry-standard exception handling practices to ensure robustness and stability.

## METHODS SUPPORTED:
- `add(Entity e1)`: Adds entity, evicts LRU if needed.
- `remove(Entity e1)`: Removes entity from both the cache and database.
- `removeAll()`: Clears all entities from both the cache and database.
- `get(Entity e1)`: Retrieves entity from cache or database.
- `clear()`: Clears the cache only.

```sh
git clone https://github.com/sschintuz/caching-service-implementation.git
cd caching-service-implementation

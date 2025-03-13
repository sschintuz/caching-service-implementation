# caching-service-implementation

An in-memory caching service with **LRU eviction** and **database synchronization** for efficient data retrieval.

##  Features
- **Configurable Cache Size**: Set max cache size.
- **LRU Eviction**: Removes least recently used items when full.
- **Cache Hit/Miss Handling**: Fetch from cache; fallback to DB.
- **Cache Clearing**: Clears cache without affecting DB.
- **Database Sync**: Evicted data is persisted.

##  Methods
- `add(Entity e1)`: Adds entity, evicts LRU if needed.
- `remove(Entity e1)`: Removes from cache & DB.
- `removeAll()`: Clears cache & DB.
- `get(Entity e1)`: Retrieves from cache or DB.
- `clear()`: Clears cache only.

##  Installation
git clone https://github.com/sschintuz/caching-service-implementation.git
cd caching-service-implementation

#!/usr/bin/env python
# coding: utf-8

# In[21]:


import logging
from typing import Dict, Optional, Any
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class Entity:
    """Entity class with unique ID and data."""
    def __init__(self, id: str, data: Any):
        self.id = id
        self.data = data
    
    def get_id(self) -> str:
        """Returns the unique ID of the entity."""
        return self.id
    
    def get_data(self) -> Any:
        """Returns the data stored in the entity."""
        return self.data
    
    def __str__(self) -> str:
        """String representation of the entity."""
        return f"Entity(id='{self.id}', data='{self.data}')"

class DatabaseService:
    """Simulates a database service for storing entities."""
    def __init__(self):
        self.database: Dict[str, Entity] = {}
        self.logger = logging.getLogger(__name__ + '.DatabaseService')
    
    def save(self, entity: Entity) -> None:
        """Save an entity to the database."""
        try:
            self.database[entity.get_id()] = entity
            self.logger.info(f"Saved to database: {entity}")
        except Exception as e:
            self.logger.error(f"Error saving entity: {str(e)}")
            raise
    
    def remove(self, entity: Entity) -> None:
        """Remove an entity from the database."""
        try:
            if entity.get_id() in self.database:
                del self.database[entity.get_id()]
                self.logger.info(f"Removed from database: {entity}")
            else:
                self.logger.info(f"Entity not found in database: {entity}")
        except Exception as e:
            self.logger.error(f"Error removing entity: {str(e)}")
            raise
    
    def clear(self) -> None:
        """Clear all entities from the database."""
        try:
            self.database.clear()
            self.logger.info("Database cleared")
        except Exception as e:
            self.logger.error(f"Error clearing database: {str(e)}")
            raise
    
    def get(self, id: str) -> Optional[Entity]:
        """Retrieve an entity from the database by its ID."""
        try:
            entity = self.database.get(id)
            if entity:
                self.logger.info(f"Retrieved from database: {entity}")
            else:
                self.logger.info(f"Entity with ID '{id}' not found in database")
            return entity
        except Exception as e:
            self.logger.error(f"Error getting entity: {str(e)}")
            return None

class CacheService:
    """Caching service with configurable size and least-used eviction policy."""
    def __init__(self, max_size: int, database_service: DatabaseService):
        """
        Initialize the cache service with a maximum size and database service.
        
        Args:
            max_size: Maximum number of elements to keep in the cache
            database_service: Service to store evicted entities
        """
        if max_size <= 0:
            raise ValueError("Max size must be greater than 0")
            
        self.max_size = max_size
        self.cache: Dict[str, Entity] = {}
        self.access_timestamps: Dict[str, float] = {}
        self.database_service = database_service
        self.logger = logging.getLogger(__name__ + '.CacheService')
    
    def add(self, entity: Entity) -> None:
        """
        Add an entity to the internal cache.
        Evicts least used entity if cache is full.
        """
        try:
            # Update access timestamp if entity is already in cache
            if entity.get_id() in self.cache:
                self.access_timestamps[entity.get_id()] = time.time()
                self.logger.info(f"Updated access time for entity in cache: {entity}")
            else:
                # Evict least used element if cache is full
                if len(self.cache) >= self.max_size:
                    self._evict()
                
                # Add to cache and update access timestamp
                self.cache[entity.get_id()] = entity
                self.access_timestamps[entity.get_id()] = time.time()
                self.logger.info(f"Entity added to cache: {entity}")
        except Exception as e:
            self.logger.error(f"Error adding entity: {str(e)}")
            raise
    
    def remove(self, entity: Entity) -> None:
        """
        Remove an entity from both the internal cache and database.
        """
        try:
            # Remove from cache
            if entity.get_id() in self.cache:
                del self.cache[entity.get_id()]
                if entity.get_id() in self.access_timestamps:
                    del self.access_timestamps[entity.get_id()]
            
            # Remove from database
            self.database_service.remove(entity)
            self.logger.info(f"Entity removed from cache and database: {entity}")
        except Exception as e:
            self.logger.error(f"Error removing entity: {str(e)}")
            raise
    
    def removeAll(self) -> None:
        """
        Remove all entities from the internal cache and database.
        """
        try:
            self.cache.clear()
            self.access_timestamps.clear()
            self.database_service.clear()
            self.logger.info("All entities removed from cache and database")
        except Exception as e:
            self.logger.error(f"Error removing all entities: {str(e)}")
            raise
    
    def get(self, entity: Entity) -> Optional[Entity]:
        """
        Return an entity from the internal cache or from database.
        Updates access time on cache hit.
        """
        try:
            entity_id = entity.get_id()
            
            # Try to get from cache first
            cached_entity = self.cache.get(entity_id)
            
            if cached_entity is None:
                # If not in cache, try to get from database
                cached_entity = self.database_service.get(entity_id)
                
                # If found in database, add to cache
                if cached_entity is not None:
                    self.add(cached_entity)
            else:
                self.logger.info(f"Cache hit for entity: {cached_entity}")
                
            # Update access timestamp if entity was found
            if cached_entity is not None:
                self.access_timestamps[entity_id] = time.time()
                
            return cached_entity
        except Exception as e:
            self.logger.error(f"Error getting entity: {str(e)}")
            return None
    
    def clear(self) -> None:
        """
        Clear the internal cache only. No impact on database entries.
        """
        try:
            self.cache.clear()
            self.access_timestamps.clear()
            self.logger.info("Cache cleared")
        except Exception as e:
            self.logger.error(f"Error clearing cache: {str(e)}")
            raise
    
    def _evict(self) -> None:
        """
        Evict the least-used element from cache and save it to database.
        """
        if not self.access_timestamps:
            return
            
        # Find the least recently used entity
        oldest_id = min(self.access_timestamps, key=self.access_timestamps.get)
        oldest_entity = self.cache.get(oldest_id)
        
        if oldest_entity:
            # Remove from cache
            del self.cache[oldest_id]
            del self.access_timestamps[oldest_id]
            
            # Save to database
            self.database_service.save(oldest_entity)
            self.logger.info(f"Evicted entity to database: {oldest_entity}")
        else:
            self.logger.warning("No entity to evict, cache is empty or unexpected behavior")

def test_cache_service():
    """Test the cache service functionality."""
    logger.info("Starting Cache Service Test")
    
    # Initialize services
    db_service = DatabaseService()
    cache_service = CacheService(max_size=2, database_service=db_service)
    
    # Create test entities
    e1 = Entity("1", "Data 1")
    e2 = Entity("2", "Data 2")
    e3 = Entity("3", "Data 3")
    
    # Test add and get
    cache_service.add(e1)
    cache_service.add(e2)
    cache_service.add(e3)  # This should evict e1 to the database
    
    # Check cache contents
    logger.info(f"Cache contents after adding e3: {cache_service.cache}")
    
    # Check if e1 was evicted and stored in DB
    evicted_e1 = db_service.get(e1.get_id())  # Manually check if e1 is in the DB
    assert evicted_e1 is not None, "e1 should be evicted and stored in DB"
    logger.info(f"e1 stored in DB: {evicted_e1}")
    
    # Cache size check
    assert len(cache_service.cache) <= cache_service.max_size, "Cache size exceeded max_size"
    logger.info(f"Cache size after eviction: {len(cache_service.cache)}")  # Should be <= max_size
    
    # e2 and e3 should still be in cache
    assert cache_service.get(e2) is not None, "e2 should still be in cache"
    assert cache_service.get(e3) is not None, "e3 should still be in cache"
    logger.info(f"Get e2: {cache_service.get(e2)}")  # Should fetch from cache
    logger.info(f"Get e3: {cache_service.get(e3)}")  # Should fetch from cache
    
    # Test remove
    cache_service.remove(e2)
    assert cache_service.get(e2) is None, "e2 should be removed from cache"
    logger.info(f"Get e2 after removal: {cache_service.get(e2)}")  # Should return None
    
    # Test removeAll
    cache_service.removeAll()
    assert len(cache_service.cache) == 0, "Cache should be empty after removeAll"
    logger.info("Cache after removeAll: {}".format(cache_service.cache))

    # Additional Test - Removing non-existing entity
    non_existing_entity = Entity("99", "Non-Existing Entity")
    cache_service.remove(non_existing_entity)  # Should not throw an error
    logger.info(f"Non-existing entity removal test passed.")

    # Additional Test - Clear Cache
    cache_service.clear()
    assert len(cache_service.cache) == 0, "Cache should be cleared after clear()"
    logger.info(f"Cache after clear: {cache_service.cache}")

test_cache_service()


# In[ ]:





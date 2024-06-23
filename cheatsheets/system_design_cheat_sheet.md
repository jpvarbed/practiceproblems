### System Design Cheat Sheet

#### Step 1: Understand the Problem and High-Level Scope

- **Functional Requirements:**
  - What is the core functionality?
  - Who are the users?
  - What actions can users perform?
  - What are the input and output of the system?
  - Are there any user interactions or workflows to consider?
- **Non-Functional Requirements:**
  - Scalability: How many users and what is the expected load?
  - Performance: What are the latency and throughput requirements?
  - Availability: What is the required uptime?
  - Consistency: How critical is data consistency?
  - Durability: How long should the data be retained?
  - Security: Are there specific security or compliance requirements?
  - Extensibility: How easy should it be to add new features?

Example Questions for Nearby Friends Feature:

- How close is "nearby"? (e.g., 5 miles)
- Can I assume the distance is a straight line?
- How many users are expected? (e.g., 1 billion, 10% use the feature)
- Should location history be stored?
- Should friends disappear after 10 minutes of inactivity?

#### Step 2: Propose High-Level Design and Get Buy-In

- **API Design:**
  - REST, gRPC, GraphQL – which is suitable and why?
  - Define endpoints, request/response formats, and error handling.
- **Data Model:**
  - What are the key entities?
  - How are they related?
  - What attributes do they have?
- **Algorithms:**
  - Any specific algorithms for data processing, retrieval, etc.?

API Choices:

- **REST:**
  - Easy to use and well-known.
  - Good for CRUD operations.
- **gRPC:**
  - High performance with binary protocol.
  - Suitable for microservices.
- **GraphQL:**
  - Flexible query mechanism.
  - Reduces over-fetching and under-fetching.

#### Step 3: Design Deep Dive

- **Scalability:**
  - **Database Scaling:**
    - Sharding vs. replication.
    - Read/write patterns.
  - **Caching:**
    - What data to cache?
    - Cache eviction policies.
  - **Load Balancing:**
    - Distribute requests across multiple servers.
    - Health checks and failover mechanisms.
- **Database Choice:**
  - SQL vs. NoSQL.
  - Considerations for data consistency, availability, and partition tolerance.
- **Query Patterns:**
  - Identify common query patterns.
  - Optimize read/write paths.
- **Service Discovery:**
  - Use tools like etcd, Zookeeper.
  - Key-value stores for configuration.
- **Handling High Throughput:**
  - Batching requests.
  - Write-ahead logs for sequential access.

#### Example Detailed Design: Redis Pub/Sub System

- **Memory:**
  - Estimate total memory needed (e.g., 200 GB for 1 billion users, 10% active, 20 bytes per friend).
  - Determine the number of servers required based on available memory.
- **CPU:**
  - Estimate the number of servers needed to handle peak load (e.g., 140 servers for 14 million pushes per second).
- **Service Discovery:**
  - Implement service discovery with etcd or Zookeeper.
  - Ensure real-time updates and health checks.

### Final Architecture Considerations

- **Data Storage:**
  - **Traffic Patterns:**
    - Write-heavy or read-heavy.
    - Sequential read/write patterns.
  - **Options:**
    - Relational vs. NoSQL databases.
    - Write-ahead log for high throughput.
- **Geospatial Indexing:**
  - Use geohashing for efficient location-based queries.
  - Shard by business ID for load distribution.
- **Caching Strategy:**
  - Use in-memory caches for frequently accessed data.
  - Consider cache invalidation strategies.

#### Final Architecture Diagram

- Include all components:
  - API Gateway
  - Load Balancers
  - Application Servers
  - Databases
  - Cache Servers
  - Service Discovery Components
  - Monitoring and Logging

| Requirement           | Database Choice               | Load Balancer                  | Caching Strategy          |
| --------------------- | ----------------------------- | ------------------------------ | ------------------------- |
| Write-heavy           | Cassandra, HBase              | Round-robin, Least connections | Write-through, Write-back |
| Read-heavy            | MySQL, PostgreSQL, Redis      | Least connections, IP Hash     | Read-through, Cache-aside |
| Low latency           | Redis, Memcached              | Any (focus on low latency)     | In-memory caching         |
| High durability       | MySQL, PostgreSQL             | Weighted round-robin           | Write-through, Write-back |
| Complex queries       | PostgreSQL, MySQL             | Weighted round-robin           | Cache-aside               |
| Large-scale analytics | BigQuery, Redshift, Snowflake | Least connections              | Cache-aside               |
| Geospatial queries    | MongoDB, PostGIS (PostgreSQL) | Geographically distributed     | Cache-aside               |
| Real-time data        | Redis, Kafka                  | Least connections              | Write-through             |

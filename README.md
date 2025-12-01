# inverted_index_search_engine
- Designed and implemented a full-stack search engine, from data injection with html crawlers to user interface.
- Utilized MapReduce programming model to build a scalable, segmented inverted index server. Implemented core Information Retrieval algorithms, including Term Frequency–Inverse Document Frequency (TF-IDF) for content relevance scoring and PageRank for link analysis and query result weighting.
- Developed a Service-Oriented Architecture composed of an index server and a search server. 
- Index Server: A REST API microservice designed to run on distributed machines in parallel. Each node serves one index segment each, while performing real-time query processing. 
- Search Server: A frontend Flask application that serves as middleware between index server and users;  orchestrates API calls to the index server, aggregate hits, and display filtered search results. 

# graphQ
## discussion on graph(Question)
GraphQL specific anti patterns question and answer tool kit.

The introduction of graphql in 2013 introduced graph specific vulnerabilities that the security community is just now catching up enough to scratch the surface of testing this api query language.

This tool seeks to bring deeper analysis to the table by applying common graph algorithms to analyze graphql apis as they should be seen: as graphs. GraphQL endpoints are different from the explicit routing we are used to seeing with REST: Functions and resolvers return objects with edges that all relate to each other, like a graph, this opens up the possibility of traversing to sensitive fields (BOLA) or circularly traversing to a composite node in a sufficiently large request to crash (DoS) the server.

See this [paper](https://www.diva-portal.org/smash/get/diva2:1302887/FULLTEXT01.pdf) that discusses the use of Tarjan's Algorithm for strongly connected components on a graphql schema, but unfortunately, this paper does not have a lot of visibility, and in the testing phase we don't always have direct access to the schema source code. We must leverage the introspection result. Luckily, we can transform introspection access into the schema. We can also take cycle detection optimization a step further by doing a top level cycles first and creating sub graphs to search, which can reduce our graph size drastically for secondary searching. Previous implementations of cycle detection struggle to handle large graphs with naive repetitive depth first traversals, which is the unfortunate direction of many mature graphql apis, a single schema contains too many vertex/edges for previous tools to . This implementation handles the massive github graphql backend with ease. 

## Features

Points of Interest: Direct your attention to a specific node that might be worth looking for BOLA vulnerabilities.

Cycles: Detect cycles or the DoS anti pattern of circular references in the graph. If the engineer failed to set a depth limit to the graphql query, it could be vulnerable to a DoS.

## How to use
...
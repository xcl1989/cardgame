# Neo4j Setup Guide

Neo4j has been successfully installed and configured on your system.

## Status
- Neo4j is running as a service
- Version: 2025.12.1

## Connection Information
- **HTTP Endpoint**: http://localhost:7474
- **Bolt Endpoint**: bolt://localhost:7687
- **Default Username**: neo4j

## Getting Started

### 1. Access Neo4j Browser
Open your web browser and navigate to:
```
http://localhost:7474
```

### 2. Set Initial Password
On first access, you'll need to set a password:
1. Go to http://localhost:7474
2. Login with username `neo4j` and password `neo4j`
3. You'll be prompted to set a new password

### 3. Using Neo4j in Python
The Neo4j Python driver is installed in your environment. You can use it in your Python code:

```python
from neo4j import GraphDatabase

# Connect to Neo4j
driver = GraphDatabase.driver("bolt://localhost:7687", auth=("neo4j", "your_password"))

# Example query
with driver.session() as session:
    result = session.run("RETURN 'Hello, Neo4j!' AS greeting")
    for record in result:
        print(record["greeting"])

# Don't forget to close the driver when done
driver.close()
```

## Service Management

### Start Neo4j
```bash
brew services start neo4j
```

### Stop Neo4j
```bash
brew services stop neo4j
```

### Restart Neo4j
```bash
brew services restart neo4j
```

## Troubleshooting

### If Neo4j fails to start
1. Check if another instance is running
2. Look at the logs: `~/Library/Logs/neo4j/neo4j.log`
3. Try starting manually: `/opt/homebrew/opt/neo4j/bin/neo4j console`

### Common Issues
- Port conflicts: Make sure ports 7474 (HTTP) and 7687 (Bolt) are free
- Memory: Ensure your system has enough RAM allocated to Neo4j
- Permissions: Make sure Neo4j has proper file system permissions

## Uninstalling Neo4j
If you need to uninstall Neo4j:
```bash
brew services stop neo4j
brew uninstall neo4j
```
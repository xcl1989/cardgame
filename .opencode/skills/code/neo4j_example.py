"""
Example script demonstrating how to connect to and use Neo4j
"""

from neo4j import GraphDatabase


def connect_to_neo4j(uri, username, password):
    """
    Connect to Neo4j database
    :param uri: The URI of the Neo4j instance (e.g., "bolt://localhost:7687")
    :param username: Username for authentication
    :param password: Password for authentication
    :return: Driver instance
    """
    try:
        driver = GraphDatabase.driver(uri, auth=(username, password))
        # Test the connection
        with driver.session() as session:
            result = session.run("RETURN 'Connected to Neo4j!' AS message")
            record = result.single()
            print(record["message"])
        return driver
    except Exception as e:
        print(f"Failed to connect to Neo4j: {e}")
        return None


def create_test_knowledge_base(driver):
    """
    Create a test knowledge base with sample data
    :param driver: Neo4j driver instance
    """
    with driver.session() as session:
        # Clear existing data (optional, be careful in production!)
        session.run("MATCH (n) DETACH DELETE n")

        # Create sample entities for a test knowledge base
        queries = [
            # Create people
            "CREATE (p:Person {name: '张三', age: 30, occupation: '工程师'})",
            "CREATE (p:Person {name: '李四', age: 25, occupation: '设计师'})",
            "CREATE (p:Person {name: '王五', age: 35, occupation: '产品经理'})",

            # Create organizations
            "CREATE (o:Organization {name: '科技公司A', industry: '互联网', location: '北京'})",
            "CREATE (o:Organization {name: '设计公司B', industry: '创意设计', location: '上海'})",

            # Create topics/concepts
            "CREATE (t:Topic {name: '人工智能', category: '技术'})",
            "CREATE (t:Topic {name: '用户体验', category: '设计'})",
            "CREATE (t:Topic {name: '项目管理', category: '管理'})",

            # Create relationships
            "MATCH (p:Person {name: '张三'}), (t:Topic {name: '人工智能'}) CREATE (p)-[:INTERESTED_IN]->(t)",
            "MATCH (p:Person {name: '李四'}), (t:Topic {name: '用户体验'}) CREATE (p)-[:INTERESTED_IN]->(t)",
            "MATCH (p:Person {name: '王五'}), (t:Topic {name: '项目管理'}) CREATE (p)-[:INTERESTED_IN]->(t)",
            "MATCH (p:Person {name: '张三'}), (o:Organization {name: '科技公司A'}) CREATE (p)-[:WORKS_AT]->(o)",
            "MATCH (p:Person {name: '李四'}), (o:Organization {name: '设计公司B'}) CREATE (p)-[:WORKS_AT]->(o)"
        ]

        for query in queries:
            session.run(query)

        print("测试知识库创建完成！包含人员、组织、主题及它们之间的关系。")


def create_node(driver, label, properties):
    """
    Create a node in Neo4j
    :param driver: Neo4j driver instance
    :param label: Label for the node
    :param properties: Dictionary of properties for the node
    """
    with driver.session() as session:
        query = f"CREATE (n:{label} $props) RETURN n"
        result = session.run(query, props=properties)
        record = result.single()
        print(f"Created node: {record['n']}")


def run_query(driver, query, parameters=None):
    """
    Run a Cypher query
    :param driver: Neo4j driver instance
    :param query: Cypher query string
    :param parameters: Optional parameters for the query
    :return: Result of the query
    """
    with driver.session() as session:
        result = session.run(query, parameters)
        return [record.data() for record in result]


def query_test_knowledge_base(driver):
    """
    Query the test knowledge base to verify it was created correctly
    :param driver: Neo4j driver instance
    """
    with driver.session() as session:
        # Query all persons
        result = session.run("MATCH (p:Person) RETURN p.name AS name, p.age AS age, p.occupation AS occupation")
        print("\n人员列表:")
        for record in result:
            print(f"- {record['name']}, {record['age']}岁, 职业: {record['occupation']}")

        # Query all organizations
        result = session.run("MATCH (o:Organization) RETURN o.name AS name, o.industry AS industry, o.location AS location")
        print("\n组织列表:")
        for record in result:
            print(f"- {record['name']}, 行业: {record['industry']}, 地点: {record['location']}")

        # Query all topics
        result = session.run("MATCH (t:Topic) RETURN t.name AS name, t.category AS category")
        print("\n主题列表:")
        for record in result:
            print(f"- {record['name']}, 类别: {record['category']}")

        # Query relationships
        result = session.run("""
            MATCH (p:Person)-[r]->(connected)
            RETURN p.name AS person, type(r) AS relationship, connected.name AS connected_to
        """)
        print("\n关系列表:")
        for record in result:
            print(f"- {record['person']} -[{record['relationship']}]-> {record['connected_to']}")


if __name__ == "__main__":
    # Example usage
    # Replace with your actual Neo4j connection details
    NEO4J_URI = "bolt://localhost:7687"
    NEO4J_USERNAME = "neo4j"
    NEO4J_PASSWORD = "12345678"  # 请替换为您设置的实际密码

    # Connect to Neo4j
    driver = connect_to_neo4j(NEO4J_URI, NEO4J_USERNAME, NEO4J_PASSWORD)

    if driver:
        print("正在创建测试知识库...")
        create_test_knowledge_base(driver)

        print("\n正在查询测试知识库...")
        query_test_knowledge_base(driver)

        # Example: Run a simple query
        results = run_query(driver, "MATCH (n) RETURN count(n) AS count")
        print(f"\n数据库中节点总数: {results[0]['count']}")

        # Close the driver
        driver.close()
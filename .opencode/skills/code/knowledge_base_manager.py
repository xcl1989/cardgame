"""
知识库管理系统
用于管理Neo4j图数据库中的知识库
"""

from neo4j import GraphDatabase


class KnowledgeBaseManager:
    def __init__(self, uri="bolt://localhost:7687", username="neo4j", password="12345678"):
        """
        初始化知识库管理器
        :param uri: Neo4j连接URI
        :param username: 用户名
        :param password: 密码
        """
        self.driver = GraphDatabase.driver(uri, auth=(username, password))

    def close(self):
        """关闭数据库连接"""
        self.driver.close()

    def create_person(self, name, age=None, occupation=None):
        """创建人员节点"""
        with self.driver.session() as session:
            query = "CREATE (p:Person {name: $name"
            params = {"name": name}
            
            if age is not None:
                query += ", age: $age"
                params["age"] = age
            
            if occupation is not None:
                query += ", occupation: $occupation"
                params["occupation"] = occupation
                
            query += "}) RETURN p"
            
            result = session.run(query, params)
            record = result.single()
            return record["p"]

    def create_organization(self, name, industry=None, location=None):
        """创建组织节点"""
        with self.driver.session() as session:
            query = "CREATE (o:Organization {name: $name"
            params = {"name": name}
            
            if industry is not None:
                query += ", industry: $industry"
                params["industry"] = industry
                
            if location is not None:
                query += ", location: $location"
                params["location"] = location
                
            query += "}) RETURN o"
            
            result = session.run(query, params)
            record = result.single()
            return record["o"]

    def create_topic(self, name, category=None):
        """创建主题节点"""
        with self.driver.session() as session:
            query = "CREATE (t:Topic {name: $name"
            params = {"name": name}
            
            if category is not None:
                query += ", category: $category"
                params["category"] = category
                
            query += "}) RETURN t"
            
            result = session.run(query, params)
            record = result.single()
            return record["t"]

    def create_relationship(self, from_label, from_name, rel_type, to_label, to_name):
        """创建两个实体之间的关系"""
        with self.driver.session() as session:
            query = f"""
            MATCH (from:{from_label} {{name: $from_name}})
            MATCH (to:{to_label} {{name: $to_name}})
            CREATE (from)-[:{rel_type}]->(to)
            RETURN from, to
            """
            params = {"from_name": from_name, "to_name": to_name}
            result = session.run(query, params)
            return result.single()

    def query_all_entities(self):
        """查询所有实体"""
        with self.driver.session() as session:
            result = session.run("""
                MATCH (n)
                WHERE n:Person OR n:Organization OR n:Topic
                RETURN labels(n)[0] AS type, n.name AS name, n
            """)
            return [{"type": record["type"], "name": record["name"], "properties": dict(record["n"])} 
                    for record in result]

    def query_by_type(self, entity_type):
        """根据类型查询实体"""
        with self.driver.session() as session:
            result = session.run(f"""
                MATCH (n:{entity_type})
                RETURN n
            """)
            return [dict(record["n"]) for record in result]

    def query_relationships(self, person_name=None):
        """查询关系"""
        with self.driver.session() as session:
            if person_name:
                query = """
                MATCH (p:Person {name: $person_name})-[r]->(connected)
                RETURN p.name AS person, type(r) AS relationship, connected.name AS connected_to, labels(connected)[0] AS connected_type
                """
                params = {"person_name": person_name}
            else:
                query = """
                MATCH (p:Person)-[r]->(connected)
                RETURN p.name AS person, type(r) AS relationship, connected.name AS connected_to, labels(connected)[0] AS connected_type
                """
                params = {}
                
            result = session.run(query, params)
            return [{"person": record["person"], 
                     "relationship": record["relationship"],
                     "connected_to": record["connected_to"],
                     "connected_type": record["connected_type"]} 
                    for record in result]

    def clear_knowledge_base(self):
        """清空知识库（谨慎使用）"""
        with self.driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")


def main():
    print("知识库管理系统")
    print("=" * 50)

    # 连接到数据库
    kb_manager = KnowledgeBaseManager()

    try:
        # 清空现有数据
        print("正在清空现有数据...")
        kb_manager.clear_knowledge_base()
        print("数据已清空！")

    except Exception as e:
        print(f"发生错误: {e}")
    finally:
        kb_manager.close()


if __name__ == "__main__":
    main()
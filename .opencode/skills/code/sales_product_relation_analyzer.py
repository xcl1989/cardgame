import mysql.connector
from neo4j import GraphDatabase
import json
from decimal import Decimal
from datetime import datetime, date, time


class SalesProductRelationAnalyzer:
    def __init__(self, mysql_host="127.0.0.1", mysql_user="root", mysql_password="12345678", mysql_db="Test",
                 neo4j_uri="bolt://localhost:7687", neo4j_user="neo4j", neo4j_password="12345678"):
        # MySQL连接
        self.mysql_conn = mysql.connector.connect(
            host=mysql_host,
            user=mysql_user,
            password=mysql_password,
            database=mysql_db
        )
        
        # Neo4j连接
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close_connections(self):
        """关闭数据库连接"""
        self.mysql_conn.close()
        self.neo4j_driver.close()

    def get_sales_and_product_data(self):
        """从MySQL获取sales和product表的数据"""
        cursor = self.mysql_conn.cursor(dictionary=True)

        # 获取销售数据和对应的产品信息
        # 注意：sales表中的客户字段名为"custom"而非"customerid"
        query = """
        SELECT s.id, s.custom, s.date, s.amount, s.productid,
               p.name as product_name, p.category as product_category, p.brand as product_brand
        FROM sales s
        LEFT JOIN Product p ON s.productid = p.id
        """

        cursor.execute(query)
        results = cursor.fetchall()
        cursor.close()

        return results

    def clear_neo4j_graph(self):
        """清空Neo4j中的现有图数据"""
        with self.neo4j_driver.session() as session:
            session.run("MATCH (n) DETACH DELETE n")
            print("已清空Neo4j中的现有图数据")

    def create_nodes_and_relationships(self, sales_data):
        """在Neo4j中创建节点和关系"""
        with self.neo4j_driver.session() as session:
            # 创建索引以提高性能
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:Customer) ON (c.name)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (p:Product) ON (p.productid)")

            # 收集唯一的客户和产品
            customers = {}
            products = {}

            for record in sales_data:
                customer_name = record['custom']  # 使用正确的字段名
                product_id = record['productid']

                # 收集客户信息
                if customer_name not in customers:
                    customers[customer_name] = {
                        'name': customer_name,
                        'total_purchases': 0,
                        'total_amount': 0
                    }

                # 收集产品信息
                if product_id and product_id not in products and record['product_name']:
                    products[product_id] = {
                        'productid': product_id,
                        'name': record['product_name'],
                        'category': record['product_category'],
                        'brand': record['product_brand']
                    }

                # 更新客户的购买统计
                if customer_name:  # 确保客户名不为空
                    customers[customer_name]['total_purchases'] += 1
                    if record['amount']:
                        customers[customer_name]['total_amount'] += float(record['amount'])

            # 创建客户节点
            for customer in customers.values():
                session.run("""
                    MERGE (c:Customer {name: $name})
                    SET c.total_purchases = $total_purchases,
                        c.total_amount = $total_amount
                """,
                name=customer['name'],
                total_purchases=customer['total_purchases'],
                total_amount=customer['total_amount'])

            # 创建产品节点
            for product in products.values():
                session.run("""
                    MERGE (p:Product {productid: $productid})
                    SET p.name = $name,
                        p.category = $category,
                        p.brand = $brand
                """,
                productid=product['productid'],
                name=product['name'],
                category=product['category'],
                brand=product['brand'])

            # 创建客户和产品之间的购买关系
            for record in sales_data:
                if record['productid'] and record['productid'] in products and record['custom']:  # 确保产品和客户都存在
                    session.run("""
                        MATCH (c:Customer {name: $customer_name})
                        MATCH (p:Product {productid: $productid})
                        MERGE (c)-[r:BOUGHT]->(p)
                        ON CREATE SET r.times = 1, r.total_amount = $amount, r.avg_amount = $amount, r.date = $date
                        ON MATCH SET r.times = r.times + 1,
                                  r.total_amount = r.total_amount + $amount,
                                  r.avg_amount = r.total_amount / r.times
                    """,
                    customer_name=record['custom'],
                    productid=record['productid'],
                    amount=float(record['amount']) if record['amount'] else 0,
                    date=str(record['date']) if record['date'] else None)

        print(f"成功处理了 {len(sales_data)} 条销售记录")
        print(f"创建了 {len(customers)} 个客户节点")
        print(f"创建了 {len(products)} 个产品节点")
        print("客户-产品购买关系已建立")

    def analyze_and_store_relations(self):
        """分析并存储客户和商品的关联关系"""
        print("正在从MySQL获取销售和产品数据...")
        sales_data = self.get_sales_and_product_data()
        
        print("正在清空Neo4j中的现有数据...")
        self.clear_neo4j_graph()
        
        print("正在创建节点和关系...")
        self.create_nodes_and_relationships(sales_data)
        
        print("客户和商品关联关系已成功存储到Neo4j中！")


def main():
    analyzer = SalesProductRelationAnalyzer()
    
    try:
        analyzer.analyze_and_store_relations()
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
    finally:
        analyzer.close_connections()


if __name__ == "__main__":
    main()
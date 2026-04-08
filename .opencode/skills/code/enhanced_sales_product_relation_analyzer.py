import mysql.connector
from neo4j import GraphDatabase
import json
from decimal import Decimal
from datetime import datetime, date, time
from collections import defaultdict


class EnhancedSalesProductRelationAnalyzer:
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

    def create_enhanced_nodes_and_relationships(self, sales_data):
        """在Neo4j中创建增强的节点和关系，包含时间维度和客户关系"""
        with self.neo4j_driver.session() as session:
            # 创建索引以提高性能
            session.run("CREATE INDEX IF NOT EXISTS FOR (c:Customer) ON (c.name)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (p:Product) ON (p.productid)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (y:Year) ON (y.year)")
            session.run("CREATE INDEX IF NOT EXISTS FOR (m:Month) ON (m.month_key)")
            
            # 收集唯一的客户、产品和时间信息
            customers = {}
            products = {}
            years = {}
            months = {}
            customer_purchase_history = defaultdict(lambda: defaultdict(list))  # customer -> year -> [(month, product_id)]
            
            for record in sales_data:
                customer_name = record['custom']
                product_id = record['productid']
                
                # 解析日期信息
                sale_date = record['date']
                if sale_date:
                    year = sale_date.year
                    month = sale_date.month
                    year_month_key = f"{year}-{month:02d}"
                    
                    # 收集年份信息
                    if year not in years:
                        years[year] = {'year': year}
                    
                    # 收集月份信息
                    if year_month_key not in months:
                        months[year_month_key] = {
                            'year': year,
                            'month': month,
                            'month_key': year_month_key
                        }
                    
                    # 记录客户购买历史
                    customer_purchase_history[customer_name][year].append((month, product_id))
                
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
            
            # 创建年份节点
            for year_info in years.values():
                session.run("""
                    MERGE (y:Year {year: $year})
                """,
                year=year_info['year'])
            
            # 创建月份节点
            for month_info in months.values():
                session.run("""
                    MERGE (m:Month {month_key: $month_key})
                    SET m.year = $year,
                        m.month = $month
                """,
                month_key=month_info['month_key'],
                year=month_info['year'],
                month=month_info['month'])
            
            # 创建客户和产品之间的购买关系（带时间维度）
            for record in sales_data:
                if record['productid'] and record['productid'] in products and record['custom']:  # 确保产品和客户都存在
                    # 提取日期信息
                    sale_year = record['date'].year if record['date'] else None
                    sale_month_key = f"{sale_year}-{record['date'].month:02d}" if record['date'] else None
                    
                    session.run("""
                        MATCH (c:Customer {name: $customer_name})
                        MATCH (p:Product {productid: $productid})
                        OPTIONAL MATCH (y:Year {year: $year})
                        OPTIONAL MATCH (m:Month {month_key: $month_key})
                        
                        MERGE (c)-[r:BOUGHT]->(p)
                        ON CREATE SET r.times = 1, r.total_amount = $amount, r.avg_amount = $amount
                        ON MATCH SET r.times = r.times + 1, 
                                  r.total_amount = r.total_amount + $amount,
                                  r.avg_amount = r.total_amount / r.times
                        
                        // 创建时间关系
                        FOREACH (x IN CASE WHEN y IS NOT NULL THEN [1] ELSE [] END |
                          MERGE (c)-[:PURCHASED_IN_YEAR]->(y)
                          MERGE (p)-[:SOLD_IN_YEAR]->(y)
                        )
                        FOREACH (x IN CASE WHEN m IS NOT NULL THEN [1] ELSE [] END |
                          MERGE (c)-[:PURCHASED_IN_MONTH]->(m)
                          MERGE (p)-[:SOLD_IN_MONTH]->(m)
                        )
                        
                        // 创建购买事件节点
                        WITH c, p, y, m
                        MERGE (e:Event {id: $event_id})
                        SET e.date = $date, e.amount = $amount
                        MERGE (e)-[:BY_CUSTOMER]->(c)
                        MERGE (e)-[:OF_PRODUCT]->(p)
                        FOREACH (x IN CASE WHEN y IS NOT NULL THEN [1] ELSE [] END |
                          MERGE (e)-[:IN_YEAR]->(y)
                        )
                        FOREACH (x IN CASE WHEN m IS NOT NULL THEN [1] ELSE [] END |
                          MERGE (e)-[:IN_MONTH]->(m)
                        )
                    """,
                    customer_name=record['custom'],
                    productid=record['productid'],
                    year=sale_year,
                    month_key=sale_month_key,
                    amount=float(record['amount']) if record['amount'] else 0,
                    date=str(record['date']) if record['date'] else None,
                    event_id=record['id'])
            
            # 分析并创建客户之间的关系（基于共同购买相同产品）
            print("正在分析客户之间的关系...")
            for customer, yearly_purchases in customer_purchase_history.items():
                for year, monthly_purchases in yearly_purchases.items():
                    # 获取该客户在这一年购买的产品
                    purchased_products = set([prod_id for _, prod_id in monthly_purchases])
                    
                    # 查找其他购买了相同产品的客户
                    for other_customer, other_yearly_purchases in customer_purchase_history.items():
                        if customer != other_customer and year in other_yearly_purchases:
                            other_purchased_products = set([prod_id for _, prod_id in other_yearly_purchases[year]])
                            
                            # 计算共同购买的产品数量
                            common_products = purchased_products.intersection(other_purchased_products)
                            
                            if len(common_products) > 0:
                                session.run("""
                                    MATCH (c1:Customer {name: $customer1})
                                    MATCH (c2:Customer {name: $customer2})
                                    MERGE (c1)-[r:SIMILAR_TASTE]->(c2)
                                    ON CREATE SET r.common_products = $common_count, r.year = $year
                                    ON MATCH SET r.common_products = $common_count
                                """,
                                customer1=customer,
                                customer2=other_customer,
                                common_count=len(common_products),
                                year=year)
        
        print(f"成功处理了 {len(sales_data)} 条销售记录")
        print(f"创建了 {len(customers)} 个客户节点")
        print(f"创建了 {len(products)} 个产品节点")
        print(f"创建了 {len(years)} 个年份节点")
        print(f"创建了 {len(months)} 个月份节点")
        print("增强版客户-产品-时间关联关系已建立")

    def analyze_and_store_enhanced_relations(self):
        """分析并存储增强版的客户和商品关联关系"""
        print("正在从MySQL获取销售和产品数据...")
        sales_data = self.get_sales_and_product_data()
        
        print("正在清空Neo4j中的现有数据...")
        self.clear_neo4j_graph()
        
        print("正在创建增强版的节点和关系...")
        self.create_enhanced_nodes_and_relationships(sales_data)
        
        print("增强版客户和商品关联关系已成功存储到Neo4j中！")


def main():
    analyzer = EnhancedSalesProductRelationAnalyzer()
    
    try:
        analyzer.analyze_and_store_enhanced_relations()
    except Exception as e:
        print(f"处理过程中出现错误: {e}")
    finally:
        analyzer.close_connections()


if __name__ == "__main__":
    main()
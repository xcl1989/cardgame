from neo4j import GraphDatabase
import json


class RelationshipAnalyzer:
    def __init__(self, neo4j_uri="bolt://localhost:7687", neo4j_user="neo4j", neo4j_password="12345678"):
        self.neo4j_driver = GraphDatabase.driver(neo4j_uri, auth=(neo4j_user, neo4j_password))

    def close_connection(self):
        """关闭数据库连接"""
        self.neo4j_driver.close()

    def analyze_single_element(self, element):
        """分析单个元素的数据"""
        with self.neo4j_driver.session() as session:
            # 检查是否为客户
            result = session.run("MATCH (c:Customer {name: $name}) RETURN c", name=element)
            record = result.single()
            if record:
                # 客户数据分析
                customer_analysis = session.run("""
                    MATCH (c:Customer {name: $name})
                    OPTIONAL MATCH (c)-[r:BOUGHT]->(p:Product)
                    RETURN 
                        c.name AS customer_name,
                        c.total_purchases AS total_purchases,
                        c.total_amount AS total_amount,
                        count(p) AS product_variety,
                        collect({product: p.name, times: r.times, total_amount: r.total_amount}) AS purchase_details
                """, name=element)
                return customer_analysis.single()

            # 检查是否为产品
            result = session.run("MATCH (p:Product {name: $name}) RETURN p", name=element)
            record = result.single()
            if record:
                # 产品数据分析
                product_analysis = session.run("""
                    MATCH (p:Product {name: $name})
                    OPTIONAL MATCH (c:Customer)-[r:BOUGHT]->(p)
                    RETURN 
                        p.name AS product_name,
                        p.category AS category,
                        p.brand AS brand,
                        count(c) AS customer_count,
                        sum(r.times) AS total_sales_times,
                        sum(r.total_amount) AS total_revenue,
                        avg(r.avg_amount) AS avg_price,
                        collect({customer: c.name, times: r.times, amount: r.total_amount}) AS customer_details
                """, name=element)
                return product_analysis.single()

            # 检查是否为年份
            try:
                year = int(element)
                year_analysis = session.run("""
                    MATCH (y:Year {year: $year})
                    OPTIONAL MATCH (c:Customer)-[:PURCHASED_IN_YEAR]->(y)
                    OPTIONAL MATCH (p:Product)-[:SOLD_IN_YEAR]->(y)
                    RETURN 
                        y.year AS year,
                        count(DISTINCT c) AS customer_count,
                        count(DISTINCT p) AS product_count,
                        count((c)-[:PURCHASED_IN_YEAR]->(y)) AS transaction_count
                """, year=year)
                return year_analysis.single()
            except ValueError:
                pass

            # 检查是否为月份
            if "-" in element and len(element) == 7:  # 格式应为 YYYY-MM
                try:
                    year, month = element.split("-")
                    year = int(year)
                    month = int(month)
                    month_key = f"{year}-{month:02d}"
                    
                    month_analysis = session.run("""
                        MATCH (m:Month {month_key: $month_key})
                        OPTIONAL MATCH (c:Customer)-[:PURCHASED_IN_MONTH]->(m)
                        OPTIONAL MATCH (p:Product)-[:SOLD_IN_MONTH]->(m)
                        RETURN 
                            m.month_key AS month,
                            count(DISTINCT c) AS customer_count,
                            count(DISTINCT p) AS product_count,
                            count((c)-[:PURCHASED_IN_MONTH]->(m)) AS transaction_count
                    """, month_key=month_key)
                    return month_analysis.single()
                except ValueError:
                    pass

            return None

    def analyze_relationships(self, elements):
        """分析多个元素之间的关系"""
        if len(elements) == 1:
            # 单个元素分析
            result = self.analyze_single_element(elements[0])
            if result:
                return {
                    "type": "single_element_analysis",
                    "element": elements[0],
                    "data": dict(result)
                }
            else:
                return {
                    "type": "error",
                    "message": f"未找到元素: {elements[0]}"
                }

        elif len(elements) == 2:
            # 两个元素之间的关系分析
            elem1, elem2 = elements
            return self._analyze_two_elements(elem1, elem2)

        elif len(elements) >= 3:
            # 多个元素之间的关系分析
            return self._analyze_multiple_elements(elements)

    def _analyze_two_elements(self, elem1, elem2):
        """分析两个元素之间的关系"""
        with self.neo4j_driver.session() as session:
            # 检查客户-客户关系
            result = session.run("""
                MATCH (c1:Customer {name: $elem1})-[r:SIMILAR_TASTE]-(c2:Customer {name: $elem2})
                RETURN r
            """, elem1=elem1, elem2=elem2)
            record = result.single()
            if record:
                return {
                    "type": "customer_similarity",
                    "elements": [elem1, elem2],
                    "relationship": "SIMILAR_TASTE",
                    "data": dict(record['r'])
                }

            # 检查客户-产品关系
            result = session.run("""
                MATCH (c:Customer {name: $customer})-[r:BOUGHT]->(p:Product {name: $product})
                RETURN r
            """, customer=elem1, product=elem2)
            records = list(result)
            if len(records) > 0:
                record = records[0]
            else:
                result = session.run("""
                    MATCH (c:Customer {name: $customer})-[r:BOUGHT]->(p:Product {name: $product})
                    RETURN r
                """, customer=elem2, product=elem1)
                records = list(result)
                if len(records) > 0:
                    record = records[0]
                else:
                    record = None
            
            if record:
                rel_data = dict(record['r'])
                if elem1 in [r['name'] for r in session.run("MATCH (c:Customer) WHERE c.name=$name RETURN c", name=elem1).value()]:
                    customer = elem1
                    product = elem2
                else:
                    customer = elem2
                    product = elem1
                return {
                    "type": "customer_product_relationship",
                    "elements": [customer, product],
                    "relationship": "BOUGHT",
                    "data": rel_data
                }

            # 检查客户-时间关系
            try:
                # 检查是否为年份
                year = int(elem2)
                result = session.run("""
                    MATCH (c:Customer {name: $customer})-[:PURCHASED_IN_YEAR]->(y:Year {year: $year})
                    RETURN count(*) AS count
                """, customer=elem1, year=year)
                if result.single()['count'] > 0:
                    return {
                        "type": "customer_time_relationship",
                        "elements": [elem1, str(year)],
                        "relationship": "PURCHASED_IN_YEAR",
                        "data": {"year": year}
                    }
            except ValueError:
                pass

            try:
                # 检查是否为月份
                if "-" in elem2 and len(elem2) == 7:
                    year, month = elem2.split("-")
                    year = int(year)
                    month = int(month)
                    month_key = f"{year}-{month:02d}"
                    result = session.run("""
                        MATCH (c:Customer {name: $customer})-[:PURCHASED_IN_MONTH]->(m:Month {month_key: $month_key})
                        RETURN count(*) AS count
                    """, customer=elem1, month_key=month_key)
                    if result.single()['count'] > 0:
                        return {
                            "type": "customer_time_relationship",
                            "elements": [elem1, elem2],
                            "relationship": "PURCHASED_IN_MONTH",
                            "data": {"month": elem2}
                        }
            except ValueError:
                pass

            # 检查产品-时间关系
            try:
                # 检查是否为年份
                year = int(elem2)
                result = session.run("""
                    MATCH (p:Product {name: $product})-[:SOLD_IN_YEAR]->(y:Year {year: $year})
                    RETURN count(*) AS count
                """, product=elem1, year=year)
                if not result.single()['count'] > 0:
                    result = session.run("""
                        MATCH (p:Product {name: $product})-[:SOLD_IN_YEAR]->(y:Year {year: $year})
                        RETURN count(*) AS count
                    """, product=elem2, year=year)
                if result.single()['count'] > 0:
                    return {
                        "type": "product_time_relationship",
                        "elements": [elem1 if elem1 != str(year) else elem2, str(year)],
                        "relationship": "SOLD_IN_YEAR",
                        "data": {"year": year}
                    }
            except ValueError:
                pass

            try:
                # 检查是否为月份
                if "-" in elem2 and len(elem2) == 7:
                    year, month = elem2.split("-")
                    year = int(year)
                    month = int(month)
                    month_key = f"{year}-{month:02d}"
                    result = session.run("""
                        MATCH (p:Product {name: $product})-[:SOLD_IN_MONTH]->(m:Month {month_key: $month_key})
                        RETURN count(*) AS count
                    """, product=elem1, month_key=month_key)
                    if not result.single()['count'] > 0:
                        result = session.run("""
                            MATCH (p:Product {name: $product})-[:SOLD_IN_MONTH]->(m:Month {month_key: $month_key})
                            RETURN count(*) AS count
                        """, product=elem2, month_key=month_key)
                    if result.single()['count'] > 0:
                        return {
                            "type": "product_time_relationship",
                            "elements": [elem1 if elem1 != elem2 else elem2, elem2],
                            "relationship": "SOLD_IN_MONTH",
                            "data": {"month": elem2}
                        }
            except ValueError:
                pass

            return {
                "type": "no_direct_relationship",
                "elements": [elem1, elem2],
                "message": f"元素 {elem1} 和 {elem2} 之间没有直接关系"
            }

    def _analyze_multiple_elements(self, elements):
        """分析多个元素之间的关系"""
        with self.neo4j_driver.session() as session:
            # 分析所有元素的类型
            customers = []
            products = []
            years = []
            months = []
            
            for elem in elements:
                # 检查是否为客户
                result = session.run("MATCH (c:Customer {name: $name}) RETURN c", name=elem)
                if result.single():
                    customers.append(elem)
                    continue
                
                # 检查是否为产品
                result = session.run("MATCH (p:Product {name: $name}) RETURN p", name=elem)
                if result.single():
                    products.append(elem)
                    continue
                
                # 检查是否为年份
                try:
                    year = int(elem)
                    years.append(year)
                    continue
                except ValueError:
                    pass
                
                # 检查是否为月份
                if "-" in elem and len(elem) == 7:
                    try:
                        year, month = elem.split("-")
                        year = int(year)
                        month = int(month)
                        months.append(elem)
                        continue
                    except ValueError:
                        pass
                
                # 如果都不是，标记为未知
                pass
            
            # 返回多元素分析结果
            return {
                "type": "multi_element_analysis",
                "elements": elements,
                "breakdown": {
                    "customers": customers,
                    "products": products,
                    "years": years,
                    "months": months
                },
                "relationships": self._find_relationships_among_elements(session, elements)
            }

    def _find_relationships_among_elements(self, session, elements):
        """查找元素之间的关系"""
        relationships = []
        
        # 检查所有客户之间的相似关系
        for i, elem1 in enumerate(elements):
            for elem2 in elements[i+1:]:
                # 检查客户-客户关系
                result = session.run("""
                    MATCH (c1:Customer {name: $elem1})-[r:SIMILAR_TASTE]-(c2:Customer {name: $elem2})
                    RETURN r
                """, elem1=elem1, elem2=elem2)
                record = result.single()
                if record:
                    relationships.append({
                        "type": "SIMILAR_TASTE",
                        "elements": [elem1, elem2],
                        "data": dict(record['r'])
                    })
                
                # 检查客户-产品关系
                result = session.run("""
                    MATCH (c:Customer {name: $customer})-[r:BOUGHT]->(p:Product {name: $product})
                    RETURN r
                """, customer=elem1, product=elem2)
                record = result.single()
                if not record:
                    result = session.run("""
                        MATCH (c:Customer {name: $customer})-[r:BOUGHT]->(p:Product {name: $product})
                        RETURN r
                    """, customer=elem2, product=elem1)
                    record = result.single()
                
                if record:
                    rel_data = dict(record['r'])
                    if elem1 in [r['name'] for r in session.run("MATCH (c:Customer) WHERE c.name=$name RETURN c", name=elem1).value()]:
                        customer = elem1
                        product = elem2
                    else:
                        customer = elem2
                        product = elem1
                    relationships.append({
                        "type": "BOUGHT",
                        "elements": [customer, product],
                        "data": rel_data
                    })
        
        return relationships


def analyze_elements(elements):
    """
    分析输入元素的关系和数据
    :param elements: 输入的元素数组，可以是客户名称、时间、商品名称
    :return: 分析结果
    """
    analyzer = RelationshipAnalyzer()
    try:
        result = analyzer.analyze_relationships(elements)
        return result
    finally:
        analyzer.close_connection()


# 示例用法
if __name__ == "__main__":
    # 示例：分析单个客户
    print("=== 单个客户分析 ===")
    result = analyze_elements(["李四"])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\\n=== 客户-产品关系分析 ===")
    result = analyze_elements(["李四", "笔记本电脑B"])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
    print("\\n=== 多元素分析 ===")
    result = analyze_elements(["李四", "王五", "笔记本电脑B"])
    print(json.dumps(result, indent=2, ensure_ascii=False))
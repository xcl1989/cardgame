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
            result = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=element)
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
            result = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=element)
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
                RETURN r LIMIT 1
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
            # 先确定哪个是客户，哪个是产品
            result1_customer = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem1)
            result1_product = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem1)
            result2_customer = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem2)
            result2_product = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem2)

            customer = None
            product = None

            # 检查 elem1 是客户，elem2 是产品的情况
            if result1_customer.single() and result2_product.single():
                customer = elem1
                product = elem2
            # 检查 elem1 是产品，elem2 是客户的情况
            elif result1_product.single() and result2_customer.single():
                customer = elem2
                product = elem1

            if customer and product:
                result = session.run("""
                    MATCH (c:Customer {name: $customer})-[r:BOUGHT]->(p:Product {name: $product})
                    RETURN r LIMIT 1
                """, customer=customer, product=product)
                record = result.single()
                if record:
                    return {
                        "type": "customer_product_relationship",
                        "elements": [customer, product],
                        "relationship": "BOUGHT",
                        "data": dict(record['r'])
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
                if result.single()['count'] > 0:
                    return {
                        "type": "product_time_relationship",
                        "elements": [elem1, str(year)],
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
                    if result.single()['count'] > 0:
                        return {
                            "type": "product_time_relationship",
                            "elements": [elem1, elem2],
                            "relationship": "SOLD_IN_MONTH",
                            "data": {"month": elem2}
                        }
            except ValueError:
                pass

            # 检查事件-客户关系
            result1_event = session.run("MATCH (e:Event {id: $id}) RETURN e LIMIT 1", id=int(elem1) if elem1.isdigit() else 0)
            result2_event = session.run("MATCH (e:Event {id: $id}) RETURN e LIMIT 1", id=int(elem2) if elem2.isdigit() else 0)

            event = None
            other_entity = None

            if result1_event.single() and result2_customer.single():
                event = elem1
                other_entity = elem2
                rel_type = "BY_CUSTOMER"
            elif result2_event.single() and result1_customer.single():
                event = elem2
                other_entity = elem1
                rel_type = "BY_CUSTOMER"
            elif result1_event.single() and result2_product.single():
                event = elem1
                other_entity = elem2
                rel_type = "OF_PRODUCT"
            elif result2_event.single() and result1_product.single():
                event = elem2
                other_entity = elem1
                rel_type = "OF_PRODUCT"
            elif result1_event.single() and (elem2.isdigit() or ("-" in elem2 and len(elem2) == 7)):
                event = elem1
                other_entity = elem2
                try:
                    int(elem2)  # 年份
                    rel_type = "IN_YEAR"
                except ValueError:
                    rel_type = "IN_MONTH"
            elif result2_event.single() and (elem1.isdigit() or ("-" in elem1 and len(elem1) == 7)):
                event = elem2
                other_entity = elem1
                try:
                    int(elem1)  # 年份
                    rel_type = "IN_YEAR"
                except ValueError:
                    rel_type = "IN_MONTH"

            if event and other_entity:
                # 检查事件与其他实体的关系
                if rel_type == "BY_CUSTOMER":
                    result = session.run("""
                        MATCH (e:Event {id: $event_id})-[:BY_CUSTOMER]->(c:Customer {name: $customer_name})
                        RETURN e
                    """, event_id=int(event), customer_name=other_entity)
                elif rel_type == "OF_PRODUCT":
                    result = session.run("""
                        MATCH (e:Event {id: $event_id})-[:OF_PRODUCT]->(p:Product {name: $product_name})
                        RETURN e
                    """, event_id=int(event), product_name=other_entity)
                elif rel_type == "IN_YEAR":
                    try:
                        year = int(other_entity)
                        result = session.run("""
                            MATCH (e:Event {id: $event_id})-[:IN_YEAR]->(y:Year {year: $year})
                            RETURN e
                        """, event_id=int(event), year=year)
                    except ValueError:
                        result = None
                elif rel_type == "IN_MONTH":
                    if "-" in other_entity and len(other_entity) == 7:
                        year, month = other_entity.split("-")
                        year = int(year)
                        month = int(month)
                        month_key = f"{year}-{month:02d}"
                        result = session.run("""
                            MATCH (e:Event {id: $event_id})-[:IN_MONTH]->(m:Month {month_key: $month_key})
                            RETURN e
                        """, event_id=int(event), month_key=month_key)
                    else:
                        result = None

                if result and result.single():
                    return {
                        "type": "event_entity_relationship",
                        "elements": [event, other_entity],
                        "relationship": rel_type,
                        "data": {"event_id": int(event)}
                    }

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
                result = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem)
                if result.single():
                    customers.append(elem)
                    continue
                
                # 检查是否为产品
                result = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem)
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
                    RETURN r LIMIT 1
                """, elem1=elem1, elem2=elem2)
                record = result.single()
                if record:
                    relationships.append({
                        "type": "SIMILAR_TASTE",
                        "elements": [elem1, elem2],
                        "data": dict(record['r'])
                    })

                # 检查客户-产品关系
                # 先判断元素类型
                result1_customer = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem1)
                result1_product = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem1)
                result2_customer = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem2)
                result2_product = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem2)

                customer = None
                product = None

                if result1_customer.single() and result2_product.single():
                    # elem1是客户，elem2是产品
                    customer = elem1
                    product = elem2
                elif result2_customer.single() and result1_product.single():
                    # elem2是客户，elem1是产品
                    customer = elem2
                    product = elem1

                if customer and product:
                    result = session.run("""
                        MATCH (c:Customer {name: $customer})-[r:BOUGHT]->(p:Product {name: $product})
                        RETURN r LIMIT 1
                    """, customer=customer, product=product)
                    record = result.single()
                    if record:
                        rel_data = dict(record['r'])
                        relationships.append({
                            "type": "BOUGHT",
                            "elements": [customer, product],
                            "data": rel_data
                        })

                # 检查客户-时间关系
                try:
                    year = int(elem2)
                    result = session.run("""
                        MATCH (c:Customer {name: $customer})-[:PURCHASED_IN_YEAR]->(y:Year {year: $year})
                        RETURN count(*) AS count
                    """, customer=elem1, year=year)
                    if result.single()['count'] > 0:
                        relationships.append({
                            "type": "PURCHASED_IN_YEAR",
                            "elements": [elem1, elem2],
                            "data": {"year": year}
                        })
                except ValueError:
                    pass

                try:
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
                            relationships.append({
                                "type": "PURCHASED_IN_MONTH",
                                "elements": [elem1, elem2],
                                "data": {"month": elem2}
                            })
                except ValueError:
                    pass

                # 检查产品-时间关系
                try:
                    year = int(elem1)
                    result = session.run("""
                        MATCH (p:Product {name: $product})-[:SOLD_IN_YEAR]->(y:Year {year: $year})
                        RETURN count(*) AS count
                    """, product=elem2, year=year)
                    if result.single()['count'] > 0:
                        relationships.append({
                            "type": "SOLD_IN_YEAR",
                            "elements": [elem2, elem1],
                            "data": {"year": year}
                        })
                except ValueError:
                    pass

                try:
                    if "-" in elem1 and len(elem1) == 7:
                        year, month = elem1.split("-")
                        year = int(year)
                        month = int(month)
                        month_key = f"{year}-{month:02d}"
                        result = session.run("""
                            MATCH (p:Product {name: $product})-[:SOLD_IN_MONTH]->(m:Month {month_key: $month_key})
                            RETURN count(*) AS count
                        """, product=elem2, month_key=month_key)
                        if result.single()['count'] > 0:
                            relationships.append({
                                "type": "SOLD_IN_MONTH",
                                "elements": [elem2, elem1],
                                "data": {"month": elem1}
                            })
                except ValueError:
                    pass

                # 检查事件关系
                try:
                    event_id = int(elem1)
                    result = session.run("MATCH (e:Event {id: $id}) RETURN e LIMIT 1", id=event_id)
                    if result.single():
                        # 检查事件与另一个元素的关系
                        result_customer = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem2)
                        result_product = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem2)

                        if result_customer.single():
                            # 事件-客户关系
                            result = session.run("""
                                MATCH (e:Event {id: $event_id})-[:BY_CUSTOMER]->(c:Customer {name: $customer_name})
                                RETURN e
                            """, event_id=event_id, customer_name=elem2)
                            if result.single():
                                relationships.append({
                                    "type": "BY_CUSTOMER",
                                    "elements": [str(event_id), elem2],
                                    "data": {"event_id": event_id}
                                })
                        elif result_product.single():
                            # 事件-产品关系
                            result = session.run("""
                                MATCH (e:Event {id: $event_id})-[:OF_PRODUCT]->(p:Product {name: $product_name})
                                RETURN e
                            """, event_id=event_id, product_name=elem2)
                            if result.single():
                                relationships.append({
                                    "type": "OF_PRODUCT",
                                    "elements": [str(event_id), elem2],
                                    "data": {"event_id": event_id}
                                })
                        else:
                            # 检查是否为时间
                            try:
                                year = int(elem2)
                                result = session.run("""
                                    MATCH (e:Event {id: $event_id})-[:IN_YEAR]->(y:Year {year: $year})
                                    RETURN e
                                """, event_id=event_id, year=year)
                                if result.single():
                                    relationships.append({
                                        "type": "IN_YEAR",
                                        "elements": [str(event_id), elem2],
                                        "data": {"event_id": event_id}
                                    })
                            except ValueError:
                                if "-" in elem2 and len(elem2) == 7:
                                    year, month = elem2.split("-")
                                    year = int(year)
                                    month = int(month)
                                    month_key = f"{year}-{month:02d}"
                                    result = session.run("""
                                        MATCH (e:Event {id: $event_id})-[:IN_MONTH]->(m:Month {month_key: $month_key})
                                        RETURN e
                                    """, event_id=event_id, month_key=month_key)
                                    if result.single():
                                        relationships.append({
                                            "type": "IN_MONTH",
                                            "elements": [str(event_id), elem2],
                                            "data": {"event_id": event_id}
                                        })
                except ValueError:
                    pass

                try:
                    event_id = int(elem2)
                    result = session.run("MATCH (e:Event {id: $id}) RETURN e LIMIT 1", id=event_id)
                    if result.single():
                        # 检查事件与另一个元素的关系
                        result_customer = session.run("MATCH (c:Customer {name: $name}) RETURN c LIMIT 1", name=elem1)
                        result_product = session.run("MATCH (p:Product {name: $name}) RETURN p LIMIT 1", name=elem1)

                        if result_customer.single():
                            # 事件-客户关系
                            result = session.run("""
                                MATCH (e:Event {id: $event_id})-[:BY_CUSTOMER]->(c:Customer {name: $customer_name})
                                RETURN e
                            """, event_id=event_id, customer_name=elem1)
                            if result.single():
                                relationships.append({
                                    "type": "BY_CUSTOMER",
                                    "elements": [elem1, str(event_id)],
                                    "data": {"event_id": event_id}
                                })
                        elif result_product.single():
                            # 事件-产品关系
                            result = session.run("""
                                MATCH (e:Event {id: $event_id})-[:OF_PRODUCT]->(p:Product {name: $product_name})
                                RETURN e
                            """, event_id=event_id, product_name=elem1)
                            if result.single():
                                relationships.append({
                                    "type": "OF_PRODUCT",
                                    "elements": [elem1, str(event_id)],
                                    "data": {"event_id": event_id}
                                })
                        else:
                            # 检查是否为时间
                            try:
                                year = int(elem1)
                                result = session.run("""
                                    MATCH (e:Event {id: $event_id})-[:IN_YEAR]->(y:Year {year: $year})
                                    RETURN e
                                """, event_id=event_id, year=year)
                                if result.single():
                                    relationships.append({
                                        "type": "IN_YEAR",
                                        "elements": [elem1, str(event_id)],
                                        "data": {"event_id": event_id}
                                    })
                            except ValueError:
                                if "-" in elem1 and len(elem1) == 7:
                                    year, month = elem1.split("-")
                                    year = int(year)
                                    month = int(month)
                                    month_key = f"{year}-{month:02d}"
                                    result = session.run("""
                                        MATCH (e:Event {id: $event_id})-[:IN_MONTH]->(m:Month {month_key: $month_key})
                                        RETURN e
                                    """, event_id=event_id, month_key=month_key)
                                    if result.single():
                                        relationships.append({
                                            "type": "IN_MONTH",
                                            "elements": [elem1, str(event_id)],
                                            "data": {"event_id": event_id}
                                        })
                except ValueError:
                    pass

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
    
    result = analyze_elements(["李四", "笔记本电脑B","2024"])
    print(json.dumps(result, indent=2, ensure_ascii=False))
    
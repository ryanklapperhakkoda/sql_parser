import re
import sqlparse

def clean_content(content):
    # Remove multiple whitespaces and newline characters
    cleaned_content = re.sub(r'\s+', ' ', content).replace("\n", "").strip()
    return cleaned_content

def extract_from_content(query):
    # Use regular expression to find the location of the main "FROM" keyword
    from_match = re.search(r'\bFROM\b', query)
    
    # If no match found, return an empty string
    if not from_match:
        return ""
    
    # Start after the matched "FROM"
    start_idx = from_match.end()
    end_idx = len(query)

    # Check for subsequent SQL clauses that might indicate the end of the "FROM" clause
    for clause in ["WHERE", "GROUP BY", "ORDER BY", "HAVING", "LIMIT", "OFFSET"]:
        clause_match = re.search(r'\b' + clause + r'\b', query[start_idx:])
        if clause_match:
            end_idx = start_idx + clause_match.start()
            break

    return query[start_idx:end_idx].strip()

def parse_sql(query):
    # Formatting the query
    formatted_query = sqlparse.format(query, reindent=True, keyword_case='upper')
    
    # Aggregations check
    aggregations = ["SUM", "AVG", "COUNT", "MAX", "MIN"]
    has_aggregations = any(agg in formatted_query.upper() for agg in aggregations)

    # Extract FROM contents
    from_content = extract_from_content(formatted_query)

    # Use the start of the FROM clause to extract SELECT contents
    from_start_idx = formatted_query.find(from_content)
    select_content = formatted_query[len("SELECT"):from_start_idx].strip() if from_start_idx != -1 else ""

    # Extract WHERE contents
    where_content = formatted_query.split('WHERE')[-1].split('GROUP BY')[0].split('ORDER BY')[0].strip() if 'WHERE' in formatted_query else ""

    return {
        "SELECT": clean_content(select_content).rstrip("FROM").strip(),
        "FROM": clean_content(from_content),
        "WHERE": clean_content(where_content),
        "HAS_AGGREGATIONS": has_aggregations
    }

def has_alias(query):
    # Check for 'column_name AS alias_name' pattern
    if re.search(r'\bAS\b', query, re.IGNORECASE):
        return True

    # Check for 'table_name alias' pattern
    table_alias_pattern = re.compile(r'\b(FROM|JOIN)\s+\w+\s+\w+\b', re.IGNORECASE)
    if table_alias_pattern.search(query):
        return True

    return False
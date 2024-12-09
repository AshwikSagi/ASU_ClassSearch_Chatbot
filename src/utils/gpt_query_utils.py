# import openai
# import sqlite3
# import pandas as pd
# import os

# # OpenAI API Configuration


# def generate_sql_query(user_input):
#     """Generate SQL query using GPT."""
#     try:
#         response = openai.ChatCompletion.create(
#     model="gpt-3.5-turbo",
#     messages=[{"role": "system", "content": "You are an SQL expert."},
#               {"role": "user", "content": user_input}],
#     max_tokens=150,
#     temperature=0.5,
# )
#         sql_query = response["choices"][0]["message"]["content"]
#         return sql_query.strip()
#     except Exception as e:
#         print(f"Error generating SQL query: {e}")
#         return None


# def query_database(db_path, sql_query):
#     """Query the database using the generated SQL query."""
#     try:
#         connection = sqlite3.connect(db_path)
#         results = pd.read_sql_query(sql_query, connection)
#         connection.close()
#         return results
#     except Exception as e:
#         return f"Error executing query: {e}"


# if __name__ == "__main__":
#     # Test Functions
#     test_input = "Show all courses taught by K. Selcuk Candan."
#     sql_query = generate_sql_query(test_input)
#     print("Generated SQL Query:")
#     print(sql_query)

#     if sql_query:
#         DB_PATH = "../database/class_search_bot.db"
#         results = query_database(DB_PATH, sql_query)
#         print("Query Results:")
#         print(results)
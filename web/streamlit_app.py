import os
import sqlite3
import pandas as pd
import streamlit as st

# Path to your SQLite database
DB_PATH = "/Users/ashwiksagi/Downloads/ASU_ClassSearch_Chatbot/database/class_search_bot.db"
# Function to fetch data from the database
def fetch_table_data(table_name):
    """Fetch all data from a specific table."""
    try:
        connection = sqlite3.connect(DB_PATH)
        query = f"SELECT * FROM {table_name}"
        data = pd.read_sql_query(query, connection)
        connection.close()
        return data
    except Exception as e:
        return f"Error fetching data from {table_name}: {e}"

def main():
    # Streamlit App Title
    st.title("ASU Class Search Virtual Assistant")
    st.markdown("### View Data from the Database Tables")

    # Show table options
    tables = ["courses", "instructors", "reviews"]
    selected_table = st.selectbox("Select a table to view:", tables)

    # Display the selected table's data
    if selected_table:
        st.markdown(f"### Data from `{selected_table}` table:")
        table_data = fetch_table_data(selected_table)
        
        if isinstance(table_data, str):  # If an error message is returned
            st.error(table_data)
        else:
            st.dataframe(table_data)

    # Query section
    st.markdown("### Execute a Custom SQL Query")
    custom_query = st.text_area("Enter your SQL query:")

    if st.button("Execute Query"):
        if custom_query.strip():
            try:
                connection = sqlite3.connect(DB_PATH)
                query_result = pd.read_sql_query(custom_query, connection)
                connection.close()

                st.markdown("#### Query Results:")
                st.dataframe(query_result)
            except Exception as e:
                st.error(f"Error executing query: {e}")
        else:
            st.warning("Please enter a valid SQL query.")

if __name__ == "__main__":
    main()
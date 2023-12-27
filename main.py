import streamlit as st
import snowflake.connector
from parse_tools import parse_sql
from datetime import datetime
from dotenv import load_dotenv
import os

load_dotenv()  # This loads the environment variables from .env

# Function to write data to Snowflake
def write_to_snowflake(data):
    # Establish connection to Snowflake
    conn = snowflake.connector.connect(
        user=os.environ.get('SNOWFLAKE_USER'),
        password=os.environ.get('SNOWFLAKE_PASSWORD'),
        account=os.environ.get('SNOWFLAKE_ACCOUNT'),
        warehouse=os.environ.get('SNOWFLAKE_WAREHOUSE'),
        database=os.environ.get('SNOWFLAKE_DATABASE'),
        schema=os.environ.get('SNOWFLAKE_SCHEMA')
    )


    # Create a cursor object
    cur = conn.cursor()

    # Insert data into Snowflake
    try:
        # Assuming 'data' is a tuple containing (email, query, parsed_query, is_correct, user_feedback, timestamp)
        sql = "INSERT INTO SQL_METRICS (email, sql_query, sql_query_parsed, is_correct, user_feedback, timestamp) VALUES (%s, %s, %s, %s, %s, %s)"
        cur.execute(sql, data)
        conn.commit()
    except Exception as e:
        st.error(f"Failed to write to Snowflake: {e}")
    finally:
        cur.close()
        conn.close()


def app():
    st.title("SQL Query Parser")

    # Initialize session state variables
    if 'parsed_query' not in st.session_state:
        st.session_state['parsed_query'] = None
    if 'feedback_submitted' not in st.session_state:
        st.session_state['feedback_submitted'] = False

    query = st.text_area("Enter your SQL query:", height=250)
    
    if st.button("Parse Query"):
        st.session_state['parsed_query'] = parse_sql(query)
        st.session_state['feedback_submitted'] = False

    if st.session_state['parsed_query']:
        st.subheader("Parsed Query")
        st.json(st.session_state['parsed_query'])

        # Feedback section
        feedback = st.radio("Is this parsing correct?", ('Yes', 'No'))
        user_feedback = ""
        if feedback == 'No':
            user_feedback = st.text_area("What wasn't correct?")

        # Button to submit feedback
        if st.button("Submit Feedback"):
            user_email = st.experimental_user['email']
            data_to_store = (user_email, query, str(st.session_state['parsed_query']), feedback == 'Yes', user_feedback, datetime.now())
            write_to_snowflake(data_to_store)
            st.session_state['feedback_submitted'] = True
            st.success("Feedback submitted!")

    if st.session_state['feedback_submitted']:
        st.write("Thank you for your feedback!")

if __name__ == "__main__":
    app()

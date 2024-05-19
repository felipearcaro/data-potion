import streamlit as st

from snowflake_client import SnowflakeClient
from model_manager import ModelManager


MODEL = {"Snowflake Arctic": ModelManager().get_arctic_response,
         "OpenAI": ModelManager().get_open_ai_response}


DDL = """

-- Create customers table
CREATE TABLE IF NOT EXISTS sales_data.customer_info.customers (
    customer_id INT PRIMARY KEY COMMENT 'Unique identifier for each customer',
    first_name STRING COMMENT 'First name of the customer',
    last_name STRING COMMENT 'Last name of the customer',
    email STRING
);

-- Create products table
CREATE TABLE IF NOT EXISTS sales_data.customer_info.products (
    product_id INT PRIMARY KEY COMMENT 'Unique identifier for each product',
    product_name STRING,
    price FLOAT COMMENT 'Price of the product'
);

-- Create orders table
-- Create orders table
CREATE TABLE IF NOT EXISTS sales_data.customer_info.orders (
    order_id INT PRIMARY KEY COMMENT 'Unique identifier for each order',
    customer_id INT COMMENT 'Foreign key referencing the customer_id in customers table',
    product_id INT,
    order_date DATE COMMENT 'Date of the order',
    FOREIGN KEY (customer_id) REFERENCES sales_data.customer_info.customers(customer_id),
    FOREIGN KEY (product_id) REFERENCES sales_data.customer_info.products(product_id)
);

"""


def main():

    st.set_page_config(page_title='Data Potion', page_icon=None,
                       layout="centered", initial_sidebar_state="auto", menu_items=None)
    st.title('Data Potion')
    st.subheader('Get insights from your data the right way')
    st.divider()

    st.write("First, let's connect your Snowflake account to get started:")

    user = st.text_input('Snowflake user')
    account = st.text_input('Snowflake account')
    password = st.text_input('Snowflake password', type='password')
    role = st.text_input('Snowflake role')
    warehouse = st.text_input('Snowflake warehouse')
    database = st.text_input('Snowflake database')

    st.write('Now, let\'s get to the fun part!')
    user_question = st.text_input(
        'Ask anything (really) about your data')

    user_role = st.radio(
        "What's your role?",
        ["Marketing rockstart", "Data geek"],
        captions=["I am only here for the viz!", "GET ME THE DATA!"])

    user_model = st.radio(
        "What magic tool should we use?",
        ["Snowflake Arctic", "OpenAI"],
        captions=["No brainer, right?", "Who? OpenAI? Never heard of it..."])

    if st.button('Go!'):
        try:
            metadata = SnowflakeClient(user=user, account=account, password=password,
                                       role=role, warehouse=warehouse, database=database).get_metadata()
            st.subheader("Connection successful! Let's get to work...")
            st.divider()
            if user_role == 'Marketing rockstart':
                st.write(
                    'You are a marketing rockstar! Let\'s get you some insights...')
                query = MODEL[user_model](
                    f'Based on this metadata {metadata} and these tables DDLs {DDL}, come up with a SQL query for this question {user_question}- make sure to use (schema_name.table_name) and answer ONLY with the SQL statement since it will be used to query snowflake directly.')
                formated_query = query.replace('```sql', '').replace('```', '')
                query_result = SnowflakeClient(user=user, account=account, password=password,
                                               role=role, warehouse=warehouse, database=database).execute_query(formated_query)
                query_result.reset_index(drop=True, inplace=True)
                if len(query_result) == 1:
                    st.write('Seems like you are looking for a single value...')
                    st.write(query_result.iloc[0, 0])
                else:
                    st.write('Nice! That requires a bar chart :)')
                    st.bar_chart(query_result)
            else:
                st.spinner('We are taking a look at your data metadata...')
                st.write(
                    'You are a Data Geek! We got you covered...')
                suggested_metadata = MODEL[user_model](
                    f'Based on this DDLs {DDL}, can you return a table containing table name, column name, current description/comment, suggested description/comment? Use the table name and column name to figure out the context of the description')
                st.subheader('Metadata analysis')
                st.write(
                    'It seems like your metadata could use some improvement. I mean, we will use it to give your customers the best answer after all!')
                st.write(suggested_metadata)
                st.divider()
                st.spinner('We are working on your query...')
                query = MODEL[user_model](
                    f'Based on this metadata {metadata} and these tables DDLs {DDL}, come up with a SQL query for this question - make sure to use (schema_name.table_name) and answer ONLY with the SQL statement since it will be used to query snowflake directly: {user_question}. Also, the SQL should contain either one or two columns only to be shown on a graph')
                st.subheader('Query suggestion')
                st.write('Here is the suggested SQL query to answer your question')
                formated_query = query.replace('```sql', '').replace('```', '')
                st.code(formated_query)
                query_result = SnowflakeClient(user=user, account=account, password=password,
                                               role=role, warehouse=warehouse, database=database).execute_query(formated_query)
                st.divider()
                st.subheader('Query result (Pandas dataframe)')
                st.dataframe(query_result)
                st.divider()
                st.subheader('Query performance analysis')
                performance = MODEL[user_model](
                    f"Based on this {query}- how could it be improved for better performance? Answer with a brief explanation.")
                st.write(performance)
                st.divider()
                st.subheader('Data lineage analysis')
                lineage = MODEL[user_model](
                    f"Can you create an asci art diagram showing the data lineage for the tables in the query? {formated_query} Please, only return the diagram, no extra text")
                st.code(lineage)

        except Exception as e:
            st.error(f'Connection failed! Please check your credentials {e}')


if __name__ == "__main__":
    main()

import streamlit as st
from dotenv import load_dotenv

from chains.expert_role.linkedin_profile_summarizer_with_parser_for_app import linkedin_summarizer

load_dotenv()  # Load environment variables


# Streamlit app configuration
st.set_page_config(
    page_title="Startup Business Summary App",
    page_icon="💼",
    layout="wide",
)

# App header and description
st.title("🚀 Startup Business Summary App")
st.markdown("""
This application generates a concise summary and interesting facts about startups or companies using their LinkedIn profiles.
Simply provide a query (e.g., company name) to get started.
""")

# Input form for the query
with st.form("query_form"):
    query = st.text_input("Enter LinkedIn query (e.g., company name):")
    submitted = st.form_submit_button("Generate Summary")

if submitted:
    if not query:
        st.warning("Please enter a valid query to proceed.")
    else:
        st.info("Fetching LinkedIn data and generating the summary...")

        # Generate summary
        try:
            # Fetch LinkedIn data
            company_summary, linkedin_data = linkedin_summarizer(query)

            result = linkedin_data

            st.success("Summary generated successfully!")

            # Display the summary
            st.subheader("📄 Company Summary")
            st.write(company_summary)  # Display the entire AI response

            # Display the company data
            st.subheader("📊 Company Data")
            st.write(linkedin_data)  # Display the entire AI response

        except Exception as e:
            st.error(f"An error occurred: {e}")

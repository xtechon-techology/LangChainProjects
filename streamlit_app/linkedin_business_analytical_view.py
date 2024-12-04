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

            # Inspect the types of the returned data
            # st.write("Debug Info: Type of `company_summary`", company_summary)
            # st.write("Debug Info: Type of `linkedin_data`", linkedin_data)

            st.success("Summary generated successfully!")

            # Access attributes or keys based on the structure
            summary_text = getattr(company_summary, "summary", "No summary available.") \
                if hasattr(company_summary, "summary") else company_summary.get("summary", "No summary available.")

            interesting_facts = getattr(company_summary, "facts", []) \
                if hasattr(company_summary, "facts") else company_summary.get("facts", [])

            company = linkedin_data.get("company", {})

            # Display company logo
            logo_url = company.get("logo")
            if logo_url:
                st.image(logo_url, width=200, caption=company.get("name", "Company Logo"))



            # Display summary
            st.subheader("📄 Company Summary")
            st.markdown(f"**Summary:** {summary_text}")

            # Display interesting facts
            st.subheader("💡 Interesting Facts")
            for fact in interesting_facts:
                st.markdown(f"- {fact}")

            # Display company metrics
            st.subheader("📊 Company Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Employee Count", company.get("employeeCount", "N/A"))
            with col2:
                st.metric("Follower Count", company.get("followerCount", "N/A"))
            with col3:
                st.metric("Founded Year", company.get("foundedOn", {}).get("year", "N/A"))

            # Display company details in a table

            st.subheader("📋 Company Details")
            details = {
                "Name": company.get("name"),
                "Industry": company.get("industry", "N/A"),
                "Headquarters": f"{company.get('headquarter', {}).get('city', 'N/A')}, {company.get('headquarter', {}).get('country', 'N/A')}",
                "Website": company.get("websiteUrl", "N/A"),
                "Phone": company.get("phone", "N/A"),
                "LinkedIn URL": company.get("linkedInUrl", "N/A"),
            }
            st.table(details.items())

            # Visualization for employee range
            employee_range = linkedin_data.get("employeeCountRange", {})
            if employee_range:
                st.subheader("📊 Employee Count Range")
                # Corrected bar chart visualization
                employee_data = {
                    "Category": ["Min", "Max"],
                    "Count": [employee_range.get("start", 0), employee_range.get("end", 0)],
                }
                st.bar_chart(employee_data)

        except Exception as e:
            st.error(f"An error occurred: {e}")

import streamlit as st
from langchain_community.document_loaders import WebBaseLoader
import traceback

from chains import Chain
from portfolio import Portfolio
from utils import clean_text


def create_streamlit_app(llm, portfolio, clean_text):
    st.title("📧 Cold Mail Generator")
    url_input = st.text_input("Enter a URL:", value="https://jobs.nike.com/job/R-33460")
    submit_button = st.button("Submit")

    if submit_button:
        try:
            loader = WebBaseLoader([url_input])
            data = clean_text(loader.load().pop().page_content)
            st.write("✅ Page loaded and cleaned")
            
            portfolio.load_portfolio()
            st.write("✅ Portfolio loaded")
            
            jobs = llm.extract_jobs(data)
            st.write(f"✅ Found {len(jobs)} job(s)")
            
            for job in jobs:
                st.write(f"📋 Processing job: {job.get('role', 'Unknown role')}")
                skills = job.get('skills', [])
                # Debug: Show what skills looks like
                st.write(f"🔍 Debug - Skills type: {type(skills)}, Value: {skills}")
                # Ensure skills is a list of strings
                if not skills:
                    skills = []
                elif not isinstance(skills, list):
                    skills = [str(skills)]
                else:
                    skills = [str(skill) for skill in skills]
                st.write(f"✅ Skills converted: {skills}")
                
                links = portfolio.query_links(skills)
                st.write(f"✅ Found {len(links)} link(s)")
                
                email = llm.write_mail(job, links)
                st.code(email, language='markdown')
        except Exception as e:
            st.error(f"An Error Occurred: {e}")
            st.error(f"Full traceback:\n{traceback.format_exc()}")


if __name__ == "__main__":
    chain = Chain()
    portfolio = Portfolio()
    st.set_page_config(layout="wide", page_title="Cold Email Generator", page_icon="📧")
    create_streamlit_app(chain, portfolio, clean_text)



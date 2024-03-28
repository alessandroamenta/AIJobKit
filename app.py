import streamlit as st
from generator import generate_documents

def main():
    st.title("Job Search Automation")

    # User input for Anthropic API key
    st.sidebar.title("Anthropic API Key")
    api_key = st.sidebar.text_input("Enter your Anthropic API key:")

    # User inputs
    resume = st.text_area("Paste your resume here:")
    job_description = st.text_area("Paste the job description here:")
    bio = st.text_area("Paste your bio/brief intro here:")

    if st.button("Generate Documents"):
        # Generate outputs
        output = generate_documents(resume, job_description, bio, api_key)
        if output:
            # Split the output into sections based on the unique headers
            sections = output.split("===")
            # Initialize an empty dictionary to keep track of the unique sections
            documents = {}
            for section in sections:
                # Further split each section into title and content
                title_content = section.split("\n", 1)
                if len(title_content) == 2:
                    title, content = title_content
                    title = title.strip()
                    # Store the content in the dictionary using the title as the key
                    documents[title] = content.strip()

            # Now create a text area for each document section
            for doc_title in ["TAILORED RESUME", "TAILORED COVER LETTER", "CUSTOMIZED COLD EMAIL"]:
                if doc_title in documents:
                    st.subheader(doc_title)
                    st.text_area("", value=documents[doc_title], height=None, key=doc_title, disabled=True)


if __name__ == "__main__":
    main()
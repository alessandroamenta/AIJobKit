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

    # Define the output section titles
    output_section_titles = {
        "Tailored Resume": "TAILORED RESUME",
        "Tailored Cover Letter": "TAILORED COVER LETTER",
        "Customized Cold Email": "CUSTOMIZED COLD EMAIL"
    }

    if st.button("Generate Documents"):
        # Generate outputs
        outputs = generate_documents(resume, job_description, bio, api_key)
        if outputs:
            for section_title, section_key in output_section_titles.items():
                if section_key in outputs and outputs[section_key].strip():
                    st.subheader(section_title)
                    st.code(outputs[section_key], language="text")

if __name__ == "__main__":
    main()
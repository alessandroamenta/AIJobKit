import streamlit as st
from generator import generate_documents

def main():
    st.title("Job Search Automation 🚀")

    # User input for API key and provider
    st.sidebar.title("API Settings")
    ai_provider = st.sidebar.selectbox("Select AI Provider", ["Anthropic", "OpenAI"])
    api_key = st.sidebar.text_input("Enter your API key:")


    # User inputs
    st.subheader("Paste your resume here 📝")
    resume = st.text_area("", height=200, placeholder="Your resume goes here...")

    st.subheader("Paste the job description here 📋")
    job_description = st.text_area("", height=200, placeholder="The job description goes here...")

    st.subheader("Paste your bio/brief intro here 🙋‍♂️")
    bio = st.text_area("", height=100, placeholder="Your bio or brief intro goes here. For example, you can add your LinkedIn summary or a short introduction about yourself.")

    # Additional user inputs
    st.sidebar.subheader("Additional Settings 🔧")
    formality_level = st.sidebar.select_slider("Formality Level for cover letter and email 📝", ["Super Casual", "Casual", "Neutral", "Formal", "Super Formal"], value="Neutral")
    additional_info = st.sidebar.text_area("Additional Information 💡", height=100, placeholder="Anything else you want the AI to consider or focus on?")

    # Define the output section titles
    output_section_titles = {
        "Tailored Resume": "TAILORED RESUME",
        "Tailored Cover Letter": "TAILORED COVER LETTER",
        "Customized Cold Email": "CUSTOMIZED COLD EMAIL"
    }

    if st.button("Generate Documents"):
        # Show loader while generating documents
        with st.spinner("GPT is cooking up the stuff to help you out, just a sec chief! 👨‍🍳"):
            # Generate outputs
            outputs = generate_documents(resume, job_description, bio, api_key, ai_provider, formality_level, additional_info)

        if outputs:
            for section_title, section_key in output_section_titles.items():
                if section_key in outputs and outputs[section_key].strip():
                    st.subheader(section_title)
                    st.code(outputs[section_key], language="text")

    # How to use section in the sidebar
    st.sidebar.subheader("How to Use 🤖")
    with st.sidebar.expander("Click here to see a quick guide!"):
        st.markdown("""
        - 📝 Copy and paste your resume into the designated area
        - 📋 Copy and paste the job description you're applying for
        - 🙋‍♂️ Provide a brief bio or introduction about yourself
        - 🔧 Select the desired formality level for the cover letter and email
        - 💡 Add any additional information you want the AI to consider
        - 🚀 Click the "Generate Documents" button and let the magic happen!
        """)

if __name__ == "__main__":
    main()
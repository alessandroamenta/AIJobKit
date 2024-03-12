import os
import anthropic
import logging
from dotenv import load_dotenv
from docx import Document

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def read_docx_file(file_path):
    try:
        doc = Document(file_path)
        full_text = []
        for para in doc.paragraphs:
            full_text.append(para.text)
        content = '\n'.join(full_text)
        logging.info(f"Successfully read content from {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading DOCX file content: {e}")
        return None

def read_text_file(file_path):
    try:
        with open(file_path, 'r') as file:
            content = file.read()
        logging.info(f"Successfully read content from {file_path}")
        return content
    except Exception as e:
        logging.error(f"Error reading text file content: {e}")
        return None

def generate_cold_messages(resume_content, email_template, recruiter_context, company_context, job_description_context):
    try:
        load_dotenv()  # Load environment variables from .env file
        api_key = os.getenv('ANTHROPIC_API_KEY')
        if not api_key:
            logging.error("ANTHROPIC_API_KEY not found in .env file")
            return None
        client = anthropic.Anthropic(api_key=api_key)
        logging.info("Successfully created Anthropic client")
        system_prompt = (
            "You are an expert cold caller in crafting emails and LinkedIn messages to recruiters that are engaging and grab attention. "
            "You help early career graduates get a nice job through cold calling and messaging."
        )
        prompt = (
            "Given the following context:\n\n"
            f"Resume:\n{resume_content}\n\n"
            f"Email Template and LinkedIn message Template:\n{email_linkedin_template}\n\n"
            f"Recruiter Context:\n{recruiter_context}\n\n"
            f"Job Description Context:\n{job_description_context}\n\n"
            f"Company Context:\n{company_context}\n\n"
            "Please generate a personalized cold email and a LinkedIn message that incorporate the following points:\n"
            "- The candidate is 24 years old and new to the Netherlands.\n"
            "- The candidate is a hard worker and wants to set themselves apart from other applicants.\n"
            "- The candidate built the email and message using AI to get the recruiter's attention.\n"
            "- The candidate is looking for a part-time position to get started, preferably in-person, but is open to full-time.\n"
            "- Include a brief compliment or appreciation for the recruiter.\n"
            "- Emphasize the candidate's work ethic and ability to figure things out, rather than their experience. Specifically, the candidate lived in 4 countries, started out from a small town in Sicily and figured things out, learned a few languages, got degrees from different countries, and now wants to build a life and career here in the Netherlands. They just want to pour all of their energy and time into building a good life here.\n"
            "- Express interest in a product or HR role.\n"
            "- Suggest having a call and mention that the candidate is the best fit for the position.\n"
            "- Convey the candidate's desire to grow and build their career.\n\n"
            "Please generate the cold email in a friendly yet professional tone. Remember to keep the email concise and to the point; recruiters don't have much time. Be approachable, human, relatable, and keep it simple, authentic, and genuine.\n\n"
            "Additionally, please ensure the following:\n"
            "- Personalize the message by using the recruiter's name, mentioning specific details about the company or role that excite the candidate, and explaining why the candidate would be a good fit.\n"
            "- Maintain a professional tone and appearance, including proper formatting, correct spelling and grammar, and a clear subject line that mentions the role the candidate is interested in.\n"
            "- Tailor the resume to highlight relevant skills and experiences for the specific job, showing that the candidate has taken the time to understand what the company is looking for and how they can contribute.\n"
            "- Keep the email concise while still personalizing and expressing enthusiasm. A brief, impactful message is more likely to be read and appreciated by busy recruiters.\n\n"
            "For the LinkedIn message, please generate it within a strict character limit of 300 characters, including spaces.\n\n"
            "Please format the output as follows:\n"
            "===COLD EMAIL===\n"
            "[Insert generated cold email here]\n\n"
            "===LINKEDIN MESSAGE===\n"
            "[Insert generated LinkedIn message here]\n\n"
        )
        logging.info(f"Sending the following prompt to the AI: {prompt}")
        response = client.messages.create(
            model="claude-3-opus-20240229",
            max_tokens=4000,
            system=system_prompt,
            temperature=0.5,
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        }
                    ]
                }
            ]
        )
        logging.info("Successfully generated cold messages")
        logging.info(f"AI Response: {response.content[0].text.strip()}")
        return response.content[0].text.strip()
    except Exception as e:
        logging.error(f"Error generating cold messages: {e}")
        return None

def save_to_file(cold_messages, file_name):
    try:
        with open(file_name, 'w') as file:
            file.write(cold_messages)
        logging.info(f"Successfully saved output to {file_name}")
    except Exception as e:
        logging.error(f"Error saving output to file: {e}")

if __name__ == "__main__":
    resume_content = read_docx_file("Alessandro_Amenta_Resume.docx")
    email_linkedin_template = read_text_file("./context/email_linkedin_template.txt")
    recruiter_context = read_text_file("./context/recruiter_context.txt")
    company_context = read_text_file("./context/company_context.txt")
    job_description_context = read_text_file("./context/jd.txt")

    cold_messages = generate_cold_messages(resume_content, email_linkedin_template, recruiter_context, company_context, job_description_context)


    save_to_file(cold_messages, "./output/output.txt")
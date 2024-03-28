import os
import logging
from dotenv import load_dotenv
import anthropic

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_documents(resume, job_description, bio, api_key):
    try:
        if not api_key:
            logging.error("Anthropic API key not provided")
            return None

        client = anthropic.Anthropic(api_key=api_key)
        logging.info("Successfully created Anthropic client")

        system_prompt = (
            "You are an expert in early career professional resume crafting, cover letter writing, and cold email composition. "
            "Your task is to generate a tailored resume, cover letter, and cold email for a job seeker based on the provided inputs."
        )

        prompt = (
            "Given the following information:\n\n"
            "Resume:\n{resume}\n\n"
            "Job Description:\n{job_description}\n\n"
            "Bio/Brief Intro:\n{bio}\n\n"
            "Please generate the following outputs:\n\n"
            "===TAILORED RESUME===\n"
            "Tailor the resume to highlight the candidate's relevant skills and experiences that match the job requirements. Optimize the structure and formatting to make it more visually appealing and ATS-friendly, while maintaining a similar length to the original resume.\n\n"
            "===TAILORED COVER LETTER===\n"
            "Craft a personalized cover letter that introduces the candidate, emphasizes their fit for the role, and encourages the recruiter to review the candidate's resume.\n\n"
            "===CUSTOMIZED COLD EMAIL===\n"
            "Generate a customized cold email that greets the recruiter, introduces the candidate, and invites the recruiter to consider the candidate for the role.\n\n"
            "Remember to keep the outputs concise, professional, and tailored to the specific job and candidate details provided."
        ).format(resume=resume, job_description=job_description, bio=bio)

        logging.info(f"Sending the following prompt to the AI: {prompt}")
        response = client.messages.create(
            model="claude-3-haiku-20240307",
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

        logging.info("Successfully generated the documents")
        logging.info(f"AI Response: {response.content[0].text.strip()}")
        return response.content[0].text.strip()

    except Exception as e:
        logging.error(f"Error generating documents: {e}")
        return None
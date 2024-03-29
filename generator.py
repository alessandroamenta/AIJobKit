import os
import logging
from dotenv import load_dotenv
import anthropic
import openai

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def generate_documents(resume, job_description, bio, api_key, ai_provider, formality_level, additional_info):
    try:
        if not api_key:
            logging.error("API key not provided")
            return None

        if ai_provider == "Anthropic":
            client = anthropic.Anthropic(api_key=api_key)
            logging.info("Successfully created Anthropic client")
        elif ai_provider == "OpenAI":
            openai.api_key = api_key
            logging.info("Successfully set OpenAI API key")
        else:
            logging.error("Invalid AI provider selected")
            return None

        system_prompt = (
            "You are an expert in early career professional resume crafting, cover letter writing, and cold email composition. "
            "Your task is to generate a tailored resume, cover letter, and cold email for a job seeker based on the provided inputs."
        )

        prompt = (
            "Given the following information for the candidate:\n\n"
            "Resume:\n{resume}\n\n"
            "Job Description:\n{job_description}\n\n"
            "Bio/Brief Intro:\n{bio}\n\n"
            "Formality Level for the cover letter: {formality_level}\n\n"
            "Additional Information: {additional_info}\n\n"
            "Please generate the following outputs:\n\n"
            "===TAILORED RESUME===\n"
            "Tailor the resume to highlight the candidate's relevant skills and experiences that match the job requirements. "
            "Optimize the structure and formatting to make it more visually appealing and ATS-friendly, while maintaining the order of the sections and the exact length as much as possible.\n\n"
            "===TAILORED COVER LETTER===\n"
            "Craft a personalized cover letter that introduces the candidate, emphasizes their fit for the role, and encourages the recruiter to review the candidate's resume. "
            "Include a brief introduction highlighting the candidate's interest and fit for the role, specific examples of how their skills and experiences align with the job requirements, "
            "and a call-to-action encouraging the recruiter to consider the candidate for the role. Adjust the formality level based on the provided preference.\n\n"
            "===CUSTOMIZED COLD EMAIL===\n"
            "Generate a customized cold email that greets the recruiter, introduces the candidate, and invites the recruiter to consider the candidate for the role. "
            "Adjust the formality level based on the provided preference.\n\n"
            "Remember to keep the outputs concise, professional, and tailored to the specific job and candidate details provided. "
            "THIS IS VERY IMPORTANT: Ensure that each output section is clearly delineated with the '===SECTION_TITLE===' format."
        ).format(resume=resume, job_description=job_description, bio=bio, formality_level=formality_level, additional_info=additional_info)

        logging.info(f"Sending the following prompt to the AI: {prompt}")

        if ai_provider == "Anthropic":
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
            logging.info("Successfully generated the documents using Anthropic")
            logging.info(f"AI Response: {response.content[0].text.strip()}")
            ai_response = response.content[0].text.strip()
        elif ai_provider == "OpenAI":
            response = openai.chat.completions.create(
                model="gpt-4-turbo-preview",
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": prompt},
                ],
                temperature=0.5,
            )
            logging.info("Successfully generated the documents using OpenAI")
            logging.info(f"AI Response: {response.choices[0].message.content.strip()}")
            ai_response = response.choices[0].message.content.strip()
        else:
            logging.error("Invalid AI provider selected")
            return None

        # Split the AI response into the individual outputs
        sections = ai_response.split("\n\n===")
        outputs = {}
        for section in sections:
            if section.strip():
                section_title = section.strip().split("\n")[0].strip("===")
                section_content = "\n".join(section.strip().split("\n")[1:])
                outputs[section_title] = section_content

        logging.info(f"Outputs: {outputs}")
        return outputs

    except Exception as e:
        logging.error(f"Error generating documents: {e}")
        return None
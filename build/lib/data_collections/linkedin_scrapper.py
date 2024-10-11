import requests
import json
from dotenv import load_dotenv
import os


# Create a function
#   Parameters: LinkedIn company url
#   Steps:
#     1. Load the environment variables
#     2. Get the API key from the environment variables
#     3. Check if the URL is valid
#     4. Extract the company name from the URL
#     5. Check if the company name json file exists
#     6. If the company name json file exists, return the data from the file
#     7. If the company name json file does not exist, call the Scrapin API
#     8. Save the data in the company name json file
#     9. Return the data from the API
#     10. Print the data
def get_linkedin_company_data(linkedin_url, mock=False):
    #     1. Load the environment variables
    load_dotenv()
    #     2. Get the API key from the environment variables
    key = os.environ["SCRAPIN_API_KEY"]

    if mock:
        with open(f"data-intelligence-llc.json", "r") as file:
            data = json.load(file)
            return data
    else:
        #     3. Check if the URL is valid
        is_url_valid = linkedin_url.startswith("https://www.linkedin.com/company/")
        if not is_url_valid:
            return f"Invalid LinkedIn URL [{linkedin_url}]"

        #     4. Extract the company name from the URL
        #        Example: https://www.linkedin.com/company/data-intelligence-llc/ => data-intelligence-llc
        company_name = linkedin_url.split("/")[-2]

        #     5. Check if the company name json file exists
        is_file_exists = os.path.exists(f"{company_name}.json")

        #     6. If the company name json file exists, return the data from the file
        if is_file_exists:
            print(f"Reading data from {company_name}.json")
            with open(f"{company_name}.json", "r") as file:
                data = json.load(file)
                return data
        else:
            #     7. If the company name json file does not exist, call the Scrapin API
            apiEndPoint = f"https://api.scrapin.io/enrichment/company?apikey={key}&linkedinUrl={linkedin_url}"
            response = requests.request("GET", apiEndPoint)

            #     8. Save the data in the company name json file
            with open(f"{company_name}.json", "w") as file:
                file.write(response.text)

            #     9. Return the data from the API
            return response.text


# Main function
if __name__ == "__main__":
    #     10. Print the data
    linkedin_url = "https://www.linkedin.com/company/data-intelligence-llc/"

    # company_name = linkedin_url.split("/")[-2]
    # print(f"Company Name: {company_name}")
    data = get_linkedin_company_data(linkedin_url, mock=True)
    print(data)

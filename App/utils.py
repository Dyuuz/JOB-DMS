from .models import CustomUser
from urllib.parse import urlparse
from datetime import datetime
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
import google.generativeai as genai
import time
from dotenv import load_dotenv
import os
load_dotenv()

@login_required
def suggest_cover_letter(request):
    user = request.user
    typed_text = request.GET.get('text', '')

    api_key = os.getenv('API_KEY')
    genai.configure(api_key=api_key)

    model = genai.GenerativeModel('gemini-1.5-flash-latest')

    # Generate content (e.g. for a cover letter)
    suggestion = f"Based on this profile provided, use the {typed_text}, {user.userprofile.work_experience}years of experience, i have work experience in this company {user.userprofile.company_name} with the job role - {user.userprofile.job_description} and this is about me {user.userprofile.bio}, with name as {user.full_name} and email as {user.email}, use a professional tone to write a cover letter body for the job application. The cover letter should be concise, engaging, and tailored to the user's details. It should highlight my skills, about me and experiences relevant to the position."
    response = model.generate_content(suggestion)
    print(response)
    time.sleep(5)
    return JsonResponse({'suggestion': response.text})

def get_company_name(full_name):
    """
    Generate a company name from the user's full name.
    This function takes the user's full name, splits it into parts,
    and returns the first letter of each part in uppercase.

    Args:
        user (CustomUser): The user object containing the full name.

    Returns:
        list: A list of uppercase initials from the user's full name.
    """
    company_name = full_name.split()
    name_list = [name[0].upper() for name in company_name]
    name_list_joined = ''.join(name_list[:2])
    return name_list_joined

def extract_site_name(url):
    parsed_url = urlparse(url)
    domain = parsed_url.netloc or parsed_url.path
    parts = domain.split('.')

    # Handles domains like google.com or www.google.com
    if len(parts) >= 2:
        if parts[0] == 'www':
            return parts[1].title()
        return parts[0].title()
    return domain  # fallback if it doesn't split properly

def get_time_countdown(target_date_str):
    target = target_date_str.split('+')[0]

    # Convert the string to a datetime object using strptime
    target_date = datetime.strptime(target, '%Y-%m-%d %H:%M:%S.%f')
    current_date = datetime.now()

    time_difference = current_date - target_date

    # Get the total hours difference (total_seconds() / 3600)
    hours_difference = time_difference.total_seconds() / 60
    time_diff = hours_difference
    time = f"{time_diff:.0f}"

    return time

def get_download_url(cloudinary_url, filename):
    """
    Adds 'fl_attachment' to a Cloudinary raw file URL to force download.
    """
    if 'upload/' in cloudinary_url:
        return cloudinary_url.replace('upload/', f'upload/fl_attachment:{filename}/')
    return cloudinary_url

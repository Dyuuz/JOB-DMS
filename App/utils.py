from .models import CustomUser
from urllib.parse import urlparse
from datetime import datetime


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
            return parts[1]
        return parts[0]
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

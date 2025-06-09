from .models import CustomUser


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

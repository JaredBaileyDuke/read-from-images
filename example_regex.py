import re

def find_duke_emails(text):
    """
    Find all Duke email addresses in the given text.

    Args:
        text (str): The input text

    Returns:
        list: A list of Duke email addresses
    """
    duke_email_pattern = r'\b[A-Za-z0-9._%+-]+@duke\.edu\b'
    return re.findall(duke_email_pattern, text)

def find_websites(text):
    """
    Find all website URLs in the given text.

    Args:
        text (str): The input text

    Returns:
        list: A list of website URLs
    """
    website_pattern = r'\bhttps?://[^\s/$.?#].[^\s]*\b'
    return re.findall(website_pattern, text)

def find_phone_numbers(text):
    """
    Find all phone numbers in the given text.

    Args:
        text (str): The input text

    Returns:
        list: A list of phone numbers
    """
    phone_number_pattern = r'\b\+?1?[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b'
    return re.findall(phone_number_pattern, text)

if __name__ == "__main__":
    sample_text = """
    Contact us at support@duke.edu or visit our website at https://www.duke.edu.
    You can also call us at (919) 684-8111 or +1-919-684-8111.
    """

    duke_emails = find_duke_emails(sample_text)
    websites = find_websites(sample_text)
    phone_numbers = find_phone_numbers(sample_text)

    print("Duke Emails:", duke_emails)
    print("Websites:", websites)
    print("Phone Numbers:", phone_numbers)

# 4.read innate file and parse the strings to count how many times an email address is found

import re
from collections import defaultdict

def count_emails(filename):
    """Count the occurrences of each email address in the given file."""
    email_counts = defaultdict(int)  # Use defaultdict to automatically handle missing keys

    # Define a regex pattern for validating email addresses
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Read the file line by line
    with open(filename, 'r') as file:
        for line in file:
            # Find all email addresses in the line
            emails = re.findall(email_pattern, line)
            # Increment counts for each found email
            for email in emails:
                email_counts[email] += 1

    return email_counts


def find_specific_email(filename, target_email):
    """Find the occurrence count of a specific email address in the given file."""
    # Validate the target email with the same regex pattern
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'

    # Check if the target email matches the pattern
    if not re.match(email_pattern, target_email):
        return 0

    count = 0
    # Read the file line by line
    with open(filename, 'r') as file:
        for line in file:
            # Find all email addresses in the line
            emails = re.findall(email_pattern, line) # what if i dont want to use regex package and code manually
            # Increment count if the target email is found
            count += emails.count(target_email)

    return count

import re
from collections import defaultdict



def count_email(filename):

	email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
	email_count = defaultdict(int)

	with open(filename,'r') as file:
		for line in file:
			emails = re.findall(email_pattern,line)
			for email in emails:
				email_count[email] +=1

	return email_count






def main():
    filename = input("Enter the filename: ")
    emailtofind = input("Enter the Email, you want to search in the file:")
    email_counts = count_emails(filename)
    counts = find_specific_email(filename,emailtofind)
    print("count_email====>>>",count_email("email.txt"))
    print(f"count of {emailtofind} in the {filename}:{counts}")
    # Print the email counts
    for email, count in email_counts.items():
        print(f"{email}: {count}")

if __name__ == "__main__":
    main()

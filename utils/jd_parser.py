import re


def extract_email(text):

    emails = re.findall(
        r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}",
        text
    )

    return emails[0] if emails else None


def extract_company(text):

    patterns = [
        r"Company\s*:\s*(.+)",
        r"🏢\s*Company\s*:\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None


def extract_role(text):

    patterns = [
        r"Position\s*:\s*(.+)",
        r"Role\s*:\s*(.+)"
    ]

    for pattern in patterns:

        match = re.search(
            pattern,
            text,
            re.IGNORECASE
        )

        if match:
            return match.group(1).strip()

    return None
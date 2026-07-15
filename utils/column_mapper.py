def find_column(df, keywords):

    for col in df.columns:

        col_lower = str(col).strip().lower()

        for keyword in keywords:

            if keyword.lower() in col_lower:
                return col

    return None


def detect_columns(df):

    return {

        "company": find_column(
            df,
            [
                "company",
                "company name",
                "organization",
                "organisation",
                "employer",
                "startup",
                "org",
                "firm",
                "client"
            ]
        ),

        "email": find_column(
            df,
            [
                "email",
                "mail",
                "email id",
                "email address",
                "mail id",
                "contact email",
                "recruiter email",
                "official email"
            ]
        ),

        "name": find_column(
            df,
            [
                "name",
                "full name",
                "first name",
                "last name",
                "recruiter",
                "recruiter name",
                "contact",
                "contact person",
                "hr",
                "hr name",
                "talent",
                "employee",
                "person"
            ]
        ),

        "role": find_column(
            df,
            [
                "role",
                "position",
                "job title",
                "designation",
                "title"
            ]
        ),

        "jd": find_column(
            df,
            [
                "jd",
                "job description",
                "description"
            ]
        )

    }
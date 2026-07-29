DOCUMENT_KEYWORDS = {
    "resume",
    "cv",
    "cgpa",
    "college",
    "university",
    "education",
    "internship",
    "project",
    "projects",
    "skills",
    "experience",
    "certification",
    "certificate",
    "github",
    "linkedin",
    "btech",
    "diploma",
    "marks",
    "percentage",
    "technical skills"
}


def should_use_rag(question):

    question = question.lower()

    if "my" in question:
        return True

    for keyword in DOCUMENT_KEYWORDS:
        if keyword in question:
            return True

    return False
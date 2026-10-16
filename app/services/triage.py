from app.schemas import EmailTriageResult


URGENT_TERMS = (
    "urgent",
    "asap",
    "immediately",
    "overdue",
    "deadline today",
    "account suspended",
)

REPLY_TERMS = (
    "please confirm",
    "let me know",
    "can you",
    "could you",
    "what do you think",
    "please reply",
)

BOOKKEEPING_TERMS = (
    "invoice",
    "receipt",
    "payment",
    "reimbursement",
    "statement",
    "expense",
)


def triage_email(subject: str, body: str) -> EmailTriageResult:
    """Return a transparent, keyword-based email triage suggestion."""
    text = f"{subject}\n{body}".lower()

    if any(term in text for term in URGENT_TERMS):
        priority = "urgent"
        suggested_action = "Review promptly and check for a deadline."
    elif any(term in text for term in REPLY_TERMS):
        priority = "high"
        suggested_action = "Review and decide whether a reply is needed."
    else:
        priority = "normal"
        suggested_action = "Review when convenient."

    category = (
        "bookkeeping"
        if any(term in text for term in BOOKKEEPING_TERMS)
        else "general"
    )
    needs_reply = any(term in text for term in REPLY_TERMS)
    summary_text = " ".join(body.split()) or subject

    return EmailTriageResult(
        category=category,
        priority=priority,
        needs_reply=needs_reply,
        summary=summary_text[:240],
        suggested_action=suggested_action,
    )

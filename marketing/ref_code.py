"""Company code for links in outreach emails, so the growth dashboard can show which business clicked.

    python ref_code.py "Rago Arts" consignorpayables@ragoarts.com   ->  e-rago-arts-3f2a

The code is "e-" + a short slug of the company name + 4 hex characters from the email address, so the
same recipient always gets the same code and two contacts at one company stay distinct. Add it to every
link to our own sites in that recipient's email as  &ref=<code>  (after the existing utm_ parameters).
Never put it in Microsoft Store links. Record the code in the prospect CSV next to the send.
"""
import hashlib
import re
import sys


def ref_code(company: str, email: str) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", company.lower()).strip("-")
    slug = re.sub(r"-(llc|inc|co|corp|ltd|company|the)$", "", slug)[:30].strip("-") or "contact"
    tail = hashlib.sha1(email.strip().lower().encode()).hexdigest()[:4]
    return f"e-{slug}-{tail}"


if __name__ == "__main__":
    print(ref_code(sys.argv[1], sys.argv[2]))

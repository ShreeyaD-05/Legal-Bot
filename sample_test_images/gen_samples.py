"""Generate 3 sample legal document images for LegalBot upload testing."""
from PIL import Image, ImageDraw, ImageFont
import os, textwrap

OUT = os.path.dirname(os.path.abspath(__file__))
W, H = 900, 1200
BG = (255, 255, 255)
INK = (20, 20, 40)
GRAY = (100, 100, 120)
LINE = (180, 180, 200)


def new_canvas(hdr_color=(30, 58, 95)):
    img = Image.new("RGB", (W, H), BG)
    draw = ImageDraw.Draw(img)
    draw.rectangle([0, 0, W, 56], fill=hdr_color)
    draw.rectangle([0, H - 40, W, H], fill=hdr_color)
    return img, draw


def tf(size):
    for path in [
        "C:/Windows/Fonts/arialbd.ttf",
        "C:/Windows/Fonts/arial.ttf",
        "C:/Windows/Fonts/calibrib.ttf",
        "C:/Windows/Fonts/calibri.ttf",
    ]:
        try:
            return ImageFont.truetype(path, size)
        except Exception:
            pass
    return ImageFont.load_default()


def wrap_draw(draw, text, x, y, font, max_w, ink, line_h=None):
    cpl = max(1, max_w // (font.size // 2 + 1))
    lines = []
    for para in text.split("\n"):
        lines += textwrap.wrap(para, width=cpl) if para.strip() else [""]
    lh = line_h or int(font.size * 1.45)
    for ln in lines:
        draw.text((x, y), ln, font=font, fill=ink)
        y += lh
    return y


def hline(draw, y, pad=60):
    draw.line([(pad, y), (W - pad, y)], fill=LINE, width=1)


def footer(draw, hdr_color):
    draw.text(
        (30, H - 26),
        "EDUCATIONAL DOCUMENT  |  LEGALBOT TEST SAMPLE",
        font=tf(10),
        fill=(200, 220, 255),
    )


# ═══════════════════════════════════════════════════════════════
#  DOC 1  —  Residential Rent Agreement
# ═══════════════════════════════════════════════════════════════
COLOR1 = (30, 58, 95)
img, d = new_canvas(COLOR1)
d.text((30, 14), "RESIDENTIAL RENT AGREEMENT", font=tf(20), fill=(255, 255, 255))
d.text(
    (30, 36),
    "Model Tenancy Act 2021  |  Ref: MTA/2026/DL/4471",
    font=tf(11),
    fill=(180, 210, 255),
)

y = 80
d.text((W // 2 - 190, y), "RESIDENTIAL LEASE AGREEMENT", font=tf(22), fill=INK)
y += 36
d.text(
    (W // 2 - 130, y),
    "New Delhi, India  —  01 November 2026",
    font=tf(13),
    fill=GRAY,
)
y += 40
hline(d, y)
y += 18

sections = [
    (
        "PARTIES",
        (
            "LANDLORD: Mr. Arun Mehta, S/o Late R.K. Mehta, H-12, Lajpat Nagar-II,"
            " New Delhi 110024.\n"
            "TENANT: Ms. Priya Sharma, D/o S.P. Sharma, 204-B, Vasant Vihar,"
            " New Delhi 110057."
        ),
    ),
    (
        "PROPERTY",
        (
            "First-floor apartment at A-304, Green Valley Apartments, Sector 14,"
            " Dwarka, New Delhi 110078.\n"
            "Carpet Area: 920 sq.ft. | 2 BHK | Furnished."
        ),
    ),
    (
        "TERM & RENT",
        (
            "Commencement: 01 November 2026.  Duration: 11 months.\n"
            "Monthly Rent: INR 28,000/- payable by 5th of each month via NEFT/UPI."
        ),
    ),
    (
        "SECURITY DEPOSIT  (Sec.11, Model Tenancy Act 2021)",
        (
            "Security Deposit: INR 56,000/- (2 months rent) received 28-Oct-2026.\n"
            "Refund Timeline: Deposit refunded within 30 days of vacating, after\n"
            "deducting only: (i) rent arrears, (ii) structural damage costs with bills.\n"
            "Normal wear and tear (minor scuffs, faded paint) shall NOT be deducted."
        ),
    ),
    (
        "NOTICE TO QUIT  (Sec.106, Transfer of Property Act 1882)",
        "Either party may terminate by giving 30 days written notice via registered post.",
    ),
    (
        "GENERAL CONDITIONS",
        (
            "1. Tenant shall not sublet without prior written consent of Landlord.\n"
            "2. Landlord shall not cut utilities without a valid court order.\n"
            "3. Pets permitted only with Landlord written approval.\n"
            "4. Governed by laws of the National Capital Territory of Delhi."
        ),
    ),
]

for heading, body in sections:
    d.text((60, y), heading, font=tf(14), fill=COLOR1)
    y += 20
    hline(d, y, 60)
    y += 10
    y = wrap_draw(d, body, 60, y, tf(12), 780, INK) + 14

y += 10
d.text((60, y), "Landlord Signature: ________________________", font=tf(12), fill=INK)
d.text((500, y), "Tenant Signature: ________________________", font=tf(12), fill=INK)
y += 26
d.text((60, y), "Date: ________________", font=tf(12), fill=GRAY)
d.text((500, y), "Date: ________________", font=tf(12), fill=GRAY)
footer(d, COLOR1)
img.save(os.path.join(OUT, "01_rent_agreement.png"))
print("Saved 01_rent_agreement.png")


# ═══════════════════════════════════════════════════════════════
#  DOC 2  —  Non-Disclosure Agreement
# ═══════════════════════════════════════════════════════════════
COLOR2 = (10, 80, 60)
img, d = new_canvas(COLOR2)
d.text(
    (30, 14),
    "MUTUAL NON-DISCLOSURE AGREEMENT",
    font=tf(20),
    fill=(255, 255, 255),
)
d.text(
    (30, 36),
    "Indian Contract Act 1872  |  Ref: NDA/2026/MH/0089",
    font=tf(11),
    fill=(180, 255, 210),
)

y = 78
d.text((W // 2 - 205, y), "MUTUAL NON-DISCLOSURE AGREEMENT", font=tf(22), fill=INK)
y += 36
d.text(
    (W // 2 - 160, y),
    "Effective Date: 15 October 2026  |  Mumbai, Maharashtra",
    font=tf(13),
    fill=GRAY,
)
y += 40
hline(d, y)
y += 16

nda_sections = [
    (
        "PARTIES",
        (
            "PARTY A: NovaTech Solutions Pvt. Ltd., CIN: U72900MH2019PTC321456,\n"
            "Level 9, One BKC, Bandra Kurla Complex, Mumbai 400051.\n"
            "PARTY B: Mr. Vikram Desai, 14, Marine Lines, Mumbai 400002."
        ),
    ),
    (
        "PURPOSE",
        (
            "Parties intend to explore a business collaboration for AI-based legal"
            " research software.\n"
            "Both parties may disclose confidential information solely to evaluate"
            " this engagement."
        ),
    ),
    (
        "CONFIDENTIAL INFORMATION",
        (
            "Includes: source code, algorithms, customer lists, financial projections,"
            " trade secrets.\n"
            "EXCLUSIONS (ICA Sec.10 & 27):\n"
            "(a) Information already in public domain without breach of this Agreement;\n"
            "(b) Independently developed without reference to disclosed data;\n"
            "(c) Lawfully received from a third party without restriction;\n"
            "(d) Disclosure required by court order or statutory authority."
        ),
    ),
    (
        "OBLIGATIONS",
        (
            "1. Hold Confidential Information in strict confidence.\n"
            "2. Use information solely for the Purpose stated above.\n"
            "3. No disclosure to third parties without prior written consent.\n"
            "4. Standard of care: not less than the care used for own confidential data."
        ),
    ),
    ("TERM", "This Agreement shall remain in force for 3 years from the Effective Date."),
    (
        "REMEDIES  (Specific Relief Act 1963, Sec.38-39)",
        (
            "Breach entitles the aggrieved party to:\n"
            "(i) Interim and permanent injunctive relief;\n"
            "(ii) Damages per Section 73, Indian Contract Act 1872;\n"
            "(iii) Recovery of legal costs and attorney fees."
        ),
    ),
    (
        "GOVERNING LAW",
        (
            "Governed by laws of India. Disputes subject to exclusive jurisdiction"
            " of courts in Mumbai."
        ),
    ),
]

for heading, body in nda_sections:
    d.text((60, y), heading, font=tf(14), fill=COLOR2)
    y += 20
    hline(d, y, 60)
    y += 10
    y = wrap_draw(d, body, 60, y, tf(12), 780, INK) + 14

y += 8
d.text(
    (60, y),
    "Party A Authorised Signatory: ____________________",
    font=tf(12),
    fill=INK,
)
d.text((60, y + 22), "Designation: __________________________", font=tf(12), fill=GRAY)
d.text(
    (500, y), "Party B Signature: ____________________", font=tf(12), fill=INK
)
d.text((500, y + 22), "Name: __________________________", font=tf(12), fill=GRAY)
footer(d, COLOR2)
img.save(os.path.join(OUT, "02_nda_agreement.png"))
print("Saved 02_nda_agreement.png")


# ═══════════════════════════════════════════════════════════════
#  DOC 3  —  Employment Termination Letter
# ═══════════════════════════════════════════════════════════════
COLOR3 = (100, 20, 20)
img, d = new_canvas(COLOR3)
d.text((30, 14), "EMPLOYMENT TERMINATION LETTER", font=tf(20), fill=(255, 255, 255))
d.text(
    (30, 36),
    "Shops & Establishments Act  |  Ref: HR/TERM/2026/BLR/117",
    font=tf(11),
    fill=(255, 200, 200),
)

y = 78
d.text((W // 2 - 175, y), "TERMINATION OF EMPLOYMENT", font=tf(22), fill=COLOR3)
y += 36
d.text((W // 2 - 100, y), "Date: 25 October 2026", font=tf(13), fill=GRAY)
y += 40
hline(d, y)
y += 18

d.text((60, y), "To,", font=tf(13), fill=INK)
y += 22
d.text((60, y), "Mr. Rahul Krishnan", font=tf(14), fill=INK)
y += 20
d.text((60, y), "Senior Software Engineer  (Employee ID: BLR-4892)", font=tf(12), fill=GRAY)
y += 20
d.text((60, y), "Horizon Infotech Pvt. Ltd., Whitefield, Bengaluru 560066", font=tf(12), fill=GRAY)
y += 30
hline(d, y)
y += 18

d.text((60, y), "Subject: Termination of Employment — Notice & Final Settlement", font=tf(14), fill=COLOR3)
y += 28

body1 = (
    "Dear Mr. Krishnan,\n\n"
    "This letter serves as formal notice that your employment with Horizon Infotech Pvt. Ltd.\n"
    "is terminated effective 25 November 2026, i.e., after completion of the 30-day notice\n"
    "period as stipulated in your Employment Agreement dated 12 March 2022 and as required\n"
    "under the Karnataka Shops and Commercial Establishments Act, 1961."
)
y = wrap_draw(d, body1, 60, y, tf(12), 780, INK) + 14

d.text((60, y), "GROUNDS FOR TERMINATION", font=tf(14), fill=COLOR3)
y += 20
hline(d, y, 60)
y += 10

body2 = (
    "The termination is on account of organisational restructuring and role redundancy.\n"
    "This is NOT a disciplinary termination. No misconduct is alleged against the employee."
)
y = wrap_draw(d, body2, 60, y, tf(12), 780, INK) + 14

d.text((60, y), "FINAL SETTLEMENT", font=tf(14), fill=COLOR3)
y += 20
hline(d, y, 60)
y += 10

body3 = (
    "1. Notice Pay:          INR 1,12,000/- (1 month gross salary in lieu of notice).\n"
    "2. Earned Leave:        INR   28,000/- (14 days accrued and un-availed leave encashment).\n"
    "3. Gratuity (Payment of Gratuity Act 1972):  INR 1,56,000/- (4 years 7 months service).\n"
    "4. Provident Fund:      Full PF balance to be transferred to employee account.\n"
    "5. Relieving Letter:    Issued on last working day (25 November 2026).\n"
    "6. Non-Compete Clause:  Note — any post-employment non-compete clause in your contract\n"
    "   is VOID under Section 27 of the Indian Contract Act, 1872 and is not enforceable."
)
y = wrap_draw(d, body3, 60, y, tf(12), 780, INK) + 14

body4 = (
    "Please return all company assets (laptop, access cards, documents) by 25 November 2026.\n"
    "Your full-and-final settlement will be processed within 30 working days of the last date."
)
y = wrap_draw(d, body4, 60, y, tf(12), 780, INK) + 20

d.text((60, y), "Authorised Signatory", font=tf(13), fill=INK)
y += 20
d.text((60, y), "Ms. Ananya Rao  |  HR Director, Horizon Infotech Pvt. Ltd.", font=tf(12), fill=GRAY)
y += 20
d.text((60, y), "Date: 25 October 2026", font=tf(12), fill=GRAY)

footer(d, COLOR3)
img.save(os.path.join(OUT, "03_termination_letter.png"))
print("Saved 03_termination_letter.png")
print("\nAll 3 sample images generated in:", OUT)

"""
sample_documents.py — Legal knowledge base for grounding agent responses.

This module defines a curated library of legal document summaries across five
key domains:
  1. Tenancy & Residential Leases
  2. Non-Disclosure Agreements (NDAs)
  3. Intellectual Property
  4. Employment Law
  5. Consumer Protection

The search_legal_library tool uses keyword matching against this data.
Each document has:
  - id       : unique identifier
  - title    : display name used in 'sources' list
  - domain   : legal classification tag
  - keywords : list of terms that trigger this document in searches
  - content  : the actual legal text / summary
"""

from typing import List, Dict, Any

# ─────────────────────────────────────────────────────────────
#  Legal Document Library
# ─────────────────────────────────────────────────────────────

LEGAL_DOCUMENTS: List[Dict[str, Any]] = [

    # ── 1. TENANCY ────────────────────────────────────────────

    {
        "id": "tenancy_001",
        "title": "Residential Lease & Security Deposits — Statutory Guidelines",
        "domain": "Tenancy Law",
        "keywords": [
            "security deposit", "deposit", "deduction", "cleaning", "damages",
            "itemized", "itemization", "landlord", "tenant", "lease", "rent",
            "eviction", "notice", "habitability", "repair", "maintenance",
            "move-out", "move out", "rental", "residential"
        ],
        "content": """
RESIDENTIAL LEASE & SECURITY DEPOSIT — STATUTORY GUIDELINES

1. Security Deposit Limits
   - Most jurisdictions cap security deposits at 1–2 months' rent for unfurnished units
     and 2–3 months for furnished units.
   - The landlord must hold the deposit in a separate, interest-bearing account in many states.

2. Permissible Deductions
   Landlords MAY deduct from the security deposit for:
   - Unpaid rent or late fees
   - Damage beyond normal wear and tear (e.g., large holes in walls, broken fixtures)
   - Professional cleaning required to restore the unit to its original condition
   - Replacement of lost or unreturned keys

   Landlords MAY NOT deduct for:
   - Normal wear and tear (minor scuffs, faded paint, small nail holes)
   - Pre-existing damage documented at move-in
   - General cleaning if the tenant left the unit reasonably clean

3. Itemized Statement Requirement
   - Virtually all U.S. states require the landlord to provide a written itemized
     statement of all deductions within 14–30 days of the tenant vacating.
   - The statement must list each deduction with a dollar amount and reason.
   - Failure to provide a timely itemized statement typically results in the landlord
     FORFEITING the right to any deduction — even legitimate ones.
   - Some states impose double or triple damages on landlords who wrongfully withhold.

4. Cleaning Deductions Specifically
   - A landlord may deduct for cleaning ONLY if the unit was left in an unreasonably
     dirty condition beyond normal use.
   - The landlord must provide a receipt or invoice from a professional cleaner.
   - Without an itemized written statement, cleaning deductions are NOT enforceable.

5. Tenant Remedies
   - Tenant may sue in small claims court for return of wrongfully withheld deposit.
   - Courts can award statutory damages (2x or 3x the deposit) plus attorney's fees.

SOURCES: Uniform Residential Landlord and Tenant Act (URLTA); state-specific landlord-
tenant statutes; Restatement (Second) of Property — Landlord and Tenant.
        """.strip(),
    },

    {
        "id": "tenancy_002",
        "title": "Eviction Procedures & Tenant Rights",
        "domain": "Tenancy Law",
        "keywords": [
            "eviction", "notice to quit", "unlawful detainer", "30 day notice",
            "60 day notice", "retaliatory eviction", "illegal eviction",
            "self-help eviction", "lockout", "utility shutoff", "squatter"
        ],
        "content": """
EVICTION PROCEDURES & TENANT RIGHTS

1. Valid Grounds for Eviction
   - Non-payment of rent
   - Violation of lease terms (unauthorized pets, subletting without permission)
   - Expiry of lease with no renewal
   - Property damage or illegal activity on premises

2. Notice Requirements
   - Pay-or-Quit Notice: Typically 3–5 days for non-payment of rent.
   - Cure-or-Quit Notice: Typically 3–10 days to fix a lease violation.
   - Unconditional Quit Notice: Used for repeated or serious violations — no option to cure.
   - Month-to-Month Termination: Generally requires 30–60 days written notice.

3. Court Process (Unlawful Detainer / Summary Possession)
   - Landlord must file a court action after notice period expires.
   - Tenant has the right to contest the eviction at a hearing.
   - A court order (writ of possession) is required before a sheriff removes a tenant.

4. Illegal Eviction (Self-Help)
   The following actions by a landlord are ILLEGAL without a court order:
   - Changing the locks
   - Removing doors or windows
   - Shutting off utilities (water, electricity, heat)
   - Removing the tenant's belongings
   Landlords who engage in self-help eviction may face civil liability and punitive damages.

5. Retaliatory Eviction
   An eviction is unlawful if it is in retaliation for:
   - The tenant reporting health/safety code violations
   - The tenant joining a tenants' union
   - The tenant exercising any legal right
        """.strip(),
    },

    # ── 2. NDA / CONTRACTS ────────────────────────────────────

    {
        "id": "nda_001",
        "title": "Non-Disclosure Agreement (NDA) — Standard Clauses & Enforcement",
        "domain": "Contract Law",
        "keywords": [
            "nda", "non-disclosure", "confidentiality", "trade secret", "confidential",
            "proprietary information", "breach of contract", "non-compete",
            "non solicitation", "contract", "agreement", "clause", "enforce",
            "injunction", "damages", "mutual nda", "one-way nda"
        ],
        "content": """
NON-DISCLOSURE AGREEMENT (NDA) — STANDARD CLAUSES & ENFORCEMENT

1. Definition of Confidential Information
   - A well-drafted NDA clearly defines what constitutes "Confidential Information."
   - Typically includes: business plans, source code, customer lists, financial data,
     trade secrets, inventions, and technical know-how.
   - Exclusions (NOT protected): information already in the public domain, info
     independently developed by recipient, info received from a third party without
     restriction.

2. Obligations of the Receiving Party
   - Must keep confidential information secret with at least the same care used for
     its own confidential information (no less than reasonable care).
   - May not disclose to third parties without prior written consent.
   - May use information ONLY for the purpose stated in the NDA.

3. Duration (Term)
   - NDAs typically run for 2–5 years from the date of signing.
   - Trade secret protections can extend indefinitely under state trade secret laws.

4. Mutual vs. One-Way NDA
   - Mutual NDA: Both parties share and protect confidential information.
   - One-Way (Unilateral) NDA: Only one party discloses; the other only receives.

5. Remedies for Breach
   - Injunctive Relief: Courts can issue an injunction to stop ongoing disclosure.
   - Monetary Damages: Compensatory damages for actual losses caused by the breach.
   - Liquidated Damages: Some NDAs specify a pre-agreed penalty amount.
   - Attorney's Fees: Prevailing party clauses are common.

6. Enforceability
   - NDAs must be supported by consideration (something of value — a job, a deal, money).
   - Overly broad NDAs (covering all information ever shared) may be struck down.
   - Courts scrutinize non-compete clauses heavily; geographic and time scope must be
     reasonable.

SOURCES: Uniform Trade Secrets Act (UTSA); Defend Trade Secrets Act (DTSA) 18 U.S.C. § 1836;
Restatement (Third) of Unfair Competition.
        """.strip(),
    },

    {
        "id": "contract_001",
        "title": "Contract Formation, Breach & Remedies",
        "domain": "Contract Law",
        "keywords": [
            "contract", "offer", "acceptance", "consideration", "breach",
            "damages", "specific performance", "void", "voidable",
            "misrepresentation", "duress", "undue influence", "frustration",
            "force majeure", "termination", "rescission", "remedy"
        ],
        "content": """
CONTRACT FORMATION, BREACH & REMEDIES

1. Elements of a Valid Contract
   A binding contract requires ALL four elements:
   (a) Offer       — A clear proposal to enter into an agreement
   (b) Acceptance  — Unconditional agreement to the exact terms of the offer
   (c) Consideration — Something of value exchanged by both parties (money, services, a promise)
   (d) Intention   — Both parties must intend to create legally binding relations

2. Common Defences (Void / Voidable Contracts)
   - Misrepresentation: A false statement of fact that induced the contract.
   - Duress: Agreement obtained through threats or coercion.
   - Undue Influence: One party exploits a position of trust or power.
   - Mistake: Both parties share a fundamental misunderstanding of a key fact.
   - Illegality: Contracts for illegal purposes are void from the outset.

3. Breach of Contract
   - Material Breach: Failure to perform a fundamental obligation; gives innocent party
     the right to terminate and claim damages.
   - Minor / Partial Breach: Substantial performance with minor deviation; innocent party
     may claim damages but cannot terminate.

4. Remedies
   - Compensatory Damages: Put the innocent party in the position they would have been
     in had the contract been performed.
   - Consequential Damages: Foreseeable losses flowing naturally from the breach.
   - Specific Performance: Court orders the breaching party to perform (common for
     unique goods / real estate).
   - Rescission: Contract is unwound; parties restored to pre-contract position.
   - Liquidated Damages: Pre-agreed sum specified in the contract.

5. Force Majeure
   - Excuses performance when an unforeseeable, extraordinary event makes performance
     impossible (pandemics, natural disasters, war).
   - Clause must be expressly included; courts construe it narrowly.

SOURCES: Restatement (Second) of Contracts; Uniform Commercial Code (UCC) Article 2.
        """.strip(),
    },

    # ── 3. INTELLECTUAL PROPERTY ──────────────────────────────

    {
        "id": "ip_001",
        "title": "Intellectual Property Rights — Copyright, Patent & Trademark",
        "domain": "Intellectual Property Law",
        "keywords": [
            "intellectual property", "ip", "copyright", "patent", "trademark",
            "trade secret", "infringement", "fair use", "dmca", "piracy",
            "invention", "brand", "logo", "creative work", "software copyright",
            "open source", "license", "royalty", "plagiarism", "ownership"
        ],
        "content": """
INTELLECTUAL PROPERTY RIGHTS — COPYRIGHT, PATENT & TRADEMARK

1. COPYRIGHT
   - Protects original creative works: books, music, art, software code, films.
   - Arises AUTOMATICALLY upon creation — no registration required.
   - Duration: Life of the author + 70 years (works made for hire: 95 years from publication).
   - Exclusive rights: reproduce, distribute, create derivatives, publicly display/perform.
   - Fair Use Defence: Criticism, commentary, news reporting, teaching, parody may qualify.
     Courts weigh four factors: purpose, nature of work, amount used, market effect.
   - DMCA (Digital Millennium Copyright Act): Governs online infringement; safe harbour
     for platforms that act on takedown notices.

2. PATENT
   - Protects new, useful, and non-obvious inventions (products, processes, designs).
   - Must be registered with the patent office (USPTO in the U.S.).
   - Utility Patent Duration: 20 years from filing date.
   - Design Patent Duration: 15 years from grant.
   - Rights: Exclude others from making, using, selling, or importing the invention.
   - Patent Pending: Application filed but not yet granted; some protection applies.

3. TRADEMARK
   - Protects brand identifiers: names, logos, slogans that distinguish goods/services.
   - Registration not required but provides significant legal advantages.
   - Duration: Indefinite, as long as the mark is used and renewals are filed (every 10 years).
   - Infringement: Likelihood of consumer confusion test.
   - Dilution: Famous marks protected even without confusion (blurring or tarnishment).

4. TRADE SECRET
   - Confidential business information with commercial value.
   - Protection lasts as long as the secret is maintained.
   - Protected under the Defend Trade Secrets Act (DTSA) and state UTSA statutes.
   - No registration required; secrecy measures must be in place.

SOURCES: Copyright Act 17 U.S.C.; Patent Act 35 U.S.C.; Lanham Act 15 U.S.C.;
Defend Trade Secrets Act 18 U.S.C. § 1836.
        """.strip(),
    },

    # ── 4. EMPLOYMENT LAW ─────────────────────────────────────

    {
        "id": "employment_001",
        "title": "Employment Law — Worker Rights, Termination & Discrimination",
        "domain": "Employment Law",
        "keywords": [
            "employment", "employee", "employer", "termination", "fired", "wrongful termination",
            "at-will employment", "discrimination", "harassment", "hostile work environment",
            "sexual harassment", "workplace", "wage", "overtime", "minimum wage",
            "fmla", "leave", "benefits", "retaliation", "whistleblower",
            "redundancy", "layoff", "severance"
        ],
        "content": """
EMPLOYMENT LAW — WORKER RIGHTS, TERMINATION & DISCRIMINATION

1. At-Will Employment (U.S.)
   - Most U.S. employees are employed at-will: either party may end employment at any
     time for any reason or no reason, without advance notice.
   - Exceptions:
     (a) Implied Contract: Employee handbook or verbal promises may create contractual rights.
     (b) Public Policy: Cannot fire for jury duty, voting, or whistleblowing.
     (c) Anti-Discrimination Laws: Cannot fire based on protected characteristics.

2. Protected Characteristics (Federal)
   Federal law prohibits discrimination based on:
   - Race, color, national origin (Title VII, Civil Rights Act 1964)
   - Sex / Gender / Sexual Orientation / Gender Identity (Title VII as interpreted)
   - Age (40+) — Age Discrimination in Employment Act (ADEA)
   - Disability — Americans with Disabilities Act (ADA); employer must provide
     reasonable accommodations
   - Pregnancy — Pregnancy Discrimination Act
   - Religion — must accommodate sincerely held religious beliefs

3. Harassment
   - Quid Pro Quo: Job benefits/detriments conditioned on submission to harassment.
   - Hostile Work Environment: Severe or pervasive conduct that alters working conditions.
   - Employers are liable for supervisor harassment and may be liable for co-worker
     harassment if they knew or should have known and failed to act.

4. Wage & Hour (FLSA)
   - Federal minimum wage: $7.25/hour (states often higher).
   - Non-exempt employees must receive 1.5x overtime for hours over 40/week.
   - Misclassifying employees as independent contractors is a common violation.

5. FMLA (Family & Medical Leave Act)
   - Eligible employees at covered employers (50+ employees) may take up to 12 weeks
     of unpaid, job-protected leave per year for qualifying family/medical reasons.

6. Wrongful Termination Remedies
   - Reinstatement, back pay, front pay, compensatory damages, punitive damages.
   - Must file EEOC charge within 180–300 days before suing federally.

SOURCES: Title VII Civil Rights Act 1964; ADEA; ADA; FLSA; FMLA; EEOC Guidelines.
        """.strip(),
    },

    # ── 5. CONSUMER PROTECTION ────────────────────────────────

    {
        "id": "consumer_001",
        "title": "Consumer Protection Law — Fraud, Warranties & Refunds",
        "domain": "Consumer Protection Law",
        "keywords": [
            "consumer", "consumer protection", "refund", "warranty", "guarantee",
            "fraud", "deceptive", "misleading", "false advertising", "scam",
            "ftc", "lemon law", "defective product", "recall", "chargeback",
            "credit card dispute", "return policy", "unfair practice"
        ],
        "content": """
CONSUMER PROTECTION LAW — FRAUD, WARRANTIES & REFUNDS

1. Federal Trade Commission (FTC) Act
   - Prohibits "unfair or deceptive acts or practices" in commerce.
   - Covers false advertising, bait-and-switch tactics, deceptive pricing.
   - FTC can seek injunctions, civil penalties, and consumer redress.

2. Warranties
   Express Warranty:
   - Any promise, description, sample, or model that becomes part of the basis of the bargain.
   - Must honour the warranty as stated.
   Implied Warranty of Merchantability (UCC):
   - Goods must be fit for their ordinary purpose.
   - Automatically applies unless explicitly disclaimed in writing.
   Implied Warranty of Fitness for a Particular Purpose:
   - Applies when seller knows buyer's specific need and buyer relies on seller's expertise.

3. Magnuson-Moss Warranty Act
   - Governs written warranties on consumer products.
   - Full warranty: defects must be fixed or product replaced free within a reasonable time.
   - Limited warranty: limits remedies; must be clearly labeled "Limited Warranty."

4. Lemon Laws
   - Most states have lemon laws for defective new vehicles.
   - If a defect cannot be repaired after a reasonable number of attempts,
     the consumer is entitled to a replacement vehicle or full refund.

5. Right to Refund / Return
   - No federal law mandates refunds; policies are set by retailers.
   - HOWEVER: if goods are misrepresented, defective, or not as described,
     consumer has a legal right to remedy under warranty law and consumer protection acts.
   - For online purchases: FTC's "Cooling-Off Rule" gives 3 days to cancel certain
     door-to-door sales; some states extend this to online sales.

6. Credit Card Chargebacks
   - Fair Credit Billing Act (FCBA): Consumers can dispute billing errors and
     unauthorised charges within 60 days of the statement date.
   - For goods/services not delivered or not as described, chargeback rights apply.

SOURCES: FTC Act 15 U.S.C. § 45; UCC Article 2; Magnuson-Moss Warranty Act;
Fair Credit Billing Act (FCBA); state consumer protection statutes.
        """.strip(),
    },
]


# ─────────────────────────────────────────────────────────────
#  Helper: build a flat keyword → document index
# ─────────────────────────────────────────────────────────────

def build_keyword_index() -> Dict[str, List[str]]:
    """
    Returns a mapping of lowercase keyword → list of document IDs.
    Used by the search tool for fast lookup.
    """
    index: Dict[str, List[str]] = {}
    for doc in LEGAL_DOCUMENTS:
        for kw in doc["keywords"]:
            key = kw.lower()
            if key not in index:
                index[key] = []
            if doc["id"] not in index[key]:
                index[key].append(doc["id"])
    return index


# Pre-built at import time for efficiency
KEYWORD_INDEX: Dict[str, List[str]] = build_keyword_index()

# Convenience lookup by document ID
DOCUMENT_BY_ID: Dict[str, Dict[str, Any]] = {doc["id"]: doc for doc in LEGAL_DOCUMENTS}


# ─────────────────────────────────────────────────────────────
#  Indian Law Documents (ported from zip's SAMPLE_LEGAL_DOCUMENTS)
#  Added alongside existing documents — does NOT replace them.
# ─────────────────────────────────────────────────────────────

INDIAN_LEGAL_DOCUMENTS: list = [
    {
        "id": "IN-DOC-TENANCY-001",
        "title": "Tenancy & Security Deposits Framework (Model Tenancy Act & State Rent Laws)",
        "domain": "Tenancy Law",
        "keywords": [
            "tenant", "landlord", "rent", "security deposit", "model tenancy act",
            "rent control", "wear and tear", "notice to quit", "eviction",
            "transfer of property act", "india", "indian", "30 day", "refund",
        ],
        "content": (
            "TENANCY & SECURITY DEPOSITS FRAMEWORK (INDIA)\n\n"
            "1. Security Deposit Limits (Model Tenancy Act, 2021, Sec 11):\n"
            "   Security deposit for residential premises is capped at a maximum of 2 months' rent.\n"
            "   For non-residential premises, it is capped at up to 6 months' rent.\n\n"
            "2. Return Timeline & Deductions:\n"
            "   The security deposit must be refunded to the tenant within 30 days of vacating the\n"
            "   premises, after adjusting for genuine rent arrears or agreed structural damages.\n"
            "   Landlords cannot deduct for reasonable / normal wear and tear.\n\n"
            "3. Termination & Notice to Quit (Transfer of Property Act, 1882, Sec 106):\n"
            "   In the absence of a written contract, lease of immovable property for residential\n"
            "   purpose is terminable by 15 days' written notice expiring with the end of a month.\n\n"
            "4. Eviction Protections:\n"
            "   Landlords cannot arbitrarily evict tenants or cut off essential supplies\n"
            "   (water, electricity). Eviction requires orders from the Rent Authority / Rent Court.\n\n"
            "SOURCES: Model Tenancy Act 2021; Transfer of Property Act 1882 Sec 106; State Rent Control Acts."
        ),
    },
    {
        "id": "IN-DOC-CONTRACT-002",
        "title": "Commercial Contracts & Non-Disclosure Agreements (Indian Contract Act, 1872)",
        "domain": "Contract Law",
        "keywords": [
            "nda", "confidentiality", "contract act", "section 27", "trade secret",
            "non-disclosure", "injunction", "specific relief act", "exclusions",
            "india", "indian contract act", "ica",
        ],
        "content": (
            "COMMERCIAL CONTRACTS & NDAs UNDER INDIAN CONTRACT ACT, 1872\n\n"
            "1. Enforceability of Confidentiality (ICA Sec 10 & 27):\n"
            "   NDAs are valid and enforceable contracts in India. Negative covenants during\n"
            "   contract subsistence are valid but must not act as an unlawful restraint of trade.\n\n"
            "2. Standard Exclusions from Confidentiality:\n"
            "   Information is exempt if:\n"
            "   (a) Already in the public domain without breach of agreement;\n"
            "   (b) Lawfully in the recipient's possession prior to disclosure;\n"
            "   (c) Independently developed without reference to proprietary data;\n"
            "   (d) Required to be disclosed pursuant to a court summons or statutory notice.\n\n"
            "3. Legal Remedies for Breach:\n"
            "   Under the Specific Relief Act, 1963 (Sections 38 & 39), an aggrieved party can\n"
            "   seek interim and permanent injunctions plus damages under ICA Section 73.\n\n"
            "SOURCES: Indian Contract Act 1872; Specific Relief Act 1963 Sec 38-39."
        ),
    },
    {
        "id": "IN-DOC-LABOR-003",
        "title": "Employment Restrictive Covenants & Section 27 Indian Contract Act, 1872",
        "domain": "Employment Law",
        "keywords": [
            "employment", "non-compete", "section 27", "contract act", "restraint of trade",
            "termination", "severance", "percept d'mark", "zaheer khan", "india",
            "indian employment", "shops establishments act",
        ],
        "content": (
            "EMPLOYMENT RESTRICTIVE COVENANTS UNDER INDIAN LAW\n\n"
            "1. Statutory Prohibition of Non-Competes (ICA Sec 27):\n"
            "   Section 27 states: 'Every agreement by which anyone is restrained from exercising\n"
            "   a lawful profession, trade or business of any kind, is to that extent void.'\n"
            "   Indian law recognizes NO reasonableness exception for post-employment non-competes.\n\n"
            "2. Landmark Supreme Court Precedents:\n"
            "   In Percept D'Mark (India) Pvt. Ltd. v. Zaheer Khan (2006) and Niranjan Shankar\n"
            "   Golikari (1967), the Supreme Court held that restrictive covenants extending\n"
            "   beyond the term of employment are wholly void. A company cannot legally restrain\n"
            "   an ex-employee from joining a competitor or starting a rival business.\n\n"
            "3. Permissible vs Void Covenants:\n"
            "   - VALID: Non-disclosure of proprietary trade secrets, non-solicitation of\n"
            "     clients/employees (for reasonable periods during employment).\n"
            "   - VOID: Total ban on working for competitors after resignation or termination.\n\n"
            "4. Termination Notice:\n"
            "   Under state Shops & Establishments Acts, 30 days' written notice or salary in\n"
            "   lieu thereof is customary.\n\n"
            "SOURCES: Indian Contract Act 1872 Sec 27; Percept D'Mark v. Zaheer Khan (2006) SC."
        ),
    },
    {
        "id": "IN-DOC-CONSUMER-004",
        "title": "Consumer Protection Act, 2019 & E-Commerce Consumer Rules (India)",
        "domain": "Consumer Protection Law",
        "keywords": [
            "consumer", "consumer protection act", "deficiency in service", "refund",
            "unfair trade practice", "district commission", "e-commerce rules",
            "product liability", "e-daakhil", "ncdrc", "india", "indian consumer",
            "2019", "cpa 2019",
        ],
        "content": (
            "CONSUMER PROTECTION ACT, 2019 — INDIA\n\n"
            "1. Core Consumer Rights (CPA 2019, Sec 2(9)):\n"
            "   Consumers possess statutory rights to safety, information, choice, hearing, and\n"
            "   redressal against unfair or restrictive trade practices and deficiency in services.\n\n"
            "2. Deficiency in Service & Unfair Trade Practices:\n"
            "   Refusing refund for defective goods, charging above MRP, misleading advertisements,\n"
            "   and non-compliance with warranty constitutes deficiency in service under Sec 2(11).\n\n"
            "3. Dispute Resolution Hierarchy:\n"
            "   - District Commission: Claims up to ₹50 Lakhs (e-filing via e-Daakhil portal).\n"
            "   - State Commission: Claims from ₹50 Lakhs to ₹2 Crores.\n"
            "   - National Commission (NCDRC): Claims exceeding ₹2 Crores.\n\n"
            "4. Limitation Period:\n"
            "   Complaints must be filed within 2 years from the date the cause of action arose\n"
            "   (CPA 2019 Sec 69).\n\n"
            "SOURCES: Consumer Protection Act 2019; Consumer Protection (E-Commerce) Rules 2020."
        ),
    },
    {
        "id": "IN-DOC-IP-005",
        "title": "Software Copyright & Digital Data Governance (Copyright Act & IT Act, India)",
        "domain": "Intellectual Property Law",
        "keywords": [
            "copyright act", "it act", "software", "open source", "mit", "gpl",
            "section 43a", "digital personal data protection", "dpdp", "intermediary",
            "india", "indian copyright", "literary work",
        ],
        "content": (
            "SOFTWARE COPYRIGHT & DATA GOVERNANCE — INDIA\n\n"
            "1. Software as Literary Work (Copyright Act, 1957, Sec 2(o)):\n"
            "   Computer software, source code, and program manuals are protected as 'literary\n"
            "   works'. Unauthorized commercial reproduction or distribution without a license\n"
            "   constitutes copyright infringement.\n\n"
            "2. Open Source Licensing in India:\n"
            "   Permissive licenses (MIT, Apache 2.0) are enforceable contracts granting commercial\n"
            "   rights provided original copyright and warranty disclaimers are preserved.\n"
            "   Copyleft licenses (GPL v3) require distribution of derivative source code.\n\n"
            "3. IT Act, 2000 & DPDP Act, 2023:\n"
            "   Section 43A of the IT Act mandates reasonable security practices for sensitive\n"
            "   personal data. The Digital Personal Data Protection Act, 2023 establishes\n"
            "   consent-based data processing rules and penalties up to ₹250 Crores for\n"
            "   significant data breaches.\n\n"
            "SOURCES: Copyright Act 1957; Information Technology Act 2000 Sec 43A; DPDP Act 2023."
        ),
    },
]

# Merge Indian docs into the main LEGAL_DOCUMENTS list so the search tool
# picks them up automatically — no changes to tools.py needed.
LEGAL_DOCUMENTS.extend(INDIAN_LEGAL_DOCUMENTS)

# Re-build indexes to include the new entries
KEYWORD_INDEX = build_keyword_index()
DOCUMENT_BY_ID = {doc["id"]: doc for doc in LEGAL_DOCUMENTS}

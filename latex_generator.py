"""
latex_generator.py
Converts resume analysis JSON → clean, compilable LaTeX (moderncv/custom style).
Output compiles directly on Overleaf with zero extra packages to install.
"""

import re
from datetime import datetime


# ─── helpers ────────────────────────────────────────────────────────────────

def tex_escape(text: str) -> str:
    """Escape LaTeX special characters in plain text."""
    if not text:
        return ""
    replacements = [
        ("\\", r"\textbackslash{}"),
        ("&",  r"\&"),
        ("%",  r"\%"),
        ("$",  r"\$"),
        ("#",  r"\#"),
        ("_",  r"\_"),
        ("{",  r"\{"),
        ("}",  r"\}"),
        ("~",  r"\textasciitilde{}"),
        ("^",  r"\textasciicircum{}"),
    ]
    for char, replacement in replacements:
        text = text.replace(char, replacement)
    return text


def safe(val, fallback=""):
    """Return val if truthy, else fallback."""
    return val if val else fallback


# ─── section builders ────────────────────────────────────────────────────────

def build_header(personal: dict, job_role: str) -> str:
    name     = tex_escape(safe(personal.get("name"), "Your Name"))
    email    = tex_escape(safe(personal.get("email"), ""))
    phone    = tex_escape(safe(personal.get("phone"), ""))
    location = tex_escape(safe(personal.get("location"), ""))
    linkedin = tex_escape(safe(personal.get("linkedin"), ""))
    github   = tex_escape(safe(personal.get("github"), ""))
    role     = tex_escape(safe(job_role, "Software Professional"))

    contact_parts = []
    if email:    contact_parts.append(r"\faEnvelope\, \href{mailto:" + email + r"}{" + email + "}")
    if phone:    contact_parts.append(r"\faPhone\, " + phone)
    if location: contact_parts.append(r"\faMapMarker\, " + location)
    if linkedin: contact_parts.append(r"\faLinkedin\, \href{" + linkedin + r"}{LinkedIn}")
    if github:   contact_parts.append(r"\faGithub\, \href{" + github + r"}{GitHub}")

    contact_line = r" \quad|\quad ".join(contact_parts) if contact_parts else ""

    return rf"""
%% ─── HEADER ──────────────────────────────────────────────────────────────
\begin{{center}}
  {{\Huge\bfseries\color{{primary}} {name}}} \\[4pt]
  {{\large\color{{subtext}} {role}}} \\[6pt]
  \small {contact_line}
\end{{center}}
\vspace{{2pt}}
\noindent\textcolor{{primary}}{{\rule{{\linewidth}}{{1.5pt}}}}
\vspace{{6pt}}
"""


def build_summary(personal: dict, exp: dict, job_role: str, skills: dict) -> str:
    total_years = exp.get("total_years", 0)
    top_skills  = (skills.get("all") or [])[:5]
    skills_str  = tex_escape(", ".join(top_skills)) if top_skills else "various technologies"
    role        = tex_escape(safe(job_role, "Software Professional"))

    if total_years >= 8:
        exp_phrase = f"Over {int(total_years)} years of"
    elif total_years >= 1:
        exp_phrase = f"{round(total_years, 1)} years of"
    else:
        exp_phrase = "Passionate entry-level professional with"

    return rf"""
%% ─── SUMMARY ─────────────────────────────────────────────────────────────
\section{{Professional Summary}}
{exp_phrase} experience as a {role}, with proven expertise in {skills_str}.
Adept at delivering scalable solutions, collaborating across cross-functional teams,
and driving impactful outcomes aligned with business objectives.

"""


def build_experience(experiences: list) -> str:
    if not experiences:
        return ""

    lines = [r"""
%% ─── EXPERIENCE ──────────────────────────────────────────────────────────
\section{Work Experience}
"""]

    for exp in experiences:
        title   = tex_escape(safe(exp.get("title"),   "Position"))
        company = tex_escape(safe(exp.get("company"), "Company"))
        dates   = tex_escape(safe(exp.get("dates"),   ""))
        exp_type = tex_escape(safe(exp.get("type"),   "Full-time"))
        years   = exp.get("years", 0)

        # Description bullets — split on common separators
        desc    = safe(exp.get("description"), "")
        bullets = []
        if desc:
            raw = re.split(r"[•\-\*\n]+", desc)
            bullets = [b.strip() for b in raw if len(b.strip()) > 10][:4]

        bullet_block = ""
        if bullets:
            items = "\n    ".join([r"\item " + tex_escape(b) for b in bullets])
            bullet_block = rf"""
  \begin{{itemize}}[leftmargin=*,topsep=2pt,itemsep=1pt]
    {items}
  \end{{itemize}}"""

        lines.append(rf"""
\noindent
\begin{{tabularx}}{{\linewidth}}{{@{{}}X r@{{}}}}
  \textbf{{\color{{primary}}{title}}} & \textit{{\small {dates}}} \\
  \textit{{{company}}} & \textcolor{{subtext}}{{\small {exp_type} $\cdot$ {years} yrs}} \\
\end{{tabularx}}{bullet_block}
\vspace{{4pt}}
""")

    return "\n".join(lines)


def build_skills(skills: dict) -> str:
    technical = skills.get("technical") or {}
    if not technical:
        all_skills = (skills.get("all") or [])[:20]
        if not all_skills:
            return ""
        technical = {"Skills": all_skills}

    lines = [r"""
%% ─── SKILLS ──────────────────────────────────────────────────────────────
\section{Technical Skills}
\begin{tabularx}{\linewidth}{@{}lX@{}}
"""]

    category_icons = {
        "Programming Languages": r"\faCode",
        "Web Technologies":      r"\faGlobe",
        "Databases":             r"\faDatabase",
        "Data Science & ML":     r"\faBrain",
        "Cloud & DevOps":        r"\faCloud",
        "Mobile Development":    r"\faMobile",
        "Tools & Frameworks":    r"\faWrench",
        "Big Data":              r"\faServer",
    }

    for cat, skill_list in technical.items():
        if not skill_list:
            continue
        display_cat = cat.replace("_", " ").title()
        icon        = category_icons.get(display_cat, r"\faAngleRight")
        skills_str  = tex_escape(", ".join(skill_list[:10]))
        lines.append(
            rf"  {icon} \textbf{{{tex_escape(display_cat)}}} & {skills_str} \\" + "\n"
        )

    lines.append(r"""\end{tabularx}

""")
    return "\n".join(lines)


def build_education(education: dict) -> str:
    degrees      = education.get("degrees")      or []
    institutions = education.get("institutions") or []
    gpa_list     = education.get("gpa")          or []

    if not degrees and not institutions:
        return ""

    lines = [r"""
%% ─── EDUCATION ───────────────────────────────────────────────────────────
\section{Education}
"""]

    count = max(len(degrees), len(institutions))
    for i in range(count):
        degree  = tex_escape(degrees[i])      if i < len(degrees)      else ""
        inst    = tex_escape(institutions[i]) if i < len(institutions) else ""
        gpa     = tex_escape(str(gpa_list[i])) if i < len(gpa_list)   else ""
        gpa_str = rf" \textcolor{{subtext}}{{\small GPA: {gpa}}}" if gpa else ""

        lines.append(rf"""
\noindent
\begin{{tabularx}}{{\linewidth}}{{@{{}}X r@{{}}}}
  \textbf{{\color{{primary}}{degree}}} & \\
  \textit{{{inst}}}{gpa_str} & \\
\end{{tabularx}}
\vspace{{4pt}}
""")

    return "\n".join(lines)


def build_projects(projects: list) -> str:
    if not projects:
        return ""

    lines = [r"""
%% ─── PROJECTS ────────────────────────────────────────────────────────────
\section{Projects}
"""]

    for proj in projects[:4]:
        name = tex_escape(safe(proj.get("name"), "Project"))
        desc = tex_escape(safe(proj.get("description"), ""))
        tech_list = proj.get("technologies") or proj.get("tech") or []
        tech_str  = tex_escape(", ".join(tech_list[:5])) if tech_list else ""

        tech_line  = rf"\\ \textcolor{{subtext}}{{\small \textit{{Tech: {tech_str}}}}}" if tech_str else ""
        desc_line  = rf"\\ \small {desc}" if desc else ""

        lines.append(rf"""
\noindent
\textbf{{\color{{primary}}{name}}}{desc_line}{tech_line}
\vspace{{6pt}}

""")

    return "\n".join(lines)


def build_certifications(suggestions: list) -> str:
    """Extract certification mentions from suggestions list."""
    certs = []
    for s in (suggestions or []):
        if "certif" in s.lower() or "aws" in s.lower() or "certified" in s.lower():
            certs.append(s)

    if not certs:
        return ""

    items = "\n  ".join([r"\item " + tex_escape(c) for c in certs[:5]])
    return rf"""
%% ─── CERTIFICATIONS ──────────────────────────────────────────────────────
\section{{Certifications}}
\begin{{itemize}}[leftmargin=*,topsep=2pt,itemsep=1pt]
  {items}
\end{{itemize}}

"""


# ─── main generator ──────────────────────────────────────────────────────────

def generate_latex(analysis: dict) -> str:
    """
    Convert a resume analysis dict (from /analyze endpoint) into a
    fully compilable LaTeX document string.
    """
    personal   = analysis.get("personal_details", {})
    skills     = analysis.get("skills", {})
    exp_data   = analysis.get("experience", {})
    education  = analysis.get("education", {})
    projects   = analysis.get("projects", [])
    job_role   = safe(analysis.get("job_role"), "Software Engineer")
    suggestions = analysis.get("suggestions", [])
    experiences = exp_data.get("experiences", [])

    name_raw  = safe(personal.get("name"), "Resume")
    today_str = datetime.now().strftime("%B %Y")

    # ── document preamble ──────────────────────────────────────────────────
    preamble = r"""\documentclass[10pt,a4paper]{article}

%% ─── PACKAGES ────────────────────────────────────────────────────────────
\usepackage[T1]{fontenc}
\usepackage[utf8]{inputenc}
\usepackage[margin=1.8cm, top=1.5cm, bottom=1.5cm]{geometry}
\usepackage{xcolor}
\usepackage{hyperref}
\usepackage{fontawesome}
\usepackage{tabularx}
\usepackage{enumitem}
\usepackage{titlesec}
\usepackage{parskip}
\usepackage{lmodern}

%% ─── COLOURS ─────────────────────────────────────────────────────────────
\definecolor{primary}{HTML}{2D3748}
\definecolor{accent}{HTML}{667EEA}
\definecolor{subtext}{HTML}{718096}
\definecolor{rule}{HTML}{E2E8F0}

%% ─── HYPERREF SETUP ──────────────────────────────────────────────────────
\hypersetup{
  colorlinks=true,
  urlcolor=accent,
  linkcolor=primary,
  pdfauthor={""" + tex_escape(name_raw) + r"""},
  pdftitle={Resume - """ + tex_escape(name_raw) + r"""}
}

%% ─── SECTION STYLE ───────────────────────────────────────────────────────
\titleformat{\section}
  {\large\bfseries\color{primary}}
  {}{0em}{}
  [\vspace{-6pt}\noindent\textcolor{rule}{\rule{\linewidth}{0.6pt}}\vspace{2pt}]

\titlespacing*{\section}{0pt}{10pt}{4pt}

%% ─── MISC ────────────────────────────────────────────────────────────────
\setlength{\parindent}{0pt}
\pagestyle{empty}
\setlist[itemize]{leftmargin=1.5em, topsep=2pt, itemsep=0pt, parsep=0pt}

%% ─── DOCUMENT ────────────────────────────────────────────────────────────
\begin{document}
"""

    # ── build sections ─────────────────────────────────────────────────────
    header  = build_header(personal, job_role)
    summary = build_summary(personal, exp_data, job_role, skills)
    exp_sec = build_experience(experiences)
    sk_sec  = build_skills(skills)
    edu_sec = build_education(education)
    proj_sec = build_projects(projects)
    cert_sec = build_certifications(suggestions)

    footer = rf"""
%% ─── FOOTER ──────────────────────────────────────────────────────────────
\vfill
\noindent\textcolor{{rule}}{{\rule{{\linewidth}}{{0.4pt}}}}
\begin{{center}}
  \textcolor{{subtext}}{{\tiny Generated by AI Resume Analyzer Pro \textbullet\ {today_str}}}
\end{{center}}

\end{{document}}
"""

    return (
        preamble
        + header
        + summary
        + exp_sec
        + sk_sec
        + edu_sec
        + proj_sec
        + cert_sec
        + footer
    )
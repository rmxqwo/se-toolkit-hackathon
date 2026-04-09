import os
import uuid
from datetime import datetime
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import inch, mm
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    HRFlowable, KeepTogether
)
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from typing import Optional


class PDFResumeGenerator:
    """Generate professional PDF resumes using reportlab."""

    def __init__(self, output_dir: str = "generated_pdfs"):
        self.output_dir = output_dir
        os.makedirs(output_dir, exist_ok=True)

    def generate(
        self,
        first_name: str,
        last_name: str,
        email: str,
        phone: Optional[str] = None,
        location: Optional[str] = None,
        linkedin: Optional[str] = None,
        github: Optional[str] = None,
        portfolio: Optional[str] = None,
        professional_title: Optional[str] = None,
        summary: Optional[str] = None,
        skills: Optional[list[dict]] = None,
        experience: Optional[list[dict]] = None,
        education: Optional[list[dict]] = None,
        projects: Optional[list[dict]] = None,
    ) -> str:
        """
        Generate a PDF resume and return the filename.
        """
        # Generate unique filename
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        unique_id = str(uuid.uuid4())[:8]
        filename = f"resume_{first_name.lower()}_{last_name.lower()}_{timestamp}_{unique_id}.pdf"
        filepath = os.path.join(self.output_dir, filename)

        # Create document
        doc = SimpleDocTemplate(
            filepath,
            pagesize=A4,
            topMargin=0.7 * inch,
            bottomMargin=0.6 * inch,
            leftMargin=0.7 * inch,
            rightMargin=0.7 * inch,
        )

        # Build styles
        styles = self._build_styles()

        # Build document elements
        elements = []

        # Header
        elements.extend(self._build_header(
            first_name, last_name, professional_title, styles
        ))

        # Contact info
        elements.extend(self._build_contact_info(
            email, phone, location, linkedin, github, portfolio, styles
        ))

        # Divider
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor("#2563eb"), spaceAfter=12))

        # Summary
        if summary:
            elements.append(Paragraph("PROFESSIONAL SUMMARY", styles["section_header"]))
            elements.append(Spacer(1, 4))
            elements.append(Paragraph(summary.replace("\n", "<br/>"), styles["body"]))
            elements.append(Spacer(1, 10))

        # Skills
        if skills:
            elements.append(Paragraph("SKILLS", styles["section_header"]))
            elements.append(Spacer(1, 4))
            elements.extend(self._build_skills(skills, styles))
            elements.append(Spacer(1, 10))

        # Experience
        if experience:
            elements.append(Paragraph("WORK EXPERIENCE", styles["section_header"]))
            elements.append(Spacer(1, 4))
            for exp in experience:
                elements.extend(self._build_experience_entry(exp, styles))
                elements.append(Spacer(1, 6))

        # Projects
        if projects:
            elements.append(Paragraph("PROJECTS", styles["section_header"]))
            elements.append(Spacer(1, 4))
            for proj in projects:
                elements.extend(self._build_project_entry(proj, styles))
                elements.append(Spacer(1, 6))

        # Education
        if education:
            elements.append(Paragraph("EDUCATION", styles["section_header"]))
            elements.append(Spacer(1, 4))
            for edu in education:
                elements.extend(self._build_education_entry(edu, styles))
                elements.append(Spacer(1, 6))

        # Build PDF
        doc.build(elements)

        return filename

    def _build_styles(self) -> dict:
        """Create custom paragraph styles."""
        styles = getSampleStyleSheet()

        # Name style
        styles.add(ParagraphStyle(
            name='name',
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor("#1e293b"),
            alignment=TA_CENTER,
            spaceAfter=4,
        ))

        # Professional title
        styles.add(ParagraphStyle(
            name='title',
            fontName='Helvetica',
            fontSize=13,
            leading=17,
            textColor=colors.HexColor("#2563eb"),
            alignment=TA_CENTER,
            spaceAfter=8,
        ))

        # Section header
        styles.add(ParagraphStyle(
            name='section_header',
            fontName='Helvetica-Bold',
            fontSize=12,
            leading=16,
            textColor=colors.HexColor("#1e293b"),
            spaceBefore=4,
            spaceAfter=4,
        ))

        # Body text
        styles.add(ParagraphStyle(
            name='body',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155"),
            alignment=TA_JUSTIFY,
        ))

        # Company/Institution name
        styles.add(ParagraphStyle(
            name='company',
            fontName='Helvetica-Bold',
            fontSize=11,
            leading=15,
            textColor=colors.HexColor("#1e293b"),
        ))

        # Position/Degree
        styles.add(ParagraphStyle(
            name='position',
            fontName='Helvetica-BoldOblique',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#475569"),
        ))

        # Date/location
        styles.add(ParagraphStyle(
            name='date',
            fontName='Helvetica-Oblique',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#64748b"),
        ))

        # Bullet points
        styles.add(ParagraphStyle(
            name='bullet',
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor("#334155"),
            leftIndent=20,
            bulletIndent=5,
            spaceBefore=2,
            spaceAfter=2,
        ))

        # Skill category
        styles.add(ParagraphStyle(
            name='skill_category',
            fontName='Helvetica-Bold',
            fontSize=9,
            leading=12,
            textColor=colors.HexColor("#1e293b"),
        ))

        # Skill list
        styles.add(ParagraphStyle(
            name='skill_list',
            fontName='Helvetica',
            fontSize=9,
            leading=13,
            textColor=colors.HexColor("#475569"),
            leftIndent=10,
        ))

        return styles

    def _build_header(self, first_name: str, last_name: str, title: Optional[str], styles: dict) -> list:
        """Build the resume header with name and title."""
        elements = []
        elements.append(Paragraph(f"{first_name} {last_name}", styles["name"]))
        if title:
            elements.append(Paragraph(title, styles["title"]))
        return elements

    def _build_contact_info(
        self,
        email: str,
        phone: Optional[str],
        location: Optional[str],
        linkedin: Optional[str],
        github: Optional[str],
        portfolio: Optional[str],
        styles: dict,
    ) -> list:
        """Build contact information row."""
        elements = []

        contact_items = [email]
        if phone:
            contact_items.append(phone)
        if location:
            contact_items.append(location)

        # Build contact line
        contact_line = " | ".join(contact_items)
        elements.append(Paragraph(contact_line, styles["body"]))

        # Build links line
        links = []
        if linkedin:
            links.append(f"LinkedIn: {linkedin}")
        if github:
            links.append(f"GitHub: {github}")
        if portfolio:
            links.append(f"Portfolio: {portfolio}")

        if links:
            elements.append(Paragraph(" | ".join(links), styles["body"]))

        elements.append(Spacer(1, 6))
        return elements

    def _build_skills(self, skills: list[dict], styles: dict) -> list:
        """Build skills section, grouped by category."""
        elements = []

        # Group by category
        categorized = {}
        for skill in skills:
            category = skill.get("category", "Other") or "Other"
            if category not in categorized:
                categorized[category] = []
            level_text = f" ({skill.get('level', '')})" if skill.get('level') else ""
            categorized[category].append(f"{skill['name']}{level_text}")

        for category, skill_names in categorized.items():
            elements.append(Paragraph(f"<b>{category}:</b> {', '.join(skill_names)}", styles["body"]))
            elements.append(Spacer(1, 2))

        return elements

    def _build_experience_entry(self, exp: dict, styles: dict) -> list:
        """Build a single work experience entry."""
        elements = []

        company = exp.get("company", "Unknown Company")
        position = exp.get("position", "Position")
        start_date = exp.get("start_date", "")
        end_date = exp.get("end_date", "")
        location = exp.get("location", "")
        description = exp.get("description", "")
        achievements = exp.get("achievements", "")

        # Company and date on same line
        date_text = f"{start_date} - {end_date}" if end_date else start_date
        if location:
            date_text += f" | {location}"

        elements.append(Paragraph(f"{company}  <i>{date_text}</i>", styles["company"]))
        elements.append(Paragraph(position, styles["position"]))

        if description:
            elements.append(Spacer(1, 3))
            elements.append(Paragraph(description.replace("\n", "<br/>"), styles["body"]))

        if achievements:
            elements.append(Spacer(1, 3))
            # Split achievements by newlines and create bullet points
            achievement_list = [a.strip() for a in achievements.split("\n") if a.strip()]
            for achievement in achievement_list:
                # Add bullet if not present
                if not achievement.startswith(("•", "-", "*", "▸")):
                    achievement = f"• {achievement}"
                elements.append(Paragraph(achievement, styles["bullet"]))

        return elements

    def _build_project_entry(self, proj: dict, styles: dict) -> list:
        """Build a single project entry."""
        elements = []

        name = proj.get("name", "Unknown Project")
        description = proj.get("description", "")
        technologies = proj.get("technologies", [])
        link = proj.get("link", "")
        start_date = proj.get("start_date", "")
        end_date = proj.get("end_date", "")

        # Project name and date
        date_text = f"{start_date} - {end_date}" if end_date else start_date
        
        elements.append(Paragraph(f"{name}  <i>{date_text}</i>", styles["company"]))
        
        if technologies:
            tech_text = f"<b>Technologies:</b> {', '.join(technologies)}"
            elements.append(Paragraph(tech_text, styles["position"]))

        if description:
            elements.append(Spacer(1, 3))
            elements.append(Paragraph(description.replace("\n", "<br/>"), styles["body"]))

        if link:
            elements.append(Spacer(1, 2))
            elements.append(Paragraph(f"<i>Link: {link}</i>", styles["date"]))

        return elements

    def _build_education_entry(self, edu: dict, styles: dict) -> list:
        """Build a single education entry."""
        elements = []

        institution = edu.get("institution", "Unknown Institution")
        degree = edu.get("degree", "Degree")
        field = edu.get("field_of_study", "")
        grad_date = edu.get("graduation_date", "")
        gpa = edu.get("gpa", "")
        honors = edu.get("honors", "")

        # Build the degree line
        degree_line = f"{degree} in {field}" if field else degree
        if grad_date:
            degree_line += f"  <i>{grad_date}</i>"

        elements.append(Paragraph(degree_line, styles["company"]))
        elements.append(Paragraph(institution, styles["position"]))

        details = []
        if gpa:
            details.append(f"GPA: {gpa}")
        if honors:
            details.append(honors)

        if details:
            elements.append(Paragraph(" | ".join(details), styles["body"]))

        return elements


# Singleton instance
pdf_generator = PDFResumeGenerator()

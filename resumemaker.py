import streamlit as slt
from fpdf import FPDF
import base64

def create_pdf(name, email, phone, linkedin, address, education, work_experience, skills, projects, additional_info):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    
    # Add name
    pdf.set_font("Arial", 'B', 16)
    pdf.cell(200, 10, txt=name, ln=True, align='C')
    pdf.ln(10)
    
    # Add personal details
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt=f"Email: {email}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Phone: {phone}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"LinkedIn: {linkedin}", ln=True, align='L')
    pdf.cell(200, 10, txt=f"Address: {address}", ln=True, align='L')
    
    # Add Education
    pdf.set_font("Arial", 'B', size=14)
    pdf.cell(200, 10, txt="Education", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for edu in education:
        pdf.multi_cell(0, 10, f"Institution: {edu['institution']}\nPeriod: {edu['period']}\nCGPA: {edu['cgpa']}")
        pdf.ln(5)
    
    # Add Work Experience
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Work Experience", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for exp in work_experience:
        pdf.multi_cell(0, 10, f"Company: {exp['company']}\nPeriod: {exp['period']}\nRole: {exp['role']}\nDescription: {exp['description']}")
        pdf.ln(5)
    
    # Add Skills
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Skills", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for skill in skills.split('\n'):
        pdf.cell(200, 10, txt=f"- {skill}", ln=True, align='L')
        pdf.ln(5)
    
    # Add Projects
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Projects", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    for project in projects:
        pdf.multi_cell(0, 10, f"Title: {project['title']}\nDescription: {project['description']}")
        pdf.ln(5)
    
    # Add Additional Information
    pdf.set_font("Arial", 'B', 14)
    pdf.cell(200, 10, txt="Additional Information", ln=True, align='L')
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, additional_info)
    
    return pdf

def main():
    slt.title("Resume Maker App")
    
    # Sidebar with user input
    with slt.sidebar:
        slt.subheader("Personal Information")
        name = slt.text_input("Name")
        email = slt.text_input("Email")
        phone = slt.text_input("Phone")
        linkedin = slt.text_input("LinkedIn URL")
        address = slt.text_area("Address")
        
        slt.subheader("Education")
        education = []
        num_education = slt.number_input("Number of Education Entries", min_value=1, max_value=10)
        for i in range(int(num_education)):
            institution = slt.text_input(f"Institution {i+1}", key=f"institution_{i}")
            period = slt.text_input(f"Time Period {i+1}", key=f"period_{i}")
            cgpa = slt.text_input(f"CGPA {i+1}", key=f"cgpa_{i}")
            education.append({"institution": institution, "period": period, "cgpa": cgpa})
        
        slt.subheader("Work Experience")
        work_experience = []
        num_experience = slt.number_input("Number of Work Experience Entries", min_value=1, max_value=10)
        for i in range(int(num_experience)):
            company = slt.text_input(f"Company {i+1}", key=f"company_{i}")
            period = slt.text_input(f"Time Period {i+1}", key=f"work_period_{i}")
            role = slt.text_input(f"Role {i+1}", key=f"role_{i}")
            description = slt.text_area(f"Description {i+1}", key=f"description_{i}")
            work_experience.append({"company": company, "period": period, "role": role, "description": description})
    
        slt.subheader("Skills (Enter each skill on a new line)")
        skills = slt.text_area("Skills")
        
        slt.subheader("Projects")
        projects = []
        num_projects = slt.number_input("Number of Projects", min_value=1, max_value=10, step=1)
        for i in range(int(num_projects)):
            title = slt.text_input(f"Project Title {i+1}", key=f"project_title_{i}")
            description = slt.text_area(f"Description {i+1}", key=f"project_description_{i}")
            projects.append({"title": title, "description": description})
        
        slt.subheader("Additional Information")
        additional_info = slt.text_area("Additional Information")
    
    # Display the resume
    slt.write(f"## {name}")
    slt.write(f"**Email:** {email}")
    slt.write(f"**Phone:** {phone}")
    slt.write(f"**LinkedIn:** {linkedin}")
    slt.write(f"**Address:** {address}")
    
    slt.write(f"### Education")
    for edu in education:
        slt.write(f"**Institution:** {edu['institution']}")
        slt.write(f"**Period:** {edu['period']}")
        slt.write(f"**CGPA:** {edu['cgpa']}")
        slt.write("")
    
    slt.write(f"### Work Experience")
    for exp in work_experience:
        slt.write(f"**Company:** {exp['company']}")
        slt.write(f"**Period:** {exp['period']}")
        slt.write(f"**Role:** {exp['role']}")
        slt.write(f"**Description:** {exp['description']}")
        slt.write("")
    
    slt.write(f"### Skills")
    for skill in skills.split('\n'):
        slt.write(f"- {skill}")
    
    slt.write(f"### Projects")
    for project in projects:
        slt.write(f"**{project['title']}**")
        slt.write(f"{project['description']}")
    
    slt.write("### Additional Information")
    slt.write(additional_info)
    
    # Create PDF and provide download link
    if slt.button("Download Resume as PDF"):
        pdf = create_pdf(name, email, phone, linkedin, address, education, work_experience, skills, projects, additional_info)
        
        # Save PDF to a temporary file
        pdf_output = f"{name.replace(' ', '_')}_resume.pdf"
        pdf.output(pdf_output)
        
        # Convert the PDF to bytes and encode it in base64
        with open(pdf_output, "rb") as pdf_file:
            pdf_bytes = pdf_file.read()
            b64_pdf = base64.b64encode(pdf_bytes).decode()
        
        # Create a download button
        href = f'<a href="data:application/octet-stream;base64,{b64_pdf}" download="{pdf_output}">Download Resume</a>'
        slt.markdown(href, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

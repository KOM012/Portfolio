import streamlit as st
import datetime
import pandas as pd
from PIL import Image, ImageDraw, ImageFont
import io
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import os

# Page configuration
st.set_page_config(
    page_title="Kean Ocliaso | IT Portfolio",
    page_icon="👨‍🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Email configuration
EMAIL_ADDRESS = "keanocliaso12@gmail.com"  # Your email address
EMAIL_PASSWORD = st.secrets.get("EMAIL_PASSWORD", "")  # Use Streamlit secrets for password

def send_email(name, sender_email, subject, message, company=""):
    """Send email using SMTP"""
    try:
        # Create message
        msg = MIMEMultipart()
        msg['From'] = EMAIL_ADDRESS
        msg['To'] = EMAIL_ADDRESS
        msg['Subject'] = f"Portfolio Contact: {subject} - {name}"
        
        # Create email body
        body = f"""
        New message from your portfolio website:
        
        Name: {name}
        Email: {sender_email}
        Company: {company if company else 'Not provided'}
        Subject: {subject}
        
        Message:
        {message}
        
        ---
        This message was sent from your portfolio contact form.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Connect to Gmail SMTP server
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
            server.send_message(msg)
        
        return True
    except Exception as e:
        st.error(f"Error sending email: {str(e)}")
        return False

# Function to create a placeholder profile picture with initials
def create_profile_picture():
    # Create a blank image with professional blue background
    img = Image.new('RGB', (300, 300), color='#1e3a8a')
    draw = ImageDraw.Draw(img)
    
    # Create a circle for the profile picture
    draw.ellipse([50, 50, 250, 250], fill='#3b82f6')
    
    # Add initials
    try:
        font = ImageFont.truetype("arial.ttf", 100)
    except:
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 100)
        except:
            font = ImageFont.load_default()
    
    text = "KO"
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]
    
    # Center the text
    x = (300 - text_width) // 2
    y = (300 - text_height) // 2
    
    draw.text((x, y), text, fill='white', font=font)
    
    # Save to bytes
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    
    return img_bytes

# Custom CSS for professional styling
st.markdown("""
<style>
    .main-header {
        font-size: 3.5rem;
        font-weight: 700;
        color: #1e3a8a;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        font-size: 1.8rem;
        color: #374151;
        margin-bottom: 2rem;
        font-weight: 400;
    }
    .section-header {
        font-size: 2rem;
        color: #1e3a8a;
        border-bottom: 3px solid #3b82f6;
        padding-bottom: 0.5rem;
        margin-top: 2rem;
        margin-bottom: 1.5rem;
    }
    .card {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border-left: 4px solid #3b82f6;
    }
    .skill-pill {
        display: inline-block;
        background: #3b82f6;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        margin: 0.3rem;
        font-size: 0.9rem;
        font-weight: 500;
    }
    .contact-info {
        background: #1e3a8a;
        color: white;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .project-card {
        background: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
        border: 1px solid #e5e7eb;
        transition: transform 0.3s;
    }
    .project-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
    }
    .role-tag {
        display: inline-block;
        background: #10b981;
        color: white;
        padding: 0.3rem 0.8rem;
        border-radius: 15px;
        font-size: 0.8rem;
        margin-right: 0.5rem;
        margin-bottom: 0.5rem;
    }
    .stButton > button {
        background: linear-gradient(135deg, #3b82f6 0%, #1e3a8a 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 5px;
        font-weight: 600;
    }
    .profile-img {
        border-radius: 50%;
        border: 5px solid #3b82f6;
        box-shadow: 0 10px 25px rgba(0, 0, 0, 0.1);
        width: 200px;
        height: 200px;
        object-fit: cover;
    }
    .achievement-badge {
        display: inline-block;
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 5px;
        margin: 0.5rem 0;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'contact_submitted' not in st.session_state:
    st.session_state.contact_submitted = False
if 'email_sent' not in st.session_state:
    st.session_state.email_sent = False

# Create profile picture
profile_img = create_profile_picture()

# Header Section with Profile Picture
col1, col2, col3 = st.columns([1, 2, 1])

with col1:
    st.image(profile_img, caption="Kean Ocliaso", use_container_width=True)
    st.markdown("<div style='text-align: center;'>📍 Surigao City, Philippines</div>", unsafe_allow_html=True)

with col2:
    st.markdown('<h1 class="main-header">KEAN OCLIASO</h1>', unsafe_allow_html=True)
    st.markdown('<h2 class="sub-header">IT Graduate | Python & Android Developer | Aspiring Project Manager</h2>', unsafe_allow_html=True)
    
    col_stats1, col_stats2, col_stats3 = st.columns(3)
    with col_stats1:
        st.markdown("""
        <div style="text-align: center;">
            <h3>10+</h3>
            <p>Projects Completed</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats2:
        st.markdown("""
        <div style="text-align: center;">
            <h3>4.0</h3>
            <p>GPA Score</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col_stats3:
        st.markdown("""
        <div style="text-align: center;">
            <h3>150+</h3>
            <p>Students Led</p>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown("### Contact")
    st.markdown(f"""
    📧 {EMAIL_ADDRESS}  
    📱 +63 966 725 0875  
    🔗 linkedin.com/in/keanocliaso  
    💻 github.com/KOM012
    """)

# Introduction
st.markdown("""
<div class="card">
    <h3>👋 Welcome to My Portfolio</h3>
    <p>As a graduating IT student at Saint Paul University Surigao with expertise in Python, Java, and Android development, 
    I combine technical proficiency with demonstrated leadership experience. My background as Student Vice Governor and 
    Club President has equipped me with strong project management, team leadership, and strategic planning skills, 
    making me uniquely positioned for roles that bridge technology and management. Currently working on my thesis 
    "AquaSense-AI: Poolsafety Utilizing Computer Vision and Artificial Intelligence."</p>
</div>
""", unsafe_allow_html=True)

# Main content
tab1, tab2, tab3, tab4, tab5 = st.tabs(["🎓 Education & Skills", "💼 Experience", "🚀 Projects", "🏆 Achievements", "📞 Contact"])

with tab1:
    st.markdown('<div class="section-header">Education</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown("""
        <div class="card">
            <h3>🎓 Bachelor of Science in Information Technology</h3>
            <p><strong>Saint Paul University Surigao</strong> | Expected Graduation: June 2024</p>
            <p><strong>Current GPA:</strong> 4.0/4.0 (Dean's Lister All Semesters)</p>
            <p><strong>Relevant Coursework:</strong> Software Engineering, Data Structures & Algorithms, 
            Mobile Application Development, Database Management Systems, Agile Project Management, 
            Cloud Computing, Artificial Intelligence, Web Development, Network Security</p>
            <p><strong>Thesis:</strong> "AquaSense-AI: Poolsafety Utilizing Computer Vision and Artificial Intelligence" - 
            Developing an AI-powered system for pool safety monitoring using computer vision techniques.</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Technical Skills</div>', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("### 🐍 Python Expertise")
        st.markdown("""
        <div class="card">
            <div class="skill-pill">Django</div>
            <div class="skill-pill">Flask</div>
            <div class="skill-pill">FastAPI</div>
            <div class="skill-pill">Pandas</div>
            <div class="skill-pill">NumPy</div>
            <div class="skill-pill">OpenCV</div>
            <div class="skill-pill">TensorFlow</div>
            <div class="skill-pill">Streamlit</div>
            <div class="skill-pill">Automation</div>
            <div class="skill-pill">Web Scraping</div>
            <div class="skill-pill">Computer Vision</div>
            <p><strong>Experience:</strong> 3 years academic + personal projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### ☕ Java & Android Dev")
        st.markdown("""
        <div class="card">
            <div class="skill-pill">Java SE</div>
            <div class="skill-pill">Android SDK</div>
            <div class="skill-pill">Kotlin</div>
            <div class="skill-pill">Room Database</div>
            <div class="skill-pill">REST APIs</div>
            <div class="skill-pill">Firebase</div>
            <div class="skill-pill">Material Design</div>
            <div class="skill-pill">MVVM</div>
            <div class="skill-pill">Git</div>
            <div class="skill-pill">XML Layouts</div>
            <p><strong>Experience:</strong> 2 years academic projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col3:
        st.markdown("### 🛠️ Web & Database")
        st.markdown("""
        <div class="card">
            <div class="skill-pill">HTML/CSS</div>
            <div class="skill-pill">JavaScript</div>
            <div class="skill-pill">React</div>
            <div class="skill-pill">Bootstrap</div>
            <div class="skill-pill">MySQL</div>
            <div class="skill-pill">PostgreSQL</div>
            <div class="skill-pill">MongoDB</div>
            <div class="skill-pill">Git</div>
            <div class="skill-pill">Docker</div>
            <div class="skill-pill">AWS Basics</div>
            <p><strong>Experience:</strong> Academic and personal projects</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Leadership & Soft Skills</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="card">
        <div class="role-tag">Project Management</div>
        <div class="role-tag">Team Leadership</div>
        <div class="role-tag">Strategic Planning</div>
        <div class="role-tag">Public Speaking</div>
        <div class="role-tag">Event Planning</div>
        <div class="role-tag">Mentoring</div>
        <div class="role-tag">Budget Management</div>
        <div class="role-tag">Conflict Resolution</div>
        <div class="role-tag">Agile Methodologies</div>
        <div class="role-tag">Stakeholder Communication</div>
        <div class="role-tag">Problem Solving</div>
        <div class="role-tag">Time Management</div>
    </div>
    """, unsafe_allow_html=True)

with tab2:
    st.markdown('<div class="section-header">Leadership Experience</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="project-card">
        <h3>🏛️ Vice Governor | SPUS Supreme Student Government</h3>
        <p><strong>Saint Paul University Surigao | June 2022 - Present</strong></p>
        <ul>
            <li>Represented 3,000+ students in university governance and policy-making committees</li>
            <li>Managed student organization budgets and facilitated fund allocation</li>
            <li>Led the "Digital Student Services Initiative" to modernize student processes</li>
            <li>Coordinated between 20+ student organizations and university administration</li>
            <li>Organized student welfare programs and academic support initiatives</li>
            <li>Implemented feedback mechanisms that increased student satisfaction by 40%</li>
        </ul>
        <p><strong>Key Achievement:</strong> Successfully advocated for improved campus Wi-Fi infrastructure</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="project-card">
        <h3>👨‍💻 President | SPUS Information Technology Society</h3>
        <p><strong>January 2022 - Present</strong></p>
        <ul>
            <li>Grew membership from 30 to 100+ active IT students within one year</li>
            <li>Organized 15+ technical workshops on Python, Android Development, and Web Technologies</li>
            <li>Led coding bootcamps and hackathons with 200+ total participants</li>
            <li>Established mentorship program pairing senior students with freshmen</li>
            <li>Collaborated with local tech companies for industry exposure sessions</li>
            <li>Managed club budget and secured sponsorships for major events</li>
        </ul>
        <p><strong>Key Achievement:</strong> Increased member participation in tech competitions by 300%</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Technical Experience</div>', unsafe_allow_html=True)
    
    st.markdown("""
    <div class="project-card">
        <h3>💻 Student Developer | SPUS IT Projects</h3>
        <p><strong>January 2022 - Present | Surigao City</strong></p>
        <ul>
            <li>Developed "SPUS Event Manager" - Python Django web app for campus event management</li>
            <li>Created "Paulinian Portal" Android app for student information access</li>
            <li>Built REST APIs for various academic department projects</li>
            <li>Assisted in migrating legacy student databases to modern systems</li>
            <li>Participated in Agile development processes for semester-long projects</li>
            <li>Implemented responsive web designs for mobile-friendly campus applications</li>
        </ul>
        <p><strong>Technologies:</strong> Python, Django, Android, Java, MySQL, JavaScript</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="project-card">
        <h3>📱 Freelance Android Developer</h3>
        <p><strong>June 2022 - Present</strong></p>
        <ul>
            <li>Developed "Surigao Guide" - tourist information app for local visitors</li>
            <li>Created "StudyTrack" - student productivity app with assignment tracking</li>
            <li>Built custom Android applications for small local businesses</li>
            <li>Implemented clean architecture patterns (MVVM) in all projects</li>
            <li>Optimized app performance and reduced memory usage</li>
            <li>Provided technical support and maintenance for deployed applications</li>
        </ul>
        <p><strong>Technologies:</strong> Android, Kotlin, Java, Room Database, Firebase</p>
    </div>
    """, unsafe_allow_html=True)

with tab3:
    st.markdown('<div class="section-header">Academic & Personal Projects</div>', unsafe_allow_html=True)
    
    projects = [
        {
            "title": "AquaSense-AI: Pool Safety System",
            "description": "Thesis project using computer vision and AI to detect drowning incidents and pool safety violations",
            "tech": ["Python", "OpenCV", "TensorFlow", "FastAPI", "React", "PostgreSQL"],
            "features": ["Real-time drowning detection", "Lifeguard alert system", "Pool capacity monitoring", "Violation logging", "Web dashboard"],
            "achievements": "Faculty-approved thesis project, Pilot testing scheduled for 2024",
            "status": "🎓 Thesis Project"
        },
        {
            "title": "SPUS Event Management System",
            "description": "Comprehensive web application for managing university events, registrations, and attendance",
            "tech": ["Python", "Django", "JavaScript", "Bootstrap", "MySQL", "Chart.js"],
            "features": ["Event creation & management", "Online registration", "QR code check-in", "Analytics dashboard", "Email notifications"],
            "achievements": "Adopted by Student Affairs Office, 50+ events managed",
            "status": "🌐 Production"
        },
        {
            "title": "Surigao Tourist Guide App",
            "description": "Android application providing information about tourist spots, restaurants, and events in Surigao",
            "tech": ["Android", "Kotlin", "Google Maps API", "Room Database", "Retrofit"],
            "features": ["Interactive maps", "Offline content", "Event calendar", "Restaurant reviews", "Travel itineraries"],
            "achievements": "500+ downloads, Featured in local tourism office",
            "status": "📱 Published"
        },
        {
            "title": "StudyTrack Student Planner",
            "description": "Android productivity app for students with assignment tracking, schedule management, and grade calculator",
            "tech": ["Android", "Java", "Room Database", "Material Design", "Notifications"],
            "features": ["Assignment tracker", "Class schedule", "Grade calculator", "Study timer", "Progress analytics"],
            "achievements": "4.5★ rating, 1000+ downloads",
            "status": "📱 Published"
        },
        {
            "title": "Inventory Management System",
            "description": "Web-based inventory system for small businesses with barcode scanning and reporting",
            "tech": ["Python", "Flask", "JavaScript", "SQLite", "Bootstrap"],
            "features": ["Barcode generation", "Stock alerts", "Sales reports", "Supplier management", "Mobile responsive"],
            "achievements": "Implemented for 2 local businesses",
            "status": "💼 Commercial"
        }
    ]
    
    for project in projects:
        with st.expander(f"{project['status']} {project['title']}"):
            col1, col2 = st.columns([3, 1])
            with col1:
                st.markdown(f"**Description:** {project['description']}")
                st.markdown("**Key Features:**")
                for feature in project['features']:
                    st.markdown(f"• {feature}")
                st.markdown(f"**Achievements:** {project['achievements']}")
            with col2:
                st.markdown("**Technologies:**")
                for tech in project['tech']:
                    st.markdown(f"`{tech}`")
            
            st.markdown("---")

with tab4:
    st.markdown('<div class="section-header">Academic Achievements</div>', unsafe_allow_html=True)
    
    awards = [
        {"award": "🏆 Dean's Lister (All Semesters)", "year": "2020-2024", "organization": "Saint Paul University Surigao"},
        {"award": "🎖️ Outstanding IT Student Award", "year": "2023", "organization": "SPUS College of Computer Studies"},
        {"award": "🥇 1st Place - University Hackathon", "year": "2023", "organization": "SPUS Tech Innovation Challenge"},
        {"award": "🌟 Leadership Excellence Award", "year": "2023", "organization": "SPUS Student Affairs Office"},
        {"award": "📱 Best Mobile App Project", "year": "2022", "organization": "SPUS IT Department"},
        {"award": "👨‍🏫 Outstanding Student Leader", "year": "2022", "organization": "SPUS Supreme Student Government"},
        {"award": "💡 Innovation Award", "year": "2022", "organization": "SPUS Research and Development"},
        {"award": "🎯 Academic Scholarship Grantee", "year": "2020-2024", "organization": "Saint Paul University Surigao"},
    ]
    
    for award in awards:
        st.markdown(f"""
        <div class="project-card">
            <h4>{award['award']}</h4>
            <p><strong>{award['year']}</strong> | {award['organization']}</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="section-header">Certifications & Training</div>', unsafe_allow_html=True)
    
    certs = [
        "Google IT Automation with Python Professional Certificate (Coursera, 2023)",
        "Android App Development Specialization (Coursera, 2022)",
        "Python for Everybody Specialization (Coursera, 2022)",
        "Agile Project Management (Google/Coursera, 2023)",
        "Introduction to Computer Vision with OpenCV (Udemy, 2023)",
        "Web Development Bootcamp (FreeCodeCamp, 2022)",
        "Git and GitHub Complete Masterclass (Udemy, 2022)",
        "Database Management Essentials (Coursera, 2021)"
    ]
    
    for cert in certs:
        st.markdown(f"✅ {cert}")

with tab5:
    st.markdown('<div class="section-header">Get in Touch</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("### Contact Information")
        st.markdown(f"""
        <div class="contact-info">
            <p>📧 <strong>Email:</strong> {EMAIL_ADDRESS}</p>
            <p>📱 <strong>Phone:</strong> +63 966 725 0875</p>
            <p>📍 <strong>Location:</strong> Surigao City, Philippines</p>
            <p>🔗 <strong>LinkedIn:</strong> linkedin.com/in/keanocliaso</p>
            <p>💻 <strong>GitHub:</strong> github.com/KOM012</p>
            <p>🎓 <strong>University:</strong> Saint Paul University Surigao</p>
            <p>📅 <strong>Graduation:</strong> April 2024</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("### Career Interests")
        st.markdown("""
        <div class="card">
            <p><strong>🟢 Status:</strong> Open to Opportunities (Starting June 2024)</p>
            <p><strong>🎯 Preferred Roles:</strong></p>
            <ul>
                <li>Junior Software Developer</li>
                <li>Android Developer</li>
                <li>Python Developer</li>
                <li>Project Management Trainee</li>
                <li>Full-Stack Developer</li>
            </ul>
            <p><strong>📍 Preferred Location:</strong> Surigao, Cebu or Remote</p>
            <p><strong>📅 Availability:</strong> Full-time from June 2024</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("### Send Me a Message")
        
        if st.session_state.contact_submitted and st.session_state.email_sent:
            st.success("✅ Thank you for your message! I've received it and will get back to you within 24 hours.")
            if st.button("Send another message"):
                st.session_state.contact_submitted = False
                st.session_state.email_sent = False
                st.rerun()
        elif st.session_state.contact_submitted and not st.session_state.email_sent:
            st.warning("⚠️ Message saved! To enable email delivery, please set up email credentials.")
            if st.button("Send another message"):
                st.session_state.contact_submitted = False
                st.rerun()
        else:
            with st.form("contact_form"):
                name = st.text_input("Your Name *")
                email = st.text_input("Your Email *")
                company = st.text_input("Company/Organization")
                subject = st.selectbox(
                    "Subject *",
                    ["Job Opportunity", "Project Inquiry", "Collaboration", "Internship", "Mentorship", "Other"]
                )
                message = st.text_area("Your Message *", height=150, 
                                      placeholder="Hi Kean, I came across your portfolio and...")
                
                submitted = st.form_submit_button("Send Message")
                
                if submitted:
                    if name and email and message:
                        # Store message in session state
                        st.session_state.contact_data = {
                            "name": name,
                            "email": email,
                            "company": company,
                            "subject": subject,
                            "message": message
                        }
                        
                        # Try to send email if credentials are available
                        if EMAIL_PASSWORD:
                            email_sent = send_email(name, email, subject, message, company)
                            st.session_state.email_sent = email_sent
                        else:
                            st.session_state.email_sent = False
                            st.info("ℹ️ For actual email delivery, please set up email credentials in Streamlit secrets.")
                        
                        st.session_state.contact_submitted = True
                        st.rerun()
                    else:
                        st.error("Please fill in all required fields (*)")

# Footer
st.markdown("---")
col1, col2, col3 = st.columns(3)
with col2:
    current_year = datetime.datetime.now().year
    st.markdown(f"<p style='text-align: center; color: #6b7280;'>© {current_year} Kean Ocliaso. All rights reserved.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; color: #6b7280;'>Built with Python & Streamlit • Last Updated: February 2026</p>", unsafe_allow_html=True)

# Sidebar with additional info
with st.sidebar:
    st.markdown("## Quick Links")
    st.markdown("[📄 Download Resume (PDF)](#)")
    st.markdown("[📧 Email Me](mailto:keanocliaso12@gmail.com)")
    st.markdown("[💼 LinkedIn Profile](#)")
    st.markdown("[💻 GitHub Portfolio](#https://github.com/KOM012)")
    
    st.markdown("---")
    
    st.markdown("## About This Portfolio")
    st.markdown("""
    This portfolio was built using:
    - **Python** with **Streamlit**
    - Custom CSS styling
    
    Features:
    - Responsive design
    - Contact form with email integration
    - Interactive project showcases
    - Mobile-friendly layout
    """)
    
    st.markdown("---")
    
    st.markdown("## Tech Stack Proficiency")
    
    st.markdown("**Python:**")
    st.progress(0.85)
    
    st.markdown("**Android Development:**")
    st.progress(0.60)
    
    st.markdown("**Java Programming:**")
    st.progress(0.70)
    
    st.markdown("**Web Development:**")
    st.progress(0.75)
    
    st.markdown("**Project Management:**")
    st.progress(0.80)
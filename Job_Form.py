import streamlit as st
import requests
import json
from datetime import datetime

# ====== CONFIG FROM SECRETS ======
UPLOADCARE_PUBLIC_KEY = st.secrets["UPLOADCARE_PUBLIC_KEY"]
AIRTABLE_API_TOKEN = st.secrets["AIRTABLE_API_TOKEN"]
AIRTABLE_BASE_ID = st.secrets["AIRTABLE_BASE_ID"]
AIRTABLE_TABLE_NAME = st.secrets["AIRTABLE_TABLE_NAME"]


AIRTABLE_ENDPOINT = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{AIRTABLE_TABLE_NAME}"
HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_TOKEN}",
    "Content-Type": "application/json"
}

def rtl(text):
    return f"<div dir='rtl' style='text-align: right'>{text}</div>"

nationality_list = sorted([
    "United Arab Emirates", "Saudi Arabia", "India", "Pakistan", "Egypt", "Philippines", "Bangladesh",
    "United Kingdom", "United States", "Canada", "Australia", "Jordan", "Lebanon", "Syria",
    "Sudan", "Yemen", "Afghanistan", "Oman", "Qatar", "Bahrain", "Morocco", "Tunisia", "Algeria",
    "Somalia", "Ethiopia", "Nepal", "Sri Lanka", "Indonesia", "Malaysia", "Others"
])

def upload_to_uploadcare(file):
    upload_url = "https://upload.uploadcare.com/base/"
    files = {"file": (file.name, file.getvalue())}
    data = {
        "UPLOADCARE_PUB_KEY": UPLOADCARE_PUBLIC_KEY,
        "UPLOADCARE_STORE": "1"
    }
    response = requests.post(upload_url, files=files, data=data)
    if response.status_code == 200:
        result = response.json()
        file_uuid = result.get("file")
        if file_uuid:
            return f"https://ucarecdn.com/{file_uuid}/"
    else:
        st.write(f"📦 Uploadcare response code: {response.status_code}")
        st.write(f"📄 Uploadcare response content: {response.text}")
    return None

def submit_to_airtable(data):
    payload = {"fields": data}
    response = requests.post(AIRTABLE_ENDPOINT, headers=HEADERS, data=json.dumps(payload))
    if response.status_code in (200, 201):
        return True
    else:
        st.write(f"Airtable submission failed with status code: {response.status_code}")
        st.write(f"Airtable response: {response.text}")
        return False

st.set_page_config(page_title="Job Application / طلب وظيفة", layout="centered")

lang = st.radio("Language / اللغة", ["English", "Arabic 🇸🇦"], horizontal=True)

with st.form("job_form", clear_on_submit=True):
    if lang == "English":
        st.markdown("<h2 style='text-align: center; color: navy;'>Job Application Form</h2>", unsafe_allow_html=True)
        st.subheader("📝 Personal Information")
        col1, col2 = st.columns(2)
        first_name = col1.text_input("First Name *")
        last_name = col2.text_input("Last Name *")
        phone = col1.text_input("Phone Number *")
        email = col2.text_input("Email *")

        age_group_col, gender_col = st.columns(2)
        age_group = age_group_col.selectbox("Age Group *", ["18-24", "25-34", "35-44", "45-54", "55+"])
        gender = gender_col.radio("Gender *", ["Male", "Female"], horizontal=True)

        nationality = st.selectbox("Nationality *", nationality_list)
        emirate = st.selectbox("Select Emirate *", [
            "Dubai", "Abu Dhabi", "Sharjah", "Ajman", "Umm Al Quwain", "Ras Al Khaimah", "Fujairah"
        ])

        st.subheader("🎯 Position Applied For")
        job_title = st.selectbox("Job Title *", [
            "Consultant", "General Practitioner Doctor (Gp)", "Doctor Specialist", "Assistant Pharmacist",
            "Social worker", "Psychologist", "Human Resource Administrative", "Customer Happiness Executive"
        ])
        current_status = st.radio("Current Status *", [
            "Fresh Graduate", "Currently Unemployed", "Employed", "Retired"
        ])

        experience = st.selectbox("Years of Experience", [
            "0-2 years", "3-5 years", "6-10 years", "10+ years"
        ])
        last_job = st.text_input("Current or Last Job Title")
        last_entity = st.text_input("Current or Last Entity Name")

        salary = st.text_input("Salary Expectation (AED)")
        notice = st.text_input("Notice Period (in days)")

        education = st.selectbox("Education Level *", [
            "High School / Secondary", "Diploma", "Associate Degree", "Bachelor's Degree",
            "Postgraduate Diploma / Higher Diploma", "Master's Degree", "Doctorate / PhD",
            "Fellowship / Board Certification", "Professional Certification", "Vocational Training",
            "Technical Certificate", "Medical Board Certification", "Residency Program", "Other (Please Specify)"
        ])

        st.subheader("📎 Upload CV")
        cv_file = st.file_uploader("Upload CV (PDF/DOC) *", type=['pdf', 'doc', 'docx'])

    else:
        st.markdown(rtl("<h2 style='text-align: center; color: navy;'>طلب تقديم على وظيفة</h2>"), unsafe_allow_html=True)
        st.markdown(rtl("📝 المعلومات الشخصية"), unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        first_name = col1.text_input("الاسم الأول *")
        last_name = col2.text_input("اسم العائلة *")
        phone = col1.text_input("رقم الهاتف *")
        email = col2.text_input("البريد الإلكتروني *")

        age_group_col, gender_col = st.columns(2)
        age_group = age_group_col.selectbox("الفئة العمرية *", ["18-24", "25-34", "35-44", "45-54", "55+"])
        gender = gender_col.radio("الجنس *", ["ذكر", "أنثى"], horizontal=True)

        nationality = st.selectbox("الجنسية *", nationality_list)
        emirate = st.selectbox("اختر الإمارة *", [
            "دبي", "أبوظبي", "الشارقة", "عجمان", "أم القيوين", "رأس الخيمة", "الفجيرة"
        ])

        st.markdown(rtl("💼 معلومات الوظيفة"), unsafe_allow_html=True)
        job_title = st.selectbox("المسمى الوظيفي *", [
            "طبيب إستشاري", "طبيب ممارس عام", "طبيب أخصائي", "مساعد صيدلي",
            "أخصائي خدمة اجتماعية", "أخصائي اجتماعي", "إداري موارد بشرية", "تنفيذي إسعاد المتعاملين"
        ])
        current_status = st.radio("الحالة الحالية *", [
            "خريج جديد", "عاطل عن العمل", "موظف", "متقاعد"
        ])

        experience = st.selectbox("سنوات الخبرة", [
            "0-2 سنوات", "3-5 سنوات", "6-10 سنوات", "أكثر من 10 سنوات"
        ])
        last_job = st.text_input("المسمى الوظيفي الحالي أو الأخير")
        last_entity = st.text_input("اسم الجهة الحالية أو الأخيرة")

        salary = st.text_input("الراتب المتوقع (بالدرهم)")
        notice = st.text_input("فترة الإشعار (بالأيام)")

        education = st.selectbox("المستوى التعليمي *", [
            "الثانوية العامة", "دبلوم", "دبلوم متوسط", "بكالوريوس",
            "دبلوم عالي / دبلوم دراسات عليا", "ماجستير", "دكتوراه",
            "زمالة / شهادة البورد", "شهادة مهنية", "تدريب مهني",
            "شهادة فنية", "شهادة البورد الطبي", "برنامج الإقامة الطبية", "أخرى (يرجى التحديد)"
        ])

        st.markdown(rtl("📎 تحميل السيرة الذاتية"), unsafe_allow_html=True)
        cv_file = st.file_uploader("تحميل السيرة الذاتية (PDF/DOC) *", type=['pdf', 'doc', 'docx'])

    submitted = st.form_submit_button("✅ Submit / إرسال")

    if submitted:
        required_fields = [first_name, last_name, phone, email, gender, age_group, nationality, emirate, job_title,
                           current_status, education, cv_file]
        if not all(required_fields):
            st.error("❗ Please complete all required fields / الرجاء تعبئة جميع الحقول المطلوبة")
        else:
            st.info("Uploading your CV, please wait...")
            cv_url = upload_to_uploadcare(cv_file)
            if not cv_url:
                st.error("Failed to upload CV. Please try again.")
            else:
                data = {
                    "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "First Name": first_name,
                    "Last Name": last_name,
                    "Gender": gender,
                    "Email": email,
                    "Phone Number": phone,
                    "Nationality": nationality,
                    "Age Group": age_group,
                    "Education Level": education,
                    "Years of Experience": experience,
                    "Current or Last Job Title": last_job,
                    "Current or Last Entity Name": last_entity,
                    "Notice Period": notice,
                    "Salary Expectation": salary,
                    "Emirate": emirate,
                    "Job Title": job_title,
                    "Current Status": current_status,
                    "Resume (CV) Link": cv_url
                }
                success = submit_to_airtable(data)
                if success:
                    st.success("✅ Your application has been submitted successfully!")
                    st.balloons()
                else:
                    st.error("Failed to submit application to Airtable. Please try again later.")

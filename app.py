import streamlit as st
import os
import fitz
import pandas as pd
from PIL import Image
from docx import Document
from gemini import chat_with_knowledge_base, generate_comprehensive_report
import io
from dotenv import load_dotenv
load_dotenv()  


st.set_page_config(
    page_title="Iron Core Fitness Dashboard",
    page_icon="🏋️‍♂️",
    layout="wide",
    initial_sidebar_state="expanded"
)

@st.cache_data
def load_knowledge_base():
    """Load knowledge base from docx file and Excel data"""
    try:
        doc = Document("attached_assets/IronCore_Fitness_Knowledge_Base_1761407193906.docx")
        knowledge_text = "\n".join([paragraph.text for paragraph in doc.paragraphs])
        
        users = pd.read_excel("attached_assets/IronCore Dataset_1761407212823.xlsx", sheet_name='Users')
        payments = pd.read_excel("attached_assets/IronCore Dataset_1761407212823.xlsx", sheet_name='Payments')
        expenses = pd.read_excel("attached_assets/IronCore Dataset_1761407212823.xlsx", sheet_name='Expenses')
        
        excel_summary = f"""

ADDITIONAL DATASET SUMMARY:

USERS DATA (100 members):
- Total Members: {len(users)}
- Active Members: {len(users[users['Status'] == 'Active'])}
- Inactive Members: {len(users[users['Status'] == 'Inactive'])}
- Membership Distribution:
{users['Membership'].value_counts().to_string()}
- Gender Distribution:
{users['Gender'].value_counts().to_string()}
- Average Age: {users['Age'].mean():.1f} years
- Average BMI: {users['BMI'].mean():.1f}
- Most Common Goal: {users['Goal'].value_counts().index[0]} ({users['Goal'].value_counts().values[0]} members)

PAYMENTS DATA (100 transactions):
- Total Revenue: ${payments['Amount'].sum():,.2f}
- Average Payment: ${payments['Amount'].mean():,.2f}
- Payment Methods:
{payments['Mode'].value_counts().to_string()}
- Payment Status:
{payments['Status'].value_counts().to_string()}

EXPENSES DATA (90 records):
- Total Expenses: ${expenses['Amount'].sum():,.2f}
- Expense Categories:
{expenses.groupby('ExpenseType')['Amount'].sum().to_string()}
- Average Expense: ${expenses['Amount'].mean():,.2f}

FINANCIAL METRICS:
- Total Revenue: ${payments['Amount'].sum():,.2f}
- Total Expenses: ${expenses['Amount'].sum():,.2f}
- Net Profit: ${payments['Amount'].sum() - expenses['Amount'].sum():,.2f}
- Profit Margin: {((payments['Amount'].sum() - expenses['Amount'].sum()) / payments['Amount'].sum() * 100):.1f}%
"""
        
        return knowledge_text + excel_summary
    except Exception as e:
        st.error(f"Error loading knowledge base: {e}")
        return ""

@st.cache_data
def convert_pdf_to_image():
    """Convert PDF dashboard to image using PyMuPDF"""
    try:
        pdf_path = "attached_assets/GYM_Project_PDF_1761407385211.pdf"
        with fitz.open(pdf_path) as pdf_document:
            page = pdf_document[0]
            pix = page.get_pixmap(matrix=fitz.Matrix(3, 3))
            img_data = pix.tobytes("png")
        image = Image.open(io.BytesIO(img_data))
        return image
    except Exception as e:
        st.error(f"Error converting PDF: {e}")
        return None

def display_header():
    """Display header with company branding"""
    st.markdown("""
        <h1 style='text-align: center; color: #ff0000; font-size: 48px;'>🏋️‍♂️ IRON CORE FITNESS COMPANY</h1>
        <p style='text-align: center; font-size: 24px; color: #666;'>Performance Dashboard & AI Assistant</p>
        <hr style='margin-bottom: 20px;'>
    """, unsafe_allow_html=True)

def main():
    display_header()
    
    knowledge_base = load_knowledge_base()
    
    main_col, chat_col = st.columns([2, 1])
    
    with main_col:
        st.markdown("### 📊 BI Dashboard")
        
        dashboard_image = convert_pdf_to_image()
        if dashboard_image:
            st.image(dashboard_image, use_container_width=True, caption="Iron Core Fitness Analytics Dashboard")
        else:
            st.warning("Dashboard visualization unavailable")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if st.button("📄 Generate Comprehensive Report", type="primary"):
            with st.spinner("Generating comprehensive insights report..."):
                if not os.environ.get("GEMINI_API_KEY"):
                    st.error("⚠️ GEMINI_API_KEY not set. Please add API key.")
                else:
                    report = generate_comprehensive_report(knowledge_base)
                    st.markdown("### 📋 Comprehensive Business Insights Report")
                    st.markdown(report)
    
    with chat_col:
        st.markdown("### 🤖 AI Assistant")
        st.markdown("*Ask questions about the dataset*")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []
        if 'messages' not in st.session_state:
            st.session_state.messages = []
        
        chat_container = st.container(height=500)
        with chat_container:
            for message in st.session_state.messages:
                with st.chat_message(message["role"]):
                    st.markdown(message["content"])
        
        if prompt := st.chat_input("Ask about revenue, clients, trainers, etc."):
            st.session_state.messages.append({"role": "user", "content": prompt})
            
            if not os.environ.get("GEMINI_API_KEY"):
                response = "⚠️ Please set your GEMINI_API_KEY to use the chatbot."
            else:
                with st.spinner("Thinking..."):
                    response = chat_with_knowledge_base(prompt, knowledge_base, st.session_state.chat_history)
                    st.session_state.chat_history.append(f"User: {prompt}")
                    st.session_state.chat_history.append(f"Assistant: {response}")
            
            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()
        
        if st.button("🗑️ Clear Chat"):
            st.session_state.messages = []
            st.session_state.chat_history = []
            st.rerun()
        
        with st.expander("💡 Sample Questions"):
            st.markdown("""
            - What's the total revenue and profit?
            - Which membership has the most subscribers?
            - How many active clients do we have?
            - What's the average age of our members?
            - What are the top expense categories?
            - What payment methods are most popular?
            - What's the most common fitness goal?
            - What's our profit margin?
            """)

if __name__ == "__main__":
    main()

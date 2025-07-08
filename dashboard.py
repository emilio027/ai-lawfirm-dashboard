import streamlit as st
import pandas as pd
import os
from datetime import datetime, timedelta
import hashlib
import json
from pathlib import Path
import time

# Configure page
st.set_page_config(
    page_title="LegalDoc Pro - Document Management Dashboard",
    page_icon="⚖️",
    layout="wide"
)

# Initialize session state
if 'documents' not in st.session_state:
    st.session_state.documents = []
if 'clients' not in st.session_state:
    st.session_state.clients = []
if 'time_entries' not in st.session_state:
    st.session_state.time_entries = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'username' not in st.session_state:
    st.session_state.username = ""

# Login function
def login():
    st.markdown("""
    <div style="text-align: center; padding: 50px 0;">
        <h1>⚖️ LegalDoc Pro</h1>
        <h3>Document Management for Small Law Firms</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Center the login form
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col2:
        st.markdown("### 🔐 Login")
        
        with st.form("login_form"):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input("Password", type="password", placeholder="Enter your password")
            login_button = st.form_submit_button("Login", use_container_width=True)
            
            if login_button:
                if username == "admin" and password == "admin123":
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.success("Login successful! Redirecting...")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("Invalid username or password. Please try again.")
        
        # Demo credentials info
        st.markdown("---")
        st.markdown("**Demo Credentials:**")
        st.markdown("Username: `admin`")
        st.markdown("Password: `admin123`")

# Logout function
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    st.rerun()

# Check if user is logged in
if not st.session_state.logged_in:
    login()
    st.stop()

# If logged in, show the main dashboard
if not st.session_state.documents:
    st.session_state.documents = [
        {
            'id': 1,
            'name': 'Divorce_Settlement_Agreement_Smith.pdf',
            'client': 'John Smith',
            'matter': 'Divorce Proceedings',
            'type': 'Settlement Agreement',
            'date_uploaded': '2024-01-15',
            'file_size': '2.1 MB',
            'status': 'Final',
            'content': None
        },
        {
            'id': 2,
            'name': 'LLC_Formation_TechCorp.pdf',
            'client': 'TechCorp LLC',
            'matter': 'Business Formation',
            'type': 'Articles of Incorporation',
            'date_uploaded': '2024-01-20',
            'file_size': '1.8 MB',
            'status': 'Draft',
            'content': None
        },
        {
            'id': 3,
            'name': 'Child_Custody_Motion_Johnson.pdf',
            'client': 'Mary Johnson',
            'matter': 'Child Custody',
            'type': 'Court Motion',
            'date_uploaded': '2024-01-25',
            'file_size': '3.2 MB',
            'status': 'Filed',
            'content': None
        },
        {
            'id': 4,
            'name': 'Prenuptial_Agreement_Williams.pdf',
            'client': 'Sarah Williams',
            'matter': 'Prenuptial Agreement',
            'type': 'Contract',
            'date_uploaded': '2024-01-30',
            'file_size': '1.5 MB',
            'status': 'Under Review',
            'content': None
        },
        {
            'id': 5,
            'name': 'Business_Partnership_Agreement_ABC.pdf',
            'client': 'ABC Partners',
            'matter': 'Partnership Formation',
            'type': 'Partnership Agreement',
            'date_uploaded': '2024-02-05',
            'file_size': '2.8 MB',
            'status': 'Final',
            'content': None
        },
        {
            'id': 6,
            'name': 'Child_Support_Modification_Brown.pdf',
            'client': 'Michael Brown',
            'matter': 'Child Support Modification',
            'type': 'Court Motion',
            'date_uploaded': '2024-02-10',
            'file_size': '1.9 MB',
            'status': 'Filed',
            'content': None
        },
        {
            'id': 7,
            'name': 'Commercial_Lease_Agreement_RetailCorp.pdf',
            'client': 'RetailCorp Inc',
            'matter': 'Commercial Lease',
            'type': 'Lease Agreement',
            'date_uploaded': '2024-02-15',
            'file_size': '3.5 MB',
            'status': 'Under Review',
            'content': None
        },
        {
            'id': 8,
            'name': 'Adoption_Papers_Davis.pdf',
            'client': 'Jennifer Davis',
            'matter': 'Adoption Proceedings',
            'type': 'Court Filing',
            'date_uploaded': '2024-02-20',
            'file_size': '2.2 MB',
            'status': 'Pending',
            'content': None
        },
        {
            'id': 9,
            'name': 'Employment_Contract_StartupXYZ.pdf',
            'client': 'StartupXYZ LLC',
            'matter': 'Employment Contracts',
            'type': 'Employment Contract',
            'date_uploaded': '2024-02-25',
            'file_size': '1.4 MB',
            'status': 'Draft',
            'content': None
        },
        {
            'id': 10,
            'name': 'Divorce_Complaint_Thompson.pdf',
            'client': 'Lisa Thompson',
            'matter': 'Divorce Filing',
            'type': 'Court Complaint',
            'date_uploaded': '2024-03-01',
            'file_size': '2.7 MB',
            'status': 'Filed',
            'content': None
        }
    ]

if not st.session_state.clients:
    st.session_state.clients = [
        {'name': 'John Smith', 'type': 'Individual', 'active_matters': 1},
        {'name': 'TechCorp LLC', 'type': 'Business', 'active_matters': 2},
        {'name': 'Mary Johnson', 'type': 'Individual', 'active_matters': 1},
        {'name': 'Sarah Williams', 'type': 'Individual', 'active_matters': 1},
        {'name': 'ABC Partners', 'type': 'Business', 'active_matters': 1},
        {'name': 'Michael Brown', 'type': 'Individual', 'active_matters': 1},
        {'name': 'RetailCorp Inc', 'type': 'Business', 'active_matters': 1},
        {'name': 'Jennifer Davis', 'type': 'Individual', 'active_matters': 1},
        {'name': 'StartupXYZ LLC', 'type': 'Business', 'active_matters': 1},
        {'name': 'Lisa Thompson', 'type': 'Individual', 'active_matters': 1}
    ]

# Sidebar
st.sidebar.title("⚖️ LegalDoc Pro")
st.sidebar.markdown("*Document Management for Small Law Firms*")
st.sidebar.markdown(f"Welcome, **{st.session_state.username}**!")

# Logout button
if st.sidebar.button("🚪 Logout"):
    logout()

# Navigation
page = st.sidebar.selectbox(
    "Navigate",
    ["Dashboard", "Document Management", "Client Management", "Time Tracking", "Reports"]
)

# Main content
if page == "Dashboard":
    st.title("📊 Dashboard Overview")
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Documents", len(st.session_state.documents), "5 this week")
    
    with col2:
        st.metric("Active Clients", len(st.session_state.clients), "1 new")
    
    with col3:
        st.metric("Pending Reviews", 2, "-1")
    
    with col4:
        st.metric("Hours This Week", 42.5, "8.5")
    
    st.divider()
    
    # Recent activity
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📋 Recent Documents")
        recent_docs = sorted(st.session_state.documents, key=lambda x: x['date_uploaded'], reverse=True)[:5]
        for doc in recent_docs:
            with st.container():
                st.markdown(f"**{doc['name']}**")
                st.markdown(f"Client: {doc['client']} | {doc['date_uploaded']}")
                st.markdown("---")
    
    with col2:
        st.subheader("⏰ Today's Schedule")
        st.markdown("**9:00 AM** - Client consultation (Smith)")
        st.markdown("**11:30 AM** - Document review (TechCorp)")
        st.markdown("**2:00 PM** - Court filing deadline")
        st.markdown("**4:00 PM** - Settlement negotiation call")

elif page == "Document Management":
    st.title("📁 Document Management")
    
    # Search and filter section
    col1, col2, col3 = st.columns(3)
    
    with col1:
        search_term = st.text_input("🔍 Search documents", placeholder="Enter keywords...")
    
    with col2:
        client_filter = st.selectbox("Filter by Client", ["All"] + [client['name'] for client in st.session_state.clients])
    
    with col3:
        doc_type_filter = st.selectbox("Filter by Type", ["All", "Settlement Agreement", "Articles of Incorporation", "Court Motion", "Contract", "Partnership Agreement", "Lease Agreement", "Court Filing", "Employment Contract", "Court Complaint"])
    
    # Upload section
    st.subheader("📤 Upload New Document")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        uploaded_file = st.file_uploader("Choose file", type=['pdf', 'docx', 'txt'])
    
    with col2:
        upload_client = st.selectbox("Select Client", [client['name'] for client in st.session_state.clients])
    
    with col3:
        upload_matter = st.text_input("Matter Description")
    
    if uploaded_file and upload_client and upload_matter:
        if st.button("Upload Document"):
            # Read the file content
            file_content = uploaded_file.read()
            
            # Calculate file size
            file_size_kb = len(file_content) / 1024
            if file_size_kb > 1024:
                file_size_str = f"{file_size_kb / 1024:.1f} MB"
            else:
                file_size_str = f"{file_size_kb:.1f} KB"
            
            # Determine document type based on file name
            doc_type = "General Document"
            filename_lower = uploaded_file.name.lower()
            if "contract" in filename_lower or "agreement" in filename_lower:
                doc_type = "Contract"
            elif "motion" in filename_lower or "complaint" in filename_lower:
                doc_type = "Court Motion"
            elif "llc" in filename_lower or "incorporation" in filename_lower:
                doc_type = "Articles of Incorporation"
            elif "lease" in filename_lower:
                doc_type = "Lease Agreement"
            elif "employment" in filename_lower:
                doc_type = "Employment Contract"
            
            new_doc = {
                'id': len(st.session_state.documents) + 1,
                'name': uploaded_file.name,
                'client': upload_client,
                'matter': upload_matter,
                'type': doc_type,
                'date_uploaded': datetime.now().strftime('%Y-%m-%d'),
                'file_size': file_size_str,
                'status': 'New',
                'content': file_content
            }
            st.session_state.documents.append(new_doc)
            st.success(f"Document '{uploaded_file.name}' uploaded successfully!")
            st.rerun()
    
    st.divider()
    
    # Document list
    st.subheader("📋 Document Library")
    
    # Filter documents
    filtered_docs = st.session_state.documents
    
    if search_term:
        filtered_docs = [doc for doc in filtered_docs if search_term.lower() in doc['name'].lower() or search_term.lower() in doc['client'].lower()]
    
    if client_filter != "All":
        filtered_docs = [doc for doc in filtered_docs if doc['client'] == client_filter]
    
    if doc_type_filter != "All":
        filtered_docs = [doc for doc in filtered_docs if doc['type'] == doc_type_filter]
    
    # Display documents
    for doc in filtered_docs:
        with st.expander(f"{doc['name']} - {doc['client']}"):
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"**Client:** {doc['client']}")
                st.markdown(f"**Matter:** {doc['matter']}")
                st.markdown(f"**Type:** {doc['type']}")
            
            with col2:
                st.markdown(f"**Date:** {doc['date_uploaded']}")
                st.markdown(f"**Size:** {doc['file_size']}")
                st.markdown(f"**Status:** {doc['status']}")
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("📖 View", key=f"view_{doc['id']}"):
                    if doc.get('content'):
                        st.info("Document content loaded successfully!")
                        # In a real app, you'd display the PDF content here
                    else:
                        st.info("This is a demo document - no content to display.")
            with col2:
                if st.button("📝 Edit", key=f"edit_{doc['id']}"):
                    st.info("Edit functionality would open here.")
            with col3:
                if st.button("📥 Download", key=f"download_{doc['id']}"):
                    if doc.get('content'):
                        st.download_button(
                            label="Click to Download",
                            data=doc['content'],
                            file_name=doc['name'],
                            mime="application/pdf",
                            key=f"dl_{doc['id']}"
                        )
                    else:
                        st.info("Demo document - no file to download.")
            with col4:
                if st.button("🗑️ Delete", key=f"delete_{doc['id']}"):
                    st.session_state.documents = [d for d in st.session_state.documents if d['id'] != doc['id']]
                    st.success(f"Document '{doc['name']}' deleted!")
                    st.rerun()

elif page == "Client Management":
    st.title("👥 Client Management")
    
    # Add new client
    st.subheader("➕ Add New Client")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        new_client_name = st.text_input("Client Name")
    
    with col2:
        new_client_type = st.selectbox("Client Type", ["Individual", "Business"])
    
    with col3:
        st.write("")  # Spacing
        if st.button("Add Client") and new_client_name:
            new_client = {
                'name': new_client_name,
                'type': new_client_type,
                'active_matters': 0
            }
            st.session_state.clients.append(new_client)
            st.success(f"Client '{new_client_name}' added successfully!")
            st.rerun()
    
    st.divider()
    
    # Client list
    st.subheader("📋 Client List")
    
    df = pd.DataFrame(st.session_state.clients)
    st.dataframe(df, use_container_width=True)
    
    # Client details
    if st.session_state.clients:
        selected_client = st.selectbox("Select client for details", [client['name'] for client in st.session_state.clients])
        
        if selected_client:
            client_docs = [doc for doc in st.session_state.documents if doc['client'] == selected_client]
            
            st.subheader(f"Documents for {selected_client}")
            
            if client_docs:
                for doc in client_docs:
                    st.markdown(f"• **{doc['name']}** ({doc['type']}) - {doc['status']}")
            else:
                st.info("No documents found for this client.")

elif page == "Time Tracking":
    st.title("⏱️ Time Tracking")
    
    # Active timer
    st.subheader("🟢 Active Timer")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        timer_client = st.selectbox("Client", [client['name'] for client in st.session_state.clients])
    
    with col2:
        timer_matter = st.text_input("Matter/Task")
    
    with col3:
        timer_rate = st.number_input("Hourly Rate ($)", min_value=0.0, value=250.0, step=25.0)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("▶️ Start Timer"):
            st.success("Timer started!")
    
    with col2:
        if st.button("⏹️ Stop Timer"):
            st.info("Timer stopped. 1.5 hours recorded.")
    
    st.divider()
    
    # Manual time entry
    st.subheader("📝 Manual Time Entry")
    
    col1, col2 = st.columns(2)
    
    with col1:
        entry_date = st.date_input("Date")
        entry_client = st.selectbox("Client ", [client['name'] for client in st.session_state.clients])
        entry_hours = st.number_input("Hours", min_value=0.0, max_value=24.0, value=1.0, step=0.25)
    
    with col2:
        entry_description = st.text_area("Description")
        entry_rate = st.number_input("Rate ($)", min_value=0.0, value=250.0, step=25.0)
    
    if st.button("Add Time Entry"):
        if entry_client and entry_description:
            new_entry = {
                'date': entry_date,
                'client': entry_client,
                'hours': entry_hours,
                'description': entry_description,
                'rate': entry_rate,
                'amount': entry_hours * entry_rate
            }
            st.session_state.time_entries.append(new_entry)
            st.success("Time entry added successfully!")
            st.rerun()
    
    st.divider()
    
    # Recent time entries
    st.subheader("📋 Recent Time Entries")
    
    if st.session_state.time_entries:
        df = pd.DataFrame(st.session_state.time_entries)
        st.dataframe(df, use_container_width=True)
    else:
        st.info("No time entries yet.")

elif page == "Reports":
    st.title("📊 Reports & Analytics")
    
    # Date range selector
    col1, col2 = st.columns(2)
    
    with col1:
        start_date = st.date_input("Start Date", value=datetime.now() - timedelta(days=30))
    
    with col2:
        end_date = st.date_input("End Date", value=datetime.now())
    
    st.divider()
    
    # Document statistics
    st.subheader("📁 Document Statistics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        doc_types = {}
        for doc in st.session_state.documents:
            doc_types[doc['type']] = doc_types.get(doc['type'], 0) + 1
        
        st.bar_chart(doc_types)
    
    with col2:
        client_docs = {}
        for doc in st.session_state.documents:
            client_docs[doc['client']] = client_docs.get(doc['client'], 0) + 1
        
        st.bar_chart(client_docs)
    
    st.divider()
    
    # Time tracking summary
    st.subheader("⏱️ Time Tracking Summary")
    
    if st.session_state.time_entries:
        total_hours = sum(entry['hours'] for entry in st.session_state.time_entries)
        total_revenue = sum(entry['amount'] for entry in st.session_state.time_entries)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Total Hours", f"{total_hours:.1f}")
        
        with col2:
            st.metric("Total Revenue", f"${total_revenue:,.2f}")
        
        with col3:
            st.metric("Average Rate", f"${total_revenue/total_hours:.2f}/hr" if total_hours > 0 else "$0/hr")
    else:
        st.info("No time entries to analyze yet.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("*LegalDoc Pro v1.0*")
st.sidebar.markdown("*Simplifying legal document management*")
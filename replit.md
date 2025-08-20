# Overview

A Streamlit-based medical appointment preparation assistant designed to help patients prepare for doctor consultations. The application guides users through a step-by-step process to organize their medical information, symptoms, medications, and questions before their appointment. It generates comprehensive PDF summaries that patients can bring to their consultations to ensure more effective and productive medical visits.

# User Preferences

Preferred communication style: Simple, everyday language.

# System Architecture

## Frontend Architecture
- **Framework**: Streamlit for the main application interface
- **UI Components**: Multi-step wizard with progress tracking using session state management
- **Styling**: HTML/CSS with Tailwind CSS framework for responsive design
- **Language**: Indonesian language interface for local medical context

## Application Structure
- **Main Application**: `app.py` serves as the entry point with Streamlit configuration and session state management
- **Utilities Module**: `utils.py` contains helper functions for PDF generation and common medical questions
- **Step-based Navigation**: Six-step wizard process managed through session state variables

## Session State Management
- Persistent user data across steps using Streamlit's session state
- Key data points tracked: patient information, appointment details, symptoms, medications, and questions
- Progress tracking with visual progress bar

## PDF Generation System
- **Library**: ReportLab for creating professional medical summary documents
- **Output Format**: A4 format PDFs with structured layout
- **Content**: Comprehensive summary including patient data, symptoms, medications, and prepared questions
- **Styling**: Professional medical document formatting with consistent typography

## Data Storage
- **Session-based**: No persistent database storage, all data maintained in browser session
- **Temporary Files**: PDF generation creates temporary BytesIO objects for download
- **File Upload**: Support for uploading medical documents or test results

## Content Management
- **Predefined Questions**: Common medical questions library in Indonesian
- **Dynamic Content**: User-customizable medication lists and symptom descriptions
- **Document Handling**: File upload capability for supporting medical documents

# External Dependencies

## Python Libraries
- **streamlit**: Web application framework for the main interface
- **reportlab**: PDF generation and document creation
- **datetime**: Date and time handling for appointments
- **base64**: File encoding for downloads

## Frontend Libraries (HTML version)
- **Tailwind CSS**: Utility-first CSS framework for styling
- **html2canvas**: Client-side screenshot and PDF generation
- **Google Fonts (Inter)**: Typography system

## No External Services
- No database connections required
- No third-party APIs or authentication systems
- Fully self-contained application suitable for local deployment
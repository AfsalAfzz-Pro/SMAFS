## SMAFS - Student Management And Feedback System

This project is a Django web application designed to support Brototype, a 27-week self-learning platform for students to acquire programming skills and job-ready qualifications.

**Problem:**

Brototype recently established a communication team with four trainers who developed a comprehensive syllabus for student communication development. However, with over 500 students, there's a lack of trainers to provide individual feedback for audio tasks, creating a bottleneck in the learning process.

**Solution:**

SMAFS aims to bridge this gap by offering a web-based solution with the following functionalities:

* **Student Features:**
    * Login and upload audio recordings for self-assessment.
    * Receive AI-generated reports analyzing their communication skills.
* **Batch Coordinator Features:**
    * Submit attendance forms for batch members during communication sessions and audio task submissions.
* **Trainer Features (Work in Progress):**
    * View dashboards displaying batch-wise data on:
        * Student attendance
        * Number of students in each batch

**Technology Stack:**

* **Backend:**
    * Django (Web Framework)
    * Python (Programming Language)
* **Cloud Services:**
    * Google Cloud Functions (For processing audio files in the cloud)
    * Google Cloud Storage (For storing student audio files)
    * Google Workspace (For data storage using Google Sheets API)
* **AI & Speech Analysis:**
    * Whisper API from OpenAI (For speech transcription)

**Project Phases:**

1. **Phase 1: Initial Idea (Completed)**
    * Define project scope and identify key functionalities.
    * Research potential technologies and libraries.

2. **Phase 2: Basic Working Prototype (In Progress)**
    * Develop core functionalities for student login, audio upload, and basic feedback generation (using pre-built sample).

3. **Phase 3: Fully Functional Web Application (Planned)**
    * Implement Batch Coordinator and Trainer features.
    * Integrate Whisper API for real-time speech transcription.
    * Develop custom AI-powered analysis pipeline using the transcribed text for report generation.
    * Prioritize security and performance optimization.

4. **Phase 4: Deployment and alpha testing (Planned)**
    * Securely deploy the application to a cloud platform.
    * Conduct alpha testing with a limited group of students and trainers.

**Note:** This is a private repository. 

**Sample Functionality:**

A sample working model for AI-powered audio analysis and report generation is already implemented for demonstration purposes. 

**Disclaimer:** This project utilizes Google Cloud services and OpenAI's Whisper API. Usage of these services may incur costs depending on their pricing models.

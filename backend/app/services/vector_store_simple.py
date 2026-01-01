from typing import List, Dict, Any, Optional
import uuid


class VectorStore:
    """Simple mock vector store for basic functionality"""
    
    def __init__(self):
        self.documents = []
        self.collection_name = "project_templates"
    
    def initialize(self):
        """Initialize mock vector store"""
        if not self.documents:
            self.seed_templates()
    
    def add_documents(
        self,
        texts: List[str],
        metadatas: Optional[List[Dict[str, Any]]] = None,
        ids: Optional[List[str]] = None
    ):
        """Add documents to mock vector store"""
        if ids is None:
            ids = [str(uuid.uuid4()) for _ in texts]
        
        if metadatas is None:
            metadatas = [{} for _ in texts]
        
        for i, text in enumerate(texts):
            self.documents.append({
                'id': ids[i],
                'text': text,
                'metadata': metadatas[i]
            })
    
    def search(
        self,
        query: str,
        top_k: int = 6
    ) -> List[Dict[str, Any]]:
        """Simple keyword-based search"""
        self.initialize()
        
        # Simple keyword matching
        query_words = query.lower().split()
        results = []
        
        for doc in self.documents:
            score = 0
            text_lower = doc['text'].lower()
            
            # Count matching words
            for word in query_words:
                if word in text_lower:
                    score += 1
            
            if score > 0:
                results.append({
                    'id': doc['id'],
                    'text': doc['text'],
                    'score': score / len(query_words),
                    'metadata': doc['metadata']
                })
        
        # Sort by score and return top_k
        results.sort(key=lambda x: x['score'], reverse=True)
        return results[:top_k]
    
    def seed_templates(self):
        """Seed comprehensive Indian engineering project templates following GTU, VTU, AICTE standards"""
        templates = [
            # ============ COMPUTER SCIENCE / IT PROJECTS ============
            {
                "text": """Computer Networks Project: Network Traffic Analyzer and Intrusion Detection System
                Subject: Computer Networks | Semester: 5-6 | University Format: GTU/VTU
                
                ABSTRACT: This project presents a comprehensive network traffic analyzer with real-time intrusion detection capabilities. The system captures network packets, analyzes traffic patterns, identifies potential security threats, and generates detailed reports. Built using Python with Scapy for packet manipulation and machine learning algorithms for anomaly detection.
                
                MODULES:
                1. Packet Capture Module (2 weeks) - Real-time packet sniffing using libpcap
                2. Protocol Analysis Module (3 weeks) - Deep packet inspection for TCP/UDP/ICMP
                3. Threat Detection Module (3 weeks) - ML-based anomaly detection using Isolation Forest
                4. Visualization Dashboard (2 weeks) - Real-time charts using Chart.js and Flask
                5. Report Generation Module (1 week) - PDF reports with traffic statistics
                
                TECHNOLOGY STACK: Python 3.8+, Scapy, Flask, SQLite, Chart.js, Scikit-learn
                
                HARDWARE REQUIREMENTS: Intel i3 or above, 8GB RAM, 100GB Storage, Network Interface Card
                SOFTWARE REQUIREMENTS: Windows 10/Ubuntu 20.04, Python 3.8+, Wireshark, VS Code
                
                SAMPLE VIVA QUESTIONS:
                - What is the difference between packet sniffing and packet capturing?
                - Explain the OSI model layers and which layers your project analyzes.
                - How does your intrusion detection system identify malicious traffic?
                - What machine learning algorithm did you use and why?
                
                Difficulty: Intermediate | Timeline: 8-10 weeks | Estimated LOC: 3000""",
                "metadata": {"subject": "Computer Networks", "difficulty": "Intermediate", "semester": 5, "university": "GTU/VTU"}
            },
            {
                "text": """Web Development Project: E-Commerce Platform with Payment Gateway Integration
                Subject: Web Development | Semester: 5-6 | University Format: GTU/VTU/AICTE
                
                ABSTRACT: A full-stack e-commerce web application featuring product catalog management, shopping cart functionality, secure user authentication, and integrated payment processing using Razorpay/Stripe. The platform supports multiple user roles (admin, vendor, customer) with a responsive design suitable for all devices.
                
                MODULES:
                1. User Authentication Module (2 weeks) - JWT-based auth with OAuth support
                2. Product Management Module (3 weeks) - CRUD operations, image upload, categories
                3. Shopping Cart & Wishlist (2 weeks) - Real-time cart updates, session persistence
                4. Payment Gateway Integration (2 weeks) - Razorpay/Stripe checkout flow
                5. Order Management (2 weeks) - Order tracking, invoice generation
                6. Admin Dashboard (2 weeks) - Analytics, inventory management
                
                TECHNOLOGY STACK: React.js, Node.js, Express.js, MongoDB, Razorpay API, JWT
                
                DATABASE DESIGN:
                - Users (id, name, email, password_hash, role, created_at)
                - Products (id, name, description, price, stock, category_id, images)
                - Orders (id, user_id, total, status, payment_id, shipping_address)
                - Cart_Items (id, user_id, product_id, quantity)
                
                SAMPLE VIVA QUESTIONS:
                - What is JWT and how does it work for authentication?
                - Explain the payment flow in your application.
                - How do you handle concurrent users updating the same cart?
                - What security measures did you implement?
                
                Difficulty: Advanced | Timeline: 10-12 weeks | Estimated LOC: 5000""",
                "metadata": {"subject": "Web Development", "difficulty": "Advanced", "semester": 6, "university": "GTU/VTU"}
            },
            {
                "text": """Database Management Project: Hospital Management System
                Subject: DBMS | Semester: 4-5 | University Format: GTU/Government Polytechnic
                
                ABSTRACT: A comprehensive hospital management system for managing patient records, doctor appointments, billing, pharmacy inventory, and medical reports. The system uses a normalized relational database with efficient query optimization and supports multi-user access with role-based permissions.
                
                MODULES:
                1. Patient Registration Module (2 weeks) - Patient demographics, medical history
                2. Appointment Scheduling (2 weeks) - Doctor availability, booking system
                3. Medical Records Management (3 weeks) - Diagnoses, prescriptions, lab reports
                4. Billing & Invoicing (2 weeks) - Treatment costs, insurance claims
                5. Pharmacy Inventory (2 weeks) - Medicine stock, expiry tracking
                6. Reports & Analytics (1 week) - Patient statistics, revenue reports
                
                TECHNOLOGY STACK: MySQL 8.0, PHP 8.0, HTML5/CSS3, Bootstrap 5, AJAX
                
                DATABASE DESIGN (3NF Normalized):
                - Patients (patient_id PK, name, dob, gender, phone, address, blood_group)
                - Doctors (doctor_id PK, name, specialization, phone, schedule)
                - Appointments (appt_id PK, patient_id FK, doctor_id FK, date, time, status)
                - Medical_Records (record_id PK, patient_id FK, doctor_id FK, diagnosis, prescription)
                - Bills (bill_id PK, patient_id FK, amount, payment_status, date)
                
                SAMPLE VIVA QUESTIONS:
                - What is database normalization? Explain 1NF, 2NF, 3NF with examples.
                - How do you handle concurrent appointment bookings?
                - What indexing strategies did you use and why?
                - Explain the ER diagram of your project.
                
                Difficulty: Beginner-Intermediate | Timeline: 8 weeks | Estimated LOC: 2500""",
                "metadata": {"subject": "DBMS", "difficulty": "Beginner", "semester": 4, "university": "GTU/Polytechnic"}
            },
            {
                "text": """Machine Learning Project: Student Performance Prediction System
                Subject: Machine Learning / AI | Semester: 6-7 | University Format: VTU/AICTE
                
                ABSTRACT: An intelligent system that predicts student academic performance based on various factors including attendance, previous marks, study hours, family background, and extracurricular activities. The project compares multiple ML algorithms (Linear Regression, Random Forest, SVM, Neural Networks) and deploys the best model as a web application.
                
                MODULES:
                1. Data Collection & Preprocessing (2 weeks) - Dataset cleaning, feature engineering
                2. Exploratory Data Analysis (1 week) - Statistical analysis, visualization
                3. Model Training & Comparison (3 weeks) - Training 5+ algorithms, cross-validation
                4. Model Optimization (2 weeks) - Hyperparameter tuning, feature selection
                5. Web Interface Development (2 weeks) - Flask-based prediction interface
                6. Deployment & Documentation (1 week) - Cloud deployment, API documentation
                
                TECHNOLOGY STACK: Python, Pandas, Scikit-learn, TensorFlow, Flask, Matplotlib, Seaborn
                
                ALGORITHMS COMPARED:
                - Linear Regression (Baseline)
                - Random Forest Classifier
                - Support Vector Machine (SVM)
                - K-Nearest Neighbors (KNN)
                - Artificial Neural Network (ANN)
                
                SAMPLE VIVA QUESTIONS:
                - What is overfitting and how did you prevent it?
                - Explain the difference between classification and regression.
                - Why did you choose Random Forest as your final model?
                - What preprocessing techniques did you apply on the dataset?
                - How do you evaluate model performance? Explain precision, recall, F1-score.
                
                Difficulty: Intermediate-Advanced | Timeline: 10 weeks | Estimated LOC: 2000""",
                "metadata": {"subject": "Machine Learning", "difficulty": "Intermediate", "semester": 6, "university": "VTU/AICTE"}
            },
            {
                "text": """Operating Systems Project: CPU Scheduling Algorithm Simulator
                Subject: Operating Systems | Semester: 4-5 | University Format: GTU/VTU
                
                ABSTRACT: A visual simulator for CPU scheduling algorithms including FCFS, SJF, Priority, Round Robin, and Multilevel Queue. The project provides an interactive interface to input process details, visualize Gantt charts, and compare algorithm performance metrics like average waiting time, turnaround time, and CPU utilization.
                
                MODULES:
                1. Process Input Module (1 week) - Process creation, arrival time, burst time
                2. FCFS & SJF Implementation (2 weeks) - First Come First Serve, Shortest Job First
                3. Priority & Round Robin (2 weeks) - Preemptive and non-preemptive variants
                4. Gantt Chart Visualization (2 weeks) - Interactive timeline visualization
                5. Performance Comparison (1 week) - Metrics calculation and comparison
                
                TECHNOLOGY STACK: C++, Qt Framework, or Python with Tkinter/PyQt
                
                ALGORITHMS IMPLEMENTED:
                - FCFS (First Come First Serve)
                - SJF (Shortest Job First) - Preemptive & Non-preemptive
                - Priority Scheduling - Preemptive & Non-preemptive
                - Round Robin with variable time quantum
                - Multilevel Queue Scheduling
                
                SAMPLE VIVA QUESTIONS:
                - What is the difference between preemptive and non-preemptive scheduling?
                - How does Round Robin prevent starvation?
                - What is convoy effect in FCFS?
                - Calculate average waiting time for given processes.
                
                Difficulty: Intermediate | Timeline: 6-8 weeks | Estimated LOC: 1500""",
                "metadata": {"subject": "Operating Systems", "difficulty": "Intermediate", "semester": 4, "university": "GTU/VTU"}
            },
            # ============ IOT / EMBEDDED SYSTEMS PROJECTS ============
            {
                "text": """IoT Project: Smart Home Automation System with Voice Control
                Subject: Internet of Things | Semester: 6-7 | University Format: GTU/VTU/AICTE
                
                ABSTRACT: An IoT-based smart home automation system that allows users to control home appliances (lights, fans, AC, security cameras) remotely via a mobile app and voice commands. The system uses ESP8266/ESP32 microcontrollers, MQTT protocol for communication, and integrates with Google Assistant/Alexa for voice control.
                
                MODULES:
                1. Hardware Setup (2 weeks) - ESP32, relay modules, sensors connection
                2. Firmware Development (3 weeks) - Embedded C for microcontroller
                3. MQTT Broker Setup (1 week) - Mosquitto broker configuration
                4. Mobile App Development (3 weeks) - React Native/Flutter app
                5. Voice Integration (2 weeks) - Google Assistant/Alexa integration
                6. Cloud Dashboard (1 week) - Firebase/AWS IoT monitoring
                
                TECHNOLOGY STACK: ESP32, Arduino IDE, MQTT, Node-RED, Firebase, React Native
                
                HARDWARE REQUIREMENTS:
                - ESP32 Development Board
                - 4-Channel Relay Module
                - DHT11 Temperature/Humidity Sensor
                - PIR Motion Sensor
                - 5V Power Supply
                
                SAMPLE VIVA QUESTIONS:
                - What is MQTT protocol and why is it preferred for IoT?
                - Explain the difference between ESP8266 and ESP32.
                - How do you ensure security in IoT communication?
                - What is the role of relay module in home automation?
                
                Difficulty: Advanced | Timeline: 10-12 weeks | Estimated LOC: 2000""",
                "metadata": {"subject": "IoT", "difficulty": "Advanced", "semester": 6, "university": "GTU/VTU"}
            },
            {
                "text": """Embedded Systems Project: Automatic Irrigation System using Arduino
                Subject: Embedded Systems | Semester: 5-6 | University Format: Government Polytechnic/GTU
                
                ABSTRACT: An automated irrigation system that monitors soil moisture levels and controls water pumps automatically. The system uses Arduino microcontroller, soil moisture sensors, and a water pump with relay control. It also includes an LCD display for real-time status and optional GSM module for SMS alerts.
                
                MODULES:
                1. Sensor Interfacing (1 week) - Soil moisture sensor calibration
                2. Relay Control Circuit (1 week) - Water pump control logic
                3. Display Interface (1 week) - 16x2 LCD status display
                4. Main Control Logic (2 weeks) - Threshold-based automation
                5. GSM Module Integration (2 weeks) - SMS alerts for low water
                
                TECHNOLOGY STACK: Arduino UNO, Soil Moisture Sensor, Relay Module, GSM SIM800L, LCD
                
                CIRCUIT DIAGRAM COMPONENTS:
                - Arduino UNO (Main controller)
                - Soil Moisture Sensor (Analog input A0)
                - 5V Relay Module (Digital pin 7)
                - 16x2 LCD Display (I2C interface)
                - 12V Water Pump
                
                SAMPLE VIVA QUESTIONS:
                - How does a soil moisture sensor work?
                - What is the role of relay in controlling AC appliances?
                - Explain analog to digital conversion in Arduino.
                - How did you set the moisture threshold values?
                
                Difficulty: Beginner | Timeline: 5-6 weeks | Estimated LOC: 500""",
                "metadata": {"subject": "Embedded Systems", "difficulty": "Beginner", "semester": 5, "university": "Polytechnic/GTU"}
            },
            # ============ MOBILE APPLICATION PROJECTS ============
            {
                "text": """Android Project: Campus Event Management Application
                Subject: Mobile Application Development | Semester: 6-7 | University Format: VTU/GTU
                
                ABSTRACT: A native Android application for managing college campus events including event creation, registration, attendance tracking, QR code-based check-in, and push notifications. The app supports multiple user roles (admin, organizer, student) and integrates with Google Calendar for event reminders.
                
                MODULES:
                1. User Authentication (2 weeks) - Firebase Auth, Google Sign-In
                2. Event Management (3 weeks) - Create, update, delete events
                3. Registration System (2 weeks) - Event registration, capacity management
                4. QR Code Module (2 weeks) - QR generation and scanning for attendance
                5. Notifications (1 week) - FCM push notifications
                6. Analytics Dashboard (1 week) - Attendance reports, event statistics
                
                TECHNOLOGY STACK: Android Studio, Kotlin/Java, Firebase, Room Database, Retrofit
                
                SAMPLE VIVA QUESTIONS:
                - What is the difference between Activity and Fragment?
                - Explain the Android activity lifecycle.
                - How does Firebase Cloud Messaging work?
                - What is Room Database and why is it preferred over SQLite?
                
                Difficulty: Intermediate | Timeline: 9-10 weeks | Estimated LOC: 3500""",
                "metadata": {"subject": "Mobile App Development", "difficulty": "Intermediate", "semester": 6, "university": "VTU/GTU"}
            },
            # ============ ARTIFICIAL INTELLIGENCE PROJECTS ============
            {
                "text": """AI Project: Chatbot for College Admission Enquiry
                Subject: Artificial Intelligence | Semester: 6-7 | University Format: AICTE/GTU
                
                ABSTRACT: An AI-powered chatbot designed to answer frequently asked questions about college admissions, courses, fees, and eligibility criteria. The chatbot uses Natural Language Processing (NLP) with intent classification and entity recognition. Built using Python with NLTK/spaCy for NLP and deployed as a web widget.
                
                MODULES:
                1. Data Collection (2 weeks) - FAQ compilation, intent definition
                2. NLP Pipeline (3 weeks) - Tokenization, stemming, intent classification
                3. Response Generation (2 weeks) - Template-based and generative responses
                4. Web Interface (2 weeks) - Chat widget, conversation history
                5. Integration & Testing (1 week) - Website embedding, testing
                
                TECHNOLOGY STACK: Python, NLTK, TensorFlow, Flask, HTML/CSS/JavaScript
                
                NLP TECHNIQUES USED:
                - Tokenization and Lemmatization
                - TF-IDF Vectorization
                - Intent Classification using Neural Network
                - Named Entity Recognition (NER)
                
                SAMPLE VIVA QUESTIONS:
                - What is the difference between stemming and lemmatization?
                - How does intent classification work in chatbots?
                - What is TF-IDF and how is it used in NLP?
                - How do you handle out-of-scope queries?
                
                Difficulty: Intermediate | Timeline: 8-10 weeks | Estimated LOC: 2000""",
                "metadata": {"subject": "Artificial Intelligence", "difficulty": "Intermediate", "semester": 6, "university": "AICTE/GTU"}
            },
            {
                "text": """Deep Learning Project: Real-time Face Mask Detection System
                Subject: Deep Learning / Computer Vision | Semester: 7-8 | University Format: VTU/AICTE
                
                ABSTRACT: A deep learning-based system for real-time detection of face masks in video streams and images. The project uses Convolutional Neural Networks (CNN) with transfer learning (MobileNetV2/ResNet) to classify faces as 'with mask', 'without mask', or 'incorrect mask'. The system can process live webcam feeds and generate alerts.
                
                MODULES:
                1. Dataset Preparation (2 weeks) - Data collection, augmentation
                2. Model Architecture Design (2 weeks) - CNN with transfer learning
                3. Model Training (3 weeks) - Training, validation, hyperparameter tuning
                4. Face Detection Integration (2 weeks) - MTCNN/Haar Cascade for face detection
                5. Real-time Processing (2 weeks) - OpenCV video stream processing
                6. Deployment (1 week) - Raspberry Pi or cloud deployment
                
                TECHNOLOGY STACK: Python, TensorFlow/Keras, OpenCV, NumPy, Raspberry Pi (optional)
                
                MODEL ARCHITECTURE:
                - Base Model: MobileNetV2 (pretrained on ImageNet)
                - Custom Classifier Head: Dense layers with dropout
                - Output: Softmax with 3 classes
                
                SAMPLE VIVA QUESTIONS:
                - What is transfer learning and why is it useful?
                - Explain the architecture of MobileNetV2.
                - What data augmentation techniques did you use?
                - How do you calculate model accuracy, precision, and recall?
                
                Difficulty: Advanced | Timeline: 10-12 weeks | Estimated LOC: 1500""",
                "metadata": {"subject": "Deep Learning", "difficulty": "Advanced", "semester": 7, "university": "VTU/AICTE"}
            },
            # ============ CYBERSECURITY PROJECTS ============
            {
                "text": """Cybersecurity Project: Password Strength Analyzer and Breach Checker
                Subject: Cyber Security | Semester: 6-7 | University Format: GTU/VTU
                
                ABSTRACT: A comprehensive password security tool that analyzes password strength using multiple criteria (length, complexity, entropy), checks against known breached password databases, and provides suggestions for stronger passwords. The tool also includes a secure password generator.
                
                MODULES:
                1. Password Analysis Engine (2 weeks) - Strength scoring algorithm
                2. Breach Database Integration (2 weeks) - Have I Been Pwned API integration
                3. Password Generator (1 week) - Cryptographically secure random generation
                4. Web Interface (2 weeks) - User-friendly analysis interface
                5. Reporting (1 week) - Detailed security reports
                
                TECHNOLOGY STACK: Python, Flask, HTML/CSS, JavaScript, HIBP API
                
                SAMPLE VIVA QUESTIONS:
                - What makes a password strong?
                - How does the Have I Been Pwned API work?
                - What is password entropy and how do you calculate it?
                - Explain hashing and why passwords should be hashed.
                
                Difficulty: Intermediate | Timeline: 6-8 weeks | Estimated LOC: 1200""",
                "metadata": {"subject": "Cyber Security", "difficulty": "Intermediate", "semester": 6, "university": "GTU/VTU"}
            },
            # ============ DATA SCIENCE PROJECTS ============
            {
                "text": """Data Science Project: COVID-19 Data Analysis and Visualization Dashboard
                Subject: Data Science / Big Data | Semester: 6-7 | University Format: AICTE/GTU
                
                ABSTRACT: An interactive dashboard for analyzing and visualizing COVID-19 pandemic data including cases, deaths, recoveries, and vaccination statistics across different countries and time periods. The project uses real-time data from public APIs and provides insights through various chart types.
                
                MODULES:
                1. Data Collection (1 week) - API integration, web scraping
                2. Data Preprocessing (2 weeks) - Cleaning, transformation, aggregation
                3. Exploratory Analysis (2 weeks) - Statistical analysis, trend identification
                4. Visualization Dashboard (3 weeks) - Interactive charts using Plotly/D3.js
                5. Predictive Analysis (2 weeks) - Time series forecasting
                
                TECHNOLOGY STACK: Python, Pandas, NumPy, Plotly/Dash, Streamlit, Prophet
                
                VISUALIZATIONS:
                - Interactive world map with case density
                - Time series line charts for trends
                - Bar charts for country comparison
                - Pie charts for demographic distribution
                
                SAMPLE VIVA QUESTIONS:
                - What data cleaning techniques did you apply?
                - How do you handle missing values in time series data?
                - Explain the time series forecasting model you used.
                - What insights did you derive from the analysis?
                
                Difficulty: Intermediate | Timeline: 8-10 weeks | Estimated LOC: 2000""",
                "metadata": {"subject": "Data Science", "difficulty": "Intermediate", "semester": 6, "university": "AICTE/GTU"}
            },
            # ============ BLOCKCHAIN PROJECTS ============
            {
                "text": """Blockchain Project: Decentralized Voting System
                Subject: Blockchain Technology | Semester: 7-8 | University Format: VTU/GTU
                
                ABSTRACT: A blockchain-based electronic voting system that ensures transparency, immutability, and security in the voting process. The system uses Ethereum smart contracts for vote recording and counting, with a web interface for voter authentication and ballot casting.
                
                MODULES:
                1. Smart Contract Development (3 weeks) - Solidity contracts for voting
                2. Blockchain Network Setup (2 weeks) - Ganache/Ethereum testnet
                3. Voter Authentication (2 weeks) - MetaMask integration
                4. Web Interface (2 weeks) - React.js frontend
                5. Vote Counting & Results (1 week) - Transparent result computation
                
                TECHNOLOGY STACK: Solidity, Ethereum, Ganache, Web3.js, React.js, MetaMask
                
                SMART CONTRACT FUNCTIONS:
                - addCandidate() - Admin adds candidates
                - registerVoter() - Voter registration
                - castVote() - Vote submission
                - getResults() - Vote count retrieval
                
                SAMPLE VIVA QUESTIONS:
                - What is blockchain and how does it ensure immutability?
                - Explain the difference between public and private blockchain.
                - What is a smart contract?
                - How does your system prevent double voting?
                
                Difficulty: Advanced | Timeline: 8-10 weeks | Estimated LOC: 1500""",
                "metadata": {"subject": "Blockchain", "difficulty": "Advanced", "semester": 7, "university": "VTU/GTU"}
            },
            # ============ CLOUD COMPUTING PROJECTS ============
            {
                "text": """Cloud Computing Project: Serverless File Processing Pipeline
                Subject: Cloud Computing | Semester: 7-8 | University Format: AICTE/VTU
                
                ABSTRACT: A serverless application for processing uploaded files (images, PDFs) using AWS Lambda functions. The system automatically triggers processing workflows when files are uploaded to S3, performs transformations (resize, compress, OCR), and stores results in DynamoDB.
                
                MODULES:
                1. S3 Bucket Configuration (1 week) - Upload bucket, triggers
                2. Lambda Functions (3 weeks) - Image processing, PDF extraction
                3. API Gateway Setup (1 week) - REST API endpoints
                4. DynamoDB Integration (1 week) - Metadata storage
                5. Frontend Interface (2 weeks) - Upload and download interface
                
                TECHNOLOGY STACK: AWS Lambda, S3, DynamoDB, API Gateway, Python, React.js
                
                SAMPLE VIVA QUESTIONS:
                - What is serverless computing?
                - How does AWS Lambda pricing work?
                - Explain the event-driven architecture in your project.
                - What are the advantages of serverless over traditional servers?
                
                Difficulty: Advanced | Timeline: 7-8 weeks | Estimated LOC: 1500""",
                "metadata": {"subject": "Cloud Computing", "difficulty": "Advanced", "semester": 7, "university": "AICTE/VTU"}
            },
            # ============ SOFTWARE ENGINEERING PROJECTS ============
            {
                "text": """Software Engineering Project: Bug Tracking and Project Management System
                Subject: Software Engineering | Semester: 5-6 | University Format: GTU/VTU
                
                ABSTRACT: A comprehensive bug tracking and project management tool similar to Jira/Trello. The system supports project creation, task assignment, bug reporting with priority levels, sprint management, and Kanban board visualization. Includes role-based access control and notification system.
                
                MODULES:
                1. User Management (2 weeks) - Authentication, roles, permissions
                2. Project Management (2 weeks) - Create projects, assign members
                3. Bug/Issue Tracking (3 weeks) - Report bugs, assign priority, track status
                4. Kanban Board (2 weeks) - Drag-drop task management
                5. Sprint Management (2 weeks) - Sprint planning, burndown charts
                6. Reporting (1 week) - Project progress reports
                
                TECHNOLOGY STACK: Django, PostgreSQL, React.js, Redux, Chart.js
                
                SDLC MODEL FOLLOWED: Agile with 2-week sprints
                
                SAMPLE VIVA QUESTIONS:
                - What is the Agile methodology?
                - Explain the difference between Kanban and Scrum.
                - How do you prioritize bugs in your system?
                - What testing methodologies did you follow?
                
                Difficulty: Intermediate | Timeline: 10-12 weeks | Estimated LOC: 4000""",
                "metadata": {"subject": "Software Engineering", "difficulty": "Intermediate", "semester": 5, "university": "GTU/VTU"}
            },
            # ============ DIPLOMA / POLYTECHNIC LEVEL PROJECTS ============
            {
                "text": """Diploma Project: Online Attendance Management System
                Subject: Web Development | Semester: 4-5 | University Format: Government Polytechnic/GTU
                
                ABSTRACT: A simple yet effective web-based attendance management system for colleges. Teachers can mark attendance, students can view their attendance records, and administrators can generate reports. The system uses PHP with MySQL database.
                
                MODULES:
                1. User Login System (1 week) - Student, Teacher, Admin roles
                2. Attendance Marking (2 weeks) - Date-wise attendance entry
                3. Student Dashboard (1 week) - View personal attendance
                4. Teacher Dashboard (1 week) - Class-wise attendance management
                5. Reports Generation (1 week) - Attendance percentage reports
                
                TECHNOLOGY STACK: PHP 7.4, MySQL 5.7, HTML5, CSS3, Bootstrap 4
                
                DATABASE TABLES:
                - users (id, name, email, password, role)
                - students (id, roll_no, name, class_id)
                - attendance (id, student_id, date, status)
                - classes (id, class_name, teacher_id)
                
                SAMPLE VIVA QUESTIONS:
                - What is the difference between GET and POST methods?
                - How do you prevent SQL injection?
                - Explain the normalization of your database.
                - What is session management in PHP?
                
                Difficulty: Beginner | Timeline: 5-6 weeks | Estimated LOC: 1500""",
                "metadata": {"subject": "Web Development", "difficulty": "Beginner", "semester": 4, "university": "Polytechnic"}
            },
            {
                "text": """Diploma Project: Library Management System with Barcode Scanner
                Subject: DBMS | Semester: 3-4 | University Format: Government Polytechnic
                
                ABSTRACT: A library management system that manages book inventory, member registration, book issue/return with fine calculation. Features barcode scanning for quick book lookup and QR code generation for library cards.
                
                MODULES:
                1. Book Management (2 weeks) - Add, update, delete books
                2. Member Registration (1 week) - Student and faculty registration
                3. Issue & Return (2 weeks) - Book lending with due dates
                4. Fine Calculation (1 week) - Automatic fine computation
                5. Barcode Integration (2 weeks) - Barcode generation and scanning
                
                TECHNOLOGY STACK: Java, MySQL, JavaFX, Zxing Barcode Library
                
                SAMPLE VIVA QUESTIONS:
                - How is the fine calculated for late returns?
                - Explain the ER diagram of your database.
                - What is a barcode and how does scanning work?
                - How do you handle multiple copies of the same book?
                
                Difficulty: Beginner | Timeline: 6-8 weeks | Estimated LOC: 2000""",
                "metadata": {"subject": "DBMS", "difficulty": "Beginner", "semester": 3, "university": "Polytechnic"}
            },
            {
                "text": """Diploma Project: Personal Finance Tracker Mobile App
                Subject: Mobile App Development | Semester: 5-6 | University Format: GTU Polytechnic
                
                ABSTRACT: A simple Android application for tracking personal income and expenses. Users can add transactions, categorize them, view monthly summaries, and set budget limits. The app uses SQLite for local data storage.
                
                MODULES:
                1. User Interface Design (1 week) - Material Design components
                2. Transaction Entry (2 weeks) - Add income/expense with categories
                3. Data Storage (1 week) - SQLite database implementation
                4. Summary & Charts (2 weeks) - Monthly/weekly expense charts
                5. Budget Alerts (1 week) - Notifications for budget limits
                
                TECHNOLOGY STACK: Android Studio, Java/Kotlin, SQLite, MPAndroidChart
                
                SAMPLE VIVA QUESTIONS:
                - What is SQLite and how is it different from MySQL?
                - Explain Android activity lifecycle.
                - How do you implement local notifications?
                - What design patterns did you use?
                
                Difficulty: Beginner | Timeline: 6-7 weeks | Estimated LOC: 1800""",
                "metadata": {"subject": "Mobile App Development", "difficulty": "Beginner", "semester": 5, "university": "GTU Polytechnic"}
            },
            # ============ MECHANICAL / CIVIL ENGINEERING PROJECTS ============
            {
                "text": """Mechanical Engineering Project: CAD-based Gear Design and Analysis Tool
                Subject: CAD/CAM | Semester: 6-7 | University Format: GTU/VTU
                
                ABSTRACT: A software tool for designing spur gears with automated calculations for gear parameters (module, pitch, face width) based on input specifications. The tool generates 2D drawings and exports to common CAD formats.
                
                MODULES:
                1. Input Parameter Interface (1 week) - Power, speed, ratio inputs
                2. Gear Calculation Engine (3 weeks) - Lewis equation, AGMA standards
                3. 2D Drawing Generation (3 weeks) - Gear profile, tooth geometry
                4. Stress Analysis Display (2 weeks) - Bending and contact stress
                5. Export Module (1 week) - DXF/STEP file export
                
                TECHNOLOGY STACK: Python, PyQt5, Matplotlib, NumPy, ezdxf
                
                SAMPLE VIVA QUESTIONS:
                - What is the Lewis equation for gear design?
                - Explain the difference between module and diametral pitch.
                - How is contact stress different from bending stress in gears?
                - What are the applications of spur gears?
                
                Difficulty: Intermediate | Timeline: 8-10 weeks | Estimated LOC: 2500""",
                "metadata": {"subject": "CAD/CAM", "difficulty": "Intermediate", "semester": 6, "university": "GTU/VTU"}
            },
            {
                "text": """Civil Engineering Project: Construction Project Management Web Application
                Subject: Construction Management | Semester: 7-8 | University Format: GTU/VTU
                
                ABSTRACT: A web-based project management tool for construction sites that tracks project progress, manages resources (labor, materials, equipment), generates Gantt charts, and provides cost estimation and tracking features.
                
                MODULES:
                1. Project Setup (2 weeks) - Project details, milestones
                2. Resource Management (2 weeks) - Labor, materials tracking
                3. Task Scheduling (3 weeks) - Gantt chart generation
                4. Cost Tracking (2 weeks) - Budget vs actual costs
                5. Progress Reporting (1 week) - Status reports, dashboards
                
                TECHNOLOGY STACK: Django, PostgreSQL, React.js, Chart.js, dhtmlxGantt
                
                SAMPLE VIVA QUESTIONS:
                - What is Critical Path Method (CPM) in project management?
                - How do you calculate project duration using PERT?
                - What is resource leveling?
                - Explain the concept of earned value management.
                
                Difficulty: Intermediate | Timeline: 8-10 weeks | Estimated LOC: 3000""",
                "metadata": {"subject": "Construction Management", "difficulty": "Intermediate", "semester": 7, "university": "GTU/VTU"}
            }
        ]
        
        texts = [t["text"] for t in templates]
        metadatas = [t["metadata"] for t in templates]
        
        self.add_documents(texts, metadatas)


# Singleton instance
vector_store = VectorStore()
# Knowledge Base Application: KnowFlow

## Overview
The Knowledge Base Application is a web application that allows users to search for questions and answers from platforms like Stack Overflow and Reddit. It provides functionalities for searching, filtering, sorting, and emailing search results.

## Technologies Used
- Python
- Flask
- Flask-Mail
- PRAW (Python Reddit API Wrapper)
- HTML/CSS/JavaScript for frontend

## Setup Instructions

### Prerequisites
- Python 3.x
- Pip (Python package installer)

### Installation
1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/KnowledgeApp.git
   cd KnowledgeApp
2. **Create and activate a virtual environment (optional)**:
   ```bash
   python -m venv venv
> **Activate on Windows** ```bash venv\Scripts\activate```
> **Activate on macOS/Linux** ```bash source venv/bin/activate ```
3. **Install required packages**:
   ```bash
   pip install -r requirements.txt
4. **Create a .env file with your email credentials**:
   ```bash
   EMAIL_USER=your_email@gmail.com
   EMAIL_PASS=your_email_password
5. **Run the application**:
   ```bash
   python app.py
7. **Access the app in your browser at**
   ```bash
   http://127.0.0.1:5000/.

### Usage
Enter a query in the search bar and click "Search" to fetch results.
View results from Stack Overflow and Reddit.
Click "Send Email" to receive results via email.

### Contributing
Contributions are welcome! Feel free to submit a pull request or open an issue.

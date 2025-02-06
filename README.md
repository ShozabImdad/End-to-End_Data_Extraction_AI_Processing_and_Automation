# End-to-End Data Extraction, AI Processing, and Automation

## Overview
This project is an automated system that:
1. Scrapes news articles from BBC World News
2. Processes and paraphrases the content using NLP
3. Posts the processed content to GitHub Gists
4. Saves both original and processed content to CSV files

## Setup Instructions

### Prerequisites
- Python 3.8 or higher
- Git
- GitHub account with a Personal Access Token

### Installation

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd <repository-directory>
   ```

2. **Set Up the Virtual Environment**
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
   ```

3. **Install Dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Download spaCy Model**
   ```bash
   python -m spacy download en_core_web_lg
   ```

5. **Set Up Environment Variables**
   - Create a `.env` file in the root directory with the following content:
     ```
     GITHUB_ACCESS_TOKEN=your_github_token
     ```

6. **Run the Script**
   ```bash
   python src/main.py
   ```

## Additional Notes
- Ensure you have a valid GitHub token with gist permissions.
- The scraper is designed for BBC News and may need adjustments for other sites.
- The paraphraser uses spaCy's word vectors, which may not always find synonyms for all words.
- Logging is set up to provide detailed information about the process, which can be useful for debugging. 
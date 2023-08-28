# Email Follow-up Server

This script is designed to work as an SMTP server that receives emails, processes the content using ChatGPT (from OpenAI), and sends a follow-up email based on the processed content.

## Prerequisites:

1. Python 3.6 or higher.
2. `openai` Python package. Install with:
   ```bash
   pip install openai
3. Gmail account for sending emails.
4. OpenAI API key.   

## Setup

1. Clone the repository:
   ```bash
   git clone [Repo URL]
   cd [Repo Directory]
2. Set up environment variables:
   - OPENAI_KEY: Your OpenAI API key.
   - GMAIL_USER: Your Gmail email address.
   - GMAIL_PASSWORD: Your Gmail password or App-specific password (recommended).

For the bash shell:
   ```bash
   export OPENAI_KEY=your_openai_key
   export GMAIL_USER=your_gmail_user
   export GMAIL_PASSWORD=your_gmail_password
   ```

## Usage

1. Run the server:
   ```bash
   python email_followup_server.py --log_level=INFO
2. Configure your email client to send emails to this server. The server will run locally on port 8025.
3. Send an email: After sending an email, you'll receive a processed follow-up email based on the content.

## Logging

You can control the logging level using the --log_level argument. Options are: DEBUG, INFO, WARNING, and ERROR. The default is INFO.

## Notes

- Ensure that you allow less secure apps on your Gmail if you're using your Gmail password. More info: [Google Less Secure Apps](https://support.google.com/accounts/answer/6010255?hl=en).
- For better security, it's recommended to use [App-specific passwords](https://support.google.com/accounts/answer/185833?hl=en) for Gmail.

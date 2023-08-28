#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# email_followup_server.py

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning)

import os
import smtpd
import asyncore
import logging
import smtplib
import threading
import argparse
from email.mime.text import MIMEText
from email import message_from_bytes, policy
import openai
logging.getLogger('openai').setLevel(logging.WARNING)
 
def parse_arguments():
    """Parse and validate script arguments."""
    parser = argparse.ArgumentParser(description='SMTP Server script with OpenAI and Gmail integration.')
    parser.add_argument('--log-level', choices=['DEBUG', 'INFO', 'WARNING', 'ERROR'], default='INFO', help='Set the logging level.')
    args = parser.parse_args()

    openai.api_key = os.environ.get('OPENAI_KEY')
    if not openai.api_key:
        raise ValueError("The OPENAI_KEY environment variable is not set!")

    global GMAIL_USER, GMAIL_PASSWORD
    GMAIL_USER = os.environ.get('GMAIL_USER')
    if not GMAIL_USER:
        raise ValueError("The GMAIL_USER environment variable is not set!")

    GMAIL_PASSWORD = os.environ.get('GMAIL_PASSWORD')
    if not GMAIL_PASSWORD:
        raise ValueError("The GMAIL_PASSWORD environment variable is not set!")

    return args

def setup_logging(log_level):
    """Setup logging configuration."""
    logging.basicConfig(level=log_level, format='%(asctime)s - %(levelname)s - %(message)s')

def send_to_chatgpt(content):
    """Send content to ChatGPT and get a response."""
    message_content = (
        "This is an automated email I forwarded on, which I now need to turn "
        "into a follow up email to send to the customer based on the meeting "
        f"summary section: {content}"
    )
    message = {
        "role": "system",
        "content": message_content
    }
    try:
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{
                "role": "system",
                "content": (
                    "This is an automated email I forwarded on, which I now need to turn "
                    f"into a follow up email to send to the customer based on the meeting summary section: {content}"
                )
            }]
        )
        logging.info('chatGTP successful')
        result = completion.choices[0].message
        logging.debug(f"ChatGPT content: {result['content']}")
        return result
    except Exception as e:
        logging.error(f'chatGTP error: {e}')
        return {"error": "Error processing request."} 

def send_email_response(subject, body):
    """Send an email response."""
    global GMAIL_USER, GMAIL_PASSWORD
    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = GMAIL_USER
    msg['To'] = GMAIL_USER
    try:
        server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
        server.login(GMAIL_USER, GMAIL_PASSWORD)
        server.sendmail(GMAIL_USER, GMAIL_USER, msg.as_string())
        server.close()
        logging.info('Email sent!')
    except Exception as e:
        logging.error(f'Failed to send email: {e}')

def process_email_async(body):
    """Process the received email with chatGTP and send results back"""
    response = send_to_chatgpt(body)
    
    # If response contains an error or is None, don't proceed
    if response is None or 'error' in response:
        logging.error("Failed to process email with ChatGPT.")
        return

    send_email_response("ChatGPT Response", response['content'])        

class CustomSMTPServer(smtpd.SMTPServer):
    """Custom SMTP Server to process incoming emails."""

    def auth(self, args):
        """ Dummy authentication handler. Always returns successful. """
        return (235, b'2.7.0 Authentication successful')  # This means authentication was successful

    def process_message(self, peer, mailfrom, rcpttos, data, **kwargs):
        """Process incoming email messages."""
        logging.info('Message received')
        msg = message_from_bytes(data, policy=policy.default)
        if msg.is_multipart():
            for part in msg.iter_parts():
                content_type = part.get_content_type()
                content_disposition = str(part.get("Content-Disposition"))
                if "attachment" not in content_disposition and (content_type == "text/plain" or content_type == "text/html"):
                    body = part.get_payload(decode=True).decode()
                    break
        else:
            body = msg.get_payload(decode=True).decode()
        logging.debug(f"\nMessage from: {mailfrom}\nMessage for: {rcpttos}\nMessage content: {body}")
        threading.Thread(target=process_email_async, args=(body,)).start()
    
def main():
    """Main function to run the SMTP server."""
    args = parse_arguments()
    setup_logging(args.log_level)
    server = CustomSMTPServer(('127.0.0.1', 8025), None)
    print("SMTP server started at localhost:8025")
    try:
        asyncore.loop()
    except KeyboardInterrupt:
        print("\nSMTP server stopped.")

if __name__ == "__main__":
    try:
        main()
    except ValueError as e:
        print(e)

import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json
import threading

# Function to load the configuration from the JSON file
def load_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
        return config
    except FileNotFoundError:
        print("Configuration file not found.")
        return None

config = load_config()

if config is None:
    exit(1)

# Function to get the HTML content of the monitored element for a specific website
def get_element(url, element_selector):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        element = soup.select_one(element_selector)
        return str(element)
    except (requests.RequestException, AttributeError) as e:
        print(f"Error: {e}")
        return None

# Function to send an email
def send_email(website, previous_html_content, html_content):
    try:
        # Create an HTML email message
        msg = MIMEMultipart()
        msg['From'] = config["sender_email"]
        msg['To'] = config["receiver_email"]
        msg['Subject'] = website["email_subject"]

        raw_body = f'''
        <html>
        <body>
            <h2>{website["email_subject"]} Detected</h2>
            <h3>Previous:</h3>
            <pre>{previous_html_content}</pre>
            <h3>Current:</h3>
            <pre>{html_content}</pre>
        </body>
        </html>
        '''
        # Attach the HTML content to the email message
        body = MIMEText(raw_body, 'html')
        msg.attach(body)

        # Send the email
        with smtplib.SMTP_SSL(config["smtp_server"], config["smtp_port"]) as server:
            server.login(config["smtp_username"], config["smtp_password"])
            server.sendmail(config["sender_email"], config["receiver_email"], msg.as_string())
            print(f'Email sent for website: {website["url"]}')
    except smtplib.SMTPException as e:
        print(f"Email error: {e}")

# Function to monitor a website
def monitor_website(website):
    current_text = get_element(website["url"], website["element_selector"])
    print('=' * 40)
    print(f'Website: {website["url"]}')
    print(current_text)
    print('=' * 40)
    if current_text is None:
        return

    try:
        with open(f'previous_content_{website["url"].replace("https://", "").replace("/", "_")}.txt', 'r') as file:
            previous_text = file.read()

        if current_text != previous_text:
            with open(f'previous_content_{website["url"].replace("https://", "").replace("/", "_")}.txt', 'w') as file:
                file.write(current_text)
            send_email(website, previous_text, current_text)
    except FileNotFoundError:
        with open(f'previous_content_{website["url"].replace("https://", "").replace("/", "_")}.txt', 'w') as file:
            file.write(current_text)
        send_email(website, 'None', current_text)

# Function to update the schedule based on the configuration
def update_schedule():
    schedule.clear()
    for website in config["websites"]:
        schedule.every(website["check_interval"]).seconds.do(monitor_website, website)

# Thread for running the monitoring schedule
def monitoring_thread():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Thread for watching for changes in the configuration file
def config_watch_thread():
    global config
    while True:
        updated_config = load_config()
        if updated_config != config:
            print("Configuration updated. Updating schedule...")
            config = updated_config
            update_schedule()
        time.sleep(1)

# Function to initiate monitoring
def start_monitoring():
    update_schedule()
    monitoring = threading.Thread(target=monitoring_thread)
    config_watch = threading.Thread(target=config_watch_thread)
    
    monitoring.start()
    config_watch.start()

# Start monitoring
start_monitoring()

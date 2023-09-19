import tkinter as tk
from tkinter import simpledialog
import requests
from bs4 import BeautifulSoup
import smtplib
import schedule
import time
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import json

# Initialize the main tkinter window
root = tk.Tk()
root.title("Website Monitor")

# Function to load or create a configuration file
def load_or_create_config():
    try:
        with open('config.json', 'r') as config_file:
            config = json.load(config_file)
    except FileNotFoundError:
        config = {
            "smtp_server": "",
            "smtp_port": "",
            "smtp_username": "",
            "smtp_password": "",
            "sender_email": "",
            "receiver_email": "",
            "websites": []
        }
    return config

config = load_or_create_config()

# Function to save the configuration to a file
def save_config():
    with open('config.json', 'w') as config_file:
        json.dump(config, config_file, indent=4)

# SMTP Configuration Frame
smtp_frame = tk.Frame(root, padx=10, pady=10)
smtp_frame.pack()

smtp_label = tk.Label(smtp_frame, text="SMTP Configuration")
smtp_label.pack()

smtp_server_label = tk.Label(smtp_frame, text="SMTP Server:")
smtp_server_label.pack()

smtp_server_entry = tk.Entry(smtp_frame, width=50)
smtp_server_entry.insert(0, config["smtp_server"])
smtp_server_entry.pack()

smtp_port_label = tk.Label(smtp_frame, text="SMTP Port:")
smtp_port_label.pack()

smtp_port_entry = tk.Entry(smtp_frame, width=50)
smtp_port_entry.insert(0, config["smtp_port"])
smtp_port_entry.pack()

smtp_username_label = tk.Label(smtp_frame, text="SMTP Username:")
smtp_username_label.pack()

smtp_username_entry = tk.Entry(smtp_frame, width=50)
smtp_username_entry.insert(0, config["smtp_username"])
smtp_username_entry.pack()

smtp_password_label = tk.Label(smtp_frame, text="SMTP Password:")
smtp_password_label.pack()

smtp_password_entry = tk.Entry(smtp_frame, show="*", width=50)
smtp_password_entry.insert(0, config["smtp_password"])
smtp_password_entry.pack()

# Email Configuration Frame
email_frame = tk.Frame(root, padx=10, pady=10)
email_frame.pack()

email_label = tk.Label(email_frame, text="Email Configuration")
email_label.pack()

sender_email_label = tk.Label(email_frame, text="Sender Email:")
sender_email_label.pack()

sender_email_entry = tk.Entry(email_frame, width=50)
sender_email_entry.insert(0, config["sender_email"])
sender_email_entry.pack()

receiver_email_label = tk.Label(email_frame, text="Receiver Email:")
receiver_email_label.pack()

receiver_email_entry = tk.Entry(email_frame, width=50)
receiver_email_entry.insert(0, config["receiver_email"])
receiver_email_entry.pack()

# Websites Configuration Frame
websites_frame = tk.Frame(root, padx=10, pady=10)
websites_frame.pack()

websites_label = tk.Label(websites_frame, text="Websites Configuration")
websites_label.pack()

# Function to add a website to the list
def add_website():
    website_url = simpledialog.askstring("Website URL", "Enter the website URL:")
    if website_url:
        element_selector = simpledialog.askstring("Element Selector", "Enter the CSS selector for the element:")
        if element_selector:
            check_interval = simpledialog.askinteger("Check Interval", "Enter the check interval (in seconds):", initialvalue=300)
            if check_interval:
                email_subject = simpledialog.askstring("Email Subject", "Enter the email subject:")
                if email_subject:
                    config["websites"].append({"url": website_url, "element_selector": element_selector, "check_interval": check_interval, "email_subject": email_subject})
                    update_website_list()

add_website_button = tk.Button(websites_frame, text="Add Website", command=add_website)
add_website_button.pack()

websites_listbox = tk.Listbox(websites_frame, selectmode=tk.SINGLE, width=70)
websites_listbox.pack()

# Function to remove a selected website from the list
def remove_website():
    selected_index = websites_listbox.curselection()
    if selected_index:
        index = selected_index[0]
        config["websites"].pop(index)
        update_website_list()

remove_website_button = tk.Button(websites_frame, text="Remove Website", command=remove_website)
remove_website_button.pack()

def update_website_list():
    websites_listbox.delete(0, tk.END)
    for website in config["websites"]:
        websites_listbox.insert(tk.END, f'{website["url"]} - {website["element_selector"]} - Check Interval: {website["check_interval"]} seconds - Subject: {website["email_subject"]}')

update_website_list()

# Function to save the configuration and start monitoring
def start_monitoring():
    config["smtp_server"] = smtp_server_entry.get()
    config["smtp_port"] = smtp_port_entry.get()
    config["smtp_username"] = smtp_username_entry.get()
    config["smtp_password"] = smtp_password_entry.get()
    config["sender_email"] = sender_email_entry.get()
    config["receiver_email"] = receiver_email_entry.get()
    save_config()

    # Start monitoring code here (similar to the previous script)

start_button = tk.Button(root, text="Start Monitoring", command=start_monitoring)
start_button.pack()

root.mainloop()

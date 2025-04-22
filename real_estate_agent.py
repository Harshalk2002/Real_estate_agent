import requests
import pandas as pd
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from langchain.agents import initialize_agent, Tool
from langchain.llms import OpenAI
import os

# ✅ Apify Task Details (Environment Variables Recommended)
APIFY_TOKEN = os.getenv("APIFY_TOKEN")
TASK_ID = os.getenv("APIFY_TASK_ID")
API_URL = f"https://api.apify.com/v2/actor-tasks/{TASK_ID}/run-sync-get-dataset-items?token={APIFY_TOKEN}"

# 🔧 Tool: Scrape Zillow
def scrape_zillow():
    response = requests.get(API_URL)
    data = response.json()
    return data

# 🔧 Tool: Score and Filter Listings
def score_and_filter(data):
    df = pd.DataFrame(data)
    df["price"] = pd.to_numeric(df["unformattedPrice"], errors='coerce')
    df["daysListed"] = pd.to_numeric(df.get("daysOnZillow", 0), errors='coerce')
    df = df.dropna(subset=["price"])
    df["score"] = 100 - (df["daysListed"] * 3)
    df = df[df["price"] < 800000]  # filter by budget
    top_df = df.sort_values("score", ascending=False).head(10)
    output_file = "best_properties.csv"
    top_df.to_csv(output_file, index=False)
    return output_file

# 🔧 Tool: Send Email (Credentials should be set via environment variables)
def send_email(file_path):
    sender = os.getenv("EMAIL_SENDER")
    receiver = os.getenv("EMAIL_RECEIVER")
    password = os.getenv("EMAIL_PASSWORD")
    subject = "Top Real Estate Leads"

    msg = MIMEMultipart()
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject

    part = MIMEBase('application', "octet-stream")
    with open(file_path, "rb") as f:
        part.set_payload(f.read())
    encoders.encode_base64(part)
    part.add_header("Content-Disposition", f"attachment; filename={file_path}")
    msg.attach(part)

    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()
    server.login(sender, password)
    server.sendmail(sender, receiver, msg.as_string())
    server.quit()
    return f"✅ Email sent to {receiver} with CSV."

# LangChain Agent Setup
llm = OpenAI(temperature=0)
tools = [
    Tool(name="Zillow Scraper", func=scrape_zillow, description="Scrapes Zillow property data"),
    Tool(name="Filter and Score Listings", func=score_and_filter, description="Filters top listings and saves CSV"),
    Tool(name="Email CSV", func=send_email, description="Sends best listings to client via email")
]

agent = initialize_agent(tools, llm, agent="zero-shot-react-description", verbose=True)

# Final Run
result = agent.run("Scrape Zillow data, find best properties under 800K, and email top listings as a CSV")
print(result)
# 🏡 LangChain Real Estate Lead Generator

This LangChain-based agentic tool:
- Scrapes Zillow property data using Apify
- Filters and ranks the best listings
- Automatically emails top 10 leads as a CSV

## 🔧 Setup Instructions

### 1. Environment Variables

Create a `.env` file or configure the following in your environment:

```bash
APIFY_TOKEN=your_apify_api_token
APIFY_TASK_ID=your_apify_task_id (e.g. username~taskname)
EMAIL_SENDER=youremail@gmail.com
EMAIL_RECEIVER=clientemail@example.com
EMAIL_PASSWORD=your_app_specific_password
```

### 2. Run the Script

```bash
python real_estate_agent.py
```

### 3. Output

- `best_properties.csv`: a file with the top listings.
- Email is sent with the file attached.

## 🧠 Built with:
- [LangChain](https://www.langchain.com/)
- [Apify](https://apify.com/)
- [Pandas](https://pandas.pydata.org/)
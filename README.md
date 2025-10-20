---
title: {{title}}
emoji: {{emoji}}
colorFrom: {{colorFrom}}
colorTo: {{colorTo}}
sdk: {{sdk}}
sdk_version: "{{sdkVersion}}"
app_file: app.py
pinned: false
---

# 📧 Smart Email Classifier: Classifying emails using Natural Language Processing (NLP)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-App%20Framework-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-Apache-yellow.svg)](https://www.apache.org/licenses/LICENSE-2.0.txt)

> **Smart Email Classifier application is your companion to classify emails of different types based on email subject or body using advanced Natural Language Processing (NLP) techniques and fine-tuned model.**

## ▶️ Run the App: https://huggingface.co/spaces/kaisarhossain/Smart-Email-Classification-App

## 🧠 Categories
- 📢 **Promotions**
- 🚫 **Spam**
- 💬 **Social Media Updates**
- 🗣️ **Forum Updates**
- 🔢 **Code Verification**
- 💼 **Work Updates**

---

## 🧩 Project Structure

```
Smart-Email-Classification-App/
│
├── app.py                                # Main Streamlit application
├── .env                                  # Secret API Keys (not in Git, need to be manually created)
├── requirements.txt                      # Required Python dependencies
├── README.md                             # Project documentation
├── pyproject.toml                        # Defines project's intended dependencies which is the single truth source
├── Dockerfile                            # Docker setup for Hugging Face deployment
└── .gitignore                            # Ignored files
```

---

## ⚙️ Installation and Setup

### 1️⃣ Create a Virtual Environment (Recommended)

```bash
python -m venv venv
source venv/bin/activate       # (Linux/Mac)
venv\Scripts\activate          # (Windows)
```

### 2️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

### 3️⃣ Add Your API Keys (if any)

Create a `.env` file in your project root:

```bash
HF_TOKEN=<Your HF Token>
MODEL_REPO=kaisarhossain/email-classifier-distilbert-finetuned-kaisar
```
---

## 4️⃣ GitHub + PyCharm Workflow (Safe)
1. Clone / open project in PyCharm
2. Set up Git: Preferences → Version Control → Git
3. Authenticate with PAT: Preferences → GitHub → Log in via Token
4. Pull remote changes first: git pull origin main --rebase
5. Make changes → commit:
6. git add .
git commit -m "Your commit message"
7. Push changes: git push origin main

---

## ▶️ Run the App Locally

```bash
streamlit run app.py
```

The app will launch automatically in your browser at:
```
http://localhost:8501
```

---

## 🐳 Deploying on Hugging Face (Docker Method)

### 1️⃣ Create a `Dockerfile`
Example:
```dockerfile
# Base image
FROM python:3.10

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose Streamlit port
EXPOSE 8501

# Run Streamlit app
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### 2️⃣ Push to Hugging Face Space

- Create a new **Hugging Face Space** → Select **Docker** as the SDK.  
- Connect your **GitHub repository** or upload the project manually.  
- Hugging Face automatically builds and runs your app.

---

## 🧾 Example Usage

**Input:**  
> "Your verification code is 348211. Please do not share it with anyone."

**Predicted Category:**  
> 🔢 **Code Verification**

---

## 💡 Future Enhancements
- Integrate real-time Gmail API ingestion  
- Add multilingual email classification  
- Enable fine-tuning with user-specific data  

---

## 🤝 Contributing
Contributions are welcome!  
Fork this repo, make your improvements, and submit a pull request.

---

## 🪪 License
This project is licensed under the **Apache 2.0 License** — feel free to use and modify it.

---

## 👨‍💻 Author
Mohammed Golam Kaisar Hossain Bhuyan
🚀 AI | ML | NLP | Deep Learning  
🔗 [LinkedIn](https://www.linkedin.com/in/kaisarhossain) | [GitHub](https://github.com/kaisarhossain)

---
=======
---
title: Smart Email Classification App
emoji: 🐢
colorFrom: indigo
colorTo: green
sdk: gradio
sdk_version: 5.49.1
app_file: app.py
pinned: false
license: apache-2.0
short_description: Smart-Email-Classification-App
---

Check out the configuration reference at https://huggingface.co/docs/hub/spaces-config-reference
>>>>>>> f3f984eb444ce50d2f26830c247442faab422fb5






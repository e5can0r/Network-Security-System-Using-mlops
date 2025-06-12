import streamlit as st
import requests
import pandas as pd
import base64

st.set_page_config(page_title="Batch URL Safety Predictor", layout="centered")

st.title("🔐 Batch URL Safety Predictor")

# 🧠 Intro for users
st.markdown("""
This app predicts whether a batch of websites (given in a CSV file) are **Safe** or **Malicious**, using a trained machine learning model.

---

#### 📌 What is Batch Prediction?
Rather than checking websites one-by-one, cybersecurity researchers or internal teams often analyze a list of domains/URLs in bulk — that's **batch prediction**.

#### 🧪 Try It Yourself
Use the **sample CSV file** below to test the app easily:

""")

# 🔽 Download button for sample CSV
with open("sample.csv", "rb") as f:
    csv_bytes = f.read()
    b64 = base64.b64encode(csv_bytes).decode()
    href = f'<a href="data:file/csv;base64,{b64}" download="sample.csv">📥 Download Sample CSV</a>'
    st.markdown(href, unsafe_allow_html=True)

st.markdown("""
---

### 🧬 Required Features in Your CSV

| Feature Name                  | Description                                     |
|-------------------------------|-------------------------------------------------|
| `Prefix_Suffix`               | Checks for dashes in domain                     |
| `having_Sub_Domain`           | Counts number of subdomains                     |
| `SSLfinal_State`              | Analyzes SSL certificate                        |
| `Domain_registeration_length` | Measures domain registration duration           |
| `Favicon`                     | Checks favicon source                           |
| `port`                        | Detects unusual ports                           |
| `HTTPS_token`                 | Flags 'HTTPS' in domain name                    |
| `Request_URL`                 | Checks resource loading domains                 |
| `URL_of_Anchor`               | Analyzes anchor tag destinations                |
| `Links_in_tags`               | Measures links in HTML tags                     |
| `SFH`                         | Checks form handler locations                   |
| `Submitting_to_email`         | Flags form submission to email                  |
| `Abnormal_URL`                | Identifies URL-domain mismatches                |
| `Redirect`                    | Counts redirections                             |
| `on_mouseover`                | Detects JavaScript events                       |
| `RightClick`                  | Identifies right-click disabling                |
| `popUpWidnow`                 | Flags popup windows                             |
| `Iframe`                      | Detects invisible iframes                       |
| `age_of_domain`               | Analyzes domain age                             |
| `DNSRecord`                   | Checks DNS records                              |
| `web_traffic`                 | Measures website traffic                        |
| `Page_Rank`                   | Checks page rank                                |
| `Google_Index`                | Identifies Google indexing                      |
| `Links_pointing_to_page`      | Counts inbound links                            |
| `Statistical_report`          | Flags reported suspicious activity              |

🧠 **Ensure your CSV has all of these exact column names.**
""")

# 📤 Upload CSV
uploaded_file = st.file_uploader("📤 Upload your CSV file", type=["csv"])

if uploaded_file:
    st.success("✅ File uploaded successfully!")

    if st.button("🚀 Predict"):
        files = {"file": uploaded_file.getvalue()}
        api_url = "https://network-security-system-using-mlops-production.up.railway.app/predict"


        try:
            response = requests.post(api_url, files=files, headers={"accept": "application/json"})


            if response.status_code == 200:
                try:
                    predictions = response.json()["predictions"]

                    # 🧠 Map to human-readable labels
                    label_map = {0: "✅ Safe", 1: "⚠️ Malicious"}
                    labels = [label_map[p] for p in predictions]

                    # 📊 Display results
                    st.subheader("🔎 Prediction Results")
                    df_result = pd.DataFrame({
                        "Website No.": list(range(1, len(predictions) + 1)),
                        "Prediction": predictions,
                        "Label": labels
                    })
                    st.dataframe(df_result, use_container_width=True)

                    st.markdown("""
                    - `Website No.`: Index of the row in your input.
                    - `Prediction`: Raw model output (0 = Safe, 1 = Malicious).
                    - `Label`: Friendly label for understanding.

                    
                    """)
                except ValueError:
                    st.error("❌ Could not parse JSON from backend.")
            else:
                st.error(f"❌ Failed with status code {response.status_code}")
        except Exception as e:
            st.error(f"❌ Error occurred: {e}")

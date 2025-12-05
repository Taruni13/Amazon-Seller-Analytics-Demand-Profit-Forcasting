Deploying to Streamlit Community Cloud

1) Prepare your GitHub repo
- Ensure the repository contains `app.py` at the repository root (Streamlit entry point).
- Commit all changes and push the branch you want to deploy (e.g., `analytics_forcasting`).

  git add .
  git commit -m "Prepare app for Streamlit Community Cloud"
  git push origin analytics_forcasting

2) Connect to Streamlit Community Cloud
- Open https://share.streamlit.io and log in with your GitHub account.
- Click "New app" → Select the repository and branch (`analytics_forcasting`).
- Set the main file to `app.py`.
- Click "Deploy".

3) Runtime considerations
- This repository requests `python-3.11.4` in `runtime.txt`. Streamlit Cloud supports multiple Python versions; if deployment fails, switch to a supported Python (e.g., `python-3.10.12`).
- `requirements.txt` lists required Python packages. Streamlit Cloud will install them at deploy time.
- If you have large data files or private credentials, consider using Streamlit Secrets or storing data externally (S3, Google Drive, etc.).

4) After deploy
- The app will be available at `https://<your-username>.streamlit.app/<repo>/<branch>` (Streamlit provides the exact URL).
- For logs and redeploys, use the Streamlit Cloud dashboard.

5) Troubleshooting
- If deployment fails due to package versions, pin compatible versions in `requirements.txt`.
- If the app requires more memory/time during startup, consider reducing dataset sizes or using lighter alternatives.


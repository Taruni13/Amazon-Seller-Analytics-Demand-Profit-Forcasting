import streamlit as st


def add_custom_css():
    """Inject the project's global CSS so all pages share the same theme."""
    st.markdown(
        """
        <style>
        :root {
            --pacific-orange: #E87500;
            --pacific-dark: #111111;
            --pacific-light-bg: #faf6f0;
        }

        /* App background */
        .stApp {
            background: var(--pacific-light-bg);
        }

        /* General headings */
        h1, h2, h3, h4 {
            color: var(--pacific-dark);
            font-family: "Segoe UI", system-ui, -apple-system, BlinkMacSystemFont, sans-serif;
        }

        /* --- FLOATING TOP NAVBAR --- */
        .top-nav {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 48px;
            background-color: var(--pacific-dark);
            display: flex;
            align-items: center;
            justify-content: space-between;
            padding: 0 24px;
            z-index: 9999;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }

        .top-nav-title {
            color: var(--pacific-orange);
            font-weight: 600;
            letter-spacing: 0.04em;
        }

        .top-nav-links a {
            color: #ffffff;
            margin-left: 18px;
            text-decoration: none;
            font-size: 15px;
        }

        .top-nav-links a:hover {
            color: var(--pacific-orange);
            text-decoration: underline;
        }

        /* Layout adjustments */
        .main-block {
            padding-top: 12px !important;
            padding-bottom: 60px; /* space for footer */
            margin-top: 0 !important;
        }

        /* Card-style sections */
        .info-card {
            background-color: #f7f7f7;
            padding: 20px;
            border-radius: 12px;
            border-left: 6px solid var(--pacific-orange);
            box-shadow: 0 0 8px rgba(0,0,0,0.1);
        }

        /* --- CUSTOM FOOTER --- */
        .custom-footer {
            position: fixed;
            left: 0;
            right: 0;
            bottom: 0;
            background-color: var(--pacific-dark);
            color: #ffffff;
            padding: 6px 18px;
            font-size: 13px;
            display: flex;
            justify-content: space-between;
            align-items: center;
            z-index: 9999;
        }

        .custom-footer a {
            color: var(--pacific-orange);
            text-decoration: none;
        }

        .custom-footer a:hover {
            text-decoration: underline;
        }

        /* Hide default Streamlit header/footer/menu */
        header, header[role="banner"], #MainMenu, .css-18e3th9, .css-1lsmgbg, .reportview-container .main header {display: none !important;}
        footer {visibility: hidden;} footer:after {content: ""; visibility: hidden;}

        /* Sidebar: match main dashboard background and uppercase page names */
        [data-testid="stSidebar"] { background: var(--pacific-light-bg) !important; }
        [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] .css-1v3fvcr { text-transform: uppercase !important; font-weight:600 !important; color:var(--pacific-dark) !important; }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # Inject a shared floating navbar so every page displays consistent navigation
    st.markdown(
        """
        <div class="top-nav">
            <div class="top-nav-title">Amazon Seller Analytics</div>
            <div class="top-nav-links">
                <a href="#overview">Overview</a>
                <a href="#course-details">Course</a>
                <a href="#team-details">Team</a>
                <a href="#datasets">Datasets</a>
                <a href="#contact">Contact</a>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

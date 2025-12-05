import streamlit as st


def add_custom_css(show_navbar=True):
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

        /* --- CUSTOM HEADER (for non-home pages) --- */
        .custom-header {
            position: fixed;
            top: 0;
            left: 0;
            right: 0;
            height: 48px;
            background-color: #111111;
            color: #ffffff;
            display: flex;
            align-items: center;
            justify-content: flex-end; /* move title to the right */
            padding: 0 24px;
            z-index: 9999;
            box-shadow: 0 2px 6px rgba(0,0,0,0.25);
        }

        .custom-header h2 {
            margin: 0;
            color: #E87500;
            font-size: 20px;
            font-weight: 600;
        }

        /* Layout adjustments */
        .main-block {
            padding-top: 60px !important;
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
            background-color: #111111;
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

          /* Hide default Streamlit top header while keeping the sidebar/menu accessible.
              Removing selectors that target #MainMenu or generic Streamlit classes prevents
              accidentally hiding the left sidebar or app menu in newer Streamlit versions. */
          header, header[role="banner"], .css-18e3th9, .reportview-container .main header {display: none !important;}
          /* Keep Streamlit's menu and sidebar selectors untouched so the navigation remains available. */
          footer {visibility: hidden;} footer:after {content: ""; visibility: hidden;}

        /* Sidebar: match main dashboard background and uppercase page names */
        [data-testid="stSidebar"] { background: var(--pacific-light-bg) !important; }
        [data-testid="stSidebar"] .stText, [data-testid="stSidebar"] .css-1v3fvcr { text-transform: uppercase !important; font-weight:600 !important; color:var(--pacific-dark) !important; }


        /* --- SIDEBAR NAV STYLING (custom look like screenshot) --- */
        /* Use min-width instead of forcing a fixed width so Streamlit can
           collapse the sidebar and still render the collapsed toggle. */
        [data-testid="stSidebar"] {
            min-width: 220px !important;
            padding-top: 6px !important;
            border-right: 0px !important;
            box-shadow: none !important;
            transition: min-width 180ms ease !important;
        }

        /* Style the inner complementary panel but do not force full viewport height
           or absolute sizing (this allows Streamlit to insert the collapsed toggle). */
        [data-testid="stSidebar"] > div[role="complementary"] {
            background: #eef3f6 !important;
            padding-left: 12px !important;
            padding-right: 12px !important;
            box-sizing: border-box !important;
        }

        /* Force the sidebar to remain visible and prevent collapsing.
           This hides the small collapse/expand widget so users cannot hide the sidebar.
           Use cautiously — if you want users to be able to collapse, remove these rules. */
        body [data-testid="stSidebar"] {
            transform: none !important;
            visibility: visible !important;
            opacity: 1 !important;
            position: relative !important;
            left: 0 !important;
            margin-left: 0 !important;
            width: 260px !important;
            min-width: 260px !important;
        }

        /* Hide any sidebar toggle controls so the sidebar cannot be collapsed */
        button[aria-label="Toggle sidebar"],
        button[aria-label*="Expand"],
        button[title*="Toggle"],
        [data-testid="collapsedSidebarToggle"],
        [data-testid="stSidebarToggleButton"] {
            display: none !important;
            visibility: hidden !important;
            pointer-events: none !important;
        }

        /* Page list / nav items — normalize links to look like vertical nav */
        [data-testid="stSidebar"] ul[role="list"] {
            list-style: none !important;
            padding-left: 6px !important;
            margin-top: 8px !important;
        }

        [data-testid="stSidebar"] ul[role="list"] li a,
        [data-testid="stSidebar"] a[data-testid^="stSidebarNav"] {
            display: block !important;
            padding: 10px 14px !important;
            margin: 6px 6px !important;
            border-radius: 8px !important;
            color: #2b2b2b !important;
            text-transform: none !important;
            font-weight: 600 !important;
            text-decoration: none !important;
        }

        /* Selected / active nav item — pill background */
        [data-testid="stSidebar"] a[data-testid$="-nav-item"]:not([href]) ,
        [data-testid="stSidebar"] a.st-a:focus, [data-testid="stSidebar"] a.st-a[aria-current="true"] {
            background: #e8f0f2 !important;
            border-left: 8px solid var(--pacific-orange) !important;
            color: var(--pacific-dark) !important;
            padding-left: 12px !important;
        }

        /* Ensure the collapsed/expand toggle is visible and above other elements.
           Streamlit uses different selectors across versions; target common attributes
           for the toggle control and add a z-index so it remains clickable. */
        button[aria-expanded], button[aria-label*="Expand"], button[title*="Expand"] {
            z-index: 100000 !important;
            display: block !important;
            position: relative !important;
        }

        /* Fallback: some Streamlit versions render a collapsed control with data-testid */
        [data-testid="collapsedSidebarToggle"], [data-testid="stSidebarToggleButton"] {
            z-index: 100000 !important;
            display: block !important;
            position: relative !important;
        }

        /* Divider line below the page list */
        [data-testid="stSidebar"] .css-1outpf7 { border-top: 1px solid rgba(0,0,0,0.06) !important; margin-top: 18px !important; }

        </style>
        """,
        unsafe_allow_html=True,
    )

    # Conditionally inject navbar only if show_navbar is True (for home page)
    if show_navbar:
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


def add_custom_header(page_title):
    """Add a custom black header with the page title."""
    st.markdown(
        f"""
        <div class="custom-header">
            <h2>{page_title}</h2>
        </div>
        """,
        unsafe_allow_html=True,
    )


def add_custom_footer():
    """Add a custom black footer with copyright and contact information."""
    st.markdown(
        """
        <div class="custom-footer">
            <span>© 2025 University of the Pacific – MSBA Program</span>
            <span>
                Contact: 
                <a href="mailto:t_atodariya@u.pacific.edu">t_atodariya@u.pacific.edu</a> |
                <a href="mailto:a_gohel@u.pacific.edu">a_gohel@u.pacific.edu</a>
            </span>
        </div>
        """,
        unsafe_allow_html=True,
    )

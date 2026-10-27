import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ============================================================
# PAGE SETTINGS
# ============================================================

st.set_page_config(
    page_title="Khwezi Mining Monitoring System",
    page_icon="⛏️",
    layout="wide"
)

# ============================================================
# USER ACCOUNTS
# ============================================================

users = {
    "admin": {
        "password": "admin123",
        "role": "Administrator"
    },
    "safety": {
        "password": "safety123",
        "role": "Safety Officer"
    },
    "mining": {
        "password": "mining123",
        "role": "Mining Engineer"
    },
    "maintenance": {
        "password": "maintenance123",
        "role": "Maintenance Engineer"
    },
    "manager": {
        "password": "manager123",
        "role": "Manager"
    }
}

# ============================================================
# ROLE-BASED PERMISSIONS
# ============================================================

permissions = {
    "Administrator": [
        "Dashboard",
        "Worker Safety",
        "Safety Incidents",
        "Equipment",
        "Maintenance",
        "Risk Assessment",
        "Alerts & Recommendations",
        "Data Analysis",
        "Reports",
        "Manage Users"
    ],

    "Safety Officer": [
        "Dashboard",
        "Worker Safety",
        "Safety Incidents",
        "Risk Assessment",
        "Alerts & Recommendations",
        "Data Analysis",
        "Reports"
    ],

    "Mining Engineer": [
        "Dashboard",
        "Worker Safety",
        "Safety Incidents",
        "Equipment",
        "Risk Assessment",
        "Alerts & Recommendations",
        "Data Analysis",
        "Reports"
    ],

    "Maintenance Engineer": [
        "Dashboard",
        "Equipment",
        "Maintenance",
        "Alerts & Recommendations",
        "Data Analysis",
        "Reports"
    ],

    "Manager": [
        "Dashboard",
        "Worker Safety",
        "Safety Incidents",
        "Equipment",
        "Maintenance",
        "Risk Assessment",
        "Alerts & Recommendations",
        "Data Analysis",
        "Reports"
    ]
}

# ============================================================
# LOAD DATASETS
# ============================================================

try:
    workers = pd.read_excel("Workers.xlsx")
    incidents = pd.read_excel("Incidents.xlsx")
    equipment = pd.read_excel("Equipment.xlsx")

except FileNotFoundError:
    st.error(
        "One or more Excel files could not be found. "
        "Make sure Workers.xlsx, Incidents.xlsx and Equipment.xlsx "
        "are in the same folder as app.py."
    )
    st.stop()

# ============================================================
# FUNCTIONS
# ============================================================

# -----------------------------
# LOGIN
# -----------------------------

def login(username, password):

    if username in users:

        if users[username]["password"] == password:
            return users[username]["role"]

        else:
            return "Incorrect password"

    else:
        return "Username not found"


# -----------------------------
# ACCESS CONTROL
# -----------------------------

def access_control(username, password):

    role = login(username, password)

    if role == "Incorrect password" or role == "Username not found":
        return role

    return role, permissions[role]


# -----------------------------
# PERMISSION CHECK
# -----------------------------

def has_permission(role, function):

    if function in permissions[role]:
        return True

    else:
        return False


# -----------------------------
# PPE COMPLIANCE
# -----------------------------

def calculate_ppe_compliance(data):

    compliant = (data["PPE_Compliance"] == "Yes").sum()

    total_workers = len(data)

    percentage = (compliant / total_workers) * 100

    return percentage


# -----------------------------
# WORKER SAFETY
# -----------------------------

def check_worker_safety(worker):

    warnings = []

    if worker["PPE_Compliance"] == "No":
        warnings.append("PPE non-compliance")

    if worker["Training_Status"] == "Incomplete":
        warnings.append("Training incomplete")

    if worker["Fatigue_Level"] == "High":
        warnings.append("High fatigue level")

    if worker["Risk_Level"] in ["High", "Critical"]:
        warnings.append("High or critical risk")

    return warnings


# -----------------------------
# INCIDENT FUNCTIONS
# -----------------------------

def count_incidents(data):

    return len(data)


def highest_incident_department(data):

    counts = data["Department"].value_counts()

    department = counts.idxmax()

    number = counts.max()

    return department, number


def highest_incident_shift(data):

    counts = data["Shift"].value_counts()

    highest = counts.max()

    shifts = counts[counts == highest].index.tolist()

    return shifts, highest


def count_near_misses(data):

    return (data["Incident_Type"] == "Near Miss").sum()


def most_frequent_incident(data):

    counts = data["Incident_Type"].value_counts()

    highest = counts.max()

    incident_types = counts[counts == highest].index.tolist()

    return incident_types, highest


def count_high_critical_incidents(data):

    return data["Severity"].isin(
        ["High", "Critical"]
    ).sum()


# -----------------------------
# EQUIPMENT CONDITION
# -----------------------------

def check_temperature(temperature):

    if temperature < 80:
        return "NORMAL"

    elif temperature <= 100:
        return "WARNING"

    else:
        return "CRITICAL"


def check_vibration(vibration):

    if vibration < 5:
        return "NORMAL"

    elif vibration <= 8:
        return "WARNING"

    else:
        return "CRITICAL"


# -----------------------------
# MAINTENANCE
# -----------------------------

def check_maintenance(equipment_item):

    status = equipment_item["Maintenance_Status"]

    if status == "Overdue":
        return "OVERDUE"

    elif status == "Due":
        return "DUE"

    else:
        return "UP TO DATE"


# -----------------------------
# MONITOR EQUIPMENT
# -----------------------------

def monitor_all_equipment(data):

    results = []

    for index, equipment_item in data.iterrows():

        temperature = equipment_item["Temperature"]

        temperature_status = check_temperature(
            temperature
        )

        vibration = equipment_item["Vibration"]

        vibration_status = check_vibration(
            vibration
        )

        maintenance_status = check_maintenance(
            equipment_item
        )

        downtime = equipment_item["Downtime"]

        availability = equipment_item["Availability"]

        warnings = []

        if temperature_status == "WARNING":

            warnings.append("High temperature")

        elif temperature_status == "CRITICAL":

            warnings.append("Critical temperature")

        if vibration_status == "WARNING":

            warnings.append("High vibration")

        elif vibration_status == "CRITICAL":

            warnings.append("Critical vibration")

        if maintenance_status == "DUE":

            warnings.append("Maintenance due")

        elif maintenance_status == "OVERDUE":

            warnings.append("Maintenance overdue")

        if downtime > 30:

            warnings.append("Excessive downtime")

        if availability < 99.5:

            warnings.append("Low availability")

        if (
            temperature_status == "CRITICAL"
            or vibration_status == "CRITICAL"
        ):

            overall_status = "CRITICAL"

        elif warnings:

            overall_status = "WARNING"

        else:

            overall_status = "NORMAL"

        results.append([
            equipment_item["Equipment_ID"],
            temperature,
            temperature_status,
            vibration,
            vibration_status,
            maintenance_status,
            downtime,
            availability,
            ", ".join(warnings),
            overall_status
        ])

    return results


# -----------------------------
# EQUIPMENT ALERTS
# -----------------------------

def generate_equipment_alerts(data):

    alerts = []

    for index, equipment_item in data.iterrows():

        temperature_status = check_temperature(
            equipment_item["Temperature"]
        )

        vibration_status = check_vibration(
            equipment_item["Vibration"]
        )

        maintenance_status = check_maintenance(
            equipment_item
        )

        downtime = equipment_item["Downtime"]

        availability = equipment_item["Availability"]

        if temperature_status == "CRITICAL":

            alerts.append([
                equipment_item["Equipment_ID"],
                "CRITICAL",
                "High temperature"
            ])

        elif temperature_status == "WARNING":

            alerts.append([
                equipment_item["Equipment_ID"],
                "WARNING",
                "High temperature"
            ])

        if vibration_status == "CRITICAL":

            alerts.append([
                equipment_item["Equipment_ID"],
                "CRITICAL",
                "High vibration"
            ])

        elif vibration_status == "WARNING":

            alerts.append([
                equipment_item["Equipment_ID"],
                "WARNING",
                "High vibration"
            ])

        if maintenance_status == "OVERDUE":

            alerts.append([
                equipment_item["Equipment_ID"],
                "CRITICAL",
                "Maintenance overdue"
            ])

        elif maintenance_status == "DUE":

            alerts.append([
                equipment_item["Equipment_ID"],
                "WARNING",
                "Maintenance due"
            ])

        if downtime > 30:

            alerts.append([
                equipment_item["Equipment_ID"],
                "CRITICAL",
                "Excessive downtime"
            ])

        if availability < 99.5:

            alerts.append([
                equipment_item["Equipment_ID"],
                "WARNING",
                "Low availability"
            ])

    return alerts


# -----------------------------
# EQUIPMENT AVAILABILITY
# -----------------------------

def equipment_available(data):

    return (
        data["Maintenance_Status"] == "Up to Date"
    ).sum()


def equipment_under_maintenance(data):

    return (
        data["Maintenance_Status"]
        == "Under Maintenance"
    ).sum()


# -----------------------------
# RISK ASSESSMENT
# -----------------------------

def classify_risk(likelihood, consequence):

    risk_score = likelihood * consequence

    if risk_score <= 4:

        risk_level = "Low"

    elif risk_score <= 9:

        risk_level = "Medium"

    elif risk_score <= 16:

        risk_level = "High"

    else:

        risk_level = "Critical"

    return risk_score, risk_level


def calculate_likelihood(worker):

    score = 1

    if worker["PPE_Compliance"] == "No":

        score += 1

    if worker["Training_Status"] == "Incomplete":

        score += 1

    if worker["Fatigue_Level"] == "Medium":

        score += 1

    elif worker["Fatigue_Level"] == "High":

        score += 2

    if worker["Near_Misses"] >= 2:

        score += 1

    if score > 5:

        score = 5

    return score


def calculate_consequence(worker):

    score = 1

    if worker["Previous_Incidents"] >= 1:

        score += 1

    if worker["Safety_Observations"] >= 4:

        score += 1

    if worker["Safety_Observations"] >= 6:

        score += 1

    if worker["Risk_Level"] == "High":

        score += 1

    elif worker["Risk_Level"] == "Critical":

        score += 2

    if score > 5:

        score = 5

    return score


# -----------------------------
# DATA ANALYSIS FUNCTIONS
# -----------------------------

def highest_risk_department(data):

    risk_counts = data[
        data["Risk_Level"].isin(
            ["High", "Critical"]
        )
    ]["Department"].value_counts()

    if risk_counts.empty:

        return "No high-risk departments"

    highest = risk_counts.max()

    departments = risk_counts[
        risk_counts == highest
    ].index.tolist()

    return departments, highest


def highest_downtime_equipment(data):

    highest = data["Downtime"].max()

    equipment_id = data.loc[
        data["Downtime"] == highest,
        "Equipment_ID"
    ].tolist()

    return equipment_id, highest


def lowest_availability_equipment(data):

    lowest = data["Availability"].min()

    equipment_id = data.loc[
        data["Availability"] == lowest,
        "Equipment_ID"
    ].tolist()

    return equipment_id, lowest


def highest_vibration_equipment(data):

    highest = data["Vibration"].max()

    equipment_id = data.loc[
        data["Vibration"] == highest,
        "Equipment_ID"
    ].tolist()

    return equipment_id, highest


def highest_temperature_equipment(data):

    highest = data["Temperature"].max()

    equipment_id = data.loc[
        data["Temperature"] == highest,
        "Equipment_ID"
    ].tolist()

    return equipment_id, highest


def equipment_requiring_maintenance(data):

    result = data[
        data["Maintenance_Status"].isin(
            ["Due", "Overdue"]
        )
    ]

    return result["Equipment_ID"].tolist()


def overdue_equipment(data):

    result = data[
        data["Maintenance_Status"] == "Overdue"
    ]

    return result["Equipment_ID"].tolist()


def equipment_needing_inspection(data):

    equipment_list = []

    for index, equipment_item in data.iterrows():

        temperature_status = check_temperature(
            equipment_item["Temperature"]
        )

        vibration_status = check_vibration(
            equipment_item["Vibration"]
        )

        maintenance_status = check_maintenance(
            equipment_item
        )

        if (
            temperature_status == "CRITICAL"
            or vibration_status == "CRITICAL"
            or maintenance_status == "OVERDUE"
            or equipment_item["Downtime"] > 30
        ):

            equipment_list.append(
                equipment_item["Equipment_ID"]
            )

    return equipment_list


# -----------------------------
# MANAGEMENT ATTENTION
# -----------------------------

def management_attention(
    workers,
    incidents,
    equipment
):

    attention = []

    high_risk = workers[
        workers["Risk_Level"].isin(
            ["High", "Critical"]
        )
    ].shape[0]

    if high_risk > 0:

        attention.append(
            "High-risk workers identified"
        )

    serious_incidents = incidents[
        incidents["Severity"].isin(
            ["High", "Critical"]
        )
    ].shape[0]

    if serious_incidents > 0:

        attention.append(
            "High or critical safety incidents identified"
        )

    ppe = calculate_ppe_compliance(workers)

    if ppe < 90:

        attention.append(
            "PPE compliance below 90%"
        )

    inspection = equipment_needing_inspection(
        equipment
    )

    if len(inspection) > 0:

        attention.append(
            "Equipment requiring immediate inspection: "
            + str(inspection)
        )

    return attention


# -----------------------------
# EQUIPMENT RECOMMENDATIONS
# -----------------------------

def equipment_recommendation(equipment_item):

    recommendations = []

    temperature_status = check_temperature(
        equipment_item["Temperature"]
    )

    vibration_status = check_vibration(
        equipment_item["Vibration"]
    )

    maintenance_status = check_maintenance(
        equipment_item
    )

    if temperature_status == "CRITICAL":

        recommendations.append(
            "Inspect equipment and check cooling system"
        )

    if vibration_status == "CRITICAL":

        recommendations.append(
            "Inspect equipment and initiate maintenance"
        )

    if maintenance_status == "OVERDUE":

        recommendations.append(
            "Schedule maintenance immediately"
        )

    if equipment_item["Downtime"] > 30:

        recommendations.append(
            "Investigate excessive downtime"
        )

    if equipment_item["Availability"] < 99.5:

        recommendations.append(
            "Investigate low equipment availability"
        )

    return recommendations


# ============================================================
# SESSION STATE
# ============================================================

if "logged_in" not in st.session_state:

    st.session_state.logged_in = False


if "role" not in st.session_state:

    st.session_state.role = None


# ============================================================
# LOGIN PAGE
# ============================================================

if not st.session_state.logged_in:

    # Custom styling for the welcome screen only.
    st.markdown(
        """
        <style>
        .stApp {
            background:
                radial-gradient(circle at 12% 8%, rgba(145, 190, 105, 0.13), transparent 28%),
                linear-gradient(135deg, #f5f7f3 0%, #edf2ec 100%);
        }

        .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }

        .khwezi-hero {
            background: linear-gradient(125deg, #10251f 0%, #1c4032 58%, #315d43 100%);
            border: 1px solid rgba(255,255,255,0.08);
            border-radius: 24px;
            padding: 2.2rem 2.3rem;
            color: #ffffff;
            box-shadow: 0 18px 45px rgba(18, 43, 32, 0.16);
            margin-bottom: 1.2rem;
        }

        .khwezi-eyebrow {
            color: #b7dc8b;
            font-size: 0.76rem;
            font-weight: 700;
            letter-spacing: 0.17em;
            text-transform: uppercase;
            margin-bottom: 0.7rem;
        }

        .khwezi-title {
            font-size: clamp(2.1rem, 5vw, 3.6rem);
            line-height: 1.03;
            font-weight: 850;
            letter-spacing: -0.04em;
            margin: 0;
        }

        .khwezi-title span {
            color: #b7dc8b;
        }

        .khwezi-subtitle {
            color: #e0e9e1;
            font-size: 1.03rem;
            line-height: 1.65;
            max-width: 650px;
            margin-top: 1rem;
            margin-bottom: 0;
        }

        .khwezi-tag {
            display: inline-block;
            border: 1px solid rgba(183, 220, 139, 0.45);
            color: #d9edc4;
            border-radius: 999px;
            padding: 0.38rem 0.75rem;
            margin-top: 1.2rem;
            font-size: 0.76rem;
            letter-spacing: 0.04em;
        }

        .khwezi-section-label {
            color: #42624b;
            font-size: 0.75rem;
            font-weight: 800;
            letter-spacing: 0.13em;
            text-transform: uppercase;
            margin: 1.35rem 0 0.7rem 0;
        }

        .khwezi-feature {
            min-height: 128px;
            background: rgba(255,255,255,0.82);
            border: 1px solid #dfe7dc;
            border-radius: 16px;
            padding: 1rem 1rem 0.9rem 1rem;
            box-shadow: 0 5px 18px rgba(29, 55, 38, 0.045);
        }

        .khwezi-feature-icon {
            font-size: 1.55rem;
            margin-bottom: 0.45rem;
        }

        .khwezi-feature-title {
            color: #1d382a;
            font-size: 0.96rem;
            font-weight: 750;
            margin-bottom: 0.35rem;
        }

        .khwezi-feature-copy {
            color: #627066;
            font-size: 0.82rem;
            line-height: 1.45;
        }

        .khwezi-footer {
            text-align: center;
            color: #718075;
            font-size: 0.75rem;
            padding-top: 1.2rem;
        }

        div[data-testid="stForm"] {
            background: #ffffff;
            border: 1px solid #dfe7dc;
            border-radius: 20px;
            padding: 1.5rem 1.5rem 1.2rem 1.5rem;
            box-shadow: 0 12px 32px rgba(29, 55, 38, 0.07);
        }

        div.stButton > button[kind="primary"],
        div.stButton > button {
            border-radius: 10px;
            min-height: 2.8rem;
            font-weight: 700;
            border: 1px solid #2d5a3d;
        }

        div.stButton > button[kind="primary"] {
            background: #28563a;
            color: white;
        }

        div.stButton > button:hover {
            border-color: #a5cf75;
            color: #1b3828;
        }

        @media (max-width: 700px) {
            .khwezi-hero {
                padding: 1.5rem;
            }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <div class="khwezi-hero">
            <div class="khwezi-eyebrow">Mining intelligence · Safety · Reliability</div>
            <h1 class="khwezi-title">KHWEZI<br><span>MINING MONITORING</span></h1>
            <p class="khwezi-subtitle">
                One workspace for monitoring worker safety, incidents, equipment
                condition and operational risk — helping teams make informed decisions.
            </p>
            <div class="khwezi-tag">⛏ &nbsp; MINE SAFETY AND EQUIPMENT INSIGHT</div>
        </div>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        '<div class="khwezi-section-label">One system. Four key areas.</div>',
        unsafe_allow_html=True
    )

    feature_columns = st.columns(4)
    feature_cards = [
        ("👷", "Worker safety", "Review PPE, training, fatigue and worker risk indicators."),
        ("🚨", "Incident tracking", "Explore incident records, severity and near misses."),
        ("⚙️", "Equipment health", "Monitor temperature, vibration and equipment availability."),
        ("🛡️", "Risk and alerts", "Identify warning signs and maintenance priorities."),
    ]

    for column, (icon, title, description) in zip(feature_columns, feature_cards):
        with column:
            st.markdown(
                f"""
                <div class="khwezi-feature">
                    <div class="khwezi-feature-icon">{icon}</div>
                    <div class="khwezi-feature-title">{title}</div>
                    <div class="khwezi-feature-copy">{description}</div>
                </div>
                """,
                unsafe_allow_html=True
            )

    st.markdown(
        '<div class="khwezi-section-label">Secure workspace</div>',
        unsafe_allow_html=True
    )

    left_space, login_column, right_space = st.columns([1, 1.25, 1])

    with login_column:
        st.markdown("### Welcome back")
        st.caption("Sign in with your assigned account to continue.")

        with st.form("khwezi_login_form", clear_on_submit=False):
            username = st.text_input("Username", placeholder="Enter your username")
            password = st.text_input(
                "Password",
                type="password",
                placeholder="Enter your password"
            )
            submitted = st.form_submit_button(
                "Sign in to Khwezi",
                use_container_width=True,
                type="primary"
            )

        if submitted:
            if username in users:
                if users[username]["password"] == password:
                    st.session_state.logged_in = True
                    st.session_state.role = users[username]["role"]
                    st.rerun()
                else:
                    st.error("Incorrect password.")
            else:
                st.error("Username not found.")

    st.markdown(
        '<div class="khwezi-footer">KHWEZI MINING MONITORING SYSTEM &nbsp; · &nbsp; Authorised users only</div>',
        unsafe_allow_html=True
    )

# ============================================================
# MAIN APPLICATION
# ============================================================

else:

    role = st.session_state.role

    # -----------------------------
    # SIDEBAR
    # -----------------------------

    st.sidebar.title(
        "⛏️ Khwezi Mining"
    )

    st.sidebar.success(
        "Logged in as:\n" + role
    )

    selected_function = st.sidebar.radio(
        "Select a function",
        permissions[role]
    )

    if st.sidebar.button("Logout"):

        st.session_state.logged_in = False

        st.session_state.role = None

        st.rerun()

    # ========================================================
    # DASHBOARD
    # ========================================================

    if selected_function == "Dashboard":

        st.title(
            "⛏️ Mining Health, Safety and Equipment Dashboard"
        )

        st.write(
            "Overview of worker safety, incidents and equipment condition."
        )

        total_workers = len(workers)

        total_incidents = len(incidents)

        near_misses = count_near_misses(
            incidents
        )

        high_risk_workers = workers[
            workers["Risk_Level"].isin(
                ["High", "Critical"]
            )
        ].shape[0]

        ppe = calculate_ppe_compliance(
            workers
        )

        total_equipment = len(equipment)

        available_equipment = equipment_available(
            equipment
        )

        under_maintenance = equipment_under_maintenance(
            equipment
        )

        alerts = generate_equipment_alerts(
            equipment
        )

        critical_alerts = sum(
            1 for alert in alerts
            if alert[1] == "CRITICAL"
        )

        average_availability = equipment[
            "Availability"
        ].mean()

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Total Workers",
            total_workers
        )

        col2.metric(
            "Total Incidents",
            total_incidents
        )

        col3.metric(
            "Near Misses",
            near_misses
        )

        col4.metric(
            "High-Risk Workers",
            high_risk_workers
        )

        col5, col6, col7, col8 = st.columns(4)

        col5.metric(
            "PPE Compliance",
            f"{ppe:.1f}%"
        )

        col6.metric(
            "Total Equipment",
            total_equipment
        )

        col7.metric(
            "Equipment Available",
            available_equipment
        )

        col8.metric(
            "Under Maintenance",
            under_maintenance
        )

        col9, col10, col11 = st.columns(3)

        col9.metric(
            "Total Alerts",
            len(alerts)
        )

        col10.metric(
            "Average Availability",
            f"{average_availability:.2f}%"
        )

        col11.metric(
            "Critical Alerts",
            critical_alerts
        )

        st.divider()

        st.subheader(
            "Management Attention"
        )

        attention = management_attention(
            workers,
            incidents,
            equipment
        )

        if attention:

            for item in attention:

                st.warning(item)

        else:

            st.success(
                "No immediate management attention required."
            )

    # ========================================================
    # WORKER SAFETY
    # ========================================================

    elif selected_function == "Worker Safety":

        st.title(
            "👷 Worker Health and Safety Monitoring"
        )

        st.metric(
            "PPE Compliance",
            f"{calculate_ppe_compliance(workers):.1f}%"
        )

        st.subheader(
            "Worker Safety Database"
        )

        search_worker = st.text_input(
            "Search Worker ID"
        )

        filtered_workers = workers.copy()

        if search_worker:

            filtered_workers = filtered_workers[
                filtered_workers["Worker_ID"]
                .astype(str)
                .str.contains(
                    search_worker,
                    case=False
                )
            ]

        st.dataframe(
            filtered_workers,
            use_container_width=True
        )

        st.subheader(
            "Unsafe Conditions and Warnings"
        )

        warning_found = False

        for index, worker in workers.iterrows():

            warnings = check_worker_safety(
                worker
            )

            if warnings:

                warning_found = True

                st.warning(
                    f"{worker['Worker_ID']}: "
                    + ", ".join(warnings)
                )

        if not warning_found:

            st.success(
                "No worker safety warnings found."
            )

    # ========================================================
    # SAFETY INCIDENTS
    # ========================================================

    elif selected_function == "Safety Incidents":

        st.title(
            "🚨 Safety Incident Database"
        )

        col1, col2, col3 = st.columns(3)

        col1.metric(
            "Total Incidents",
            count_incidents(incidents)
        )

        col2.metric(
            "Near Misses",
            count_near_misses(incidents)
        )

        col3.metric(
            "High/Critical Incidents",
            count_high_critical_incidents(incidents)
        )

        st.subheader(
            "Search and Filter Incidents"
        )

        search_incident = st.text_input(
            "Search Incident ID"
        )

        filtered_incidents = incidents.copy()

        if search_incident:

            filtered_incidents = filtered_incidents[
                filtered_incidents["Incident_ID"]
                .astype(str)
                .str.contains(
                    search_incident,
                    case=False
                )
            ]

        col1, col2 = st.columns(2)

        with col1:

            shift_filter = st.selectbox(
                "Shift",
                ["All", "Day", "Night"]
            )

        with col2:

            severity_filter = st.selectbox(
                "Severity",
                [
                    "All",
                    "Low",
                    "Medium",
                    "High",
                    "Critical"
                ]
            )

        if shift_filter != "All":

            filtered_incidents = filtered_incidents[
                filtered_incidents["Shift"]
                == shift_filter
            ]

        if severity_filter != "All":

            filtered_incidents = filtered_incidents[
                filtered_incidents["Severity"]
                == severity_filter
            ]

        st.dataframe(
            filtered_incidents,
            use_container_width=True
        )

        st.subheader(
            "Incident Analysis"
        )

        department, number = highest_incident_department(
            incidents
        )

        shifts, shift_number = highest_incident_shift(
            incidents
        )

        types, type_number = most_frequent_incident(
            incidents
        )

        st.write(
            f"**Department with most incidents:** "
            f"{department} ({number})"
        )

        st.write(
            f"**Highest incident shift:** "
            f"{', '.join(shifts)} ({shift_number})"
        )

        st.write(
            f"**Most frequent incident types:** "
            f"{', '.join(types)} ({type_number} each)"
        )

        incident_counts = incidents[
            "Incident_Type"
        ].value_counts()

        fig, ax = plt.subplots()

        incident_counts.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Incidents by Type"
        )

        ax.set_xlabel(
            "Incident Type"
        )

        ax.set_ylabel(
            "Number of Incidents"
        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        st.pyplot(fig)

    # ========================================================
    # EQUIPMENT
    # ========================================================

    elif selected_function == "Equipment":

        st.title(
            "🚜 Equipment Database and Condition Monitoring"
        )

        search_equipment = st.text_input(
            "Search Equipment ID"
        )

        filtered_equipment = equipment.copy()

        if search_equipment:

            filtered_equipment = filtered_equipment[
                filtered_equipment["Equipment_ID"]
                .astype(str)
                .str.contains(
                    search_equipment,
                    case=False
                )
            ]

        st.dataframe(
            filtered_equipment,
            use_container_width=True
        )

        st.subheader(
            "Equipment Condition Monitoring"
        )

        results = monitor_all_equipment(
            equipment
        )

        monitoring_table = pd.DataFrame(
            results,
            columns=[
                "Equipment ID",
                "Temperature",
                "Temperature Status",
                "Vibration",
                "Vibration Status",
                "Maintenance Status",
                "Downtime",
                "Availability",
                "Warnings",
                "Overall Status"
            ]
        )

        st.dataframe(
            monitoring_table,
            use_container_width=True
        )

    # ========================================================
    # MAINTENANCE
    # ========================================================

    elif selected_function == "Maintenance":

        st.title(
            "🔧 Equipment Maintenance Monitoring"
        )

        due = equipment[
            equipment["Maintenance_Status"] == "Due"
        ]

        overdue = equipment[
            equipment["Maintenance_Status"] == "Overdue"
        ]

        up_to_date = equipment[
            equipment["Maintenance_Status"]
            == "Up to Date"
        ]

        low_availability = equipment[
            equipment["Availability"] < 99.5
        ]

        col1, col2, col3, col4 = st.columns(4)

        col1.metric(
            "Maintenance Due",
            len(due)
        )

        col2.metric(
            "Maintenance Overdue",
            len(overdue)
        )

        col3.metric(
            "Up to Date",
            len(up_to_date)
        )

        col4.metric(
            "Low Availability",
            len(low_availability)
        )

        st.subheader(
            "Maintenance Due"
        )

        st.dataframe(
            due,
            use_container_width=True
        )

        st.subheader(
            "Maintenance Overdue"
        )

        st.dataframe(
            overdue,
            use_container_width=True
        )

        st.subheader(
            "Low Availability Equipment"
        )

        st.dataframe(
            low_availability,
            use_container_width=True
        )

        st.subheader(
            "Equipment Under Maintenance"
        )

        under = equipment[
            equipment["Maintenance_Status"]
            == "Under Maintenance"
        ]

        if len(under) > 0:

            st.dataframe(
                under,
                use_container_width=True
            )

        else:

            st.info(
                "No equipment is currently marked as under maintenance."
            )

    # ========================================================
    # RISK ASSESSMENT
    # ========================================================

    elif selected_function == "Risk Assessment":

        st.title(
            "⚠️ Worker Risk Assessment"
        )

        risk_results = []

        for index, worker in workers.iterrows():

            likelihood = calculate_likelihood(
                worker
            )

            consequence = calculate_consequence(
                worker
            )

            risk_score, risk_level = classify_risk(
                likelihood,
                consequence
            )

            risk_results.append([
                worker["Worker_ID"],
                worker["Department"],
                likelihood,
                consequence,
                risk_score,
                risk_level
            ])

        risk_table = pd.DataFrame(
            risk_results,
            columns=[
                "Worker ID",
                "Department",
                "Likelihood",
                "Consequence",
                "Risk Score",
                "Risk Level"
            ]
        )

        st.dataframe(
            risk_table,
            use_container_width=True
        )

        critical_risks = risk_table[
            risk_table["Risk Level"]
            == "Critical"
        ]

        high_risks = risk_table[
            risk_table["Risk Level"]
            == "High"
        ]

        col1, col2 = st.columns(2)

        col1.metric(
            "Critical Risks",
            len(critical_risks)
        )

        col2.metric(
            "High Risks",
            len(high_risks)
        )

        if len(critical_risks) > 0:

            st.error(
                "Critical risk workers require immediate attention."
            )

            st.dataframe(
                critical_risks,
                use_container_width=True
            )

    # ========================================================
    # ALERTS AND RECOMMENDATIONS
    # ========================================================

    elif selected_function == "Alerts & Recommendations":

        st.title(
            "🚨 Alerts and Recommendations"
        )

        alerts = generate_equipment_alerts(
            equipment
        )

        st.subheader(
            "Equipment Alerts"
        )

        if alerts:

            alert_table = pd.DataFrame(
                alerts,
                columns=[
                    "Equipment ID",
                    "Severity",
                    "Alert"
                ]
            )

            st.dataframe(
                alert_table,
                use_container_width=True
            )

        else:

            st.success(
                "No equipment alerts."
            )

        st.subheader(
            "Equipment Recommendations"
        )

        for index, item in equipment.iterrows():

            recommendations = equipment_recommendation(
                item
            )

            if recommendations:

                st.warning(
                    f"**{item['Equipment_ID']}**"
                )

                for recommendation in recommendations:

                    st.write(
                        "• " + recommendation
                    )

        st.subheader(
            "Worker Safety Alerts"
        )

        for index, worker in workers.iterrows():

            warnings = check_worker_safety(
                worker
            )

            if warnings:

                st.warning(
                    f"{worker['Worker_ID']}: "
                    + ", ".join(warnings)
                )

    # ========================================================
    # DATA ANALYSIS
    # ========================================================

    elif selected_function == "Data Analysis":

        st.title(
            "📊 Interactive Mining Data Analysis"
        )

        st.subheader(
            "Equipment Analysis"
        )

        downtime_ids, downtime = highest_downtime_equipment(
            equipment
        )

        availability_ids, availability = (
            lowest_availability_equipment(
                equipment
            )
        )

        vibration_ids, vibration = (
            highest_vibration_equipment(
                equipment
            )
        )

        temperature_ids, temperature = (
            highest_temperature_equipment(
                equipment
            )
        )

        col1, col2 = st.columns(2)

        with col1:

            st.write(
                f"**Highest downtime:** "
                f"{', '.join(downtime_ids)} "
                f"({downtime} hours)"
            )

            st.write(
                f"**Lowest availability:** "
                f"{', '.join(availability_ids)} "
                f"({availability:.2f}%)"
            )

        with col2:

            st.write(
                f"**Highest vibration:** "
                f"{', '.join(vibration_ids)} "
                f"({vibration} mm/s)"
            )

            st.write(
                f"**Highest temperature:** "
                f"{', '.join(temperature_ids)} "
                f"({temperature} °C)"
            )

        st.subheader(
            "Maintenance Analysis"
        )

        maintenance_needed = (
            equipment_requiring_maintenance(
                equipment
            )
        )

        overdue_items = overdue_equipment(
            equipment
        )

        inspection_items = equipment_needing_inspection(
            equipment
        )

        st.write(
            "**Equipment requiring maintenance:**",
            maintenance_needed
        )

        st.write(
            "**Overdue equipment:**",
            overdue_items
        )

        st.write(
            "**Equipment requiring immediate inspection:**",
            inspection_items
        )

        st.subheader(
            "Worker Risk Analysis"
        )

        risk_departments = highest_risk_department(
            workers
        )

        if isinstance(risk_departments, tuple):

            departments, number = risk_departments

            st.write(
                f"**Department with the most high/critical "
                f"risk workers:** "
                f"{', '.join(departments)} ({number})"
            )

        else:

            st.write(
                risk_departments
            )

        st.subheader(
            "Incident Analysis"
        )

        incident_by_department = (
            incidents["Department"]
            .value_counts()
        )

        fig, ax = plt.subplots()

        incident_by_department.plot(
            kind="bar",
            ax=ax
        )

        ax.set_title(
            "Incidents by Department"
        )

        ax.set_xlabel(
            "Department"
        )

        ax.set_ylabel(
            "Number of Incidents"
        )

        plt.xticks(rotation=0)

        plt.tight_layout()

        st.pyplot(fig)

        st.subheader(
            "Equipment Downtime"
        )

        fig2, ax2 = plt.subplots()

        ax2.bar(
            equipment["Equipment_ID"],
            equipment["Downtime"]
        )

        ax2.set_title(
            "Equipment Downtime"
        )

        ax2.set_xlabel(
            "Equipment"
        )

        ax2.set_ylabel(
            "Downtime (hours)"
        )

        plt.xticks(rotation=45)

        plt.tight_layout()

        st.pyplot(fig2)

    # ========================================================
    # REPORTS
    # ========================================================

    elif selected_function == "Reports":

        st.title(
            "📄 Mining Safety and Equipment Report"
        )

        ppe = calculate_ppe_compliance(
            workers
        )

        high_risk = workers[
            workers["Risk_Level"].isin(
                ["High", "Critical"]
            )
        ].shape[0]

        high_incidents = count_high_critical_incidents(
            incidents
        )

        alerts = generate_equipment_alerts(
            equipment
        )

        critical_alerts = sum(
            1 for alert in alerts
            if alert[1] == "CRITICAL"
        )

        report = f"""
KHWEZI MINING MONITORING SYSTEM
EXECUTIVE REPORT

WORKER SAFETY
Total workers: {len(workers)}
PPE compliance: {ppe:.1f}%
High/Critical risk workers: {high_risk}

SAFETY INCIDENTS
Total incidents: {len(incidents)}
Near misses: {count_near_misses(incidents)}
High/Critical incidents: {high_incidents}

EQUIPMENT
Total equipment: {len(equipment)}
Equipment available: {equipment_available(equipment)}
Equipment under maintenance: {equipment_under_maintenance(equipment)}
Average availability: {equipment["Availability"].mean():.2f}%

ALERTS
Total equipment alerts: {len(alerts)}
Critical alerts: {critical_alerts}

MANAGEMENT ATTENTION
"""

        attention = management_attention(
            workers,
            incidents,
            equipment
        )

        for item in attention:

            report += "\n- " + item

        st.text_area(
            "Generated Report",
            report,
            height=500
        )

        st.download_button(
            label="Download Report",
            data=report,
            file_name="Khwezi_Mining_Report.txt",
            mime="text/plain"
        )

    # ========================================================
    # MANAGE USERS
    # ========================================================

    elif selected_function == "Manage Users":

        st.title(
            "👤 Manage Users"
        )

        st.subheader(
            "Current Users"
        )

        user_table = []

        for username, details in users.items():

            user_table.append([
                username,
                details["role"]
            ])

        user_dataframe = pd.DataFrame(
            user_table,
            columns=[
                "Username",
                "Role"
            ]
        )

        st.dataframe(
            user_dataframe,
            use_container_width=True
        )

        st.subheader(
            "Add New User"
        )

        new_username = st.text_input(
            "New Username"
        )

        new_password = st.text_input(
            "New Password",
            type="password"
        )

        new_role = st.selectbox(
            "Role",
            [
                "Administrator",
                "Safety Officer",
                "Mining Engineer",
                "Maintenance Engineer",
                "Manager"
            ]
        )

        if st.button("Add User"):

            if new_username == "":

                st.error(
                    "Please enter a username."
                )

            elif new_password == "":

                st.error(
                    "Please enter a password."
                )

            elif new_username in users:

                st.error(
                    "Username already exists."
                )

            else:

                users[new_username] = {
                    "password": new_password,
                    "role": new_role
                }

                st.success(
                    f"User {new_username} added successfully."
                )
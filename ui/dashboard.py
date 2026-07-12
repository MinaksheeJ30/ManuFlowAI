import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.append(str(ROOT))

import streamlit as st

from agents.planner_agent import planner_agent
from agents.inventory_agent import inventory_agent
from agents.purchase_agent import purchase_agent
from agents.employee_agent import employee_agent
from agents.workshop_agent import workshop_agent

from database.google_sheets import add_job
from models.manufacturing_job import ManufacturingJob


# -----------------------------
# Page Configuration
# -----------------------------
st.set_page_config(
    page_title="ManuFlowAI",
    layout="wide"
)

with open("ui/styles/style.css") as f:
    st.markdown(
        f"<style>{f.read()}</style>",
        unsafe_allow_html=True
    )


# -----------------------------
# Sidebar
# -----------------------------
with st.sidebar:

    st.title("🏭 ManuFlowAI")
    st.caption("AI Manufacturing Planning Platform")

    st.divider()

    st.subheader("🚀 Features")

    st.write("✅ AI Planning")
    st.write("✅ Inventory Check")
    st.write("✅ Employee Allocation")
    st.write("✅ Workshop Planning")
    st.write("✅ Google Sheets")
    st.write("✅ Email Automation")

    st.divider()

    st.subheader("👩‍💻 Developer")

    st.write("**Minakshee Jamsandekar**")
    st.write("Mechanical Engineering")
    st.write("VJTI Mumbai")
    st.write("Lenovo LEAP Internship")

    st.divider()

    st.caption("Version 1.0")


# -----------------------------
# Header
# -----------------------------
st.image("ui/assets/manuflow_logo.png", width=500)

st.markdown("""
### AI Manufacturing Planning Assistant

Plan manufacturing jobs using AI agents, inventory checking,
employee allocation and workshop planning.

---
""")


# -----------------------------
# Metrics
# -----------------------------
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("🤖 AI Agents", "5")

with col2:
    st.metric("⚙️ n8n Workflows", "4")

with col3:
    st.metric("📋 Jobs Planned", "Live")


# -----------------------------
# User Input
# -----------------------------
request = st.text_area(
    "Manufacturing Request",
    height=180,
    placeholder="Example:\n\nManufacture 20 EN8 shafts using a lathe before 6 August 2026"
)

st.caption("💡 Describe the manufacturing job in natural language.")

# ==========================================================
# MAIN WORKFLOW
# ==========================================================

if st.button(
    "🚀 Generate Manufacturing Plan",
    use_container_width=True
):

    # -----------------------------
    # Planner
    # -----------------------------
    planner = planner_agent(request)

    with st.expander("📋 AI Planner Output", expanded=True):

        col1, col2 = st.columns(2)

        with col1:
            st.write("**Part Name**")
            st.success(planner["part_name"])

            st.write("**Material**")
            st.success(planner["material"])

            st.write("**Quantity**")
            st.success(str(planner["quantity"]))

        with col2:
            st.write("**Machine**")
            st.success(planner["machine"])

            st.write("**Deadline**")
            st.success(planner["deadline"])

            st.write("**Status**")
            st.success("Planning Completed ✅")

    if not planner["completed"]:
        st.warning("Please provide the following missing information:")

        for field in planner["missing_fields"]:
            st.write(f"• {field}")

        st.stop()

    # -----------------------------
    # Create Job
    # -----------------------------
    job = ManufacturingJob(
        part_name=planner["part_name"],
        material=planner["material"],
        quantity=planner["quantity"],
        machine=planner["machine"],
        deadline=planner["deadline"]
    )

    # -----------------------------
    # Inventory
    # -----------------------------
    inventory = inventory_agent(job)

    with st.expander("📦 Inventory Status"):

        if inventory["available"]:
            st.success("✅ Material Available in Inventory")
        else:
            st.error("❌ Material Not Available")

    if not inventory["available"]:

        purchase = purchase_agent(
            job.material,
            inventory["required"],
            inventory["stock"]
        )

        st.subheader("🛒 Purchase Request")
        st.json(purchase)

        st.stop()

    # -----------------------------
    # Employee
    # -----------------------------
    employee = employee_agent(job.machine)

    if employee is None:
        st.error("❌ No employee available.")
        st.stop()

    job.assigned_to = employee["Name"]

    with st.expander("👷 Employee Allocation"):

        st.write(f"**Employee ID:** {employee['Employee ID']}")
        st.write(f"**Name:** {employee['Name']}")
        st.write(f"**Department:** {employee['Department']}")
        st.write(f"**Email:** {employee['Email']}")
        st.write(f"**Current Tasks:** {employee['Current Tasks']}")

    # -----------------------------
    # Save Job
    # -----------------------------
    add_job(job)

    # -----------------------------
    # Workshop
    # -----------------------------
    workshop = workshop_agent(job)

    with st.expander("🏭 Workshop Operation Sheet"):

        st.write("### Operations")

        for op in workshop["operations"]:
            st.write(f"✅ {op}")

        st.write("### Estimated Time")
        st.info(workshop["estimated_time"])

        st.write("### Safety Instructions")

        for item in workshop["safety"]:
            st.write(f"🦺 {item}")

    st.balloons()

    st.success(
        "🎉 Manufacturing Plan Generated Successfully!\n\n"
        "✔ AI Planner completed\n"
        "✔ Inventory verified\n"
        "✔ Employee assigned\n"
        "✔ Workshop operations prepared\n"
        "✔ Job stored in Google Sheets\n"
        "✔ Ready for Production"
    )
    
st.markdown("---")

st.markdown(
    """
<div style="text-align:center; color:gray; font-size:14px;">
Built with ❤️ using <b>LangGraph</b>, <b>Streamlit</b>, <b>Google Sheets</b> & <b>n8n</b><br><br>

<b>ManuFlowAI v1.0</b><br>

Developed by <b>Minakshee Jamsandekar</b><br>

VJTI Mumbai | Lenovo LEAP Internship 2026
</div>
""",
    unsafe_allow_html=True
)
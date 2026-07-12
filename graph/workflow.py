from typing import TypedDict, Optional

from langgraph.graph import StateGraph, END

from agents.planner_agent import planner_agent
from agents.inventory_agent import inventory_agent
from agents.purchase_agent import purchase_agent
from agents.employee_agent import employee_agent
from agents.workshop_agent import workshop_agent

from database.google_sheets import add_job
from models.manufacturing_job import ManufacturingJob

print("USING WORKFLOW FILE:", __file__)

class WorkflowState(TypedDict, total=False):
    request: str

    planner: dict
    inventory: dict
    purchase: dict
    employee: dict
    workshop: dict

    job: ManufacturingJob

    status: str


# ----------------------------------------------------
# Planner
# ----------------------------------------------------

def planner_node(state: WorkflowState):

    planner = planner_agent(state["request"])

    state["planner"] = planner

    print("\n===== PLANNER STATE =====")
    print(planner)
    print("=========================\n")

    if not planner["completed"]:
        state["status"] = "missing_information"
        return state

    job = ManufacturingJob(
        part_name=planner["part_name"],
        material=planner["material"],
        quantity=planner["quantity"],
        machine=planner["machine"],
        deadline=planner["deadline"]
    )

    state["job"] = job
    state["status"] = "planned"

    return state


# ----------------------------------------------------
# Planner Router
# ----------------------------------------------------

def planner_router(state: WorkflowState):

    if state["status"] == "missing_information":
        return "end"

    return "inventory"


# ----------------------------------------------------
# Inventory
# ----------------------------------------------------

def inventory_node(state: WorkflowState):

    print("\n===== INVENTORY STATE =====")
    print(state)
    print("===========================\n")

    inventory = inventory_agent(state["job"])
    state["inventory"] = inventory

    if inventory["available"]:
        state["status"] = "inventory_available"
    else:
        state["status"] = "inventory_unavailable"

    return state


# ----------------------------------------------------
# Inventory Router
# ----------------------------------------------------

def inventory_router(state: WorkflowState):

    if state["status"] == "inventory_available":
        return "employee"

    return "purchase"


# ----------------------------------------------------
# Purchase
# ----------------------------------------------------

def purchase_node(state: WorkflowState):

    purchase = purchase_agent(
        state["job"].material,
        state["inventory"]["required"],
        state["inventory"]["stock"]
    )

    state["purchase"] = purchase

    return state


# ----------------------------------------------------
# Employee
# ----------------------------------------------------

def employee_node(state: WorkflowState):

    employee = employee_agent(state["job"].machine)

    state["employee"] = employee

    if employee is not None:
        state["job"].assigned_to = employee["Name"]

    return state

# ----------------------------------------------------
# Workshop
# ----------------------------------------------------

def workshop_node(state: WorkflowState):

    print("\n===== JOB OBJECT =====")
    print(state["job"])
    print("======================\n")

    add_job(state["job"])

    workshop = workshop_agent(state["job"])

    state["workshop"] = workshop

    return state


# ----------------------------------------------------
# Graph
# ----------------------------------------------------

builder = StateGraph(WorkflowState)

builder.add_node("planner", planner_node)
builder.add_node("inventory", inventory_node)
builder.add_node("purchase", purchase_node)
builder.add_node("employee", employee_node)
builder.add_node("workshop", workshop_node)

builder.set_entry_point("planner")

# Planner routing
builder.add_conditional_edges(
    "planner",
    planner_router,
    {
        "inventory": "inventory",
        "end": END
    }
)

# Inventory routing
builder.add_conditional_edges(
    "inventory",
    inventory_router,
    {
        "employee": "employee",
        "purchase": "purchase"
    }
)

builder.add_edge("employee", "workshop")

builder.add_edge("purchase", END)

builder.add_edge("workshop", END)

workflow = builder.compile()
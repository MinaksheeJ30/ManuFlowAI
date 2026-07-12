from database.inventory import check_inventory


def inventory_agent(job):

    inventory = check_inventory(job.material, job.quantity)

    if inventory["available"]:

        return {
            "available": True,
            "message": "Material available in inventory."
        }

    return {
        "available": False,
        "message": "Material not available.",
        "stock": inventory["stock"],
        "required": inventory["required"]
    }
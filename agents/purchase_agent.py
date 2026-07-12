from database.purchase_requests import add_purchase_request


def purchase_agent(material, required, stock):

    purchase = {
        "material": material,
        "required_qty": required,
        "current_stock": stock,
        "qty_to_order": required - stock,
        "priority": "High",
        "status": "Pending"
    }

    add_purchase_request(purchase)

    return purchase
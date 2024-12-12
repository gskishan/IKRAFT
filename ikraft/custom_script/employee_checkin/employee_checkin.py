import frappe

@frappe.whitelist()
def validate(doc, method):
    if checkifduplicate(doc) and doc.is_new():
        frappe.throw("This employee already has a log-{} with the same date".format(doc.log_type))

def checkifduplicate(doc):
    sql = """SELECT name FROM `tabEmployee Checkin` 
             WHERE employee = "{0}" AND log_type = "{1}" AND DATE(time) = DATE("{2}")""".format(doc.employee, doc.log_type, doc.time)
    
    if frappe.db.sql(sql, as_dict=True):
        return True
    else:
        return False

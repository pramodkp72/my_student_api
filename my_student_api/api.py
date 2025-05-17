import frappe

@frappe.whitelist()
def hello_world():
    return "Hello from my_student_api!"

@frappe.whitelist()
def get_student_attendance(student_id):
    # This is where you'll put your logic from the previous examples
    if not student_id:
        frappe.throw("Student ID is required")

    # Dummy data for now, replace with actual frappe.get_all call
    # when you have Student and Attendance DocTypes defined in this app or another
    attendance_records = [
        {"date": "2023-01-01", "status": "Present"},
        {"date": "2023-01-02", "status": "Absent"},
    ]
    return {"student_id": student_id, "attendance": attendance_records}
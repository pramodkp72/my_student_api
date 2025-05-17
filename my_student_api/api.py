import frappe

@frappe.whitelist()
def hello_world():
    return "Hello from my_student_api!"

@frappe.whitelist()
def get_student_attendance(student_id):
    """
    Retrieves attendance records for a specific student.
    (Assuming Student and Attendance DocTypes exist and are linked)
    """
    if not student_id:
        frappe.throw("Student ID is required.", title="Missing Parameter")

    # Check if student exists (optional but good practice)
    if not frappe.db.exists("Student", student_id):
        frappe.response.status_code = 404 # Not Found
        return {"error": f"Student with ID '{student_id}' not found."}

    # Placeholder for actual attendance fetching logic
    # Example:
    # attendance_records = frappe.get_all(
    # "Attendance",
    # filters={"student": student_id},
    # fields=["date", "status", "subject"] # Customize fields
    # )
    # if not attendance_records:
    # return {"message": f"No attendance records found for student '{student_id}'."}
    # return attendance_records

    # Dummy data for now, replace with actual frappe.get_all call
    attendance_records = [
        {"date": "2023-01-01", "status": "Present"},
        {"date": "2023-01-02", "status": "Absent"},
    ]
    return {"student_id": student_id, "attendance": attendance_records}


@frappe.whitelist() # This makes the function accessible via API
def get_student_details(student_id):
    """
    Retrieves details for a specific student based on their ID (name).
    :param student_id: The ID (name) of the student.
    """
    if not student_id:
        frappe.throw("Student ID is required.", title="Missing Parameter")
        return # Should not be reached if frappe.throw is used

    # Check if the student document exists
    if not frappe.db.exists("Student", student_id):
        # Set HTTP status code for "Not Found"
        frappe.response.status_code = 404
        return {"error": f"Student with ID '{student_id}' not found."}

    # Fetch the student document
    # Specify the fields you want to return
    # Ensure these fields exist in your "Student" DocType
    student_fields = ["name", "first_name", "last_name", "email_address", "date_of_birth", "program"] # Customize as needed

    try:
        student_doc = frappe.get_doc("Student", student_id)
        student_data = {field: student_doc.get(field) for field in student_fields if hasattr(student_doc, field)}

        # If you prefer to fetch specific fields directly without loading the whole document (more efficient for few fields):
        # student_data = frappe.get_value("Student", student_id, student_fields, as_dict=True)
        # if not student_data: # frappe.get_value returns None if not found, though frappe.db.exists should catch this
        #     frappe.response.status_code = 404
        #     return {"error": f"Student with ID '{student_id}' not found (get_value check)."}

    except frappe.DoesNotExistError:
        # This case should ideally be caught by frappe.db.exists, but good to have as a fallback
        frappe.response.status_code = 404
        return {"error": f"Student with ID '{student_id}' does not exist."}
    except Exception as e:
        frappe.log_error(frappe.get_traceback(), "Error in get_student_details")
        frappe.response.status_code = 500 # Internal Server Error
        return {"error": "An unexpected error occurred while fetching student details."}

    return student_data
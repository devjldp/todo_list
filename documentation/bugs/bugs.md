# Bugs

### BUG-001:

**Description:** When updating the user profile, the date_birth field does not get updated in the database. Other fields update correctly, but the date of birth remains unchanged.

**Steps:** 
1. Log in as an employee.
2. Navigate to the user dashboard
3. Introduce data.
4. Submit the form
5. Check database for the nupdated value.
5. Check the user dashboard view.

**Expected result:** All data is updated in the database
**Actual result:**  The date_birth field in the user_Details remains the previous value (Null)

**Root Cause:** The value from the form is submitted as a string. Problem with data type.

**Functions:**

1. update_user_details(employee_details) -> models.py
2. user_dashboard() ->  controller.py

**Fix:**
1. import *datetime* buitl-in package in python.

2. Create an extra key in the dictionary employee_Details

```python
# controller.py: user_dashbpard()
    employee_details = {
        "user_id": user[0],
        "name": user[1].capitalize() if user[1] else None,
        "phone": user[2].capitalize() if user[2] else None,
        "date_birth": user[3],
        "date_birth_str": user[3].strftime("%Y-%m-%d") if user[3] else None, 
        "address": user[4].capitalize() if user[4] else None,
        "city": user[5].capitalize() if user[5] else None,
        "role": user[6].capitalize() if user[6] else None
    }
```

3. If the field is empty, assign *None* to allow Null in the database or *empty string*.

```python
# models.py: update_user_details()
 if not date_birth_str or date_birth_str == "":
    employee_details["date_birth"] = None
else:
    employee_details["date_birth"] = datetime.strptime(date_birth_str, "%Y-%m-%d").date()
```


---

### BUG-002:

**Description:** When removing an employee, the employee is not removed from the child table.

**Steps:** 
1. Log in as an administrator.
2. Navigate to the admin dashboard
3. Select an employee and attempt to delete the employee.

**Expected result:** the ekmployee is removed from the database and is not displayed in the admin dashboard
**Actual result:** The deletion fails with a database error indicating that the record cannot be removed because it is referenced in a child table.

**Root Cause:** The foreign key constraint in the child table does not include ON DELETE CASCADE, preventing the deletion of the parent record.

**Fix:**
1. imOpen PgAdmin, select the database and modify.
2. Paste the following code.

```sql
ALTER TABLE user_details
DROP CONSTRAINT "FK_user_id"; 

ALTER TABLE user_details
ADD CONSTRAINT "FK_user_id"
FOREIGN KEY (user_id)
REFERENCES users(user_id)
ON DELETE CASCADE;
```


---
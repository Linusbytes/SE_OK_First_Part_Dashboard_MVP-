import csv
import random
import os
from datetime import datetime, timedelta

# --- Configuration ---
NUM_EMPLOYEES = 20
DAYS_BACK = 14
DEPARTMENTS = ['Logistics', 'Packaging', 'Sorting', 'Maintenance']
FORM_RESULTS = ['OK', 'NOK']
ROSTER_STATUSES = ['Active', 'Absent']

def generate_data():
    print("Generating data using pure Python...")
    
    # --- Step 1: Master Employee List ---
    employees = []
    for i in range(1, NUM_EMPLOYEES + 1):
        employees.append({
            'EmployeeID': f'E{i:03d}',
            'Name': f'Worker {i}',
            'Department': random.choice(DEPARTMENTS)
        })
    
    # --- Step 2: Date Dimension ---
    end_date = datetime.now().date()
    # Create list of date strings YYYY-MM-DD
    dates = [(end_date - timedelta(days=x)) for x in range(DAYS_BACK)]
    
    # --- Step 3: Scaffold (Cross Join + Roster Status) ---
    scaffold = []
    for emp in employees:
        for d in dates:
            # Simulate Roster Status: 90% Active, 10% Absent
            roster_status = 'Active' if random.random() < 0.9 else 'Absent'
            
            scaffold.append({
                'EmployeeID': emp['EmployeeID'],
                'Name': emp['Name'],
                'Department': emp['Department'],
                'Date': d, # Keep as date object for comparison
                'Roster_Status': roster_status
            })
    
    # Sort by Name then Date (Optional, for readability)
    scaffold.sort(key=lambda x: (x['Name'], x['Date']))
    
    # --- Step 4 & 5: Simulate Responses & Join Logic ---
    # We will compute the row directly as we process the scaffold
    final_rows = []
    
    for row in scaffold:
        # Defaults for the response part
        submission_time = ""
        form_result = ""
        comment = ""
        
        # Simulate Response Logic
        # If Active: 85% chance to have a submission. 
        # If Absent: 1% chance.
        
        chance = 0.85 if row['Roster_Status'] == 'Active' else 0.01
        
        has_submission = random.random() < chance
        
        if has_submission:
            # Generate Submission Details
            form_result = random.choices(FORM_RESULTS, weights=[0.9, 0.1])[0] # 90% OK
            
            # Submission Time: Random time between 06:00 and 09:00
            time_obj = datetime.combine(row['Date'], datetime.min.time()) + timedelta(hours=random.randint(6,8), minutes=random.randint(0,59))
            submission_time = time_obj.strftime('%Y-%m-%d %H:%M:%S')
            
            if form_result == 'NOK':
                issues = ['Sensor misalignment', 'Belt jammed', 'Safety guard loose', 'Pressure low', 'Debris on track']
                comment = random.choice(issues)
        
        # --- Step 6: Calculated 'True_Status' ---
        true_status = "Unknown"
        
        if has_submission:
            if form_result == 'OK':
                true_status = 'Green'
            elif form_result == 'NOK':
                true_status = 'Red'
        else:
            # No submission
            if row['Roster_Status'] == 'Active':
                true_status = 'Missing'
            elif row['Roster_Status'] == 'Absent':
                true_status = 'Gray'
        
        # Prepare Final Row
        final_rows.append({
            'EmployeeID': row['EmployeeID'],
            'Name': row['Name'],
            'Department': row['Department'],
            'Date': row['Date'].strftime('%Y-%m-%d'),
            'Roster_Status': row['Roster_Status'],
            'Submission_Time': submission_time,
            'Form_Result': form_result,
            'Comment': comment,
            'True_Status': true_status
        })
    
    # --- Output to CSV ---
    output_file = 'Schneider_DC_Cleaned_Data.csv'
    fieldnames = ['EmployeeID', 'Name', 'Department', 'Date', 'Roster_Status', 'Submission_Time', 'Form_Result', 'Comment', 'True_Status']
    
    try:
        with open(output_file, 'w', newline='') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(final_rows)
        
        print(f"Success! Data exported to {os.path.abspath(output_file)}")
        print("First 5 rows:")
        for r in final_rows[:5]:
            print(r)
            
    except Exception as e:
        print(f"Error writing file: {e}")

if __name__ == "__main__":
    generate_data()

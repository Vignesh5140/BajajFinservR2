import re
import hashlib
from datetime import datetime
import json
import pandas as pd
import matplotlib as plt

def transform_gender(gender):
    if gender == 'M':
        return 'male'
    elif gender == 'F':
        return 'female'
    else:
        return 'others'

def is_valid_mobile(phone_number):
    phone_number = re.sub(r'\D', '', phone_number)
  
    pattern = r'^(\+91|91)?[6-9]\d{9}$'
    if re.match(pattern, phone_number):
        return True
    else:
        return False

def calculate_age(dob):
    if not dob:
        return None  

    current_date = datetime.now()
    dob = datetime.strptime(dob, '%Y-%m-%dT%H:%M:%S.%fZ')
    age = current_date.year - dob.year
    if (current_date.month, current_date.day) < (dob.month, dob.day):
        age -= 1
    return age

with open('./DataEngineeringQ2.json') as file:
    data = json.load(file)


selected_data = []

# Initialize counters
valid_phone_numbers = 0
appointments = 0
medicines = 0
active_medicines = 0

for record in data:
    appointment_id = record['appointmentId']
    phone_number = record['phoneNumber']
    first_name = record['patientDetails']['firstName']
    last_name = record['patientDetails']['lastName']
    
    gender = record['patientDetails'].get('gender')
    if gender is not None:
        gender = transform_gender(gender)
    else:
        gender = 'others'
    
    dob = record['patientDetails'].get('birthDate')
    if dob is None:
        dob = ''

    medicines_data = record['consultationData'].get('medicines')
    if medicines_data:
        medicines += len(medicines_data)
        active_medicines += sum(medicine.get('IsActive', False) for medicine in medicines_data)

    full_name = f"{first_name} {last_name}"


    is_valid = is_valid_mobile(phone_number)

    if is_valid:
        phone_number_hash = hashlib.sha256(phone_number.encode()).hexdigest()
        valid_phone_numbers += 1
    else:
        phone_number_hash = None

    age = calculate_age(dob)

    selected_data.append({
        'appointmentId': appointment_id,
        'fullName': full_name,
        'phoneNumber': phone_number,
        'isValidMobile': is_valid,
        'phoneNumberHash': phone_number_hash,
        'gender': gender,
        'DOB': dob,
        'Age': age,
        'noOfMedicines': len(medicines_data),
        'noOfActiveMedicines': sum(medicine.get('IsActive', False) for medicine in medicines_data),
        'noOfInactiveMedicines': sum(not medicine.get('IsActive', False) for medicine in medicines_data),
        'MedicineNames': ', '.join(medicine['Name'] for medicine in medicines_data if medicine.get('IsActive', False))
    })

df = pd.DataFrame(selected_data)

df.to_csv('output.csv', index=False, sep='~')

aggregated_data = {
    'Age': df['Age'].mean(),
    'gender': df['gender'].value_counts().to_dict(),
    'validPhoneNumbers': valid_phone_numbers,
    'appointments': appointments,
    'medicines': medicines,
    'activeMedicines': active_medicines
}

with open('aggregated_data.json', 'w') as file:
    json.dump(aggregated_data, file)


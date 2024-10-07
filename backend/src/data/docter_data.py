import random
import json
from datetime import datetime, timedelta

# Predefined lists for generating random Indian names
first_names = ["Aarav", "Diya", "Arjun", "Ananya", "Rohan", "Meera", "Siddharth", "Priya", "Vikram", "Riya"]
last_names = ["Sharma", "Verma", "Reddy", "Iyer", "Singh", "Patel", "Das", "Gupta", "Mishra", "Nair"]

specializations = [
    "Gynecologist", "Obstetrician", "Pediatrician", "Neonatologist", "Cardiologist", "Surgeon", "Cardiothoracic Surgeon", 
    "Pulmonologist", "Respiratory Therapist", "Orthopedic Surgeon", "Orthopedic Specialist"
]

locations = [
    ("Anna Nagar, Chennai", (13.0704, 80.2275)),
    ("T. Nagar, Chennai", (13.0400, 80.2238)),
    ("Alwarpet, Chennai", (13.0364, 80.2460)),
    ("Vadapalani, Chennai", (13.0498, 80.2265)),
    ("Adyar, Chennai", (13.0020, 80.2521)),
    ("Manapakkam, Chennai", (13.0181, 80.1975)),
    ("Porur, Chennai", (13.0013, 80.1991)),
    ("Perumbakkam, Chennai", (12.9636, 80.2031)),
    ("Thousand Lights, Chennai", (13.0633, 80.2785))
]

# Function to generate a random phone number
def generate_phone_number():
    return f"+91 {random.randint(70000, 99999)} {random.randint(10000, 99999)}"

# Function to generate random email
def generate_email(first_name, last_name):
    domains = ["example.com", "mail.com", "healthcare.org"]
    return f"{first_name.lower()}.{last_name.lower()}@{random.choice(domains)}"

# Function to generate a random appointment time within the next month
def generate_appointment_time():
    start_date = datetime.now()
    appointment_time = start_date + timedelta(days=random.randint(1, 30), hours=random.randint(9, 17))
    return appointment_time.strftime("%Y-%m-%dT%H:%M:%S")

# Store all generated data here
doctors_data = []

# Generate random doctor data
for _ in range(100):  # Generate 100 doctors
    # Randomly select names, specialization, and location with lat/lng
    first_name = random.choice(first_names)
    last_name = random.choice(last_names)
    doctor_name = f"Dr. {first_name} {last_name}"
    
    specialization = random.choice(specializations)
    location, (latitude, longitude) = random.choice(locations)
    
    # Generate random contact details
    contact = generate_email(first_name, last_name)
    phone = generate_phone_number()
    
    # Generate random rating (between 4.0 and 5.0)
    rating = round(random.uniform(4.0, 5.0), 1)

    # Create doctor entry
    doctor_entry = {
        "doctor_name": doctor_name,
        "specialization": specialization,
        "location": location,
        "contact": contact,
        "phone": phone,
        "rating": rating,
        "latitude": latitude,
        "longitude": longitude,
        "appointment_time": generate_appointment_time()
    }

    # Append to the list
    doctors_data.append(doctor_entry)

# Save the generated data to a JSON file
with open('backend/src/data/indian_doctors_data.json', 'w') as json_file:
    json.dump(doctors_data, json_file, indent=4)

print("Random Indian doctor data generated and saved to indian_doctors_data.json")

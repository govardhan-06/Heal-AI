# HealAI

## Overview

HealAI is your complete healthcare companion, guiding you every step of the way. From finding the right doctor and booking appointments to analyzing medical reports and recommending lifestyle changes, HealAI ensures you're supported throughout your healing journey. Whether it's getting to your appointment or providing detailed insights from prescriptions and lab reports, HealAI takes care of it all. With AI-powered agents working for you, the app handles everything seamlessly, allowing you to focus on what matters most—your health. Let HealAI steer the process while you relax in the back seat, knowing you're in safe hands.

## How Does the App Work?

The HealAI app features three main AI agents:

1. **User Agent**
2. **Doctor Agent**
3. **Healer Agent**

### User Agent

The User Agent helps users analyze their health conditions. Powered by the Meta Llama 3.1 70B model, it processes the user's input and recommends doctors based on the diagnosis. Users can then confirm appointments, which will be scheduled automatically. This agent also has additional features, such as:

- **Appointment Scheduling**: Once a doctor is confirmed, the appointment is booked.
- **Google Calendar Integration**: Adds the confirmed appointment to the user's Google Calendar.
- **Uber Ride Booking**: Users can book a ride with a custom deeplink provided by the agent.

### Doctor Agent

The Doctor Agent receives appointment details after the User Agent has scheduled an appointment. The doctor gets all necessary details for the visit, and after the consultation, the payment is processed automatically.

### Healer Agent

The Healer Agent is a medical AI assistant for users. It provides users with medication dosage instructions and reminders. Users can also upload prescriptions, lab reports, and other medical documents, which the Healer Agent will analyze, providing relevant insights.

- **Prescription Analysis**: Offers dosage suggestions and reminders for medications.
- **Lab Report Insights**: Provides detailed insights from any uploaded lab reports or medical documents.

## Additional Features

- **Doctor Discovery Using Location Services**: The User Agent finds the nearby doctors using the device's location.
- **Blockchain-Based Payment Processing**: Payments are processed through the Fetch Blockchain using the Almanac smart contract. Users must purchase 'FET' tokens, and once the doctor visit is confirmed, the consultation fee is automatically processed.
- **Secure Medical Data Handling**: All user-uploaded documents, such as prescriptions and lab reports, are stored securely, ensuring privacy and compliance with healthcare data regulations.
- **Calendar and Ride Booking**: Google Calendar integration and Uber ride booking are supported with one tap.

## Pitch Deck

We have prepared a comprehensive Pitch Deck that details the vision and technical aspects of HealAI, including how decentralized AI agents contribute to improved healthcare. Check it out to understand our mission and future plans in detail.

## Installation

### To Setup the Backend Server:

1. Pull the Docker image:
   ```bash
   docker pull govardhan06/healai:v3
   ```
2. Run the Docker container:
   ```bash
   docker run -d -p 8000:8000 govardhan06/healai:v3
   ```
3. The backend will now be available on port 8000.

### To Setup the Flutter App:

1. Navigate to the frontend directory.
2. Connect an Android emulator or a physical device via USB debugging.
3. Run the following command:
   ```bash
   flutter run
   ```

## Usage

- Start interacting with the HealAI app by inputting your health conditions, booking doctor appointments, and receiving medical insights.
- The user can also access ride-booking services and sync their schedule with Google Calendar.

## License

This project is licensed under the Apache License. See the LICENSE file for more details.

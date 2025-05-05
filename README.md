# Election Voting System

A modern, GUI-based Election Voting System built with Python's Tkinter library. This project demonstrates secure voter registration, candidate and party management, OTP-based authentication for voting, and visualizes election results and voter turnout. **This system is for demonstration and educational purposes only.**

---

## Table of Contents
- [Features](#features)
- [Installation](#installation)
- [Setup](#setup)
- [Usage](#usage)
- [Screenshots](#screenshots)
- [Contributing](#contributing)
- [License](#license)

---

## Features

- **Voter Registration:** Register voters with name, age, gender, and phone number. Age validation ensures only eligible voters (18+) can register.
- **OTP Authentication:** Voters receive a One-Time Password (OTP) via SMS (Twilio integration) to authenticate before voting.
- **Candidate & Party Registration:** Admins can register new candidates and parties. Candidates must belong to a registered party.
- **Voting:** Authenticated voters can cast their vote for registered candidates.
- **Result Visualization:** Pie charts display voting results and voter turnout using Matplotlib.
- **Data Export:** Voter data can be exported to Excel and PDF formats.
- **Admin Login:** Secure login for admin access to sensitive features.

---

## Installation

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/election-voting-system.git
   cd election-voting-system
   ```
2. **Install dependencies:**
   ```bash
   pip install twilio matplotlib pandas
   ```
   Tkinter is included with most Python installations.

---

## Setup

1. **Twilio Setup:**
   - Sign up at [Twilio](https://www.twilio.com/).
   - Get your `account_sid`, `auth_token`, and a Twilio phone number.
   - Replace the placeholders in the script:
     ```python
     account_sid = 'YOUR_TWILIO_ACCOUNT_SID'
     auth_token = 'YOUR_TWILIO_AUTH_TOKEN'
     twilio_number = 'YOUR_TWILIO_PHONE_NUMBER'
     ```

2. **Run the Application:**
   - Save the script as `voting_system.py` (or any name you prefer).
   - Run the script:
     ```bash
     python voting_system.py
     ```

---

## Usage

1. **Login:**
   - Use the default admin credentials:
     - ID: `admin`
     - Password: `password`

2. **Register Parties and Candidates:**
   - Register parties first, then candidates (candidates must belong to a registered party).

3. **Register Voters:**
   - Enter voter details. An OTP will be sent to the provided phone number for authentication.

4. **Voting:**
   - Voters can cast their vote after OTP verification.

5. **View Results:**
   - Admin can view election results and voter turnout as pie charts (password: `admin123`).

6. **Export Data:**
   - Save voter data to Excel or PDF using the provided buttons.

---


## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

---

## License

This project is provided for educational purposes and does not include a specific license. You are free to use and modify it for learning and demonstration purposes.

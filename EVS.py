import tkinter as tk
from tkinter import messagebox
import random
import tkinter.font as tkFont
from twilio.rest import Client
import matplotlib.pyplot as plt
import pandas as pd
import os
import matplotlib.backends.backend_pdf as pdf

# Twilio credentials
account_sid = 'ACe3eeef2d5c1b93bb7588062a6aba5c9f'
auth_token = 'fc591a2e8fe163146b217bf4739cf75d'
twilio_number = '+14843244418'

# Initialize Twilio client
client = Client(account_sid, auth_token)
total_voters = 0

# Voter class
class Voter:
    def __init__(self, name, age, gender, phone_number, otp):
        self.name = name
        self.age = age
        self.gender = gender
        self.phone_number = phone_number
        self.otp = otp
        self.hasVoted = False

# Candidate class
class Candidate:
    def __init__(self, name, party):
        self.name = name
        self.party = party
        self.votes = 0

# Party class
class Party:
    def __init__(self, name, symbol):
        self.name = name
        self.symbol = symbol

# Function to generate OTP
def generate_otp():
    return ''.join(str(random.randint(0, 9)) for _ in range(6))

# Function to verify OTP
def verify_otp(entered_otp, actual_otp):
    return entered_otp == actual_otp

# Function to send OTP via Twilio
def send_otp(phone_number, otp):
    try:
        message = client.messages.create(
            body=f'Your OTP for voting is: {otp}',
            from_=twilio_number,
            to=phone_number
        )
        return True
    except Exception as e:
        print("SMS sending failed:", e)
        return False


# Function to vote
def vote():
    if not candidates:
        show_error("Error", "No candidates registered yet.")
        return

    candidate_names = "\n".join([f"{i + 1}. {candidate.name} ({candidate.party})" for i, candidate in enumerate(candidates)])
    choice_str = custom_input_dialog("Vote", f"Enter your choice (1-{len(candidates)}):\n{candidate_names}")
    if choice_str is None:
        return None  
    try:
        choice = int(choice_str)
        if 1 <= choice <= len(candidates):
            return choice
        else:
            show_error("Error", f"Invalid choice. Please enter a number between 1 and {len(candidates)}.")
            return None
    except ValueError:
        show_error("Error", "Invalid input. Please enter a valid number.")
        return None


# Function to save voters' data to Excel
def save_voters_to_excel():
    if not voters:
        show_error("Error", "No voters registered yet.")
        return

    voter_data = {
        "Name": [voter.name for voter in voters],
        "Age": [voter.age for voter in voters],
        "Gender": [voter.gender for voter in voters],
        "Phone Number": [voter.phone_number for voter in voters],
        "OTP": [voter.otp for voter in voters],
        "Has Voted": [voter.hasVoted for voter in voters]
    }

    df = pd.DataFrame(voter_data)
    excel_filename = "independentproject.xlsx"
    df.to_excel(excel_filename, index=False)
    custom_message_box("Data Saved", "Voters' data saved successfully.")
    os.system(excel_filename)


# Function to display voting results
def display_results(candidates):
    if not candidates:
        show_error("Error", "No candidates registered yet.")
        return

    password = custom_input_dialog("Display Results", "Enter the password to view results:")
    if password is None:
        return

    if password == "admin123":
        candidate_names = [f"Candidate {i + 1} ({candidate.name}), Party: {candidate.party}" for i, candidate in
                           enumerate(candidates)]
        votes = [candidate.votes for candidate in candidates]

        plt.figure(figsize=(8, 8))
        plt.pie(votes, labels=candidate_names, autopct='%1.1f%%', startangle=140)
        plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        plt.title('Voting Results')
        plt.show()
    else:
        show_error("Error", "Incorrect password. Access denied.")

# Function to register a candidate
def register_candidate():
    candidate_name = custom_input_dialog("Register Candidate", "Enter candidate's name:")
    if candidate_name: 
        candidate_party = custom_input_dialog("Register Candidate", "Enter candidate's party:")
        if candidate_party:
            # Check if the entered party is registered
            if not any(party.name == candidate_party for party in parties):
                show_error("Error", f"The party '{candidate_party}' is not registered. Please register the party first.")
                return
            
            candidates.append(Candidate(candidate_name, candidate_party))
            custom_message_box("Candidate registered", f"{candidate_name} from {candidate_party} registered successfully.")
        else:
            show_error("Error", "Candidate's party cannot be blank.")
    else:
        show_error("Error", "Candidate's name cannot be blank.")

# Function to register a party
def register_party():
    party_name = custom_input_dialog("Register Party", "Enter party's name:")
    if party_name: 
        party_symbol = custom_input_dialog("Register Party", "Enter party's symbol:")
        if party_symbol: 
            parties.append(Party(party_name, party_symbol))
            custom_message_box("Party registered", f"{party_name} with symbol {party_symbol} registered successfully.")
        else:
            show_error("Error", "Party's symbol cannot be blank.")
    else:
        show_error("Error", "Party's name cannot be blank.")
total_voters = 0

# Function to register a voter
def register_voter():
    global total_voters
    if total_voters < 100:
        input_dialog = tk.Toplevel()
        input_dialog.title("Register Voter")
        input_dialog.geometry("350x350")
        input_dialog.configure(bg='#2D142C')

        labels = ["Name:", "Age:", "Gender:", "Phone Number:"]
        entries = []

        for i, label_text in enumerate(labels):
            label = tk.Label(input_dialog, text=label_text, font=("Arial", 12), bg='#2D142C', fg='#eeeeee')
            label.grid(row=i, column=0, padx=10, pady=5, sticky="w")

            if label_text == "Gender:":
                gender_var = tk.StringVar(input_dialog)
                gender_var.set("Select Gender")  # Default value
                genders = ["Male", "Female", "Rather not say"]
                gender_menu = tk.OptionMenu(input_dialog, gender_var, *genders)
                gender_menu.config(font=("Arial", 12), bg="#EE4540", fg='black', relief=tk.FLAT, width=15)
                gender_menu["menu"].config(font=("Arial", 12), bg="#EE4540", fg='black', relief=tk.FLAT)
                gender_menu.grid(row=i, column=1, padx=10, pady=5, sticky="e")
                entries.append(gender_var)
            else:
                entry_var = tk.StringVar()
                entry = tk.Entry(input_dialog, textvariable=entry_var, font=("Arial", 12))
                entry.grid(row=i, column=1, padx=10, pady=5, sticky="e")
                entries.append(entry_var)

        def submit():
            voter_info = {
                'name': entries[0].get(),
                'age': entries[1].get(),
                'gender': entries[2].get(),
                'phone_number': entries[3].get()
            }

            if not all(voter_info.values()):
                show_error("Error", "All fields are required.")
                return

            try:
                voter_info['age'] = int(voter_info['age'])
                if voter_info['age'] < 18:
                    show_error("Error", "Voters must be 18 years or older.")
                    return
            except ValueError:
                show_error("Error", "Age must be a number.")
                return

            otp = generate_otp()
            if send_otp(voter_info['phone_number'], otp):
                custom_message_box("OTP Sent", "OTP sent successfully to the given phone number.")
                voters.append(Voter(voter_info['name'], voter_info['age'], voter_info['gender'], voter_info['phone_number'], otp))
                total_voters += 1
                input_dialog.destroy()
            else:
                show_error("Error", "Failed to send OTP. Please try again.")

        submit_button = tk.Button(input_dialog, text="Submit", command=submit, font=("Arial", 12), bg="#801336", fg='#eeeeee', relief=tk.SUNKEN)
        submit_button.grid(row=len(labels), columnspan=2, pady=10)

        input_dialog.grab_set()
        input_dialog.wait_window()
    else:
        show_error("Error", "Maximum voters reached.")
def total_voters_voted():
    if not voters:
        messagebox.showinfo("No Voters", "No voters registered yet.")
        return

    voted = sum(1 for voter in voters if voter.hasVoted)
    not_voted = len(voters) - voted
    labels = ['Voted', 'Not Voted']
    sizes = [voted, not_voted]
    colors = ['#ff9999', '#66b3ff']
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Voters who have voted vs. Voters who have not voted')
    plt.axis('equal')
    plt.show()

# Function to cast a vote
def cast_vote():
    username = custom_input_dialog("Vote", "Enter your name:")
    if username is None: 
        return  

    voter_index = next((i for i, voter in enumerate(voters) if voter.name == username), -1)
    if voter_index != -1 and not voters[voter_index].hasVoted:
        entered_otp = custom_input_dialog("Vote", "Enter OTP:")
        if entered_otp is None:  
            return  

        if verify_otp(entered_otp, voters[voter_index].otp):
            choice = vote()
            if choice is None: 
                return  

            chosen_candidate = candidates[choice - 1]
            custom_message_box("Vote", f"You voted for {chosen_candidate.party} ({chosen_candidate.name})")
            chosen_candidate.votes += 1
            voters[voter_index].hasVoted = True
        else:
            show_error("Error", "Invalid OTP. Please try again.")
    else:
        show_error("Error", "Invalid username or you have already voted.")

# Function to show registered candidates
def show_registered_candidates():
    if not candidates:
        show_error("Registered Candidates", "No candidates registered yet.")
        return

    candidate_list_window = tk.Toplevel()
    candidate_list_window.title("Registered Candidates")
    candidate_list_window.geometry("400x300")
    candidate_list_window.configure(bg='#2D142C')

    label = tk.Label(candidate_list_window, text="Registered Candidates", font=("Arial", 14), bg='#2D142C', fg='#eeeeee')
    label.pack(pady=10)

    for i, candidate in enumerate(candidates, start=1):
        candidate_info = f"{i}. Name: {candidate.name}, Party: {candidate.party}"
        tk.Label(candidate_list_window, text=candidate_info, font=("Arial", 12), bg='#2D142C', fg='#eeeeee').pack()

# Function to show registered voters
def show_registered_voters():
    if not voters:
        show_error("Registered Voters", "No voters registered yet.")
        return

    voter_list_window = tk.Toplevel()
    voter_list_window.title("Registered Voters")
    voter_list_window.geometry("400x300")
    voter_list_window.configure(bg='#2D142C')

    label = tk.Label(voter_list_window, text="Registered Voters", font=("Arial", 14), bg='#2D142C', fg='#eeeeee')
    label.pack(pady=10)

    for i, voter in enumerate(voters, start=1):
        voter_info = f"{i}. Name: {voter.name}, Age: {voter.age}, Gender: {voter.gender}, Phone: {voter.phone_number}"
        tk.Label(voter_list_window, text=voter_info, font=("Arial", 12), bg='#2D142C', fg='#eeeeee').pack()

# Function to show error messages
def show_error(title, message):
    messagebox.showerror(title, message)

# Function for custom input dialog
def custom_input_dialog(title, prompt):
    input_dialog = tk.Toplevel()
    input_dialog.title(title)
    input_dialog.geometry("300x150")
    input_dialog.configure(bg='#2D142C')

    label = tk.Label(input_dialog, text=prompt, font=("Arial", 12), bg='#2D142C', fg='#eeeeee')
    label.pack(pady=10)

    entry_var = tk.StringVar()
    entry = tk.Entry(input_dialog, textvariable=entry_var, font=("Arial", 12))
    entry.pack(pady=5)

    ok_button = tk.Button(input_dialog, text="OK", command=lambda: input_dialog.destroy(), font=("Arial", 12), bg="#801336", fg='#eeeeee', relief=tk.SUNKEN)
    ok_button.pack(pady=10)

    entry.focus_set()
    input_dialog.grab_set()
    input_dialog.wait_window()

    return entry_var.get()

# Function for custom message box
def custom_message_box(title, message):
    message_box = tk.Toplevel()
    message_box.title(title)
    message_box.geometry("400x100")
    message_box.configure(bg='#2D142C')

    label = tk.Label(message_box, text=message, font=("Arial", 12), bg='#2D142C', fg='#eeeeee')
    label.pack(pady=10)

    ok_button = tk.Button(message_box, text="OK", command=lambda: message_box.destroy(), font=("Arial", 12) ,bg="#801336", fg='#eeeeee', relief=tk.SUNKEN)
    ok_button.pack(pady=10)

    message_box.grab_set()
    message_box.wait_window()

# Function to save voters' data to Excel and PDF
def save_voters_data():
    if not voters:
        show_error("Error", "No voters registered yet.")
        return

    voter_data = {
        "Name": [voter.name for voter in voters],
        "Age": [voter.age for voter in voters],
        "Gender": [voter.gender for voter in voters],
        "Phone Number": [voter.phone_number for voter in voters],
        "OTP": [voter.otp for voter in voters],
        "Has Voted": [voter.hasVoted for voter in voters]
    }

    df = pd.DataFrame(voter_data)
    excel_filename = "voters_data.xlsx"
    df.to_excel(excel_filename, index=False)
    custom_message_box("Data Saved", "Voters' data saved successfully in Excel format.")
    os.system(excel_filename)

# Function to save voters' data to PDF
def save_voters_to_pdf():
    if not voters:
        show_error("Error", "No voters registered yet.")
        return

    # Prepare data for table
    voter_data = {
        "Name": [voter.name for voter in voters],
        "Age": [voter.age for voter in voters],
        "Gender": [voter.gender for voter in voters],
        "Phone Number": [voter.phone_number for voter in voters],
        "OTP": [voter.otp for voter in voters],
        "Has Voted": ["Yes" if voter.hasVoted else "No" for voter in voters]
    }

    # Prepare data for pie chart
    voted = sum(1 for voter in voters if voter.hasVoted)
    not_voted = len(voters) - voted
    labels = ['Voted', 'Not Voted']
    sizes = [voted, not_voted]

     # Create PDF
    pdf_filename = "voters_data.pdf"
    with pdf.PdfPages(pdf_filename) as pdf_pages:
        # Add table to PDF
        fig, ax = plt.subplots(figsize=(10, 6))
        ax.axis('tight')
        ax.axis('off')
        ax.table(cellText=[list(voter_data.keys())] + list(zip(*voter_data.values())),
                 colLabels=None,
                 cellLoc='center',
                 loc='center')
        pdf_pages.savefig(fig, bbox_inches='tight')
        plt.close()
        # Add pie chart to PDF
        plt.figure(figsize=(8, 6))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', startangle=90)
        plt.title('Voters who have voted vs. Voters who have not voted')
        plt.axis('equal')
        pdf_pages.savefig()
        plt.close()


    custom_message_box("Data Saved", "Voters' data saved successfully in PDF format.")    

    # Create a PDF file
    pdf_filename = "voters_data.pdf"
    pdf_pages = pdf.PdfPages(pdf_filename)

    # Create a subplot for the table
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.axis('tight')
    ax.axis('off')
    ax.table(cellText=df.values, colLabels=df.columns, cellLoc='center', loc='center')  # type: ignore
    # Add the table to the PDF
    pdf_pages.savefig(fig, bbox_inches='tight')
    plt.close()

    #Pie chart showing the percentage of voters who have voted vs. not voted
    voted = sum(1 for voter in voters if voter.hasVoted)
    not_voted = len(voters) - voted
    labels = ['Voted', 'Not Voted']
    sizes = [voted, not_voted]
    colors = ['#ff9999', '#66b3ff']
    plt.figure(figsize=(8, 6))
    plt.pie(sizes, colors=colors, labels=labels, autopct='%1.1f%%', startangle=90)
    plt.title('Voters who have voted vs. Voters who have not voted')
    plt.axis('equal')
    pdf_pages.savefig(plt.gcf(), bbox_inches='tight')
    plt.close()

    pdf_pages.close()

    custom_message_box("Data Saved", "Voters' data saved successfully in both Excel and PDF formats.")
    os.system(excel_filename) # type: ignore
    os.system(pdf_filename)

def authenticate():
    id_entered = id_var.get()
    password_entered = password_var.get()

    if id_entered == "admin" and password_entered == "password":
        login_window.destroy()
        main()
    else:
        show_error("Error", "Invalid ID or password.")
        login_window.destroy()

def create_login_window():
    global login_window, id_var, password_var

    login_window = tk.Tk()
    login_window.title("Login")

    # Set window to fullscreen
    login_window.attributes('-fullscreen', True)
    login_window.configure(bg="#2D142C") 

    # Frame to contain the ID and password fields
    login_frame = tk.Frame(login_window, bg="#2D142C")  
    login_frame.pack(expand=True)

    # Function to exit the application
    def exit_application():
        login_window.destroy()

    # Title label
    title_label = tk.Label(login_frame, text="Election Voting System Login", font=("Calibri Light (Headings)", 24, "bold"), bg="#2D142C", fg="#EEEEEE")  
    title_label.pack(pady=(20, 10))

    id_label = tk.Label(login_frame, text="ID:", font=("Arial", 16), bg="#2D142C", fg="#EEEEEE")  
    id_label.pack(pady=10)

    id_var = tk.StringVar()
    id_entry = tk.Entry(login_frame, textvariable=id_var, font=("Calibri Light (Headings)", 12, "bold"))
    id_entry.pack(pady=10)

    password_label = tk.Label(login_frame, text="Password:", font=("Calibri Light (Headings)", 16, "bold"), bg="#2D142C", fg="#EEEEEE")  
    password_label.pack(pady=10)

    password_var = tk.StringVar()
    password_entry = tk.Entry(login_frame, textvariable=password_var, show="*", font=("Calibri Light (Headings)", 12, "bold"))
    password_entry.pack(pady=10)

    button_width = 15

    login_button = tk.Button(login_frame, text="Login", command=authenticate, font=("Calibri Light (Headings)", 12, "bold"), bg="#801336", fg="#EEEEEE", relief=tk.SUNKEN, bd=3, width=button_width)  
    login_button.pack(pady=10)

    exit_button = tk.Button(login_frame, text="Exit", command=exit_application, font=("Calibri Light (Headings)", 12, "bold"), bg="#801336", fg="#EEEEEE", relief=tk.SUNKEN, bd=3, width=button_width)  
    exit_button.pack(pady=10)

    # Center the login frame within the window
    login_frame.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

    login_window.mainloop()



# Main function
def main():
    root = tk.Tk()
    root.title("Election Voting System")

    # Set window to fullscreen
    root.attributes('-fullscreen', True)

    menu_frame = tk.Frame(root, bg="#2D142C")
    menu_frame.pack(fill=tk.BOTH, expand=True)

    # Top heading
    top_heading = tk.Label(root, text="Election Voting System", font=("Calibri Light (Headings)", 36, "bold"), bg='#2D142C', fg='#EE4540')
    top_heading.pack(side="top", fill="x")

    menu_frame = tk.Frame(root, bg="#2D142C")
    menu_frame.pack(fill=tk.BOTH, expand=True)

    # Upper section
    upper_frame = tk.Frame(menu_frame, bg="#2D142C")
    upper_frame.pack(side="top", pady=50, expand=True)

    # Upper left section
    upper_left_frame = tk.Frame(upper_frame, bg="#2D142C")
    upper_left_frame.pack(side="left", padx=50, expand=True)

    # Vertical line between upper left and upper center sections
    vertical_line1 = tk.Frame(upper_frame, width=2, bg="black")
    vertical_line1.pack(side="left", fill="y", padx=50, pady=10)

    # Upper center section
    upper_center_frame = tk.Frame(upper_frame, bg="#2D142C")
    upper_center_frame.pack(side="left", padx=50, expand=True)

    # Vertical line between upper center and upper right sections
    vertical_line2 = tk.Frame(upper_frame, width=2, bg="black")
    vertical_line2.pack(side="left", fill="y", padx=50, pady=10)

    # Upper right section
    upper_right_frame = tk.Frame(upper_frame, bg="#2D142C")
    upper_right_frame.pack(side="left", padx=50, expand=True)

    # Lower section
    lower_frame = tk.Frame(menu_frame, bg="#2D142C")
    lower_frame.pack(side="bottom", pady=50, expand=True)

    # Define button font
    button_font = tkFont.Font(family="Calibri Light (Headings)", size=16, weight="bold")

    # Set a fixed width for all buttons
    button_width = 25

    # Heading for Voter privileges
    lbl_voter_heading = tk.Label(upper_left_frame, text="Voter Privileges", font=("Calibri Light (Headings)", 20, "bold"), fg="#C72C41", bg="#2D142C")
    lbl_voter_heading.pack(pady=(20, 10))

    # Voter privileges buttons
    btn_register_voter = tk.Button(upper_left_frame, text="Register Voter", command=register_voter, font=button_font,
                                   relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_register_voter.pack(pady=10)

    btn_vote = tk.Button(upper_left_frame, text="Vote", command=cast_vote, font=button_font, relief=tk.SUNKEN, bd=3,
                         bg="#801336", fg="#eeeeee", width=button_width)
    btn_vote.pack(pady=10)

    btn_show_voters = tk.Button(upper_left_frame, text="Show registered Voters", command=show_registered_voters,
                                font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_show_voters.pack(pady=10)

    # Heading for Candidate privileges
    lbl_candidate_heading = tk.Label(upper_center_frame, text="Candidate Privileges", font=("Calibri Light (Headings)", 20, "bold"), fg="#C72C41", bg="#2D142C")
    lbl_candidate_heading.pack(pady=(5, 55))

    # Candidate privileges buttons
    btn_register_candidate = tk.Button(upper_center_frame, text="Register Candidate", command=register_candidate,
                                       font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_register_candidate.pack(pady=10)

    btn_show_candidates = tk.Button(upper_center_frame, text="Show registered Candidates", command=show_registered_candidates,
                                    font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_show_candidates.pack(pady=10)
    
    # Heading for Admin privileges
    lbl_admin_heading = tk.Label(upper_right_frame, text="Admin Privileges", font=("Calibri Light (Headings)", 20, "bold"), fg="#C72C41", bg="#2D142C")
    lbl_admin_heading.pack(pady=(5, 55))

    # Admin privileges buttons
    btn_register_party = tk.Button(upper_right_frame, text="Register Party", command=register_party,
                                   font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_register_party.pack(pady=10)

    btn_display_results = tk.Button(upper_right_frame, text="Display Results", command=lambda: display_results(candidates),
                                    font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_display_results.pack(pady=10)

    # Voter Turnout
    btn_total_voters_voted = tk.Button(lower_frame, text="Voter Turnout", command=total_voters_voted,
                                   font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_total_voters_voted.pack(pady=10)
    

    #button to Save Voters Data to Excel
    btn_save_data = tk.Button(lower_frame, text="Save Voters Data to Excel", command=save_voters_to_excel,
                              font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_save_data.pack(pady=10)

    #button to Save Voters Data to PDF
    btn_save_pdf = tk.Button(lower_frame, text="Save Voters Data to PDF", command=save_voters_to_pdf,
                             font=button_font, relief=tk.SUNKEN, bd=3, bg="#801336", fg="#eeeeee", width=button_width)
    btn_save_pdf.pack(pady=10)

    # Exit button
    btn_exit = tk.Button(lower_frame, text="Exit", command=root.destroy, font=button_font, relief=tk.SUNKEN, bd=3,
                         bg="#801336", fg="#eeeeee", width=button_width)
    btn_exit.pack(pady=10)
    

    root.mainloop()


if __name__ == "__main__":
    voters = []
    candidates = []
    parties = []
    total_voters = 0
    create_login_window()
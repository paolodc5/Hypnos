# Hypnos

**Hypnos** is our application for sleep monitoring and remote patient management.  
It is the final project for the **Medical Informatics** course 2024–25 @ Politecnico di Milano.

This is the link to the github repo: 
https://github.com/paolodc5/Hypnos

---

## How to Run Hypnos

Follow these steps to run the app correctly:

### 1. Clone the repo
To get started with Hypnos locally, you need to clone the repository from GitHub:
```bash
git clone https://github.com/your-username/hypnos.git
cd hypnos
```

### 2. (Optional) Create and activate a virtual environment

Open a terminal, navigate to the project folder, and run:

```bash
# Create a virtual environment
python -m venv venv

# Activate the virtual environment
# On Windows
venv\Scripts\activate

# On macOS/Linux
source venv/bin/activate
```
### 3. Install requirements
Once the virtual environment is activated, install the required packages:
```bash
pip install -r requirements.txt
```

### 4. Run the application
After installing the dependencies, start the app with:
```bash
# Run from the project's root directory
python main.py
```

## Test users credentials
All the passwords are "12345", you can see all the therapist already registered in the database file.  
**Example Patient:**  
- Name: *Katrina*  
- Surname: *Salas*

**Example Doctor:**  
- Name: *Brooke*  
- Surname: *Lane*


## Project structure
```bash
hypnos/
├── main.py                 # Application entry point
├── requirements.txt        # Required Python packages
├── db/                     # Database handling module
├── gui/                    # Graphical User Interface (customTkinter)
├── models/                 # Domain classes (patients, doctors, prescriptions, etc.)
└── services/               # Application logic layer
```










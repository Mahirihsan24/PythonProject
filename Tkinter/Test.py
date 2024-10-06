import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import sqlite3

def initialize_database():
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    phone_number TEXT PRIMARY KEY,
                    name TEXT,
                    balance REAL,
                    pin_hash TEXT,
                    account_type TEXT,
                    interest_rate REAL,
                    loan_amount REAL,
                    policy_number TEXT
                 )''')
    conn.commit()
    conn.close()


def create_account_in_db(phone_number, name, balance, pin_hash, account_type, interest_rate=None, loan_amount=None, policy_number=None):
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    c.execute('INSERT INTO accounts (phone_number, name, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
              (phone_number, name, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number))
    conn.commit()
    conn.close()


def get_account_from_db(phone_number):
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE phone_number=?', (phone_number,))
    account = c.fetchone()
    conn.close()
    return account


def update_account_in_db(phone_number, balance, loan_amount=None, name=None):
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    if loan_amount is not None and name is not None:
        c.execute('UPDATE accounts SET balance=?, loan_amount=?, name=? WHERE phone_number=?', (balance, loan_amount, name, phone_number))
    elif loan_amount is not None:
        c.execute('UPDATE accounts SET balance=?, loan_amount=? WHERE phone_number=?', (balance, loan_amount, phone_number))
    elif name is not None:
        c.execute('UPDATE accounts SET balance=?, name=? WHERE phone_number=?', (balance, name, phone_number))
    else:
        c.execute('UPDATE accounts SET balance=? WHERE phone_number=?', (balance, phone_number))
    conn.commit()
    conn.close()

class MobileMoneyAccount:
    def __init__(self, phone_number: str, balance: float, pin: str):
        self.phone_number = phone_number
        self.balance = balance
        self.pin_hash = hashlib.sha256(pin.encode()).hexdigest()

    def deposit(self, amount: float) -> None:
        self.balance += amount
        print(f"{self.phone_number} Deposited {amount} Tk/=. Current balance is: {self.balance} Tk/=")

    def withdraw(self, amount: float) -> None:
        if self.balance >= amount:
            self.balance -= amount
            print(f"{self.phone_number} Withdrew {amount} Tk/=. Current balance is: {self.balance} Tk/=")
        else:
            print("You don't have enough funds to withdraw.")


class SavingsAccount(MobileMoneyAccount):
    def __init__(self, phone_number: str, balance: float, pin: str, name: str, interest_rate: float):
        super().__init__(phone_number, balance, pin)
        self.name = name
        self.interest_rate = interest_rate

    def calculate_interest(self) -> float:
        return self.balance * self.interest_rate


class LoanAccount(MobileMoneyAccount):
    def __init__(self, phone_number: str, balance: float, pin: str, name: str, loan_amount: float):
        super().__init__(phone_number, balance, pin)
        self.name = name
        self.loan_amount = loan_amount

    def repay_loan(self, amount: float) -> None:
        if amount <= self.loan_amount:
            self.loan_amount -= amount
            print(f"Loan repaid with amount {amount}. Remaining loan: {self.loan_amount}")
        else:
            print("Amount is more than the loan.")


class InsuranceAccount(MobileMoneyAccount):
    def __init__(self, phone_number: str, balance: float, pin: str, name: str, policy_number: str):
        super().__init__(phone_number, balance, pin)
        self.name = name
        self.policy_number = policy_number

    def claim_insurance(self, claim_amount: float) -> None:
        print(f"Insurance claim of {claim_amount} has been made on policy number {self.policy_number}")


class MobileBankingSystem:
    def __init__(self):
        self.accounts = {}
        initialize_database()

    def create_account(self, phone_number: str, name: str, pin: str, account_type: str, **kwargs) -> bool:
        if get_account_from_db(phone_number) is not None:
            print("Mobile number already registered.")
            return False
        else:
            pin_hash = hashlib.sha256(pin.encode()).hexdigest()
            balance = 0
            interest_rate = kwargs.get('interest_rate')
            loan_amount = kwargs.get('loan_amount')
            policy_number = kwargs.get('policy_number')
            create_account_in_db(phone_number, name, balance, pin_hash, account_type, interest_rate, loan_amount,
                                 policy_number)
            if account_type == 'savings':
                self.accounts[phone_number] = SavingsAccount(phone_number, balance, pin, name, interest_rate)
            elif account_type == 'loan':
                self.accounts[phone_number] = LoanAccount(phone_number, balance, pin, name, loan_amount)
            elif account_type == 'insurance':
                self.accounts[phone_number] = InsuranceAccount(phone_number, balance, pin, name, policy_number)
            else:
                self.accounts[phone_number] = MobileMoneyAccount(phone_number, balance, pin)
            print(f"{phone_number} {account_type} account created successfully.")
            return True

    def login(self, phone_number: str, pin: str) -> MobileMoneyAccount:
        account_data = get_account_from_db(phone_number)
        if account_data:
            _, name, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number = account_data
            if pin_hash == hashlib.sha256(pin.encode()).hexdigest():
                if account_type == 'savings':
                    self.accounts[phone_number] = SavingsAccount(phone_number, balance, pin, name, interest_rate)
                elif account_type == 'loan':
                    self.accounts[phone_number] = LoanAccount(phone_number, balance, pin, name, loan_amount)
                elif account_type == 'insurance':
                    self.accounts[phone_number] = InsuranceAccount(phone_number, balance, pin, name, policy_number)
                else:
                    self.accounts[phone_number] = MobileMoneyAccount(phone_number, balance, pin)
                print(f"{phone_number} logged in successfully.")
                return self.accounts[phone_number]
        print("Invalid mobile number or pin.")
        return None


class MobileBankingSystemController:
    def __init__(self, mobile_banking_system: MobileBankingSystem):
        self.mobile_banking_system = mobile_banking_system
        self.account_manager = AccountManager()

    def create_account(self, phone_number: str, name: str, pin: str, account_type: str, **kwargs) -> bool:
        return self.mobile_banking_system.create_account(phone_number, name, pin, account_type, **kwargs)

    def login(self, phone_number: str, pin: str) -> MobileMoneyAccount:
        return self.mobile_banking_system.login(phone_number, pin)

    def deposit(self, account: MobileMoneyAccount, amount: float) -> None:
        account.deposit(amount)
        update_account_in_db(account.phone_number, account.balance)

    def withdraw(self, account: MobileMoneyAccount, amount: float) -> None:
        account.withdraw(amount)
        update_account_in_db(account.phone_number, account.balance)

    def calculate_interest(self, account: SavingsAccount) -> float:
        return account.calculate_interest()

    def repay_loan(self, account: LoanAccount, amount: float) -> None:
        account.repay_loan(amount)
        update_account_in_db(account.phone_number, account.balance, account.loan_amount)

    def claim_insurance(self, account: InsuranceAccount, claim_amount: float) -> None:
        account.claim_insurance(claim_amount)

    def transfer(self, source_account: MobileMoneyAccount, target_account: MobileMoneyAccount, amount: float) -> None:
        if source_account.balance >= amount:
            source_account.withdraw(amount)
            target_account.deposit(amount)
            update_account_in_db(source_account.phone_number, source_account.balance)
            update_account_in_db(target_account.phone_number, target_account.balance)
            print(f"Transferred {amount} Tk/= from {source_account.phone_number} to {target_account.phone_number}")
        else:
            print("Insufficient balance to complete the transfer.")


class AccountManager:
    def __init__(self):
        self.accounts = {}

    def add_account(self, account: MobileMoneyAccount) -> None:
        self.accounts[account.phone_number] = account

    def display_all_accounts(self) -> None:
        for phone_number, account in self.accounts.items():
            print(f"Phone Number: {phone_number}")
            print(f"Name: {account.name}")
            print(f"Balance: {account.balance}")
            print("------------------------")


class GUI:
    def __init__(self, master, mobile_banking_system_controller: MobileBankingSystemController):
        self.master = master
        self.mobile_banking_system_controller = mobile_banking_system_controller

        self.create_account_frame = tk.Frame(self.master, bg="#e0f7fa")
        self.create_account_frame.pack(fill="both", expand=True)

        self.login_frame = tk.Frame(self.master, bg="#e8f5e9")
        self.login_frame.pack(fill="both", expand=True)

        self.create_account_widgets()
        self.login_widgets()

    def create_account_widgets(self) -> None:
        title = tk.Label(self.create_account_frame, text="Create Account", font=("Arial", 24, "bold"), bg="#e0f7fa",
                         fg="#00796b")
        title.pack(pady=20)

        phone_label = tk.Label(self.create_account_frame, text="Phone Number:", bg="#e0f7fa", font=("Arial", 12))
        phone_label.pack(pady=5)
        self.phone_number_entry = tk.Entry(self.create_account_frame, width=30, font=("Arial", 12))
        self.phone_number_entry.pack(pady=5)

        name_label = tk.Label(self.create_account_frame, text="Name:", bg="#e0f7fa", font=("Arial", 12))
        name_label.pack(pady=5)
        self.name_entry = tk.Entry(self.create_account_frame, width=30, font=("Arial", 12))
        self.name_entry.pack(pady=5)

        pin_label = tk.Label(self.create_account_frame, text="PIN:", bg="#e0f7fa", font=("Arial", 12))
        pin_label.pack(pady=5)
        self.pin_entry = tk.Entry(self.create_account_frame, width=30, show="*", font=("Arial", 12))
        self.pin_entry.pack(pady=5)

        account_type_label = tk.Label(self.create_account_frame, text="Account Type:", bg="#e0f7fa", font=("Arial", 12))
        account_type_label.pack(pady=5)
        self.account_type_var = tk.StringVar()
        self.account_type_var.set("mobile")
        account_type_menu = tk.OptionMenu(self.create_account_frame, self.account_type_var, "mobile", "savings", "loan",
                                          "insurance")
        account_type_menu.config(font=("Arial", 12))
        account_type_menu.pack(pady=5)

        create_button = tk.Button(self.create_account_frame, text="Create Account", command=self.create_account,
                                  bg="#00796b", fg="white", font=("Arial", 14))
        create_button.pack(pady=20)

        clear_button = tk.Button(self.create_account_frame, text="Clear", command=self.clear_create_account_fields,
                                 bg="#c62828", fg="white", font=("Arial", 14))
        clear_button.pack(pady=10)

    def login_widgets(self) -> None:
        title = tk.Label(self.login_frame, text="Login", font=("Arial", 24, "bold"), bg="#e8f5e9", fg="#388e3c")
        title.pack(pady=20)

        phone_label = tk.Label(self.login_frame, text="Phone Number:", bg="#e8f5e9", font=("Arial", 12))
        phone_label.pack(pady=5)
        self.login_phone_number_entry = tk.Entry(self.login_frame, width=30, font=("Arial", 12))
        self.login_phone_number_entry.pack(pady=5)

        pin_label = tk.Label(self.login_frame, text="PIN:", bg="#e8f5e9", font=("Arial", 12))
        pin_label.pack(pady=5)
        self.login_pin_entry = tk.Entry(self.login_frame, width=30, show="*", font=("Arial", 12))
        self.login_pin_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login, bg="#388e3c", fg="white",
                                 font=("Arial", 14))
        login_button.pack(pady=20)

        clear_button = tk.Button(self.login_frame, text="Clear", command=self.clear_login_fields, bg="#c62828",
                                 fg="white", font=("Arial", 14))
        clear_button.pack(pady=10)

    def account_operations_widgets(self, account) -> None:
        self.account_operations_window = tk.Toplevel(self.master)
        self.account_operations_window.title("Account Operations")
        self.account_operations_window.geometry("400x600")
        self.account_operations_window.configure(bg="#fffde7")

        title = tk.Label(self.account_operations_window, text="Account Operations", font=("Arial", 24, "bold"),
                         bg="#fffde7", fg="#f9a825")
        title.pack(pady=20)

        deposit_button = tk.Button(self.account_operations_window, text="Deposit",
                                   command=lambda: self.deposit(account), bg="#28a745", fg="white", font=("Arial", 14))
        deposit_button.pack(pady=10)

        withdraw_button = tk.Button(self.account_operations_window, text="Withdraw",
                                    command=lambda: self.withdraw(account), bg="#ff913c", fg="white",
                                    font=("Arial", 14))
        withdraw_button.pack(pady=10)

        transfer_button = tk.Button(self.account_operations_window, text="Transfer",
                                    command=lambda: self.transfer(account), bg="#007bff", fg="white",
                                    font=("Arial", 14))
        transfer_button.pack(pady=10)

        check_balance_button = tk.Button(self.account_operations_window, text="Check Balance",
                                         command=lambda: self.check_balance(account), bg="#fbc02d", fg="white",
                                         font=("Arial", 14))
        check_balance_button.pack(pady=10)

        interest_button = tk.Button(self.account_operations_window, text="Calculate Interest",
                                    command=lambda: self.calculate_interest(account), bg="#7f04a3", fg="white",
                                    font=("Arial", 14))
        interest_button.pack(pady=10)

        repay_button = tk.Button(self.account_operations_window, text="Repay Loan",
                                 command=lambda: self.repay_loan(account), bg="#615f61", fg="white", font=("Arial", 14))
        repay_button.pack(pady=10)

        claim_button = tk.Button(self.account_operations_window, text="Claim Insurance",
                                 command=lambda: self.claim_insurance(account), bg="#fc82ff", fg="white",
                                 font=("Arial", 14))
        claim_button.pack(pady=10)

        logout_button = tk.Button(self.account_operations_window, text="Logout", command=self.logout, bg="#c62828",
                                  fg="white", font=("Arial", 14))
        logout_button.pack(pady=20)

    def clear_create_account_fields(self) -> None:
        self.phone_number_entry.delete(0, tk.END)
        self.name_entry.delete(0, tk.END)
        self.pin_entry.delete(0, tk.END)
        self.account_type_var.set("mobile")

    def clear_login_fields(self) -> None:
        self.login_phone_number_entry.delete(0, tk.END)
        self.login_pin_entry.delete(0, tk.END)

    def create_account(self) -> None:
        phone_number = self.phone_number_entry.get()
        name = self.name_entry.get()
        pin = self.pin_entry.get()
        account_type = self.account_type_var.get()
        additional_kwargs = {}
        if account_type == "savings":
            interest_rate = simpledialog.askfloat("Input", "Enter Interest Rate:")
            additional_kwargs['interest_rate'] = interest_rate
        elif account_type == "loan":
            loan_amount = simpledialog.askfloat("Input", "Enter Loan Amount:")
            additional_kwargs['loan_amount'] = loan_amount
        elif account_type == "insurance":
            policy_number = simpledialog.askstring("Input", "Enter Policy Number:")
            additional_kwargs['policy_number'] = policy_number
        if self.mobile_banking_system_controller.create_account(phone_number, name, pin,account_type, **additional_kwargs):
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Error", "Account creation failed.")

    def login(self) -> None:
        phone_number = self.login_phone_number_entry.get()
        pin = self.login_pin_entry.get()
        account = self.mobile_banking_system_controller.login(phone_number, pin)
        if account:
            self.account_operations_widgets(account)
            self.login_frame.pack_forget()
        else:
            messagebox.showerror("Error", "Login failed.")

    def deposit(self, account) -> None:
        amount = simpledialog.askfloat("Input", "Enter deposit amount:")
        self.mobile_banking_system_controller.deposit(account, amount)
        messagebox.showinfo("Success", "Deposit successful!")

    def withdraw(self, account) -> None:
        amount = simpledialog.askfloat("Input", "Enter withdrawal amount:")
        self.mobile_banking_system_controller.withdraw(account, amount)
        messagebox.showinfo("Success", "Withdrawal successful!")

    def transfer(self, account) -> None:
        target_phone_number = simpledialog.askstring("Input", "Enter target phone number:")
        if target_phone_number in self.mobile_banking_system_controller.mobile_banking_system.accounts:
            target_account = self.mobile_banking_system_controller.mobile_banking_system.accounts[target_phone_number]
            amount = simpledialog.askfloat("Input", "Enter transfer amount:")
            self.mobile_banking_system_controller.transfer(account, target_account, amount)
            messagebox.showinfo("Success", "Transfer successful!")
        else:
            messagebox.showerror("Error", "Target account not found.")

    def check_balance(self, account) -> None:
        balance = account.balance
        messagebox.showinfo("Balance", f"Your current balance is: {balance} Tk/=")

    def calculate_interest(self, account) -> None:
        if isinstance(account, SavingsAccount):
            interest = self.mobile_banking_system_controller.calculate_interest(account)
            messagebox.showinfo("Interest", f"Calculated interest: {interest}")
        else:
            messagebox.showerror("Error", "This operation is not available for your account type.")

    def repay_loan(self, account) -> None:
        if isinstance(account, LoanAccount):
            amount = simpledialog.askfloat("Input", "Enter repayment amount:")
            self.mobile_banking_system_controller.repay_loan(account, amount)
            messagebox.showinfo("Success", "Loan repayment successful!")
        else:
            messagebox.showerror("Error", "This operation is not available for your account type.")

    def claim_insurance(self, account) -> None:
        if isinstance(account, InsuranceAccount):
            claim_amount = simpledialog.askfloat("Input", "Enter claim amount:")
            self.mobile_banking_system_controller.claim_insurance(account, claim_amount)
            messagebox.showinfo("Success", "Insurance claim successful!")
        else:
            messagebox.showerror("Error", "This operation is not available for your account type.")

    def logout(self) -> None:
        self.account_operations_window.destroy()
        self.login_frame.pack(fill="both", expand=True)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mobile Banking System")
    root.geometry("400x600")
    mobile_banking_system = MobileBankingSystem()
    mobile_banking_system_controller = MobileBankingSystemController(mobile_banking_system)
    gui = GUI(root, mobile_banking_system_controller)
    root.mainloop()
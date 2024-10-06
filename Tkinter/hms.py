import tkinter as tk
from tkinter import messagebox, simpledialog
import hashlib
import sqlite3


def initialize_database():
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS accounts (
                    phone_number TEXT PRIMARY KEY,
                    balance REAL,
                    pin_hash TEXT,
                    account_type TEXT,
                    interest_rate REAL,
                    loan_amount REAL,
                    policy_number TEXT
                 )''')
    conn.commit()
    conn.close()


def create_account_in_db(phone_number, balance, pin_hash, account_type, interest_rate=None, loan_amount=None, policy_number=None):
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    c.execute('INSERT INTO accounts (phone_number, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number) VALUES (?, ?, ?, ?, ?, ?, ?)',
              (phone_number, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number))
    conn.commit()
    conn.close()


def get_account_from_db(phone_number):
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    c.execute('SELECT * FROM accounts WHERE phone_number=?', (phone_number,))
    account = c.fetchone()
    conn.close()
    return account


def update_account_in_db(phone_number, balance, loan_amount=None):
    conn = sqlite3.connect('mobile_banking_system.db')
    c = conn.cursor()
    if loan_amount is not None:
        c.execute('UPDATE accounts SET balance=?, loan_amount=? WHERE phone_number=?', (balance, loan_amount, phone_number))
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
    def __init__(self, phone_number: str, balance: float, pin: str, interest_rate: float):
        super().__init__(phone_number, balance, pin)
        self.interest_rate = interest_rate

    def calculate_interest(self) -> float:
        return self.balance * self.interest_rate


class LoanAccount(MobileMoneyAccount):
    def __init__(self, phone_number: str, balance: float, pin: str, loan_amount: float):
        super().__init__(phone_number, balance, pin)
        self.loan_amount = loan_amount

    def repay_loan(self, amount: float) -> None:
        if amount <= self.loan_amount:
            self.loan_amount -= amount
            print(f"Loan repaid with amount {amount}. Remaining loan: {self.loan_amount}")
        else:
            print("Amount is more than the loan.")


class InsuranceAccount(MobileMoneyAccount):
    def __init__(self, phone_number: str, balance: float, pin: str, policy_number: str):
        super().__init__(phone_number, balance, pin)
        self.policy_number = policy_number

    def claim_insurance(self, claim_amount: float) -> None:
        print(f"Insurance claim of {claim_amount} has been made on policy number {self.policy_number}")


class MobileBankingSystem:
    def __init__(self):
        self.accounts = {}
        initialize_database()

    def create_account(self, phone_number: str, pin: str, account_type: str, **kwargs) -> bool:
        if get_account_from_db(phone_number) is not None:
            print("Mobile number already registered.")
            return False
        else:
            pin_hash = hashlib.sha256(pin.encode()).hexdigest()
            balance = 0
            interest_rate = kwargs.get('interest_rate')
            loan_amount = kwargs.get('loan_amount')
            policy_number = kwargs.get('policy_number')
            create_account_in_db(phone_number, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number)
            if account_type == 'savings':
                self.accounts[phone_number] = SavingsAccount(phone_number, balance, pin, interest_rate)
            elif account_type == 'loan':
                self.accounts[phone_number] = LoanAccount(phone_number, balance, pin, loan_amount)
            elif account_type == 'insurance':
                self.accounts[phone_number] = InsuranceAccount(phone_number, balance, pin, policy_number)
            else:
                self.accounts[phone_number] = MobileMoneyAccount(phone_number, balance, pin)
            print(f"{phone_number} {account_type} account created successfully.")
            return True

    def login(self, phone_number: str, pin: str) -> MobileMoneyAccount:
        account_data = get_account_from_db(phone_number)
        if account_data:
            _, balance, pin_hash, account_type, interest_rate, loan_amount, policy_number = account_data
            if pin_hash == hashlib.sha256(pin.encode()).hexdigest():
                if account_type == 'savings':
                    self.accounts[phone_number] = SavingsAccount(phone_number, balance, pin, interest_rate)
                elif account_type == 'loan':
                    self.accounts[phone_number] = LoanAccount(phone_number, balance, pin, loan_amount)
                elif account_type == 'insurance':
                    self.accounts[phone_number] = InsuranceAccount(phone_number, balance, pin, policy_number)
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

    def create_account(self, phone_number: str, pin: str, account_type: str, **kwargs) -> bool:
        return self.mobile_banking_system.create_account(phone_number, pin, account_type, **kwargs)

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

        pin_label = tk.Label(self.create_account_frame, text="PIN:", bg="#e0f7fa", font=("Arial", 12))
        pin_label.pack(pady=5)
        self.pin_entry = tk.Entry(self.create_account_frame, width=30, font=("Arial", 12), show="*")
        self.pin_entry.pack(pady=5)

        account_type_label = tk.Label(self.create_account_frame, text="Account Type:", bg="#e0f7fa", font=("Arial", 12))
        account_type_label.pack(pady=5)
        self.account_type_var = tk.StringVar()
        self.account_type_var.set("mobile_money")
        account_type_options = ["mobile_money", "savings", "loan", "insurance"]
        self.account_type_menu = tk.OptionMenu(self.create_account_frame, self.account_type_var, *account_type_options)
        self.account_type_menu.pack(pady=5)

        self.additional_entry_label = tk.Label(self.create_account_frame, text="", bg="#e0f7fa", font=("Arial", 12))
        self.additional_entry_label.pack(pady=5)
        self.additional_entry = tk.Entry(self.create_account_frame, width=30, font=("Arial", 12))
        self.additional_entry.pack(pady=5)

        self.account_type_var.trace("w", self.update_additional_entry_visibility)

        create_button = tk.Button(self.create_account_frame, text="Create Account", command=self.create_account,
                                  font=("Arial", 14), bg="#00796b", fg="white", relief="flat")
        create_button.pack(pady=20)

    def login_widgets(self) -> None:
        title = tk.Label(self.login_frame, text="Login", font=("Arial", 24, "bold"), bg="#e8f5e9", fg="#388e3c")
        title.pack(pady=20)

        phone_label = tk.Label(self.login_frame, text="Phone Number:", bg="#e8f5e9", font=("Arial", 12))
        phone_label.pack(pady=5)
        self.login_phone_number_entry = tk.Entry(self.login_frame, width=30, font=("Arial", 12))
        self.login_phone_number_entry.pack(pady=5)

        pin_label = tk.Label(self.login_frame, text="PIN:", bg="#e8f5e9", font=("Arial", 12))
        pin_label.pack(pady=5)
        self.login_pin_entry = tk.Entry(self.login_frame, width=30, font=("Arial", 12), show="*")
        self.login_pin_entry.pack(pady=5)

        login_button = tk.Button(self.login_frame, text="Login", command=self.login, font=("Arial", 14), bg="#388e3c",
                                 fg="white", relief="flat")
        login_button.pack(pady=20)

    def update_additional_entry_visibility(self, *args):
        account_type = self.account_type_var.get()
        if account_type == "savings":
            self.additional_entry_label.config(text="Interest Rate:")
        elif account_type == "loan":
            self.additional_entry_label.config(text="Loan Amount:")
        elif account_type == "insurance":
            self.additional_entry_label.config(text="Policy Number:")
        else:
            self.additional_entry_label.config(text="")
            self.additional_entry.delete(0, tk.END)
        self.additional_entry.pack_forget()
        if account_type in ["savings", "loan", "insurance"]:
            self.additional_entry.pack(pady=5)

    def create_account(self) -> None:
        phone_number = self.phone_number_entry.get()
        pin = self.pin_entry.get()
        account_type = self.account_type_var.get()
        additional_info = self.additional_entry.get()

        kwargs = {}
        if account_type == "savings":
            kwargs['interest_rate'] = float(additional_info)
        elif account_type == "loan":
            kwargs['loan_amount'] = float(additional_info)
        elif account_type == "insurance":
            kwargs['policy_number'] = additional_info

        if self.mobile_banking_system_controller.create_account(phone_number, pin, account_type, **kwargs):
            messagebox.showinfo("Success", "Account created successfully!")
        else:
            messagebox.showerror("Error", "Failed to create account. Phone number may already be registered.")

    def login(self) -> None:
        phone_number = self.login_phone_number_entry.get()
        pin = self.login_pin_entry.get()

        account = self.mobile_banking_system_controller.login(phone_number, pin)
        if account:
            self.show_dashboard(account)
        else:
            messagebox.showerror("Error", "Invalid mobile number or PIN.")

    def show_dashboard(self, account: MobileMoneyAccount) -> None:
        dashboard = Dashboard(self.master, account, self.mobile_banking_system_controller)
        dashboard.pack(fill="both", expand=True)
        self.create_account_frame.pack_forget()
        self.login_frame.pack_forget()


class Dashboard(tk.Frame):
    def __init__(self, master, account: MobileMoneyAccount, controller: MobileBankingSystemController):
        super().__init__(master)
        self.master = master
        self.account = account
        self.controller = controller
        self.configure(bg="#f1f8e9")

        self.create_widgets()

    def create_widgets(self):
        title = tk.Label(self, text=f"Dashboard - {self.account.phone_number}", font=("Arial", 24, "bold"), bg="#f1f8e9", fg="#2e7d32")
        title.pack(pady=20)

        balance_label = tk.Label(self, text=f"Balance: {self.account.balance} Tk/=", font=("Arial", 18), bg="#f1f8e9", fg="#2e7d32")
        balance_label.pack(pady=10)

        deposit_button = tk.Button(self, text="Deposit", command=self.deposit, font=("Arial", 14), bg="#388e3c", fg="white", relief="flat")
        deposit_button.pack(pady=10)

        withdraw_button = tk.Button(self, text="Withdraw", command=self.withdraw, font=("Arial", 14), bg="#d32f2f", fg="white", relief="flat")
        withdraw_button.pack(pady=10)

        if isinstance(self.account, SavingsAccount):
            interest_button = tk.Button(self, text="Calculate Interest", command=self.calculate_interest, font=("Arial", 14), bg="#1976d2", fg="white", relief="flat")
            interest_button.pack(pady=10)

        if isinstance(self.account, LoanAccount):
            repay_button = tk.Button(self, text="Repay Loan", command=self.repay_loan, font=("Arial", 14), bg="#f57c00", fg="white", relief="flat")
            repay_button.pack(pady=10)

        if isinstance(self.account, InsuranceAccount):
            claim_button = tk.Button(self, text="Claim Insurance", command=self.claim_insurance, font=("Arial", 14), bg="#0288d1", fg="white", relief="flat")
            claim_button.pack(pady=10)

    def deposit(self):
        amount = simpledialog.askfloat("Deposit", "Enter amount to deposit:")
        if amount is not None:
            self.controller.deposit(self.account, amount)
            messagebox.showinfo("Success", "Deposit successful!")

    def withdraw(self):
        amount = simpledialog.askfloat("Withdraw", "Enter amount to withdraw:")
        if amount is not None:
            self.controller.withdraw(self.account, amount)
            messagebox.showinfo("Success", "Withdrawal successful!")

    def calculate_interest(self):
        interest = self.controller.calculate_interest(self.account)
        messagebox.showinfo("Interest", f"Accrued Interest: {interest} Tk/=")

    def repay_loan(self):
        amount = simpledialog.askfloat("Repay Loan", "Enter amount to repay:")
        if amount is not None:
            self.controller.repay_loan(self.account, amount)
            messagebox.showinfo("Success", "Loan repayment successful!")

    def claim_insurance(self):
        claim_amount = simpledialog.askfloat("Claim Insurance", "Enter claim amount:")
        if claim_amount is not None:
            self.controller.claim_insurance(self.account, claim_amount)
            messagebox.showinfo("Success", "Insurance claim successful!")


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Mobile Banking System")
    root.geometry("400x600")
    mobile_banking_system = MobileBankingSystem()
    mobile_banking_system_controller = MobileBankingSystemController(mobile_banking_system)
    gui = GUI(root, mobile_banking_system_controller)
    root.mainloop()

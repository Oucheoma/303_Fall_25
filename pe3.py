import datetime
import string

# ----------------
# Caesar cipher
# ----------------

def _shift_char(ch, shift):
    """Lowercase letters get shifted; everything else stays the same."""
    if ch.isalpha():
        base = ch.lower()
        idx = ord(base) - ord('a')
        return chr(ord('a') + (idx + shift) % 26)
    return ch

def encode(input_text, shift):
    """
    Return (alphabet_list, encoded_text)
    - letters -> lowercase + shifted
    - non-letters unchanged
    - None treated as empty string
    """
    if input_text is None:
        input_text = ""
    alphabet = list(string.ascii_lowercase)
    encoded = "".join(_shift_char(c, shift) for c in input_text)
    return alphabet, encoded

def decode(input_text, shift):
    """Reverse of encode: shift backwards."""
    if input_text is None:
        return ""
    decoded = "".join(_shift_char(c, -shift) for c in input_text)
    return decoded


#BANK ACCOUNTS

def _normalize_date(value):
    """
    Accepts: datetime.date, (year, month, day) tuple, or None (-> today).
    Raises if invalid or in the future.
    """
    if value is None:
        d = datetime.date.today()
    elif isinstance(value, tuple):
        d = datetime.date(*value)
    elif isinstance(value, datetime.date):
        d = value
    else:
        raise Exception("creation_date must be a date or (y,m,d) tuple")
    if d > datetime.date.today():
        raise Exception("creation_date cannot be in the future")
    return d

class BankAccount:
    def __init__(self, name="Rainy", ID="1234", creation_date=None, balance=0):
        self.name = name
        self.ID = ID
        self.creation_date = _normalize_date(creation_date)
        self.balance = balance

    def deposit(self, amount):
        # Negative deposits are ignored (leave balance unchanged).
        if amount < 0:
            return self.balance
        self.balance += amount
        return self.balance

    def withdraw(self, amount):
        # No overdraft; ignore if amount exceeds balance.
        if amount < 0:
            raise Exception("cannot withdraw negative amount")
        if amount > self.balance:
            return self.balance
        self.balance -= amount
        return self.balance

    def view_balance(self):
        return self.balance

class SavingsAccount(BankAccount):
    def withdraw(self, amount):
        # Only allow if account is at least 180 days old and no overdraft.
        age_days = (datetime.date.today() - self.creation_date).days
        if age_days < 180:
            return self.balance
        if amount > self.balance or amount < 0:
            return self.balance
        self.balance -= amount
        return self.balance

class CheckingAccount(BankAccount):
    def withdraw(self, amount):
        # Allow overdraft; if it goes negative, charge $30 fee.
        if amount < 0:
            raise Exception("cannot withdraw negative amount")
        self.balance -= amount
        if self.balance < 0:
            self.balance -= 30
        return self.balance

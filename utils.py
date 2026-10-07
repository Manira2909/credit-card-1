from cryptography.fernet import Fernet
import os

# .env file la vechuko - Production ku must
# FERNET_KEY=b'YWRzZmFzZGZhc2RmYXNkZmFzZGZhc2RmYXNkZmFzZA=='
FERNET_KEY = os.getenv('FERNET_KEY', Fernet.generate_key())

try:
    fernet = Fernet(FERNET_KEY)
except Exception as e:
    print(f"Invalid Key. Generating new one: {e}")
    FERNET_KEY = Fernet.generate_key()
    fernet = Fernet(FERNET_KEY)

def encrypt_card(number: str) -> str:
    """Card number ah encrypt pannum. DB la mattum store pannu"""
    return fernet.encrypt(str(number).encode()).decode()

def decrypt_card(token: str) -> str:
    """Payment podumbodhu mattum decrypt pannu"""
    return fernet.decrypt(token.encode()).decode()

def luhn_check(card_num: str) -> bool:
    """Credit card valid ah nu check pannum - Luhn algo"""
    card_num = ''.join(filter(str.isdigit, card_num)) # spaces remove
    if not card_num:
        return False
        
    digits = [int(d) for d in card_num]
    odd_digits = digits[-1::-2]
    even_digits = digits[-2::-2]
    checksum = sum(odd_digits)
    for d in even_digits:
        checksum += sum([int(x) for x in str(d*2)])
    return checksum % 10 == 0
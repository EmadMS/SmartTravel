import secrets


secret_key = secrets.token_hex(16)  # 16 bytes = 32 characters
print("Generated Secret Key:", secret_key)
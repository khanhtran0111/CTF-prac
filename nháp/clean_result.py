#!/usr/bin/env python3

# Cleaned up result from the attack
decoded_message = "The secuet messagedis: Wht! using a stream cipher, never use the key more than once"

# Fix obvious typos
clean_message = decoded_message.replace("secuet", "secret").replace("messagedis:", "message is:").replace("Wht!", "When")

print("Raw decoded message:")
print(f"'{decoded_message}'")
print()
print("Cleaned message:")
print(f"'{clean_message}'")
print()

# Extract just the secret message part
if ": " in clean_message:
    secret_part = clean_message.split(": ", 1)[1]
    print("Secret message only:")
    print(f"'{secret_part}'")
else:
    print("Full message is the secret:")
    print(f"'{clean_message}'")
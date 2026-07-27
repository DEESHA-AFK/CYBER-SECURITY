import hmac
import hashlib

print("Name: Deesha Chavan")
print("Practical: Message Authentication Code (MAC)\n")

# Shared secret key
secret_key = b"mysecretkey"

# Sender Side
message = input("Enter the message: ")

generated_mac = hmac.new(
    secret_key,
    message.encode(),
    hashlib.sha256
).hexdigest()

print("\nGenerated MAC:", generated_mac)

print("\n Verification")

# Receiver Side
received_message = input("Enter the received message: ")

calculated_mac = hmac.new(
    secret_key,
    received_message.encode(),
    hashlib.sha256
).hexdigest()

print("Calculated MAC:", calculated_mac)

# Compare generated and calculated MAC
if hmac.compare_digest(generated_mac, calculated_mac):
    print("\nMessage Verified Successfully!")
    print("Data Integrity Maintained.")
    print("Sender is Authentic.")
else:
    print("\nVerification Failed!")
    print("Message has been Modified.")

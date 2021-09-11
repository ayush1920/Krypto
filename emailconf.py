import smtplib, ssl

smtp_server = "smtp.gmail.com"
port = 587  # For starttls
# Create a secure SSL context
context = ssl.create_default_context()

def init(sender_email, password):
    # Try to log in to server and send email
    server = smtplib.SMTP(smtp_server,port)
    server.ehlo() # Can be omitted
    server.starttls(context=context) # Secure the connection
    server.ehlo() # Can be omitted
    server.login(sender_email, password)
    return server

import imaplib
import email
import re
from email.header import decode_header
from playwright.sync_api import sync_playwright
import time

imap_server, port = "imap.gmail.com", 993
email_address = "maximistr100@gmail.com"
password = "gwih vzow qpqy tnvq"
verification_code = None

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    page = browser.new_page()
    page.goto("https://store.supercell.com/brawlstars")
    time.sleep(2)
    # .all() converts the locator group into a Python list of individual elements
    page.get_by_role("button", name="Accept All Cookies").click()
    time.sleep(1)
    # Looks for any link tag where the class name starts with 'LoginButton_LoginButton'
    page.locator("a[class^='LoginButton_LoginButton']").first.click()
    time.sleep(1)
    page.locator("input[name='email']").fill(email_address)
    page.get_by_role("button", name="Log in").click()
    
    time.sleep(10)  # Wait for the email to arrive and be processed

    try:
        print("Connecting to the mailbox...")
        mail = imaplib.IMAP4_SSL(imap_server, port)
        mail.login(email_address, password)
        mail.select("INBOX")
        
        status, data = mail.search(None, "ALL")
        mail_ids = data[0].split()[-5:]
        
        for mail_id in reversed(mail_ids):
            status, message_data = mail.fetch(mail_id, "(RFC822)")
            for response_part in message_data:
                if isinstance(response_part, tuple):
                    msg = email.message_from_bytes(response_part[1])
                    from_sender = decode_header(msg["From"])[0][0]
                    from_sender = from_sender.decode() if isinstance(from_sender, bytes) else from_sender

                    if "Supercell" in from_sender and "noreply@id.supercell.com" in from_sender:
                        subject = decode_header(msg["Subject"])[0][0]
                        subject = subject.decode() if isinstance(subject, bytes) else subject
                        verification_code = re.sub(r'\s+', '', re.search(r'\[([^\]]+)\]', subject).group(1))
                        break
        mail.close()
        mail.logout()
        print(f"Verification code: {verification_code}")
        
    except Exception as e:
        print(f"Error: {e}")
        
    if verification_code:
        page.locator("input[name='pin']").fill(verification_code)
        page.get_by_role("button", name="Continue").click()
        time.sleep(5)

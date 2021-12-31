import smtplib

# Begin Email Script
def sendEmail(dict, titleKey, priceKey, linkKey, buyItNowKey):

    gmail_user = "blurmcclure16@gmail.com"
    gmail_password = "phbrzyquvzjdgvjw"

    sent_from = gmail_user
    to = "alec.b.mcclure@gmail.com"
    subject = "New Deals Found!"

    msg = []
    for n in dict:
        msg.append("---------------------------------------")
        msg.append(f"Listing: {dict[n][titleKey]}")
        msg.append(f"Price: {dict[n][priceKey]}")
        msg.append(f"Link: {dict[n][linkKey]}")
        msg.append(f"Buy It Now?: {dict[n][buyItNowKey]}")
    msg.append("---------------------------------------")

    mybody = str(msg).replace(",", "\n").strip("[").strip("]").replace("'", "")

    email_text = f"Subject: {subject} \n\n {mybody}"

    try:
        server = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        server.ehlo()
        server.login(gmail_user, gmail_password)
        server.sendmail(sent_from, to, email_text)
        server.close()
        print("Email sent!")
    except:
        print("Something went wrong...")

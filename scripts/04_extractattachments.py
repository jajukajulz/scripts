import email
import os

path = './'
listing = os.listdir(path)

for fle in listing:
    if str.lower(fle[-3:]) == "eml":
        msg = email.message_from_file(open(fle))
        attachments = msg.get_payload()
        for attachment in attachments:
            try:
                fnam = attachment.get_filename()
                f = open(fnam, 'wb').write(attachment.get_payload(decode=True, ))
                f.close()
            except Exception as detail:
                # print detail
                pass

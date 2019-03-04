import email
import os


#path = './eml'
path = os.path.abspath('./eml')
listing = os.listdir(path)
print listing

for fle in listing:
    if str.lower(fle[-3:])=="eml":
        fle = os.path.join(path, fle)
        print fle
        msg = email.message_from_file(open(fle))
        attachments=msg.get_payload()
        for attachment in attachments:
            try:
                fnam=attachment.get_filename()
                f=open(fnam, 'wb').write(attachment.get_payload(decode=True,))
                f.close()
            except Exception as detail:
                #print detail
                pass
        email_from = msg['from']
        email_to = msg['to']
        # print 'email_from %s email to %s' % (email_from, email_to)
        # email_body
        if msg.is_multipart():
            for payload in msg.get_payload():
                # if payload.is_multipart(): ...
                print "multipart payload"
                print payload.get_payload()
        else:
            # print "non multipart payload"
            email_body = msg.get_payload().strip().decode('utf8')
            #string.split(email_body, '\n')
            #email_body.splitlines()
            #print email_body

        #string matching
        for line in email_body.splitlines():
            #print line
            if "Email :" in line: print line # you can slice the string to display only after email :
            if "first_name :" in line: print line
            if "family_name :" in line: print line
            if "checkbox_yes :" in line: print line
            # example contents of eml file:
            #Email : <email_address>@gmail.com
            #checkbox_yes : checkbox_yes
            #
            # family_name : <email_sender_surname>
            #
            # first_name : <email_sender_name>


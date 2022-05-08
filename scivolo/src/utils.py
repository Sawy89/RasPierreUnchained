import smtplib
from os.path import basename
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.utils import COMMASPACE, formatdate
from settings import EMAIL_HOST, EMAIL_HOST_USER, EMAIL_HOST_PASSWORD


def send_mail(send_to, subject, text, files=None, inline_images_list=None, server=EMAIL_HOST, mailType=None,
                  send_to_cc=None, send_to_bcc=None, send_from=EMAIL_HOST_USER):
    '''
    funzione per inviare MAIL
    INPUT: send_to come lista delle mail dei ricevitori
           subject = oggetto, text = corpo della mail
           files come lista degli allegati (se presente)
           mailType = indica se in formato testo (default) o 'HTML'
           send_to_cc e send_to_bcc sono liste con gli indirizzi mail da inserire
               (se presenti) in CC e BCC (copia nascosta)   
               
    To add inline image, within the html text, write an html like 
    <img src="cid:image1"> for each image, where image1 is the image at 
    position 1 in inline_images_list (keep calling them image1, image2,...)
    '''
    assert isinstance(send_to, list)
    send_to_all = send_to.copy() # copia per evitare di modificare la lista globale
        
    # Info mail (quelle mostrate nell'header)
    msg = MIMEMultipart('related')
    msg['From'] = send_from
    msg['To'] = COMMASPACE.join(send_to)
    msg['Date'] = formatdate(localtime=True)
    msg['Subject'] = subject
    
    # Add CC
    if send_to_cc != None:
        assert isinstance(send_to_cc, list)
        msg['Cc'] = COMMASPACE.join(send_to_cc) # header della mail
        send_to_all += send_to_cc # a chi la invia
    
    # Add BCC (nascosto) --> solo nella lista degli invii!
    if send_to_bcc != None:
        assert isinstance(send_to_bcc, list)
        send_to_all += send_to_bcc # a chi la invia
    
    # Differenze per tipo mail
    if mailType is not None and mailType == 'HTML':
        text = text.replace('\n\n','<br><br>')
        msg.attach(MIMEText(text,'HTML'))
    else:
        msg.attach(MIMEText(text))
    
    # Allegati
    for f in files or []:
        with open(f, "rb") as fil:
            part = MIMEApplication(
                fil.read(),
                Name=basename(f)
            )
        # After the file is closed
        part['Content-Disposition'] = 'attachment; filename="%s"' % basename(f)
        msg.attach(part)
    
    # Immagini inlinea
    for i,img in enumerate(inline_images_list or []) :
        image = open(img, 'rb').read()
        msgImg = MIMEImage(image, 'png')
        msgImg.add_header('Content-ID', '<image{}>'.format(i+1))
        msgImg.add_header('Content-Disposition', 'inline', filename=img)
            
    if inline_images_list:
        msg.attach(msgImg)
    
    # SEND MAIL
    smtp = smtplib.SMTP(server)
    smtp.starttls()
    smtp.login(EMAIL_HOST_USER, EMAIL_HOST_PASSWORD)
    smtp.sendmail(send_from, send_to_all, msg.as_string())
    smtp.quit()
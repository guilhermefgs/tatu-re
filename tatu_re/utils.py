import yfinance as yf

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


def get_data(start, end,ticker):
    """
    dateStart, dateStop: date start and end in string YYYY-MM-DD or datetime format
    """
    spyticker = yf.Ticker(ticker)
    return spyticker.history(period="max", interval="1d", 
                                   start=start, end=end, 
                                   auto_adjust=True, rounding=True)

def send_email(df, action, amount):
    vetor_nomes=df['Nome']
    vetor_email=df['Email']
    amount = amount if isinstance(amount, str) else str(amount)
    
    length=len(vetor_email)
    print('The number of contacts in the list is:', length)
    
    for i in range(0,length):
        
        print('Sending to contact: ', i)
        print('The name of the contact is: ',vetor_nomes[i])
        
        sender_email='christianleomil@gmail.com'
        rec_email= vetor_email[i]
        password='dvzbiujaunitykrt'
        
        mail_content ='<p>Hello'+' '+vetor_nomes[i]+','+'<p>We are contacting you to give you a daily recommendation based on the latest trends for your SPDR S&amp;P 500 ETF investment. <strong>The recommendation for the day is as follows:</strong></p><ul><li>Action: '+action+'</li><li>Amount: '+amount+'</li></ul><p><strong>Important Trends:</strong></p><p>The stock is in a medium-intensity uptrend and is forecast to stay that way.</p><p>If you have any questions, please contact us at <a href="mailto:contatct@tature.com">contatct@tature.com</a> or through your account on the chat at www.tature.com</p><p>Team Tatu RE</p>'
        
        message = MIMEMultipart()
        
        message['From'] = 'christianleomil@gmail.com'
        message['To'] = rec_email
        message['Subject'] = 'Tatu RE Daily Email – Application: SPDR S&P 500 ETF'
        message['Reply-to'] = 'christianleomil@gmail.com,rodmorais@uso.com.br,caiofreitas@usp.br,aateg29@gmail.com'
        
        message.attach(MIMEText(mail_content, 'html'))
        text=message.as_string()
        
        server=smtplib.SMTP('smtp.gmail.com',587)
        server.starttls()
        server.login(sender_email,password)
        print('Login Success')
        server.sendmail(sender_email,rec_email,text)
        print('Email has been sent')
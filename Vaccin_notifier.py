import email
import smtplib
from datetime import datetime
import time
from win10toast import ToastNotifier
import requests 

n = ToastNotifier()
  

def create_session_info(center, session):
    return {"name": center["name"],
            "date": session["date"],
            "capacity": session["available_capacity"],
             "age_limit": session["min_age_limit"]
            #, "fee_type":session['fee_type']
            }

def get_sessions(data):
    for center in data["centers"]:
        if (center["fee_type"]=="Free"):
            for session in center["sessions"]:
                if  session["available_capacity_dose1"]>0:
                    yield create_session_info(center, session)

def is_available(session):
    return session["capacity"] > 0

def is_eighteen_plus(session):
    return session["age_limit"] == 18


def get_for_seven_days(start_date):
    url = "https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByDistrict"
    para = {"district_id": 307, "date": start_date.strftime("%d-%m-%Y")}
    resp = requests.get(url, params=para)
    data = resp.json()

    #571,154

    #print(data['centers'][0])
    # print(data)
    return [session for session in get_sessions(data) if is_eighteen_plus(session) and is_available(session)]
    #and is_free(session)
def create_output(session_info):
    return f"{session_info['date']} - {session_info['name']} ({session_info['capacity']})"
while(1):   
    

    content = "\n".join([create_output(session_info) for session_info in get_for_seven_days(datetime.today())])
    #content.replace("'","\"")

    username = "gmail you want to set mail" 
    password = "password"

    if not content:
        print("No availability")
        time.sleep(15)
    else:
        email_msg = email.message.EmailMessage()
        email_msg["Subject"] = "Vaccination Slot Open"
        email_msg["From"] = username
        email_msg["To"] = username
        email_msg.set_content(content)
        print("\n\n\n\n")
        print(content)
        with smtplib.SMTP(host='smtp.gmail.com', port='587') as server:
            server.starttls()
            server.login(username, password)
            server.send_message(email_msg, username, username)
            n.show_toast("Vaccin",content, duration = 10)
            print("\n\n\n\n")
            time.sleep(5)
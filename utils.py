import pyttsx3

def style_risk(status):
    if status == "High Risk":
        return f"<span style='color:red;font-weight:bold'>{status}</span>"
    elif status == "Medium Risk":
        return f"<span style='color:orange'>{status}</span>"
    else:
        return f"<span style='color:green'>{status}</span>"

def speak_alert(text):
    try:
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
    except:
        pass

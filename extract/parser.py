def get_sample_sms():
    return [
        {"Sender": "Mom", "Message": "Call me", "Timestamp": "2025-05-20 10:35"},
        {"Sender": "Bank", "Message": "Your OTP is 4567", "Timestamp": "2025-05-20 11:00"},
        {"Sender": "Friend", "Message": "Let's meet for payment tomorrow", "Timestamp": "2025-05-19 15:42"}
    ]

def get_sample_call_logs():
    return [
        {"Name": "Dad", "Type": "Incoming", "Time": "2025-05-19 09:00"},
        {"Name": "Friend", "Type": "Missed", "Time": "2025-05-18 14:20"}
    ]

def filter_messages_by_keyword(messages, keyword):
    return [msg for msg in messages if keyword.lower() in msg['Message'].lower()]

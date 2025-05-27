import subprocess
import os

def get_real_sms():
    try:
        result = subprocess.run(
            ["adb", "shell", "content", "query", "--uri", "content://sms"],
            capture_output=True,
            text=True
        )
        messages = []
        lines = result.stdout.strip().splitlines()
        msg = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Row") and msg:
                messages.append({
                    "ID": msg.get("_id", ""),
                    "Thread ID": msg.get("thread_id", ""),
                    "Address": msg.get("address", ""),
                    "Person": msg.get("person", ""),
                    "Date": msg.get("date", ""),
                    "Date Sent": msg.get("date_sent", ""),
                    "Read": msg.get("read", ""),
                    "Status": msg.get("status", ""),
                    "Type": msg.get("type", ""),
                    "Body": msg.get("body", ""),
                    "Service Center": msg.get("service_center", "")
                })
                msg = {}
                continue
            for pair in line.split(", "):
                if "=" in pair:
                    key, val = pair.split("=", 1)
                    msg[key.strip()] = val.strip()
        if msg:
            messages.append({
                "ID": msg.get("_id", ""),
                "Thread ID": msg.get("thread_id", ""),
                "Address": msg.get("address", ""),
                "Person": msg.get("person", ""),
                "Date": msg.get("date", ""),
                "Date Sent": msg.get("date_sent", ""),
                "Read": msg.get("read", ""),
                "Status": msg.get("status", ""),
                "Type": msg.get("type", ""),
                "Body": msg.get("body", ""),
                "Service Center": msg.get("service_center", "")
            })
        print(f"DEBUG: Parsed {len(messages)} SMS")
        return messages
    except Exception as e:
        print("Error retrieving SMS:", e)
        return []

def get_real_call_logs():
    try:
        result = subprocess.run(
            ["adb", "shell", "content", "query", "--uri", "content://call_log/calls"],
            capture_output=True,
            text=True
        )
        calls = []
        lines = result.stdout.strip().splitlines()
        entry = {}
        for line in lines:
            line = line.strip()
            if not line:
                continue
            if line.startswith("Row") and entry:
                calls.append({
                    "Name": entry.get("name", ""),
                    "Number": entry.get("number", ""),
                    "Type": entry.get("type", ""),
                    "Date": entry.get("date", ""),
                    "Duration": entry.get("duration", "")
                })
                entry = {}
                continue
            for pair in line.split(", "):
                if "=" in pair:
                    key, val = pair.split("=", 1)
                    entry[key.strip()] = val.strip()
        if entry:
            calls.append({
                "Name": entry.get("name", ""),
                "Number": entry.get("number", ""),
                "Type": entry.get("type", ""),
                "Date": entry.get("date", ""),
                "Duration": entry.get("duration", "")
            })
        print(f"DEBUG: Parsed {len(calls)} Call Logs")
        return calls
    except Exception as e:
        print("Error retrieving Call Logs:", e)
        return []

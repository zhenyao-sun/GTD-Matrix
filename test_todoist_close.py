import urllib.request
import json
import os
import time

token = os.environ.get("TODOIST_API_TOKEN")
if not token:
    print("NO_TOKEN")
    exit(1)

# CREATE a recurring task
print("Creating recurring dummy task...")
req = urllib.request.Request(
    "https://api.todoist.com/rest/v2/tasks",
    data=json.dumps({"content": "[DUMMY] Recurring Test", "due_string": "every day"}).encode('utf-8'),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST"
)
try:
    with urllib.request.urlopen(req) as response:
        task = json.loads(response.read().decode())
        task_id = task['id']
        due_date = task['due']['date']
        print(f"Created task {task_id} due on {due_date}")
except Exception as e:
    print("Error creating:", e)
    exit(1)

time.sleep(1)

# CLOSE using api/v1 alias
print("Closing via /api/v1...")
try:
    req_close = urllib.request.Request(
        f"https://api.todoist.com/api/v1/tasks/{task_id}/close",
        headers={"Authorization": f"Bearer {token}"},
        method="POST"
    )
    with urllib.request.urlopen(req_close) as response:
        print("Close Status (api/v1):", response.getcode())
except Exception as e:
    print("Error closing via api/v1:", e)

    # fallback to rest/v2
    print("Falling back to /rest/v2...")
    try:
        req_close2 = urllib.request.Request(
            f"https://api.todoist.com/rest/v2/tasks/{task_id}/close",
            headers={"Authorization": f"Bearer {token}"},
            method="POST"
        )
        with urllib.request.urlopen(req_close2) as response:
            print("Close Status (rest/v2):", response.getcode())
    except Exception as e2:
        print("Error closing via rest/v2:", e2)

time.sleep(1)

# FETCH task again
print("Fetching task to verify due date...")
try:
    req_get = urllib.request.Request(
        f"https://api.todoist.com/rest/v2/tasks/{task_id}",
        headers={"Authorization": f"Bearer {token}"}
    )
    with urllib.request.urlopen(req_get) as response:
        task_after = json.loads(response.read().decode())
        print(f"Task is completed? {task_after.get('is_completed')}")
        new_due = task_after.get('due', {})
        print(f"New due date: {new_due.get('date') if new_due else 'None'}")
except Exception as e:
    print("Error getting task:", e)
    

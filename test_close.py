import urllib.request
import json
import os

token = os.environ.get("TODOIST_API_TOKEN")
if not token:
    print("NO TOKEN")
    exit(1)

# Create a recurring task via REST v2
req = urllib.request.Request(
    "https://api.todoist.com/rest/v2/tasks",
    data=json.dumps({"content": "Test Recurring Task API", "due_string": "every day"}).encode("utf-8"),
    headers={"Authorization": f"Bearer {token}", "Content-Type": "application/json"},
    method="POST"
)
try:
    with urllib.request.urlopen(req) as response:
        task = json.loads(response.read().decode())
        print(f"Created task {task['id']} with due date {task.get('due', {}).get('date')}")
        task_id = task['id']
except Exception as e:
    print(e)
    exit(1)

# Try closing it via the /api/v1 path from index.html
req_close1 = urllib.request.Request(
    f"https://api.todoist.com/api/v1/tasks/{task_id}/close",
    headers={"Authorization": f"Bearer {token}"},
    method="POST"
)
try:
    with urllib.request.urlopen(req_close1) as response:
        print("Closed via /api/v1! Code:", response.getcode())
except Exception as e:
    print("Error closing via /api/v1:", e)


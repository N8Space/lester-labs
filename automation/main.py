import os
import sys
import datetime
import pytz
from dotenv import load_dotenv

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from auth import authenticate_google_services
from gmail_service import GmailService
from tasks_service import TasksService
from calendar_service import CalendarService
from ai_processor import AIProcessor

# Load environment variables
load_dotenv()

# Configuration
USER_TIMEZONE = 'America/Chicago'
ACCOUNTS = [
    {
        "name": "nslpublishing",
        "email": "nslpublishing@gmail.com",
        "token_file": "token_nsl.json",
        "scopes": ["email"]
    },
    {
        "name": "nathan_scott_lester",
        "email": "Nathan.scott.lester@gmail.com",
        "token_file": "token_nathan.json",
        "scopes": ["email", "calendar", "tasks"] # Primary account for tools
    }
]

ARCHIVE_DAYS = 30
TRASH_YEARS = 8
DRY_RUN = False # Set to False to enable actual modification/deletion

def get_datenow_user():
    return datetime.datetime.now(pytz.timezone(USER_TIMEZONE))

def main():
    print(f"--- Starting Email Automation: {datetime.datetime.now()} (Dry Run: {DRY_RUN}) ---")
    
    ai_key = os.getenv("GEMINI_API_KEY")
    if not ai_key:
        print("Error: GEMINI_API_KEY not found in .env")
        return
    ai = AIProcessor(api_key=ai_key, model_name=os.getenv("GEMINI_MODEL", "gemini-1.5-pro"))

    all_summaries = []
    
    # Context Data
    calendar_events = []
    tasks_due = []
    
    total_archived = 0
    total_trashed = 0
    trashed_samples = []
    
    # Timezone aware dates
    now_user = get_datenow_user()
    today_str = now_user.strftime('%Y-%m-%d')
    print(f"User Date: {today_str} ({USER_TIMEZONE})")

    # 1. Process Each Account
    for account in ACCOUNTS:
        print(f"\nProcessing Account: {account['name']} ({account['email']})...")
        
        try:
            creds = authenticate_google_services(token_file=account['token_file'])
            gmail = GmailService(creds)
            
            # --- EMAIL CLEANUP ---
            # Archive > 30 days
            query_archive = f"label:INBOX older_than:{ARCHIVE_DAYS}d"
            msgs_to_archive = gmail.list_messages(query=query_archive, max_results=500)
            if msgs_to_archive:
                print(f"  Found {len(msgs_to_archive)} emails to archive (> {ARCHIVE_DAYS} days).")
                if not DRY_RUN:
                    ids = [m['id'] for m in msgs_to_archive]
                    gmail.batch_modify_messages(ids, remove_labels=['INBOX'])
                    total_archived += len(msgs_to_archive)
                else:
                    print("  [Dry Run] Would archive these messages.")

            # Trash > 8 years
            query_trash = f"older_than:{TRASH_YEARS}y -label:TRASH"
            msgs_to_trash = gmail.list_messages(query=query_trash, max_results=100) # Safety limit
            if msgs_to_trash:
                print(f"  Found {len(msgs_to_trash)} emails to trash (> {TRASH_YEARS} years).")
                for msg in msgs_to_trash:
                    # Get snippet for report before trashing
                    m = gmail.get_message(msg['id'])
                    if m:
                        snippet = m.get('snippet', '')
                        headers = m['payload']['headers']
                        subj = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
                        if len(trashed_samples) < 5: # Keep a few samples
                            trashed_samples.append(f"{subj} - {snippet[:50]}...")
                            
                if not DRY_RUN:
                    ids = [m['id'] for m in msgs_to_trash]
                    gmail.batch_trash_messages(ids)
                    total_trashed += len(msgs_to_trash)
                else:
                    print("  [Dry Run] Would trash these messages.")


            # --- DAILY INBOX PROCESSING ---
            # Fetch Unread or Recent
            recent_msgs = gmail.list_messages(query='is:unread -category:promotions -category:social', max_results=20)
            print(f"  Found {len(recent_msgs)} unread emails to analyze.")
            
            for msg in recent_msgs:
                full_msg = gmail.get_message(msg['id'])
                if not full_msg: continue
                
                headers = full_msg['payload']['headers']
                subject = next((h['value'] for h in headers if h['name'] == 'Subject'), '(No Subject)')
                sender = next((h['value'] for h in headers if h['name'] == 'From'), '(Unknown)')
                
                # Recipients (To, Cc)
                to_list = next((h['value'] for h in headers if h['name'] == 'To'), '')
                cc_list = next((h['value'] for h in headers if h['name'] == 'Cc'), '')
                recipients = f"{to_list}, {cc_list}"

                print(f"  Analyzing: {subject[:40]}...")
                body = gmail.get_message_body(full_msg)
                
                analysis = ai.analyze_email(sender, subject, body, recipients=recipients)
                
                category = analysis.get('category', 'REFERENCE')
                summary = analysis.get('summary', '')
                action_item = analysis.get('action_item')
                suggested_reply = analysis.get('suggested_reply')
                
                # Store for Digest
                all_summaries.append({
                    "account": account['name'],
                    "sender": sender,
                    "subject": subject,
                    "category": category,
                    "summary": summary,
                    "action": action_item
                })
                
                if not DRY_RUN:
                    # Action: Add Task
                    if 'tasks' in account['scopes'] and category in ['DO', 'DEFER'] and action_item:
                         tasks_svc = TasksService(creds)
                         task_title = f"[{category}] {action_item}"
                         notes = f"Source: {subject} ({sender})\nSummary: {summary}"
                         tasks_svc.create_task(tasklist_id='@default', title=task_title, notes=notes)
                    
                    # Action: Draft Reply
                    if suggested_reply:
                        print("    -> Creating draft reply.")
                        gmail.create_draft(to=sender, subject=f"Re: {subject}", body=suggested_reply)
            
            # --- ACCOUNT SPECIFIC FETICHING ---
            if "calendar" in account['scopes']:
                cal = CalendarService(creds, timezone=USER_TIMEZONE)
                print("  Fetching Calendar events...")
                # Calendar Service now handles timezone internally
                events = cal.get_todays_events()
                for e in events:
                    start = e['start'].get('dateTime', e['start'].get('date'))
                    summary = e.get('summary', '(No Title)')
                    calendar_events.append(f"{start}: {summary}")
                    
            if "tasks" in account['scopes']:
                tasks_svc = TasksService(creds)
                print("  Fetching Tasks due today/tomorrow...")
                # Due Today or Tomorrow
                # Google Tasks API 'due' is RFC3339 timestamp.
                # 'list' supports 'dueMin', 'dueMax'.
                
                # Range: Start of Today to End of Tomorrow (User Time)
                task_start = now_user.replace(hour=0, minute=0, second=0, microsecond=0)
                task_end = task_start + datetime.timedelta(days=2) # End of tomorrow (start of day after)
                
                # Convert to UTC ISO
                due_min = task_start.astimezone(pytz.utc).isoformat()
                due_max = task_end.astimezone(pytz.utc).isoformat()
                
                # Actually, tasks might use explicit date string or UTC.
                # Let's try listing without filter first if API is tricky, but passing bounds is better.
                t_items = tasks_svc.list_tasks(due_min=due_min, due_max=due_max)
                
                for t in t_items:
                    due = t.get('due', '')
                    title = t.get('title', 'Unknown Task')
                    tasks_due.append(f"{title} (Due: {due})")

        except Exception as e:
            print(f"Error processing account {account['name']}: {e}")
            import traceback
            traceback.print_exc()

    # 2. Generate Digest
    if all_summaries or calendar_events or tasks_due:
        print("\nGenerating Daily Executive Briefing...")
        digest_html = ai.generate_daily_digest(
            all_summaries, 
            calendar_events, 
            tasks_due, 
            total_archived, 
            total_trashed, 
            trashed_samples,
            report_date=today_str
        )
        
        # 3. Send Digest to Primary Account
        primary_account = next((a for a in ACCOUNTS if a['name'] == 'nathan_scott_lester'), None)
        if primary_account:
            try:
                creds = authenticate_google_services(token_file=primary_account['token_file'])
                gmail = GmailService(creds)
                if not DRY_RUN:
                    print("Sending Digest Email...")
                    gmail.send_message(
                        to=primary_account['email'], 
                        subject=f"Daily Executive Briefing - {today_str}", 
                        body=digest_html, 
                        importance='high'
                    )
                else:
                    print("--- [Dry Run] Digest HTML Content ---")
                    with open("dry_run_digest.html", "w", encoding='utf-8') as f:
                        f.write(digest_html)
                    print("Saved digest to dry_run_digest.html")
            except Exception as e:
                print(f"Error sending digest: {e}")
                
    print("\n--- Job Complete ---")

if __name__ == "__main__":
    main()

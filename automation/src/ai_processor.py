import os
from google import genai
from google.genai import types
import json
from datetime import datetime

class AIProcessor:
    def __init__(self, api_key, model_name='gemini-1.5-pro'):
        self.client = genai.Client(api_key=api_key)
        self.model_name = model_name

    def analyze_email(self, sender, subject, body, recipients=None):
        """
        Analyzes an email to determine the GTD action and generate a summary.
        """
        # Determine if direct email (heuristic: if 'me' is in recipients, or specific checks handled by caller)
        # We'll pass recipients list to helper.
        
        prompt = f"""
        You are a personal executive assistant.
        Analyze the following email.

        Sender: {sender}
        Recipients: {recipients}
        Subject: {subject}
        Body:
        {body[:3000]}

        1. Categorize:
        - DO: Urgent/Action required.
        - DEFER: Action needed later.
        - DELEGATE: Someone else handling.
        - DELETE: Spam/Promo.
        - REFERENCE: Informational.

        2. Draft Reply:
        If the email is sent DIRECTLY to users (nslpublishing@gmail.com or Nathan.scott.lester@gmail.com) AND is important/professional, draft a professional reply.
        Do NOT draft for newsletters, automated notifications, or clear promotions.

        Output JSON:
        {{
            "category": "DO" | "DEFER" | "DELEGATE" | "DELETE" | "REFERENCE",
            "summary": "One sentence summary",
            "importance": "high" | "normal" | "low",
            "action_item": "Task description if DO/DEFER",
            "suggested_reply": "Draft reply text (or null)"
        }}
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt,
                config=types.GenerateContentConfig(
                    response_mime_type="application/json"
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"AI Error: {e}")
            return {
                "category": "REFERENCE",
                "summary": "Error analyzing email",
                "importance": "normal",
                "action_item": None,
                "suggested_reply": None
            }

    def generate_daily_digest(self, summaries, calendar_events, tasks, archived_count, trashed_count, trashed_samples, report_date=None):
        """
        Generates a daily digest email body.
        """
        if not report_date:
            report_date = datetime.date.today().isoformat()

        prompt = f"""
        Create a 'Daily Executive Briefing' HTML email.
        
        Data:
        1. Emails Analyzed: {len(summaries)}
        2. Calendar Events (Today): {json.dumps(calendar_events)}
        3. Tasks (Due Today/Tmrw): {json.dumps(tasks)}
        4. Archived Emails (Old > 30d): {archived_count}
        5. Deleted Emails (Old > 8y): {trashed_count}
        6. Notable Deleted Samples: {json.dumps(trashed_samples)}
        7. Email Analysis: {json.dumps(summaries)}

        Format requirements:
        <h1>Daily Executive Briefing - {report_date}</h1>

        <h2>1) Action Required (Urgent)</h2>
        - List high importance items / safety / alerts from emails.

        <h2>2) Due today / tomorrow</h2>
        - List Calendar events and Tasks.

        <h2>3) For your review (To-Do)</h2>
        - Summary of tasks identified from daily emails (Category DO/DEFER).

        <h2>4) FYI, Reference</h2>
        - Summary of informative emails.

        <h2>5) Archived</h2>
        - "Archived {archived_count} emails older than 30 days."

        <h2>6) Deleted</h2>
        - "Moved {trashed_count} emails older than 8 years to Trash."
        - Bullet list of potentially important trashed items from 'Notable Deleted Samples' (if any).

        Output ONLY clean HTML (no markdown fence).
        """
        
        try:
            response = self.client.models.generate_content(
                model=self.model_name,
                contents=prompt
            )
            text = response.text
            # Strip markdown
            if text.startswith("```html"): text = text[7:]
            if text.startswith("```"): text = text[3:]
            if text.endswith("```"): text = text[:-3]
            return text.strip()
        except Exception as e:
            return f"Error generating digest: {e}"

from googleapiclient.discovery import build
import base64
from bs4 import BeautifulSoup

class GmailService:
    def __init__(self, credentials):
        self.service = build('gmail', 'v1', credentials=credentials)

    def list_messages(self, query='is:unread', max_results=50):
        """List Messages matching the specified query."""
        try:
            results = self.service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
            messages = results.get('messages', [])
            return messages
        except Exception as error:
            print(f'An error occurred: {error}')
            return []

    def get_message(self, msg_id):
        """Get a Message with given ID."""
        try:
            message = self.service.users().messages().get(userId='me', id=msg_id, format='full').execute()
            return message
        except Exception as error:
            print(f'An error occurred: {error}')
            return None

    def get_message_body(self, message):
        """Extracts the body of the email."""
        try:
            if 'payload' not in message:
                return ""
            payload = message['payload']
            parts = payload.get('parts')
            data = ""
            
            if parts:
                for part in parts:
                    if part['mimeType'] == 'text/plain':
                        data = part['body']['data']
                    elif part['mimeType'] == 'text/html':
                         # Prefer plain text if available, or fetch html to strip
                         data = part['body']['data']
            else:
                body = payload.get('body')
                data = body.get('data')

            if data:
                text = base64.urlsafe_b64decode(data).decode()
                # Simple HTML strip if it looks like HTML
                if "<html" in text.lower() or "<div" in text.lower():
                     soup = BeautifulSoup(text, 'html.parser')
                     return soup.get_text()
                return text
            return ""
        except Exception as error:
             print(f"Error parse body: {error}")
             return ""


    def send_message(self, to, subject, body, importance='normal'):
        """Send an email."""
        try:
            message = {
                'raw': self._create_message(to, subject, body, importance)
            }
            sent_message = self.service.users().messages().send(userId='me', body=message).execute()
            print(f'Message sent: {sent_message["id"]}')
            return sent_message
        except Exception as error:
            print(f'An error occurred: {error}')
            return None

    def create_draft(self, to, subject, body):
        """Create a draft email."""
        try:
            message = {
                'message': {
                    'raw': self._create_message(to, subject, body)
                }
            }
            draft = self.service.users().drafts().create(userId='me', body=message).execute()
            print(f'Draft id: {draft["id"]} created.')
            return draft
        except Exception as error:
            print(f'An error occurred: {error}')
            return None
    
    def _create_message(self, to, subject, message_text, importance='normal'):
        """Create a message for an email."""
        from email.mime.text import MIMEText
        import base64

        message = MIMEText(message_text, 'html')
        message['to'] = to
        message['from'] = 'me'
        message['subject'] = subject
        if importance.lower() == 'high':
            message['Importance'] = 'High'
            message['X-Priority'] = '1' # High priority
        
        return base64.urlsafe_b64encode(message.as_bytes()).decode()

    def modify_message(self, msg_id, add_labels=[], remove_labels=[]):
         """Modify the labels of a message."""
         try:
            message = self.service.users().messages().modify(userId='me', id=msg_id,
                                                    body={'addLabelIds': add_labels, 'removeLabelIds': remove_labels}).execute()
            return message
         except Exception as error:
            print(f'An error occurred: {error}')
            return None

    def trash_message(self, msg_id):
        """Moves a message to the trash."""
        try:
            self.service.users().messages().trash(userId='me', id=msg_id).execute()
            return True
        except Exception as error:
            print(f'An error occurred trashing message {msg_id}: {error}')
            return False

    def batch_modify_messages(self, msg_ids, add_labels=[], remove_labels=[]):
        """Batch modify labels for multiple messages."""
        if not msg_ids:
            return None
        try:
            body = {
                'ids': msg_ids,
                'addLabelIds': add_labels,
                'removeLabelIds': remove_labels
            }
            self.service.users().messages().batchModify(userId='me', body=body).execute()
            return True
        except Exception as error:
            print(f'An error occurred in batch modify: {error}')
            return False

    def batch_trash_messages(self, msg_ids):
        """Moves multiple messages to trash (looping, as batch operations for trash are limited)."""
        if not msg_ids:
            return
        
        # Consider using a BatchHttpRequest if performance is critical, but simple loop for now
        count = 0
        for msg_id in msg_ids:
            if self.trash_message(msg_id):
                count += 1
        print(f"Trashed {count} messages.")


from googleapiclient.discovery import build

class TasksService:
    def __init__(self, credentials):
        self.service = build('tasks', 'v1', credentials=credentials)

    def list_tasklists(self):
        """Returns a list of task lists."""
        results = self.service.tasklists().list(maxResults=10).execute()
        return results.get('items', [])

    def create_task(self, tasklist_id, title, notes=None, due=None):
        """Creates a new task on the specified task list."""
        task = {
            'title': title,
            'notes': notes,
            'due': due # RFC 3339 timestamp
        }
        result = self.service.tasks().insert(tasklist='@default', body=task).execute()
        print(f"Task created: {result['title']}")
        return result

    def list_tasks(self, due_min=None, due_max=None):
        """Lists tasks, optionally filtering by due date."""
        try:
            # Note: The 'dueMin' and 'dueMax' parameters in tasks API filter by *completed* date usually or require showCompleted=true?
            # Actually, standard list() filters: 'dueMin', 'dueMax'.
            # These are for the *due* date.
            
            kwargs = {'tasklist': '@default', 'showCompleted': False, 'maxResults': 50}
            if due_min:
                kwargs['dueMin'] = due_min
            if due_max:
                kwargs['dueMax'] = due_max
                
            results = self.service.tasks().list(**kwargs).execute()
            return results.get('items', [])
        except Exception as error:
            print(f'Tasks Error: {error}')
            return []


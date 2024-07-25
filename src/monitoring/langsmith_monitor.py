from langsmith import Client

class LangSmithMonitor:
    def __init__(self):
        self.client = Client()

    def generate_report(self, start_date, end_date):
        runs = self.client.list_runs(
            start_time=start_date,
            end_time=end_date,
            project_name="dream_interpreter"  # Make sure this matches your project name
        )
        
        total_runs = len(list(runs))
        return f"Total runs between {start_date} and {end_date}: {total_runs}"
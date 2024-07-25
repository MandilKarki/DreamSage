from src.rag.dream_interpreter import DreamInterpreter
from src.monitoring.langsmith_monitor import LangSmithMonitor

class DreamInterpreterApp:
    def __init__(self):
        print("Initializing DreamInterpreterApp...")
        self.interpreter = DreamInterpreter()
        self.monitor = LangSmithMonitor()
        print("DreamInterpreterApp initialized.")

    def run_interactive(self):
        print("Starting interactive session...")
        self.interpreter.run_interactive_session()

    def run_monitoring(self, start_date, end_date):
        print(f"Running monitoring for period: {start_date} to {end_date}")
        report = self.monitor.generate_report(start_date, end_date)
        print(report)

def main():
    print("Starting main function...")
    app = DreamInterpreterApp()
    
    while True:
        print("\nMain Menu:")
        choice = input("Choose an option:\n1. Interpret Dreams\n2. View Monitoring Report\n3. Quit\n")
        if choice == '1':
            app.run_interactive()
        elif choice == '2':
            start_date = input("Enter start date (YYYY-MM-DD): ")
            end_date = input("Enter end date (YYYY-MM-DD): ")
            app.run_monitoring(start_date, end_date)
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    print("Script started.")
    main()
    print("Script ended.")
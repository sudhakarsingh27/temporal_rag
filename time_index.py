from llama_index import BaseIndex
from datetime import datetime

class TimeBasedIndex(BaseIndex):
    def __init__(self, documents):
        super().__init__(documents)
        self.time_index = {
            datetime.strptime(doc.metadata["date"], "%Y-%m-%d"): doc
            for doc in documents
        }
        self.sorted_dates = sorted(self.time_index.keys())

    def get_events_in_range(self, start_date, end_date):
        return [
            self.time_index[date] for date in self.sorted_dates
            if start_date <= date <= end_date
        ]

# Create a custom time-based index
time_index = TimeBasedIndex(documents)

# Query events in a date range
start_date = datetime.strptime("2025-01-01", "%Y-%m-%d")
end_date = datetime.strptime("2025-01-31", "%Y-%m-%d")
filtered_docs = time_index.get_events_in_range(start_date, end_date)

# Print results
for doc in filtered_docs:
    print(f"Date: {doc.metadata['date']}, Event: {doc.text}")
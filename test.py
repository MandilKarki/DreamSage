from faker import Faker
import pandas as pd

# Initialize Faker
fake = Faker()

# Define the core columns and their possible values
core_columns_and_values = {
    "AI/Gen AI Capabilities": ["Yes", "No"],
    "SaaS Existence": ["SaaS Alone", "SaaS ↔ SaaS"],
    "Key": ["AWS Key Management Service", "Azure Key Vault", "Bring Your Own Key", "Not Using"],
    "Secret Management": ["AWS SSM", "Azure Key Vault", "Encrypted", "Not Encrypted", "Non-Standard"],
    "Data Exchange Type": ["SaaS → Bank", "SaaS ↔ SaaS"],
    "Access": ["SP-Initiated", "IDP-Initiated", "On-Premise", "Federated Identity to SaaS Access"],
    "Data Classification": ["Restricted", "Sensitive", "Confidential", "Internal", "Public"],
    "Cryptography Techniques": ["Retired", "Forbidden", "Core", "Specialized", "Declined", "Emerging"],
    "Integration Type": ["API Only", "API & UI", "UI Only", "SSO with User ID", 
                         "SSO with SaaS User ID", "SSO with Third Party", "File Transfer", "E-Messaging"],
    "Location and Regulations": ["CUSO=Yes/No", "Canada", "International"],
    "Tenancy Models": ["Isolated", "Shared", "Hybrid"],
    "Audit Logs and Regulations": ["Maintained and Have Access", "Maintained and No Access", "Not Maintained"],
    "Disaster Recovery": ["DRP and Schedule in Place", "Yes but Not Compliant", "No"],
}

# Define metadata columns (optional, can be modified or extended later)
metadata_columns_and_values = {
    "Record ID": lambda: fake.uuid4(),  # Unique identifier for each row
    "Generated Timestamp": lambda: fake.date_time_this_year(),  # Timestamp for when the row was generated
    "Reviewed": ["Yes", "No"],  # Whether the record has been reviewed
    "Region": ["North America", "Europe", "Asia-Pacific", "Global"],  # Example regional metadata
}

# Number of rows to generate
num_rows = 50

# Generate synthetic data
synthetic_data = []
for _ in range(num_rows):
    # Generate core columns
    row = {column: fake.random_element(values) for column, values in core_columns_and_values.items()}
    
    # Generate metadata columns
    for meta_column, meta_generator in metadata_columns_and_values.items():
        row[meta_column] = meta_generator() if callable(meta_generator) else fake.random_element(meta_generator)
    
    synthetic_data.append(row)

# Convert to DataFrame
df = pd.DataFrame(synthetic_data)

# Save to CSV
csv_file_name = "synthetic_dataset_with_metadata.csv"
df.to_csv(csv_file_name, index=False)

# Print a message
print(f"Enhanced synthetic dataset with {num_rows} rows saved to '{csv_file_name}'.")

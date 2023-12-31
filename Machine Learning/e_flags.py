import pandas as pd

def process_flags(file_path, output_file_path):
    df = pd.read_csv(file_path)
    # Replace missing values in 'Flags' column with 'Green Flag'
    df['Flags'].fillna('Green Flag', inplace=True)
    df['Flags'] = df['Flags'].astype(str)
    df['Flags_Code'] = pd.Categorical(df['Flags']).codes
    df['Has_Red_Flag'] = df['Flags'].str.contains('RED FLAG').astype(int)
    df['Has_Orange_Flag'] = df['Flags'].str.contains('Orange Flag').astype(int)
    df['Has_Green_Flag'] = df['Flags'].str.contains('Green Flag').astype(int)
    df.to_csv(output_file_path, index=False)

    # Ensure all column names are of string type
    df.columns = df.columns.astype(str)
    return df

# Example usage
if __name__ == "__main__":
    file_path = r'C:\Users\ayham\Desktop\5\report.csv'
    output_file_path = r'C:\Users\ayham\Desktop\5\processed_report.csv'
    processed_df = process_flags(file_path, output_file_path)
    print(processed_df.head())

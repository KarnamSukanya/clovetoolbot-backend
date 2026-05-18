from services.google_sheet_service import load_tools_sheet

df = load_tools_sheet()

print(df.head())
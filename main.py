import pandas as pd
import csv
from datetime import datetime 
from data_entry import get_amount, get_catagory, get_date, get_description
import matplotlib.pyplot as plt

class CSV:
    CSV_FILE = "finance_data.csv"
    COLUMNS = ["date", "amount", "catagory", "description"]
    FORMAT = "%d-%m-%Y"

    @classmethod
    def initalize_csv(cls):
        try:
            pd.read_csv(cls.CSV_FILE)
        except FileNotFoundError:
            df = pd.DataFrame(columns=cls.COLUMNS)
            df.to_csv(cls.CSV_FILE, index=False)



    @classmethod
    def add_entry(cls, date, amount, catagory, description):
        new_entry = {
            "date": date,
            "amount": amount,
            "catagory": catagory,
            "description": description
        }

        with open(cls.CSV_FILE, "a", newline="") as csvfile:
            writer =  csv.DictWriter(csvfile, fieldnames= cls.COLUMNS)
            writer.writerow(new_entry)
        print("Entry Successfully added")

    @classmethod
    def get_transations(cls, start_date, end_date):
        df = pd.read_csv(cls.CSV_FILE)
        df["date"] = pd.to_datetime(df["date"], format=CSV.FORMAT)
        start_date = datetime.strptime(start_date, CSV.FORMAT)
        end_date = datetime.strptime(end_date, CSV.FORMAT)

        mask = (df["date"] >= start_date) & (df ["date"] <= end_date)
        filtered_df = df.loc[mask]

        if filtered_df.empty:
            print("No transation found in the given date range")
        else:
            print(f"Transation from {start_date.strftime(CSV.FORMAT)} to {end_date.strftime(CSV.FORMAT)}")
            print(filtered_df.to_string(index=False, formatters= {"date": lambda x: x.strftime(CSV.FORMAT)}))

            total_income = filtered_df[filtered_df["catagory"] == "Income"]["amount"].sum()
            total_expense = filtered_df[filtered_df["catagory"] == "Expense"]["amount"].sum()
            print("\nSummery:")
            print(f"Total Income: ${total_income:.2f}")
            print(f"Total Expense: $ {total_expense:.2f}")
            print(f"Net Savings: $ {(total_income - total_expense):.2f}")

        return filtered_df    

def add():
    CSV.initalize_csv()
    date = get_date("Please enter the Date, Month, Year, of the transation, or enter for today's date ", allow_defult=True)
    amount = get_amount()
    catagory = get_catagory()
    description = get_description()
    CSV.add_entry(date, amount, catagory, description)

def plot_transations(df):
    df.set_index("date", inplace=True)
    
    income_df = df [df["catagory"] == "Income"].resample("D").sum().reindex(df.index, fill_value=0)
    expense_df = df [df["catagory"] == "Expense"].resample("D").sum().reindex(df.index, fill_value=0)

    plt.figure(figsize=(10,5))
    plt.plot(income_df.index, income_df["amount"], label="Income", color="g")
    plt.plot(expense_df.index, expense_df["amount"], label= "Expense", color="r")
    plt.xlabel("Date")
    plt.ylabel("Amount")
    plt.title("Income and Expense over time")
    plt.legend()
    plt.grid(True)
    plt.show()




def main():
    while True:
        print("\n1. Add a new transation")
        print("2. View Transation and summary within a date range")
        print("Exit")
        choice = input("Enter your choice (1-3): ")

        if choice == "1":
            add()
        elif choice == "2":
            start_date = get_date("Enter the start of the date (dd-mm-yyyy): ")
            end_date = get_date("Enter the end of the date (dd-mm-yyyy): ")
            df = CSV.get_transations(start_date, end_date)
            if input("do you want to see a plat (Y/N)").lower() == "y":
                plot_transations(df)  
        elif choice == "3":
            print("Exiting...")
            break
        else:
            print("invalid choice. Enter 1, 2, or 3.")

if __name__ == "__main__":
    main()

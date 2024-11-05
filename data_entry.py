from datetime import datetime 

date_format = "%d-%m-%Y"
CATAGORIES = {"I": "Income", "E": "Expense"}

def get_date(prompt, allow_defult=False):
    date_str = input(prompt)
    if allow_defult and not date_str:
        return datetime.today().strftime(date_format)
    
    try:
        valid_date = datetime.strptime(date_str, date_format)
        return valid_date.strftime(date_format)
    except ValueError:
        print("Invalid date please input a valid date")
        return get_date(prompt, allow_defult)

def get_amount():
    try:
        amount = float(input("Please enter an amount: "))
        if amount <= 0:
            raise ValueError("Please enter a valid number ")
        return amount
    except ValueError as e:
        print(e)
        return get_amount()


def get_catagory():
    catagory = input("Please entry the catagory ('I' for Income or 'E' for Expense): ").upper()
    if catagory in CATAGORIES:
        return CATAGORIES[catagory]
    
    print("invalid Category,")
    return get_catagory()


def get_description():
    return input("enter a description: ")
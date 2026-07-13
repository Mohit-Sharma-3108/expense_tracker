import argparse
import json
import datetime
import pandas as pd

FILE_NAME = "expenses.json"

month_dict = {
    1: "January",
    2: "February",
    3: "March",
    4: "April",
    5: "May",
    6: "June",
    7: "July",
    8: "August",
    9: "September",
    10: "October",
    11: "November",
    12: "December"
}

ID_WIDTH = 5
DATE_WIDTH = 10
DESCRIPTION_WIDTH = 30
AMOUNT_WIDTH = 6

def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        prog="expense_tracker",
        description="Tracks, aggregates and exports expenses",
        epilog="Add is a string while amount is a float"
    )
    subparsers = parser.add_subparsers(
        dest="command",
        help="Sub commands are available. Choose from the following list ['add', 'list', 'delete', 'summary', 'export']"
    )
    parser_add = subparsers.add_parser(
        "add", help="Add a new entry in your expenses data"
    )
    parser_add.add_argument("--description", type=str, required=True)
    parser_add.add_argument("--amount", type=float, required=True)

    parser_delete = subparsers.add_parser(
        "delete", help="Delete an entry using id column"
    )
    parser_delete.add_argument("--id", type=int, required=True)

    parser_list = subparsers.add_parser(
        "list", help="Display all records of expenses"
    )

    parser_update = subparsers.add_parser(
        "update", help="Update an entry using id column"
    )
    parser_update.add_argument("--description", type=str, required=False)
    parser_update.add_argument("--amount", type=float, required=False)
    parser_update.add_argument("--date", type=float, required=False)
    parser_update.add_argument("--id", type=int, required=True)

    parser_summary = subparsers.add_parser(
        "summary", help="Aggregate all expense based on options"
    )
    parser_summary.add_argument("--month", type=int)

    parser_export = subparsers.add_parser(
        "export", help="Export expenses to a downloadable csv file"
    )
    parser_show = subparsers.add_parser(
        "show", help="Show full description of an expense using id"
    )
    parser_show.add_argument("--id", type=int, required=True)
    return parser.parse_args()


def fetch_json(file_name: str = FILE_NAME) -> list:
    try:
        with open(file_name, "r") as f:
            expenses = json.load(f)

    except FileNotFoundError as e:
        print(f"File: {file_name} not found")
        expenses = []
        
    return expenses


def save_json(expenses: list, file_name: str = FILE_NAME) -> None:
    with open(file_name, "w") as f:
        json.dump(expenses, f, indent=4)
    print("json object written to disk successfully!")

def perform_add_action(expenses: list, description: str, amount: float) -> list | None:
    if amount < 0:
            print(f"Invalid amount. Please input only positive float values as amount.")
            return None
    if len(expenses) != 0:
        max_id = expenses[-1].get("ID") + 1
    else:
        max_id = 1
    # String conversion required as json doens't understand datetime objects
    today = datetime.date.today().isoformat()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    expenses.append({"ID": max_id, "Date": today, "Description": description, "Amount": amount, "InsertTimeStamp": timestamp})

    return expenses

def perform_update_action(expenses: list, description: str, amount: float, id: int, date: str):
    for expense in expenses:
        if expense.get("ID") == id:
            if amount is not None:
                expense["Amount"] = amount
            if description is not None:
                expense["Description"] = description
            if date is not None:
                expense["Date"] = date
            expense["InsertTimeStamp"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            
            return expenses
    
    print("No expense with id found in expenses. Please ensure the correct ID is being input")
    return None

def perform_delete_action(expenses: list, id: int):
    for expense in expenses:
            if expense.get("ID") == id:
                expenses.remove(expense)
                print(f"Delete ID: {id} from expenses")
                return expenses

    print(f"ID: {id} must be present in expenses in order to delete it.")
    return None

def perform_summary_action(expenses: list, month_num: int | None, month_dict: dict = month_dict):
    if month_num:
            month_name = month_dict[month_num]
            print(f"Summarizing expenses for month: {month_name}")
            month_amount = sum(
                [
                    expense["Amount"] 
                    for expense in expenses
                    if datetime.datetime.strptime(expense.get("Date"), "%Y-%m-%d").month == month_num
                ]
            )
            print(f"Total expense for {month_name}: {month_amount}")
    else:
        total_amount = sum([expense.get("Amount") for expense in expenses])
        print(f"Total aggregate summary: {total_amount}")
    
    return None

def perform_list_action(expenses: list) -> None:
    print(f"{'ID':<{ID_WIDTH}}{'Date':>{DATE_WIDTH}}{'Description':>{DESCRIPTION_WIDTH}}{'Amount':>{AMOUNT_WIDTH}}")
    print("-"*(ID_WIDTH+DATE_WIDTH+DESCRIPTION_WIDTH+AMOUNT_WIDTH))
    for expense in expenses:
        id = expense.get('ID')
        date = expense.get('Date')
        amount = expense.get('Amount')
        description = expense.get("Description")
        description = description if len(description) <= DESCRIPTION_WIDTH else description[:DESCRIPTION_WIDTH - 3] + "..."
        
        print(f"{id:<{ID_WIDTH}}{date:>{DATE_WIDTH}}{description:>{DESCRIPTION_WIDTH}}{amount:>{AMOUNT_WIDTH}.2f}")
    
    return None

def perform_show_action(expenses: list, id: int) -> None:
    id_found = False
    for expense in expenses:
        if expense.get("ID") == id:
            print(f"Description of id: {id} is {expense.get('Description')}")
            id_found = True
            break
    if not id_found:
        print(f"ID: {id} not found in expenses. Please select an ID which exists")
    
    return None


def perform_export_action(expenses: list):
    df = pd.DataFrame(
            expenses,
            columns=["ID", "Date", "Description", "Amount"]
        )
    df.to_csv("expenses.csv", index=False)
    return None

def check_valid_args_for_update(amount, description, date) -> bool:
    if all(val for val in (amount, description, date)):
        print("All of amount, description and date cannot be null while updating an expense. Please provide atlease one argument")
        return False
    else:
        return True

def perform_crud_actions(expenses: list, parser: argparse.Namespace):
    command = parser.command
    if command == "add":
        description = parser.description
        amount = parser.amount

        return perform_add_action(expenses=expenses, description=description, amount=amount)

    elif command == "update":
        description = parser.description
        amount = parser.amount
        date = parser.date
        id = parser.id

        bool_check = check_valid_args_for_update(amount, description, date)

        if not bool_check:
            return None
        
        return perform_update_action(expenses, description, amount, id, date)
        

    elif command == "delete":
        id = parser.id

        return perform_delete_action(expenses, id)

    elif command == "summary":
        month_num = parser.month
        
        return perform_summary_action(expenses, month_num)


    elif command == "list":
        return perform_list_action(expenses)

    elif command == "show":
        id = parser.id
        
        return perform_show_action(expenses, id)

    elif command == "export":
        
        return perform_export_action(expenses)

    else:
        print(f"Invalid command, use commands from the following list only: [add, update, delete, summary, list, export]")

def main():
    parser = parse_arguments()
    expenses = fetch_json()
    output = perform_crud_actions(expenses, parser)
    if output:
        save_json(output)
    

if __name__ == "__main__":
    main()
    
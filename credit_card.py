from argparse import ArgumentParser
import sys
# to run this program run it from the command line. python <credit_car.py> <balance_amount> <apr> <credit_line> [--payment <target_amount>] [--fees <fees>]
# ex: python credit_card.py 1500 18 5000 --payment 200 --fees 10
def get_min_payment(balance, fees=0):
    """Calculate the minimum credit card payment based on the account balance and fees.
    
    Args:
        balance (float): The total balance amount in the account that is left to pay. This should be a positive number.
        fees(int): The fees associated with credit card account.Defaults to 0 and should be a positive integer.
                    
    Returns:
        float: The calculated minimum payment. If calulated payment is less than 25 its set to 25
    """
    m = 0.02
    min_payment = (balance * m) + fees
    return max(min_payment,25)
def interest_charged(balance,apr):
    """Calculate interest accured on a credit card balance for the next payment.
    
    Args:
        balance (float): The balance of the credit card. Should be a positive number
        apr (int): The annual APR. Can assume the integer is between 0-100.
        
    Returns:
        float: The amount of interest accured in the next payment that is calculated using a formula.
    """
    days= 365
    cycle = 30
    apr = apr/100
    interest = (apr/days) * balance * cycle
    return interest
def remaining_payments(balance,apr,targetamount = None,credit_line = 5000,fees = 0):
    """Computes and returns the number of payments needed to pay off the credit card balance and tracks 
    how many payment periods the balance remains over specific percentages of the credit line
    
    Args:
        balance (float): The balance of the credit card. Should be a positive number
        apr (int): The annual APR. Can assume the integer is between 0-100.
        targetamount (foat): The target amount the user wants to pay per payment. If number is not specified (None) the minimum amount will be used. Should be a positive number.
        credit_line (int): The maximum amount fo balance that an account hjolder can have in their account. Defaults to 500 and can assume it is a positive integer.
        fees (int): The amount of fees that will be charged in addition to the minimum payment. Assume this is a positive integer.
        
    Returns:
        tuple: A tuple containing the number of payments based off the counters
    """

    payment_count = 0
    over_25_count = 0
    over_50_count = 0
    over_75_count = 0
    while balance > 0:
        if targetamount is None:
           payment = get_min_payment(balance,fees)
        else:
            payment = targetamount
        interest = interest_charged(balance,apr)
        balance_payment = payment-interest
        if balance_payment <= 0:
            print("The card balance cannot be paid off. ")
            return
        balance -= balance_payment
        if balance > .75 * credit_line:
            over_75_count += 1
        if balance > .5 * credit_line:
            over_50_count += 1
        if balance > .25 * credit_line:
            over_25_count += 1
        payment_count += 1
    return payment_count, over_25_count, over_50_count, over_75_count

def main(balance,apr,targetamount = None ,credit_line=5000,fees=0):
    """Computes recommended minimum payment using get_min_payment() function or whatever the user inputs and displays options to user.

    Args:
        balance (float): The balance of the credit card. Should be a positive number
        apr (int): The annual APR. Can assume the integer is between 0-100.
        targetamount (foat): The target amount the user wants to pay per payment. If number is not specified (None) the minimum amount will be used. Should be a positive number.
        credit_line (int): The maximum amount fo balance that an account hjolder can have in their account. Defaults to 500 and can assume it is a positive integer.
        fees (int): The amount of fees that will be charged in addition to the minimum payment. Assume this is a positive integer.
    
    Returns:
        A string message informing the user of the payment periods where the balance stays above 25%, 50%, and 75% of the credit line.
    """
    
    min_payment = get_min_payment(balance,fees)
    print(f"Your recommened starting minimum payment is: ${min_payment:.2f}")
    pays_minimum = False
    if targetamount is None:
        pays_minimum = True
    elif targetamount < min_payment:
        print("Your target payment is less than the minimum payment for this credit card")
        return
    total_payments, over_25_count, over_50_count, over_75_count = remaining_payments(
        balance, apr, targetamount, credit_line, fees
    )
    if pays_minimum:
        print(f"If you pay the minimum payments each month, you will pay off the balance in {total_payments} payments.")
    else:
        print(f"If you make payments of ${targetamount:.2f}, you will pay off the balance in {total_payments} payments")
        
    summary_message = (
        f"You will spend a total of {over_25_count} months over 25% of your credit line."
        f"You will spend a total of {over_50_count} months over 50% of your credit line."
        f"You will spend a total of {over_75_count} months over 75% of your credit line."
    )
    return summary_message
# interest_charged(), remaining_payments(), and main()
def parse_args(args_list):
    """Takes a list of strings from the command prompt and passes them through as
    arguments
    Args:
        args_list (list) : the list of strings from the command prompt
    Returns:
        args (ArgumentParser)
    """
    parser = ArgumentParser()
    parser.add_argument('balance_amount', type = float, help = 'The total amount of balance left on the credit account')
    parser.add_argument('apr', type = int, help = 'The annual APR, should be an int between 1 and 100')
    parser.add_argument('credit_line', type = int, help = 'The maximum amount of balance allowed on the credit line.')
    parser.add_argument('--payment', type = int, default = None, help = 'The amount the user wants to pay per payment, should be a positive number')
    parser.add_argument('--fees', type = float, default = 0, help = 'The fees that are applied monthly.')
    # parse and validate arguments
    args = parser.parse_args(args_list)
    if args.balance_amount < 0:
        raise ValueError("balance amount must be positive")
    if not 0 <= args.apr <= 100:
        raise ValueError("APR must be between 0 and 100")
    if args.credit_line < 1:
        raise ValueError("credit line must be positive")
    if args.payment is not None and args.payment < 0:
        raise ValueError("number of payments per year must be positive")
    if args.fees < 0:
        raise ValueError("fees must be positive")
    return args

if __name__ == "__main__":
    try:
        arguments = parse_args(sys.argv[1:])
    except ValueError as e:
        sys.exit(str(e))
    print(main(arguments.balance_amount, arguments.apr, credit_line = arguments.credit_line, targetamount = arguments.payment, fees = arguments.fees))
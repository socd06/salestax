# regular expressions
import re
import math
import argparse

def get_args():
    '''
    Gets the arguments from the command line.
    '''
    parser = argparse.ArgumentParser("Path to shopping cart text file")
    # -- Create the descriptions for the commands
    i_desc = "The location of the input file"

    # -- Add required and optional groups
    parser._action_groups.pop()
    required = parser.add_argument_group('required arguments')
    optional = parser.add_argument_group('optional arguments')

    # -- Create the arguments
    required.add_argument("-i", help=i_desc, required=True)
    args = parser.parse_args()

    return args

# define utility functions
def read_text(filename):
    with open(filename) as f:
        content = f.readlines()
    # you may also want to remove whitespace characters like `\n` at the end of each line
    content = [x.strip() for x in content]
    return content

# round to nearest 0.05
def round_to_next(val, step):
    return val - (val % step) + (step if val % step != 0 else 0)

def exempt_words():
    # use natural language processing toolkit (nltk)
    from nltk.corpus import wordnet as wn

    # write a list of common food items
    food = wn.synset('food.n.02')
    food_list = list(set([w for s in food.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))
    more_food = ["chocolates"]
    food_list = food_list + more_food

    # write a list of medicine items
    medicine = wn.synset('medicine.n.02')
    med_list = list(set([w for s in medicine.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

    # add more keywords to medicine items list
    more_meds = ["pills", "headache","heartburn", "aspirine"]
    med_list = med_list + more_meds

    # write a list of book related words
    book = wn.synset('book.n.01')
    books_list = list(set([w for s in book.closure(lambda s:s.hyponyms()) for w in s.lemma_names()]))

    more_books = ["book", "books", "BOOK", "BOOKS"]
    books_list = books_list + more_books

    exemptions = books_list + med_list + food_list

    return exemptions


def is_exempt(item_description):
    """
    Parameters:
        item (list): Item description

    Returns:
        (Boolean) True if description contains an exempted word or False otherwise.
    """
    checks = []

    exemptions = exempt_words()

    # Check if description has any word from the exempt lists
    for item in item_description:
        if item in exemptions:
            checks.append(True)
        else:
            checks.append(False)
    if any(checks) == True:
        return True
    else:
        return False


def tax(text_list):
    '''
    Parameters:
        list of strings with %d %s %f structure
        example:
            ["1 book at 12.49", "1 music CD at 14.99", "1 chocolate bar at 0.85"]
    Returns:
        Prints parsed input
        prints sales taxes
        prints total ammount
    '''

    total = 0.0
    total_taxes = 0.0

    # regular expression pattern
    pattern = "-?([0-9]\d*\.?\d*)"

    # loop through elements of list
    for text in text_list:

        # Initialize tax percentage variable
        tax = 0.0
        # Initialize sales tax variable
        sales_tax = 0.0

        qty = int(re.findall(pattern,text)[0])
        price = float(re.findall(pattern,text)[1])
        item_match = re.findall("[a-zA-Z]+",text)

        # Remove "at" from end of string, if neccesary
        if "at" in item_match:
            item_match.pop(len(item_match)-1)

        # Compare regex to exempt lists (Books, FOOD, Medical products)
        if is_exempt(item_match) == False:
            is_taxable = True
        else:
            # for debugging
            is_taxable = False

        # Import duty tax +5%
        if "imported" in item_match or "IMPORTED" in item_match == True:
            is_imported = True
        else:
            is_imported = False

        # Calculate tax %
        if is_taxable and is_imported:
            tax = 0.15 # 10%
            #print("15% tax", tax)
        elif is_taxable:
            tax = 0.1 # 10%
            #print("10% tax", tax)
        elif is_imported:
            tax = 0.05 # Add 5% to item tax
            #print("5% tax", tax)
        else:
            # for debugging
            tax = 0
            #print("Tax exempt",tax)

        # Calculate sales tax
        sales_tax = round_to_next(tax * price, 0.05)
        total_taxes += sales_tax
        #print("taxes", total_taxes)

        taxed_price = price + sales_tax
        #print("taxed price", taxed_price)

        taxed_price = taxed_price

        total += qty * taxed_price

        # Join item description using list comprehension
        item_description = " ".join(map(str, item_match))

        # print parsed item information
        print(f'{qty:.0f} {item_description}: {taxed_price:.2f}')

    print(f'Sales Taxes: {total_taxes:.2f}')
    print(f'Total: {total:.2f}')

def main():
    args = get_args()
    content = read_text(args.i)

    #compile_equations(args)
    tax(content)

if __name__ == "__main__":
    main()

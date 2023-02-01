from chatgpt_wrapper import ChatGPT


def gpt_parse_receipt(text):
    bot = ChatGPT()
    # prepare the question
    pre_question = "Here is a summary of my receipt: "
    receipt_text = text
    post_question = "Please list all the food items along with their respective prices."
    post_question += " Tax and tip should also be their own items if listed on the receipt."
    post_question += " Answer in one line, with each item separated by a semicolon."
    post_question += " The food and price should be separated by a colon."
    post_question += " Do not indent with whitespace."
    question = pre_question + ' ' + receipt_text + ' ' + post_question
    # ask gpt
    response_text = bot.ask(question)
    # parse the response
    dict_response = parse_gpt_response(response_text)
    

    return dict_response


def parse_gpt_response(response_text):
    lines = response_text.split(';')
    info = {}
    for line in lines:
        res = line.split(':')
        print(res)
        item_name = res[0]
        try:
            price = res[1].replace(' ', '')
        except IndexError:
            print(res)
            exit()
        if is_price(price.replace('$', '')):
            price = float(price.replace('$', ''))
        info[item_name] = price
    return info


def is_price(s):
    """
    check if a string is a price (aka a float)
    """
    try:
        float(s)
        return True
    except ValueError:
        return False


if __name__ == "__main__":
    # for testing out the script
    receipt_text = "HARBOR LANE CAFE 3941 GREEN OAKS BLVD CHICAGO; IL SALE 11/20/2019 11*05 AM BATCH #01aza APPR #34362 TRACE # 9 VISA 3483 1 Tacos Del Mal Shrimp S14.98 L Especial Salad Chicken S12.50 Fountain Beverage S1.99 SUBTOTAL: s29.47 Tax: S1.92 TOTAL: S31.39 TIP: TOTAL: APPROVED THANK YOU CUSTOMER COPY."
    dict_response = gpt_parse_receipt(receipt_text)
    print(dict_response)

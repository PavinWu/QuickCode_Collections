"""
Remove non-unique transactions on a transaction list CSV, then print to another csv file.
A non-unique transaction line is the one which has the same of these to at least one other transaction:
- Same name, price, item category, comment.

This script assumes the CSV file is well-formed.

The purpose for this script is that the budget app I've been using (which shall not be named, or should I?) messed up the backup. 
Specifically, some transactions seem to be missing, but recurring transactions seem OK?
I'm transitioning to another app, so want to re-record those unique transactions.

Quick and dirty script, so perhaps don't expect best coding practices.

"""

if __name__ == "__main__":
    f = open("/Users/uvin/Documents/transactions_list.csv", "r")
    
    curr_transaction = ""
    take_next = False
    headers = []
    transactions = []

    # Gather transactions
    is_first_line = True
    for line in f:
        
        if is_first_line:
            headers = line.translate(str.maketrans("", "", "\n\"")).replace("\ufeff", "").split(",")
            is_first_line = False
            print(headers)
            continue

        # A transaction may be split into multiple lines.
        if take_next:
            curr_transaction += line
        else:
            curr_transaction = line

        if not line.endswith("\"\n"):
            take_next = True
        else:
            transactions.append(curr_transaction)
            take_next = False
    
    if take_next:
        transactions.append(curr_transaction)
        take_next = False

    # Define transaction items
    all_transDict = []
    for trans in transactions:
        splits = trans.split(",")

        transDict = {}
        for id, header in enumerate(headers):
            transDict[header] = splits[id]

        # Assume last splits are the notes.
        if len(splits) > len(headers):
            transDict[headers[-1]] = transDict[headers[-1]].join(splits[len(headers):])

        all_transDict.append(transDict)

    # all_non_unique_trans_ids = []
    # for tid1, trans1 in enumerate(all_transDict):
    #     # Note: not space efficient (duplicate entries) - but doesn't matter here.
    #     non_unique_trans_ids = [tid1]
    #     for tid2, trans2 in enumerate(all_transDict):
    #         if tid1 == tid2:
    #             continue
            
    #         is_same_title = trans1["Title"] == trans2["Title"]
    #         is_same_price = trans1["Amount"] == trans2["Amount"]
    #         is_same_category = trans1["Category"] == trans2["Category"]
    #         is_same_comment = trans1["Notes"] == trans2["Notes"]

    #         if is_same_title and is_same_price and is_same_category and is_same_comment:
    #             non_unique_trans_ids.append(tid2)
        
    #     if len(non_unique_trans_ids) > 1:
    #         print("Popping non_unique_trans_ids: {}".format(non_unique_trans_ids))
    #         print("\t{}".format(all_transDict[tid1]))
    #         print()
    #         all_non_unique_trans_ids.append(non_unique_trans_ids)
    #         ## Gemini found a bug!!
    #         # for tid in non_unique_trans_ids:
    #         #     transactions.pop(tid)

    non_unique_trans_ids = set()
    for tid1, trans1 in enumerate(all_transDict):
        for tid2, trans2 in enumerate(all_transDict):
            if tid1 == tid2 or tid2 in non_unique_trans_ids:
                continue
            
            is_same_title = trans1["Title"] == trans2["Title"]
            is_same_price = trans1["Amount"] == trans2["Amount"]
            is_same_category = trans1["Category"] == trans2["Category"]
            is_same_comment = trans1["Notes"] == trans2["Notes"]

            if is_same_title and is_same_price and is_same_category and is_same_comment:
                non_unique_trans_ids.add(tid1)
                non_unique_trans_ids.add(tid2)
        

    unique_transactions = []
    non_unique_transactions = []
    for tid, trans in enumerate(all_transDict):
        if tid not in non_unique_trans_ids:
            unique_transactions.append(",".join([trans[key] for key in headers]))
        else:
            non_unique_transactions.append(",".join([trans[key] for key in headers]))

    f_new = open("/Users/uvin/Documents/transactions_list_unique.csv", "w")
    f_new.write(",".join(headers) + "\n")
    for trans in unique_transactions:
        f_new.write(trans)
    f_new.close()

    f_new = open("/Users/uvin/Documents/transactions_list_nonunique.csv", "w")
    f_new.write(",".join(headers) + "\n")
    for trans in non_unique_transactions:
        f_new.write(trans)
    f_new.close()
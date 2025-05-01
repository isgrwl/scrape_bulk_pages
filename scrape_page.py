'''
    get data from amazon product page

    queries generated from chatgpt
'''





def get_data(sb, rules):
    data = dict()
    for rule in rules:
        try:
            #select first
            if rule.single: 
                tag = sb.cdp.select(rule.qstr)
            #select all
            else:
                tag = sb.cdp.select_all(rule.qstr) 

            #insert tag after postprocessing
            data[rule.field] = rule.postprocess(tag.text)

        except Exception as error:
            print(f"Couldn't get data for: {rule.field}")
            pass

    return data

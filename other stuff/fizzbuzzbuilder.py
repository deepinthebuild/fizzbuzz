import psycopg2

# The database is localhost only don't get excited.
DB_SERVER_INFO = "dbname='rand' user='Chris' host='localhost' password=''"

# Constructor Target
TARGET_STR =  """for x in range(1,101):
    if x % 15 == 0:
        print("FizzBuzz")
    elif x % 5 == 0:
        print("Buzz")
    elif x % 3 == 0:
        print("Fizz")
    else:
        print(x)"""


# Ugly SQL query strings live here
def build_sql_query(size):
        select_op_8 =    ("SELECT seed FROM fizzbuzz WHERE "
                        "out1 = %(out1)s AND "
                        "out2 = %(out2)s AND "
                        "out3 = %(out3)s AND "
                        "out4 = %(out4)s AND "
                        "out5 = %(out5)s AND "
                        "out6 = %(out6)s AND "
                        "out7 = %(out7)s AND "
                        "out8 = %(out8)s;"
                        )
        select_op_7 = select_op_8[:-21] + ";"
        select_op_6 = select_op_7[:-21] + ";"
        select_op_5 = select_op_6[:-21] + ";"
        select_op_4 = select_op_5[:-21] + ";"
        select_op_3 = select_op_4[:-21] + ";"
        select_op_2 = select_op_3[:-21] + ";"
        select_op_1 = select_op_2[:-21] + ";"
        
        if size == 8:
            return select_op_8
        elif size == 7:
            return select_op_7
        elif size == 6:
            return select_op_6
        elif size == 5:
            return select_op_5
        elif size == 4:
            return select_op_4
        elif size == 3:
            return select_op_3
        elif size == 2:
            return select_op_2
        elif size == 1:
            return select_op_1
        else:
            raise ValueError("You gave build_sql_query a bad value.")

            
def make_ordinal_dict(input_str):
    if len(input_str) == 0:
        raise ValueError("Need at least one character to build a ordinal_dict.")
    if len(input_str) > 8:
        raise ValueError("Can't build a query out of more than 8 characters.")
     
    output_dict = dict()
    char_list = list(input_str)
    char_list = list(map(ord, char_list))

    for index, value in enumerate(char_list):
        output_dict["out" + str(index+1)] = value
    
    return output_dict

    
def build_from_junk(input_str, db_connection):
    current_point = 0
    seed_pile = []
    seed_sizes = []
    
    
    while current_point < len(input_str): 
        # Database only has 8 entries per seed
        grab_size = min(8, len(input_str) - current_point)
        result = False
        
        while grab_size >= 0:
            if grab_size == 0:
                raise RuntimeError("Can't match a substring!")
            
            args_dict = make_ordinal_dict(input_str[current_point : current_point+grab_size])
            query = build_sql_query(grab_size)
            
            with db_connection.cursor() as db_cursor:
                db_cursor.execute(query, args_dict)
                result = next(db_cursor, False) # Grab result or False if no result
                
            if result:
                seed_pile.append(result[0])
                seed_sizes.append(grab_size)
                current_point += grab_size
                break
                
            grab_size -= 1
            
    return seed_pile, seed_sizes



with psycopg2.connect(DB_SERVER_INFO) as conn:
    seeds, sizes = build_from_junk(TARGET_STR, conn)
    print("Seeds: ", seeds)
    print("Sizes: ", sizes)



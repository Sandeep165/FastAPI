# import threading
import time
import json

# def fun(seconds):
#     print(f"sleeping for {seconds}")
#     time.sleep(seconds)

# start_time = time.time()
    
# # fun(5)
# # fun(4)
# # fun(3)

# t1 = threading.Thread(target=fun, args=[10])
# t1.start()
# t2 = threading.Thread(target=fun, args=[8])
# t2.start()
# t3 = threading.Thread(target=fun, args=[5])
# t3.start()

# t1.join()
# t2.join()
# t3.join()

# end_time = time.time()

# time_taken = end_time-start_time

# print(time_taken)
# print("Run is completed...")


# even_odd = [i for i in range(0,10) if i%2==0]
even_odd = ["Even" if i%2==0 else "Odd" for i in range(0,10) ]
# print(even_odd)


    
def decorator_func(func):
    def wrapper():
        print("Execution started..............")
        func()
        print("Execution ended............")
    return wrapper


def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        print("execcution started............")
        func(*args, **kwargs)
        end_time = time.time()
        print("execution time taken to run the function is:- ",end_time-start_time)
    return wrapper
        
@time_decorator
def invite():
    print("Hello")
    time.sleep(2)
    
# invite()

'''

@app.get("/user_status/{status_code}")
def status_code(status_code: int):
    check = ""
    if status_code == 200:
        check = "Successful"
    elif status_code == 300:
        check = "Redirection"
    elif status_code == 400:
        check = "Bad Request"
    elif status_code == 404:
        check = "Not Found"
    elif status_code == 500:
        check = "Server Error"
    else:
        check = "Unknown Status Code"
    
    return{"user_id": status_code, "status": check}

@app.get("/items/")
def get_item(item: Optional[str] = None):
    return {"item name " : {item} or "no product found"}

#default query parameter value 
@app.get("/products/")
def get_product(item: Optional[str] = "default_item"):
    return {"product name " : item}
'''
with open("patients.json", "r" ) as f:
    data = json.load(f)

result = sorted(data.items(), key=lambda x: x[1]["weight"], reverse=False)
print(result)
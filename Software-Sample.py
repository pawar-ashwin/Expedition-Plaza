'''In order for this code to work you need to create a sample products DB in firebase with randomn tag values, such that the product billing will be done by cross checking the items in product DB'''


import tkinter
from tkinter.constants import BOTH
import pyrebase


root = tkinter.Tk()
root.title("Billing Application")
root.geometry('1000x1000')
root.iconbitmap('bill.ico')
root.config(bg='#aec5eb')

# CUSTOMER PRODUCTS DB
firebaseconfig_customer = {
    "apiKey": "AIzaSyDiNgautUEBs2pbwt5oJUD5OUAIBzZXmeM",
    "authDomain": "fir-db-5c0f7.firebaseapp.com",
    "databaseURL": "https://fir-db-5c0f7-default-rtdb.firebaseio.com",
    "projectId": "fir-db-5c0f7",
    "storageBucket": "fir-db-5c0f7.appspot.com",
    "messagingSenderId": "465263470942",
    "appId": "1:465263470942:web:7742ae08f50166eb3b07cf",
    "measurementId": "G-G0KYN7LH2B"
}


# PRODUCTS DB
# firebaseconfig_prod = {
#     "apiKey": "AIzaSyDwPe5TV1BPgbSjFabJLs8gJ_6lImaTF_w",
#     "authDomain": "fir-db2-ac124.firebaseapp.com",
#     "databaseURL": "https://fir-db2-ac124-default-rtdb.firebaseio.com",
#     "projectId": "fir-db2-ac124",
#     "storageBucket": "fir-db2-ac124.appspot.com",
#     "messagingSenderId": "480113293027",
#     "appId": "1:480113293027:web:bfe8ad2a9fb4c561caf7d6",
#     "measurementId": "G-HD5G9XVQRB"
# }
fb_customer = pyrebase.initialize_app(firebaseconfig_customer)
db_customer = fb_customer.database()

# fb_prod = pyrebase.initialize_app(firebaseconfig_prod)
# db_prod = fb_prod.database()


# temp2 = db_customer.child('Items').child('8467907').get()
# print(temp2.val())

# FUNCTIONS


def get_bill():
    if(num_entry.get() == ''):
        return
    s = 0
    number = num_entry.get()
    temp = db_customer.child('Customers').child(number).get()
    lb_1 = tkinter.Label(bill_frame, bg='#E0D0C1', text='ID',
                         font=('Arial', 16, 'bold'))
    lb_1.grid(row=0, column=0)

    lb_2 = tkinter.Label(bill_frame, bg='#E0D0C1', text='NAME', font=(
        'Arial', 16, 'bold'))
    lb_2.grid(row=0, column=1)

    lb_3 = tkinter.Label(bill_frame, bg='#E0D0C1', text='UNIT_PRICE',
                         font=('Arial', 16, 'bold'))
    lb_3.grid(row=0, column=2)

    lb_4 = tkinter.Label(bill_frame, bg='#E0D0C1', text='QTY', font=(
        'Arial', 16, 'bold'))
    lb_4.grid(row=0, column=3)

    lb_5 = tkinter.Label(bill_frame, bg='#E0D0C1', text='AMOUNT',
                         font=('Arial', 16, 'bold'))
    lb_5.grid(row=0, column=4)
    n = 1
    for i in temp.each():
        c = 0
        if(i.val() == None):
            continue
        Id = i.val()['ID']
        qty = i.val()['Qty']
        temp2 = db_customer.child('Items').child(str(Id)).get()
        # if(temp2.val() == None):
        #     continue
        name = temp2.val()['name']
        # print(name, type(name))
        u_price = temp2.val()['unit_price']
        # print(u_price, type(u_price))
        amt = int(u_price)*int(qty)
        s += amt
        # lb4 = tkinter.Label(bill_frame, text=str(Id) + (' '*8) + str(name) +
        #                     (' '*37) + str(u_price) + (' '*4) + str(qty) + (' '*2) + str(amt), font=('Arial', 16))
        # lb4.grid(row=n, column=0)
        label_1 = tkinter.Label(bill_frame, bg='#E0D0C1', text=str(
            Id), font=('Arial', 16))
        label_1.grid(row=n, column=c)
        c += 1

        label_2 = tkinter.Label(bill_frame, bg='#E0D0C1', text=str(
            name), font=('Arial', 16))
        label_2.grid(row=n, column=c)
        c += 1

        label_3 = tkinter.Label(
            bill_frame, bg='#E0D0C1', text=str(u_price), font=('Arial', 16))
        label_3.grid(row=n, column=c)
        c += 1

        label_4 = tkinter.Label(bill_frame, bg='#E0D0C1', text=str(
            qty), font=('Arial', 16))
        label_4.grid(row=n, column=c)
        c += 1

        label_5 = tkinter.Label(bill_frame, bg='#E0D0C1', text=str(
            amt), font=('Arial', 16))
        label_5.grid(row=n, column=c)
        c += 1

        n += 1
    tot_label = tkinter.Label(
        bill_frame, bg='#E0D0C1', text='TOTAL = ' + str(s), font=('Arial,', 20, 'bold'))
    tot_label.grid(row=n, column=0, columnspan=5, pady=10)


# FRAMES
head_frame = tkinter.Frame(root, bg='#D5573B', bd=5,
                           height=100, width=800, relief='solid')
head_frame.pack(pady=10)

inp_frame = tkinter.Frame(root, bg='#BEBBBB', bd=3,
                          height=100, width=600, relief='groove')
inp_frame.pack(pady=10)

bill_frame = tkinter.Frame(root, bg='#E0D0C1', bd=3,
                           height=600, width=800, relief='ridge')
bill_frame.pack()


# ENTRY
num_entry = tkinter.Entry(inp_frame, width=20, font=('Arial', 16))
num_entry.grid(row=0, column=1, padx=10, pady=10, sticky='E')
inp_frame.grid_propagate(0)
bill_frame.grid_propagate(0)

# LABELS
lb1 = tkinter.Label(head_frame, text="CESD lab Solutions",
                    font=('Arial', 20, 'bold'), bg='#D5573B')
lb1.pack()

lb2 = tkinter.Label(inp_frame, text="Phone Number of Customer :",
                    font=('Arial', 16), bg='#BEBBBB')
lb2.grid(row=0, column=0, padx=10, pady=10)


# BUTTONS
bu1 = tkinter.Button(
    inp_frame, text="[GET BILL]", width=20, font=('Arial', 10, 'bold'), command=get_bill)
bu1.grid(row=1, column=0, columnspan=2, pady=(0, 10), ipady=5)

root.mainloop()

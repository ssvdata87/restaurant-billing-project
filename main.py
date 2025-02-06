import tkinter as tk
from tkinter import*
from tkinter import messagebox
from tkinter import ttk
from restaurent_db import Database
db=Database("Restaurent.db")

global total_label

def open_new_window():
    
    def Add_Product_into_db():
        if txtname.get()=="" or txtprice.get()=="":
            messagebox.showerror("Error in input","Please fill the all Details")
            return
        else:
            db.insert_item(txtname.get(),txtprice.get())
            name.set("")
            price.set("")

    Add_Product = tk.Toplevel(root)
    Add_Product.title('Add New Item here')
    Add_Product.geometry("800x500+50+50")
    Add_Product.config(bg="#535c68")#
    title=tk.Label(Add_Product,text="Add New Product",font=("Calibri",18,"bold"),bg="#535c68",fg="white")
    title.grid(row=0,columnspan=2,padx=10,pady=20,sticky='w')
    lname=tk.Label(Add_Product,text='Item Name:',font=("Calibri",18,"bold"),bg="#535c68",fg="white")
    lname.grid(row=1,column=0,padx=10,pady=10,sticky='w')
    name = tk.StringVar() 
    txtname=tk.Entry(Add_Product,textvariable=name,font=("calbri",16),width=30)
    txtname.grid(row=1,column=1,padx=10,pady=10,sticky='w')
    lprice=tk.Label(Add_Product,text='Price:',font=("Calibri",18,"bold"),bg="#535c68",fg="white")
    lprice.grid(row=2,column=0,padx=10,pady=10,sticky='w')
    price = tk.StringVar() 
    txtprice=tk.Entry(Add_Product,textvariable=price,font=("calbri",16),width=30)
    txtprice.grid(row=2,column=1,padx=10,pady=10,sticky='w')
    btnAdd=tk.Button(Add_Product,command=Add_Product_into_db,text='Add Item',font=("Calibri",16,"bold"),bg="#535c68",fg="white")
    btnAdd.grid(row=3,column=0,padx=10)
    Add_Product.mainloop()

def open_show_product():
    items = db.get_items()  # Fetch items from the database
    print(items)

    show_product = tk.Toplevel(root)
    show_product.title('Show Product')
    show_product.geometry("800x500+50+50")
    show_product.config(bg="#535c68")

    title = tk.Label(show_product, text="Show Product", font=("Calibri", 18, "bold"), bg="#535c68", fg="white")
    title.grid(row=0, columnspan=2, padx=20, pady=30, sticky='w')

    # Treeview Styling
    style = ttk.Style()
    style.configure("Custom.Treeview",
                    background="white",
                    foreground="black",
                    rowheight=25,
                    fieldbackground="white",
                    borderwidth=2, relief="solid")  # Adds solid border

    style.configure("Custom.Treeview.Heading",
                    font=("Calibri", 12, "bold"),
                    background="lightgray",
                    foreground="black",
                    borderwidth=2, relief="solid")  # Heading border

    # Treeview Widget with Custom Style
    tv = ttk.Treeview(show_product, columns=("item_id", "name", "price"), show="headings", style="Custom.Treeview")

    # Define Column Headings
    tv.heading("item_id", text="ITEM ID")
    tv.heading("name", text="NAME")
    tv.heading("price", text="PRICE")

    # Set Column Width and Alignment
    tv.column("item_id", width=100, anchor="center")
    tv.column("name", width=200, anchor="center")
    tv.column("price", width=100, anchor="center")

    # Insert Data into Treeview
    for row in items:
        tv.insert("", tk.END, values=row)

    tv.grid(row=1, column=0, padx=10, pady=10)

    show_product.mainloop()




    

    
        

root = tk.Tk()
root.title('Peoples Restaurent')


# Create a menu bar
menu_bar = tk.Menu(root)
root.config(menu=menu_bar)
root.geometry("1920x1080+0+0")
root.config(bg="gray")##535c68
root.state("zoomed")

code = tk.StringVar()
item_id=tk.IntVar()
item_name=tk.StringVar()
item_price=tk.DoubleVar()

item_quantity=tk.IntVar()
total=tk.DoubleVar()
gtotal = tk.DoubleVar()



# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=0)
file1_menu = tk.Menu(menu_bar, tearoff=0)
menu_bar.add_cascade(label='Menu', menu=file_menu)
file_menu.add_command(label='Add Product', command=open_new_window)
file_menu.add_separator()
file_menu.add_command(label="Show Product",command=open_show_product)
file_menu.add_separator()
file_menu.add_command(label='Exit', command=root.quit)

def save_item():
    if item_entry.get=="" or price_entry.get()=="" or quantity_entry.get()=="" or total_entry.get()=="":
        messagebox.showerror("Error in input","Please fill the all Details")
        return
    else:
        item_id=item_id_entry.get()
        item_name=item_entry.get()
        price=price_entry.get()
        quantity=quantity_entry.get()
        subtototal=total_entry.get()
        db.insert_order_item(item_id,item_name,price,quantity,subtototal)
        display_ordered_items()
        get_gtotal()
        updatelabel()
        
    

def show_details():
    id_value = txtcode.get()
    result = db.get_item(id_value)
    
    if result:
        #print(result,type(result))
        item_id,name,price=result[0]
        item_id_entry.delete(0,tk.END)
        item_entry.delete(0, tk.END)
        price_entry.delete(0, tk.END)
        item_id_entry.insert(0,item_id)
        item_entry.insert(0,name)
        price_entry.insert(0,price)
        p=float(price)
        item_quantity=1
        tot=item_quantity*p
        quantity_entry.delete(0,tk.END)
        quantity_entry.insert(0,str(item_quantity))
        total_entry.delete(0,tk.END)
        total_entry.insert(0,str(tot))

def update_quantity():
    try:
        get_quantity=int(quantity_entry.get())
        get_price=float(price_entry.get())
        tot1=get_quantity*get_price
        total_entry.delete(0,tk.END)
        total_entry.insert(0,str(tot1))
    except ValueError:
        total_entry.delete(0,tk.END)
        total_entry.insert(0,"0")

def display_ordered_items():
    tv.delete(*tv.get_children())
    for row in db.get_ordered_items():
        tv.insert("",END,values=row)

def get_gtotal():
    gt = db.get_total()
    return gt

def updatelabel():
    gt = db.get_total()
    gv=gt[0]
    r='Rs.',str(gv)
    if total_label:
        total_label.config(text=r)
def order():
    _total=db.get_total()
    ft=_total[0]
    db.insert_order(ft)
    clear_treeview()
    txtcode.delete(0,tk.END)
    item_id_entry.delete(0,tk.END)
    item_entry.delete(0, tk.END)
    price_entry.delete(0,tk.END)
    quantity_entry.delete(0,tk.END)
    total_entry.delete(0,tk.END)

def clear_treeview():
    tv.delete(*tv.get_children())
    if total_label:
        total_label.config(text='Rs.0')


entries_frame=Frame(root,bg="#e6e6e6")
entries_frame.pack(side=TOP,fill=X)

#Item code
lname=tk.Label(entries_frame,text='Enter Item code:',font=("Calibri",18,"bold"),bg="#535c68",fg="white")
lname.grid(row=0,column=0,padx=10,pady=10,sticky='w')

txtcode=tk.Entry(entries_frame,textvariable=code,font=("calbri",16),width=20)
txtcode.grid(row=0,column=1,padx=10,pady=10,sticky='w')


#Item Name



item_label = tk.Label(entries_frame, text="Item Name:",font=("Calibri",18,"bold"),bg="#535c68",fg="white")
item_label.grid(row=1, column=0, padx=5, pady=10, sticky='w')

item_id_entry = tk.Entry(entries_frame,textvariable=item_id,font=("calbri",16),width=1)
item_id_entry.grid_remove()

item_entry = tk.Entry(entries_frame,textvariable=item_name,font=("calbri",16),width=15)
item_entry.grid(row=1, column=1, padx=10, pady=10, sticky='w')

#Item_Price
price_label = tk.Label(entries_frame, text="Price:",font=("Calibri",18,"bold"),bg="#535c68",fg="white")
price_label.grid(row=1, column=2, padx=10, pady=10, sticky='w')

price_entry = tk.Entry(entries_frame,textvariable=item_price,font=("calbri",16),width=10)
price_entry.grid(row=1, column=3, padx=10, pady=10, sticky='w')

#Item_Quantity
quantity_label = tk.Label(entries_frame, text="Quantity:",font=("Calibri",18,"bold"),bg="#535c68",fg="white")
quantity_label.grid(row=1, column=4, padx=10, pady=10, sticky='w')

quantity_entry = tk.Entry(entries_frame,textvariable=item_quantity,font=("calbri",16),width=10)
quantity_entry.grid(row=1, column=5, padx=10, pady=10, sticky='w' )

toata_label = tk.Label(entries_frame, text="Total:",font=("Calibri",18,"bold"),bg="#535c68",fg="white")
toata_label.grid(row=1, column=6, padx=10, pady=10, sticky='w')

total_entry = tk.Entry(entries_frame,textvariable=total,font=("calbri",16),width=10)
total_entry.grid(row=1, column=7, padx=10, pady=10, sticky='w' )



submit_button = tk.Button(entries_frame, command=save_item,text='Add Item',font=("Calibri",16,"bold"),bg="#535c68",fg="white")
submit_button.grid(row=1, column=8, padx=10, pady=10, sticky='w')

gtotal='Rs.',get_gtotal()
total_label = tk.Label(entries_frame, text=gtotal,font=('Ariel',16,'bold'), width=10, height=2, relief="solid",bg='#fff')
total_label.grid(row=2, column=8)

txtcode.bind("<KeyRelease>",lambda event: show_details())
quantity_entry.bind("<KeyRelease>",lambda event: update_quantity())

tree_frame= Frame(root,bg="#ecf0f1")
tree_frame.place(x=0,y=180,width=800,height=200)
style=ttk.Style()
style.configure("mystyle.Treeview",font=("calbri",14),borderwidth=2)
tv=ttk.Treeview(tree_frame,columns=("item_id","price","quantity","total"),show="headings",style="mystyle.Treeview")
tv.heading("item_id",text="ITEM")
tv.heading("price",text="PRICE")
tv.heading("quantity",text="QUANTITY")

tv.heading("total",text="TOTAL")
tv.pack()

buttom_frame=Frame(root,bg="#003366")


submit_button = tk.Button(buttom_frame, command=order,text='SUBMIT',font=("Calibri",16,"bold"),bg="#535c68",fg="white")
submit_button.grid(padx=50, pady=10, sticky='w')
buttom_frame.pack(side=BOTTOM,fill=X)
buttom_frame.pack()


display_ordered_items()



root.mainloop()

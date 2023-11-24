from flask import Flask, render_template, request, redirect, url_for
import json

app = Flask(__name__)

def show_items():
    with open('items.json', 'r') as myfile:
        return json.load(myfile)

def update_items(items):
    with open('items.json', 'w') as file:
        json.dump(items, file, indent=4)

@app.route('/')
def index():
   return redirect(url_for('display_items'))

@app.route('/list')
def display_items():
    items = show_items()
    return render_template('list.html', items=items)

@app.route('/add', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
            name = request.form['name']
            brand = request.form['brand']
            description = request.form['description'] 
            price = request.form['price']
            
            items = show_items()
            
            new_item = {'name': name, 'brand': brand, 'description': description, 'price': price}
            items.append(new_item)
            
            update_items(items)
            
            return redirect(url_for('display_items'))
    
    return render_template('additem.html') 


@app.route('/edit/<int:item_index>', methods=['GET', 'POST'])
def edit_item(item_index):
    items = show_items()
    if request.method == 'POST':
        items[item_index]['name'] = request.form['name']
        items[item_index]['brand'] = request.form['brand']
        items[item_index]['description'] = request.form['description']
        items[item_index]['price'] = request.form['price']
        update_items(items)
        return redirect(url_for('display_items'))
    return render_template('edit.html', item=items[item_index])



@app.route('/delete/<int:item_index>', methods=['GET', 'POST'])
def delete_item(item_index):
    items = show_items()
    del items[item_index]

    update_items(items)

    return redirect(url_for('display_items'))

    

if __name__ == '__main__':
    app.debug = True
    app.run()
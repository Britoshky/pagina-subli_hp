from flask import Blueprint, render_template, request, redirect, url_for
from utils.data_utils import load_data, save_data
from utils.image_utils import convert_to_webp
from utils.pagination_utils import generate_pagination
import os

def create_category_blueprint(category, json_file, upload_folder):
    bp = Blueprint(category, __name__, url_prefix=f'/{category}')

    @bp.route('/update_stock/<int:item_id>/<action>', methods=['GET'])
    def update_stock(item_id, action):
        items = load_data(json_file)
        for item in items:
            if item['id'] == item_id:
                if action == 'add':
                    item['quantity'] += 1
                elif action == 'subtract' and item['quantity'] > 0:
                    item['quantity'] -= 1
                save_data(json_file, items)
                break
        return redirect(url_for(f'{category}.list_items'))

    @bp.route('/')
    def list_items():
        items = load_data(json_file)
        search_query = request.args.get('search', '').lower()
        page = int(request.args.get('page', 1))
        items_per_page = 10

        if search_query:
            filtered_items = [item for item in items if search_query in item['name'].lower()]
        else:
            filtered_items = sorted(items, key=lambda x: x['name'])

        total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page
        paginated_items = filtered_items[start_index:end_index]

        pagination = generate_pagination(page, total_pages)

        return render_template(
            'items.html',
            items=paginated_items,
            search_query=search_query,
            page=page,
            total_pages=total_pages,
            pagination=pagination,
            category=category
        )

    @bp.route('/add', methods=['GET', 'POST'])
    def add_item():
        items = load_data(json_file)
        if request.method == 'POST':
            name = request.form['name']
            quantity = int(request.form['quantity'])
            image = request.files['image']
            if image:
                # Crear la carpeta de subida si no existe
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)
                
                # Guardar la imagen
                filename = os.path.join(upload_folder, image.filename)
                image.save(filename)
                webp_filename = convert_to_webp(filename, upload_folder)
            else:
                webp_filename = None

            # Agregar nuevo elemento
            new_item = {
                'id': len(items) + 1,
                'name': name,
                'quantity': quantity,
                'image_filename': os.path.basename(webp_filename) if webp_filename else None
            }
            items.append(new_item)
            save_data(json_file, items)
            return redirect(url_for(f'{category}.list_items'))
        return render_template('add.html', category=category)



    @bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
    def edit_item(item_id):
        items = load_data(json_file)
        item_to_edit = next((item for item in items if item['id'] == item_id), None)
        if not item_to_edit:
            return redirect(url_for(f'{category}.list_items'))
        if request.method == 'POST':
            item_to_edit['name'] = request.form['name']
            item_to_edit['quantity'] = int(request.form['quantity'])
            save_data(json_file, items)
            return redirect(url_for(f'{category}.list_items'))
        return render_template('edit.html', item=item_to_edit, category=category)

    @bp.route('/delete/<int:item_id>', methods=['GET'])
    def delete_item(item_id):
        items = load_data(json_file)
        item_to_delete = next((item for item in items if item['id'] == item_id), None)
        if item_to_delete:
            if item_to_delete['image_filename']:
                image_path = os.path.join(upload_folder, item_to_delete['image_filename'])
                if os.path.exists(image_path):
                    os.remove(image_path)
            items.remove(item_to_delete)
            save_data(json_file, items)
        return redirect(url_for(f'{category}.list_items'))

    return bp

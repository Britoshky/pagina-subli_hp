from flask import Blueprint, render_template, request, redirect, url_for
from utils.data_utils import load_data, save_data
from utils.image_utils import convert_to_webp
from utils.pagination_utils import generate_pagination
from urllib.parse import urlparse, parse_qs

import os


def create_category_blueprint(category, json_file, upload_folder):
    # Crear el blueprint dinámico para la categoría
    bp = Blueprint(category, __name__, url_prefix=f'/{category}')

    @bp.route('/update_stock/<int:item_id>/<action>', methods=['GET'])
    def update_stock(item_id, action):
        # Cargar los datos del archivo JSON específico de la categoría
        items = load_data(json_file)
        for item in items:
            if item['id'] == item_id:
                if action == 'add':
                    item['quantity'] += 1
                elif action == 'subtract' and item['quantity'] > 0:
                    item['quantity'] -= 1
                # Guardar los cambios en el archivo JSON
                save_data(json_file, items)
                break

        # Obtener la URL de referencia y procesar los parámetros actuales
        referrer = request.referrer or url_for(f'{category}.list_items')
        parsed_url = urlparse(referrer)
        parsed_query = parse_qs(parsed_url.query)
        
        # Mantener los parámetros de búsqueda, filtro y paginación
        search = parsed_query.get('search', [''])[0]
        filter_option = parsed_query.get('filter', ['todos'])[0]
        page = int(parsed_query.get('page', [1])[0])

        # Redirigir con los parámetros intactos
        return redirect(url_for(f'{category}.list_items', search=search, filter=filter_option, page=page))


    @bp.route('/')
    def list_items():
        # Cargar los datos desde el archivo JSON
        items = load_data(json_file)

        # Contadores de stock
        total_types = len(items)  # Cantidad total de tipos de productos
        total_in_stock_units = sum(item['quantity'] for item in items if item['quantity'] > 0)  # Suma total de unidades disponibles
        total_out_of_stock_types = len([item for item in items if item['quantity'] == 0])  # Número de productos sin stock

        # Obtener parámetros de búsqueda, filtro y paginación
        search_query = request.args.get('search', '').lower()
        filter_option = request.args.get('filter', 'todos')
        try:
            page = int(request.args.get('page', 1))
        except ValueError:
            page = 1
        items_per_page = 10

        # Filtrar los elementos según la opción seleccionada
        if filter_option == 'vendidos':
            filtered_items = [item for item in items if item['quantity'] == 0]
        elif filter_option == 'en-stock':
            filtered_items = [item for item in items if item['quantity'] > 0]
        else:
            filtered_items = items

        # Aplicar búsqueda si existe un query
        if search_query:
            filtered_items = [
                item for item in filtered_items if search_query in item['name'].lower()
            ]

        # Ordenar los elementos alfabéticamente por nombre
        filtered_items = sorted(filtered_items, key=lambda x: x['name'])

        # Calcular el índice de inicio y fin para la paginación
        total_pages = (len(filtered_items) + items_per_page - 1) // items_per_page
        start_index = (page - 1) * items_per_page
        end_index = start_index + items_per_page

        # Generar los elementos para la página actual
        paginated_items = filtered_items[start_index:end_index]

        # Generar el control de paginación
        pagination = generate_pagination(page, total_pages)

        # Renderizar la plantilla con los datos necesarios
        return render_template(
            'items.html',
            items=paginated_items,
            search_query=search_query,
            page=page,
            total_pages=total_pages,
            pagination=pagination,
            category=category,
            filter_option=filter_option,
            total_types=total_types,
            total_in_stock_units=total_in_stock_units,
            total_out_of_stock_types=total_out_of_stock_types
        )



    @bp.route('/add', methods=['GET', 'POST'])
    def add_item():
        # Ruta para agregar un nuevo elemento
        items = load_data(json_file)

        if request.method == 'POST':
            name = request.form['name']
            quantity = int(request.form.get('quantity', 0))  # Por defecto, la cantidad será 0
            image = request.files['image']

            # Procesar la imagen si se sube una
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

            # Calcular el próximo id correlativo
            next_id = max([item['id'] for item in items], default=0) + 1
            new_item = {
                'id': next_id,
                'name': name,
                'quantity': quantity,
                'image_filename': os.path.basename(webp_filename) if webp_filename else None
            }
            items.append(new_item)

            # Ordenar la lista de elementos alfabéticamente para determinar la página del nuevo elemento
            items = sorted(items, key=lambda x: x['name'].lower())
            save_data(json_file, items)

            # Encontrar la posición del nuevo elemento en la lista ordenada
            item_index = next((index for index, item in enumerate(items) if item['id'] == new_item['id']), 0)

            # Calcular en qué página está el elemento
            items_per_page = 10
            page = (item_index // items_per_page) + 1

            # Tomar los parámetros desde el formulario si existen, si no, usar los de la URL
            search = request.form.get('search', request.args.get('search', ''))
            filter_option = request.form.get('filter', request.args.get('filter', 'todos'))
            # Redirigir a la página donde se encuentra el nuevo elemento
            return redirect(url_for(f'{category}.list_items', page=page, search=search, filter=filter_option))

        return render_template('add.html', category=category)


    @bp.route('/edit/<int:item_id>', methods=['GET', 'POST'])
    def edit_item(item_id):
        # Cargar los datos del archivo JSON
        items = load_data(json_file)
        item_to_edit = next((item for item in items if item['id'] == item_id), None)

        if not item_to_edit:
            return redirect(url_for(f'{category}.list_items'))

        if request.method == 'POST':
            # Actualizar el nombre
            item_to_edit['name'] = request.form['name']

            # Actualizar la cantidad
            item_to_edit['quantity'] = int(request.form.get('quantity', 0))

            # Actualizar la imagen si se sube una nueva
            image = request.files.get('image')
            if image:
                # Eliminar la imagen anterior si existe
                if item_to_edit.get('image_filename'):
                    old_image_path = os.path.join(upload_folder, item_to_edit['image_filename'])
                    if os.path.exists(old_image_path):
                        os.remove(old_image_path)

                # Guardar la nueva imagen
                if not os.path.exists(upload_folder):
                    os.makedirs(upload_folder)

                new_filename = os.path.join(upload_folder, image.filename)
                image.save(new_filename)

                # Convertir la imagen a formato webp (opcional)
                webp_filename = convert_to_webp(new_filename, upload_folder)

                # Actualizar el nombre de archivo en el JSON
                item_to_edit['image_filename'] = os.path.basename(webp_filename) if webp_filename else os.path.basename(new_filename)

            # Guardar los cambios en el archivo JSON
            save_data(json_file, items)

            # Tomar los parámetros desde el formulario si existen, si no, usar los de la URL
            # Tomar los parámetros desde el formulario si existen, si no, usar los de la URL
            search = request.form.get('search', request.args.get('search', ''))
            filter_option = request.form.get('filter', request.args.get('filter', 'todos'))

            # Calcular la página exacta donde está el ítem editado
            items_per_page = 10
            filtered_items = items
            if filter_option == 'vendidos':
                filtered_items = [item for item in items if item['quantity'] == 0]
            elif filter_option == 'en-stock':
                filtered_items = [item for item in items if item['quantity'] > 0]
            if search:
                filtered_items = [item for item in filtered_items if search.lower() in item['name'].lower()]
            filtered_items = sorted(filtered_items, key=lambda x: x['name'])
            item_index = next((index for index, item in enumerate(filtered_items) if item['id'] == item_to_edit['id']), 0)
            page = (item_index // items_per_page) + 1

            # Redirigir a la página exacta del ítem editado
            return redirect(url_for(f'{category}.list_items', search=search, filter=filter_option, page=page))

        return render_template('edit.html', item=item_to_edit, category=category)

    @bp.route('/reset_stock', methods=['POST'])
    def reset_stock():
        # Cargar los datos del archivo JSON específico de la categoría
        items = load_data(json_file)

        # Establecer la cantidad en 0 para todos los productos
        for item in items:
            item['quantity'] = 0

        # Guardar los cambios en el archivo JSON
        save_data(json_file, items)

        # Redirigir a la lista con los parámetros actuales
        search = request.args.get('search', '')
        filter_option = request.args.get('filter', 'todos')
        page = int(request.args.get('page', 1))

        return redirect(url_for(f'{category}.list_items', search=search, filter=filter_option, page=page))

    @bp.route('/delete/<int:item_id>', methods=['GET'])
    def delete_item(item_id):
        # Ruta para eliminar un elemento
        items = load_data(json_file)
        item_to_delete = next((item for item in items if item['id'] == item_id), None)
        if item_to_delete:
            if item_to_delete['image_filename']:
                image_path = os.path.join(upload_folder, item_to_delete['image_filename'])
                if os.path.exists(image_path):
                    os.remove(image_path)
            items.remove(item_to_delete)
            save_data(json_file, items)
        search = request.args.get('search', '')
        filter_option = request.args.get('filter', 'todos')
        page = request.args.get('page', 1)
        return redirect(url_for(f'{category}.list_items', search=search, filter=filter_option, page=page))

    return bp

    
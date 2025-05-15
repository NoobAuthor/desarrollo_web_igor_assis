from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import joinedload
import os
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.secret_key = 'supersecretkey'  # Needed for flash messages

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'fotos')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

from models import db

db.init_app(app)

from models import Actividad, Comuna, Foto, ActividadTema, Region, ContactarPor

@app.route('/')
def home():
    actividades = (
        db.session.query(Actividad)
        .options(joinedload(Actividad.comuna), joinedload(Actividad.fotos), joinedload(Actividad.temas))
        .order_by(Actividad.id.desc())
        .limit(5)
        .all()
    )
    actividades_data = []
    for act in actividades:
        tema = act.temas[0].tema if act.temas else '-'
        foto_url = None
        if act.fotos:
            foto_url = '/static/fotos/' + act.fotos[0].nombre_archivo
        actividades_data.append({
            'dia_hora_inicio': act.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
            'dia_hora_termino': act.dia_hora_termino.strftime('%Y-%m-%d %H:%M') if act.dia_hora_termino else None,
            'comuna_nombre': act.comuna.nombre,
            'sector': act.sector,
            'tema': tema,
            'foto_url': foto_url
        })
    return render_template('index.html', actividades=actividades_data)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    regiones = Region.query.order_by(Region.nombre).all()
    comunas = []
    selected_region = None
    selected_comuna = None
    errors = []
    if request.method == 'POST':
        # Get form data
        region_id = request.form.get('region')
        comuna_id = request.form.get('comuna')
        sector = request.form.get('sector')
        nombre = request.form.get('nombre')
        email = request.form.get('email')
        celular = request.form.get('celular')
        contactos = request.form.getlist('contactar_por[]')
        contacto_ids = request.form.getlist('contacto_id[]')
        inicio = request.form.get('inicio')
        termino = request.form.get('termino')
        descripcion = request.form.get('descripcion')
        tema = request.form.get('tema')
        tema_otro = request.form.get('tema_otro')
        fotos = request.files.getlist('fotos')
        # Validation
        if not region_id:
            errors.append('Debe seleccionar una región.')
        if not comuna_id:
            errors.append('Debe seleccionar una comuna.')
        if not nombre:
            errors.append('El nombre es obligatorio.')
        if not email or '@' not in email:
            errors.append('Email inválido.')
        if celular and not celular.startswith('+'):
            errors.append('Celular debe ser +NNN.NNNNNNNN.')
        if not inicio:
            errors.append('Fecha de inicio es obligatoria.')
        if tema == 'otro' and (not tema_otro or len(tema_otro) < 3 or len(tema_otro) > 15):
            errors.append('Tema "otro" debe tener entre 3 y 15 caracteres.')
        if not tema:
            errors.append('Debe seleccionar un tema.')
        if not fotos or not any(f.filename for f in fotos):
            errors.append('Debe subir al menos una foto.')
        # Validate contacts
        for c, cid in zip(contactos, contacto_ids):
            if c and (len(cid) < 4 or len(cid) > 50):
                errors.append('ID de contacto debe tener entre 4 y 50 caracteres.')
        # Validate termino > inicio
        try:
            dt_inicio = datetime.strptime(inicio, '%Y-%m-%dT%H:%M')
            dt_termino = None
            if termino:
                dt_termino = datetime.strptime(termino, '%Y-%m-%dT%H:%M')
                if dt_termino <= dt_inicio:
                    errors.append('Fecha de término debe ser mayor que la de inicio.')
        except Exception:
            errors.append('Formato de fecha inválido.')
        # If errors, re-render form
        selected_region = int(region_id) if region_id else None
        selected_comuna = int(comuna_id) if comuna_id else None
        if selected_region:
            comunas = Comuna.query.filter_by(region_id=selected_region).order_by(Comuna.nombre).all()
        if errors:
            return render_template('agregar.html', regiones=regiones, comunas=comunas, errors=errors, selected_region=selected_region, selected_comuna=selected_comuna)
        # Insert into DB
        actividad = Actividad(
            comuna_id=comuna_id,
            sector=sector,
            nombre=nombre,
            email=email,
            celular=celular,
            dia_hora_inicio=dt_inicio,
            dia_hora_termino=dt_termino,
            descripcion=descripcion
        )
        db.session.add(actividad)
        db.session.commit()
        # Temas
        if tema == 'otro':
            tema_obj = ActividadTema(tema=tema, glosa_otro=tema_otro, actividad_id=actividad.id)
        else:
            tema_obj = ActividadTema(tema=tema, actividad_id=actividad.id)
        db.session.add(tema_obj)
        # Contactos
        for c, cid in zip(contactos, contacto_ids):
            if c and cid:
                db.session.add(ContactarPor(nombre=c, identificador=cid, actividad_id=actividad.id))
        # Fotos
        for f in fotos:
            if f and f.filename:
                filename = secure_filename(f.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(save_path)
                db.session.add(Foto(ruta_archivo=save_path, nombre_archivo=filename, actividad_id=actividad.id))
        db.session.commit()
        flash('Actividad agregada exitosamente.')
        return redirect(url_for('home'))
    # GET
    region_id = request.args.get('region')
    if region_id:
        comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
        selected_region = int(region_id)
    return render_template('agregar.html', regiones=regiones, comunas=comunas, errors=errors, selected_region=selected_region, selected_comuna=selected_comuna)

@app.route('/listado')
def listado():
    page = request.args.get('page', 1, type=int)
    per_page = 5
    actividades_query = (
        db.session.query(Actividad)
        .options(joinedload(Actividad.comuna), joinedload(Actividad.fotos), joinedload(Actividad.temas))
        .order_by(Actividad.id.desc())
    )
    actividades_pag = actividades_query.paginate(page=page, per_page=per_page, error_out=False)
    actividades_data = []
    for act in actividades_pag.items:
        tema = act.temas[0].tema if act.temas else '-'
        actividades_data.append({
            'id': act.id,
            'dia_hora_inicio': act.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
            'dia_hora_termino': act.dia_hora_termino.strftime('%Y-%m-%d %H:%M') if act.dia_hora_termino else None,
            'comuna_nombre': act.comuna.nombre,
            'sector': act.sector,
            'tema': tema,
            'nombre': act.nombre,
            'total_fotos': len(act.fotos)
        })
    return render_template('listado.html', actividades=actividades_data, page=page, has_next=actividades_pag.has_next)

@app.route('/actividad/<int:actividad_id>')
def detalle(actividad_id):
    act = (
        db.session.query(Actividad)
        .options(joinedload(Actividad.comuna), joinedload(Actividad.fotos), joinedload(Actividad.temas), joinedload(Actividad.contactos))
        .filter(Actividad.id == actividad_id)
        .first_or_404()
    )
    tema = act.temas[0].tema if act.temas else '-'
    glosa_otro = act.temas[0].glosa_otro if act.temas and act.temas[0].tema == 'otro' else None
    fotos = ['/static/fotos/' + f.nombre_archivo for f in act.fotos]
    contactos = [{'nombre': c.nombre, 'identificador': c.identificador} for c in act.contactos]
    return render_template('detalle.html', actividad=act, tema=tema, glosa_otro=glosa_otro, fotos=fotos, contactos=contactos)

@app.route('/comunas/<int:region_id>')
def comunas_por_region(region_id):
    comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
    comunas_data = [{'id': c.id, 'nombre': c.nombre} for c in comunas]
    return jsonify(comunas_data)

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

if __name__ == '__main__':
    app.run(debug=True) 
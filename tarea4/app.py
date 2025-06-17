from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_wtf.csrf import CSRFProtect
from sqlalchemy.orm import joinedload
from sqlalchemy import func, extract
import os
from datetime import datetime
from werkzeug.utils import secure_filename
from models import Actividad, Comuna, Foto, ActividadTema, Region, ContactarPor, Comentario, Nota, db
app = Flask(__name__)
app.secret_key = 'supersecretkey'
csrf = CSRFProtect(app)

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://cc5002:programacionweb@localhost:3306/tarea2'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['UPLOAD_FOLDER'] = os.path.join('static', 'fotos')

if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

db.init_app(app)

@app.route('/')
def home():
    actividades = (
        db.session.query(Actividad)
        .options(joinedload(Actividad.comuna), joinedload(Actividad.fotos), joinedload(Actividad.temas), joinedload(Actividad.notas))
        .order_by(Actividad.id.desc())
        .limit(5)
        .all()
    )
    actividades_data = []
    for act in actividades:
        tema = act.temas[0].tema if act.temas else '-'
        foto_url = f'/static/fotos/{act.fotos[0].nombre_archivo}' if act.fotos else None

        # Calcular promedio de notas
        promedio_nota = 0
        total_notas = 0
        if act.notas:
            total_notas = len(act.notas)
            promedio_nota = sum(n.nota for n in act.notas) / total_notas

        actividades_data.append({
            'id': act.id,
            'dia_hora_inicio': act.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
            'dia_hora_termino': act.dia_hora_termino.strftime('%Y-%m-%d %H:%M') if act.dia_hora_termino else None,
            'comuna_nombre': act.comuna.nombre,
            'sector': act.sector,
            'tema': tema,
            'foto_url': foto_url,
            'promedio_nota': round(promedio_nota, 1) if promedio_nota > 0 else 0,
            'total_notas': total_notas
        })
    return render_template('index.html', actividades=actividades_data)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar():
    regiones = Region.query.order_by(Region.nombre).all()
    comunas = []
    selected_region = selected_comuna = None
    errors = []
    if request.method == 'POST':
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

        # Validaciones
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
        for c, cid in zip(contactos, contacto_ids):
            if c and (len(cid) < 4 or len(cid) > 50):
                errors.append('ID de contacto debe tener entre 4 y 50 caracteres.')
        try:
            dt_inicio = datetime.strptime(inicio, '%Y-%m-%dT%H:%M')
            dt_termino = None
            if termino:
                dt_termino = datetime.strptime(termino, '%Y-%m-%dT%H:%M')
                if dt_termino <= dt_inicio:
                    errors.append('Fecha de término debe ser mayor que la de inicio.')
        except Exception:
            errors.append('Formato de fecha inválido.')

        selected_region = int(region_id) if region_id else None
        selected_comuna = int(comuna_id) if comuna_id else None
        if selected_region:
            comunas = Comuna.query.filter_by(region_id=selected_region).order_by(Comuna.nombre).all()
        if errors:
            return render_template('agregar.html', regiones=regiones, comunas=comunas, errors=errors, selected_region=selected_region, selected_comuna=selected_comuna)

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
        if tema == 'otro':
            tema_obj = ActividadTema(tema=tema, glosa_otro=tema_otro, actividad_id=actividad.id)
        else:
            tema_obj = ActividadTema(tema=tema, actividad_id=actividad.id)
        db.session.add(tema_obj)
        for c, cid in zip(contactos, contacto_ids):
            if c and cid:
                db.session.add(ContactarPor(nombre=c, identificador=cid, actividad_id=actividad.id))
        for f in fotos:
            if f and f.filename:
                filename = secure_filename(f.filename)
                save_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                f.save(save_path)
                db.session.add(Foto(ruta_archivo=save_path, nombre_archivo=filename, actividad_id=actividad.id))
        db.session.commit()
        flash('Actividad agregada exitosamente.')
        return redirect(url_for('home'))
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
        .options(joinedload(Actividad.comuna), joinedload(Actividad.fotos), joinedload(Actividad.temas), joinedload(Actividad.notas))
        .order_by(Actividad.id.desc())
    )
    actividades_pag = actividades_query.paginate(page=page, per_page=per_page, error_out=False)
    actividades_data = []
    for act in actividades_pag.items:
        tema = act.temas[0].tema if act.temas else '-'

        # Calcular promedio de notas
        promedio_nota = 0
        total_notas = 0
        if act.notas:
            total_notas = len(act.notas)
            promedio_nota = sum(n.nota for n in act.notas) / total_notas

        actividades_data.append({
            'id': act.id,
            'dia_hora_inicio': act.dia_hora_inicio.strftime('%Y-%m-%d %H:%M'),
            'dia_hora_termino': act.dia_hora_termino.strftime('%Y-%m-%d %H:%M') if act.dia_hora_termino else None,
            'comuna_nombre': act.comuna.nombre,
            'sector': act.sector,
            'tema': tema,
            'nombre': act.nombre,
            'total_fotos': len(act.fotos),
            'promedio_nota': round(promedio_nota, 1) if promedio_nota > 0 else 0,
            'total_notas': total_notas
        })
    return render_template('listado.html', actividades=actividades_data, page=page, has_next=actividades_pag.has_next)

@app.route('/actividad/<int:actividad_id>')
def detalle(actividad_id):
    act = (
        db.session.query(Actividad)
        .options(joinedload(Actividad.comuna), joinedload(Actividad.fotos), joinedload(Actividad.temas), joinedload(Actividad.contactos), joinedload(Actividad.notas))
        .filter(Actividad.id == actividad_id)
        .first_or_404()
    )
    tema = act.temas[0].tema if act.temas else '-'
    glosa_otro = act.temas[0].glosa_otro if act.temas and act.temas[0].tema == 'otro' else None
    fotos = [f'/static/fotos/{f.nombre_archivo}' for f in act.fotos]
    contactos = [{'nombre': c.nombre, 'identificador': c.identificador} for c in act.contactos]
    return render_template('detalle.html', actividad=act, tema=tema, glosa_otro=glosa_otro, fotos=fotos, contactos=contactos)

@app.route('/comunas/<int:region_id>')
def comunas_por_region(region_id):
    comunas = Comuna.query.filter_by(region_id=region_id).order_by(Comuna.nombre).all()
    return jsonify([{'id': c.id, 'nombre': c.nombre} for c in comunas])

@app.route('/estadisticas')
def estadisticas():
    return render_template('estadisticas.html')

# --- API para comentarios (AJAX) ---

@app.route('/api/comentarios/<int:actividad_id>', methods=['GET'])
def obtener_comentarios(actividad_id):
    try:
        comentarios = Comentario.query.filter_by(actividad_id=actividad_id).order_by(Comentario.fecha.desc()).all()
        return jsonify({
            'success': True,
            'data': [{
                'nombre': c.nombre,
                'texto': c.texto,
                'fecha': c.fecha.strftime('%Y-%m-%d %H:%M')
            } for c in comentarios]
        })
    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error al obtener comentarios'
        }), 500

@app.route('/api/comentarios/<int:actividad_id>', methods=['POST'])
def agregar_comentario(actividad_id):
    try:
        data = request.get_json()
        nombre = data.get('nombre', '').strip()
        texto = data.get('texto', '').strip()
        errores = []

        if not (3 <= len(nombre) <= 80):
            errores.append('El nombre debe tener entre 3 y 80 caracteres.')
        if len(texto) < 5:
            errores.append('El comentario debe tener al menos 5 caracteres.')

        if errores:
            return jsonify({
                'success': False,
                'error': '\n'.join(errores)
            }), 400

        comentario = Comentario(
            nombre=nombre,
            texto=texto,
            fecha=datetime.now(),
            actividad_id=actividad_id
        )
        db.session.add(comentario)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error al guardar el comentario'
        }), 500

# --- API para notas (AJAX) ---

@app.route('/api/notas/<int:actividad_id>', methods=['POST'])
def agregar_nota(actividad_id):
    try:
        data = request.get_json()
        nota_valor = data.get('nota')

        if not nota_valor or not (1 <= int(nota_valor) <= 5):
            return jsonify({
                'success': False,
                'error': 'La nota debe ser un número entre 1 y 5'
            }), 400

        # Verificar que la actividad existe
        actividad = Actividad.query.get(actividad_id)
        if not actividad:
            return jsonify({
                'success': False,
                'error': 'Actividad no encontrada'
            }), 404

        nota = Nota(
            actividad_id=actividad_id,
            nota=int(nota_valor)
        )
        db.session.add(nota)
        db.session.commit()

        return jsonify({'success': True})

    except Exception as e:
        db.session.rollback()
        return jsonify({
            'success': False,
            'error': 'Error al guardar la nota'
        }), 500

@app.route('/api/notas/<int:actividad_id>', methods=['GET'])
def obtener_promedio_notas(actividad_id):
    try:
        notas = Nota.query.filter_by(actividad_id=actividad_id).all()
        if not notas:
            return jsonify({
                'success': True,
                'promedio': 0,
                'total_notas': 0
            })

        promedio = sum(n.nota for n in notas) / len(notas)
        return jsonify({
            'success': True,
            'promedio': round(promedio, 1),
            'total_notas': len(notas)
        })

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error al obtener las notas'
        }), 500

# --- API para estadísticas (AJAX) ---

@app.route('/api/estadisticas/actividades_por_dia')
def actividades_por_dia():
    datos = (
        db.session.query(
            func.date(Actividad.dia_hora_inicio).label('dia'),
            func.count(Actividad.id)
        )
        .group_by('dia')
        .order_by('dia')
        .all()
    )
    return jsonify([{'dia': str(dia), 'cantidad': cantidad} for dia, cantidad in datos])

@app.route('/api/estadisticas/actividades_por_tipo')
def actividades_por_tipo():
    datos = (
        db.session.query(
            ActividadTema.tema,
            func.count(ActividadTema.id)
        )
        .group_by(ActividadTema.tema)
        .all()
    )
    return jsonify([{'tema': tema, 'cantidad': cantidad} for tema, cantidad in datos])

@app.route('/api/estadisticas/actividades_por_horario_mes')
def actividades_por_horario_mes():
    def horario(dt):
        h = dt.hour
        if h < 12:
            return 'mañana'
        elif h < 18:
            return 'mediodía'
        else:
            return 'tarde'
    datos = (
        db.session.query(
            extract('month', Actividad.dia_hora_inicio).label('mes'),
            Actividad.dia_hora_inicio,
        )
        .all()
    )
    conteo = {}
    for mes, dt in datos:
        if mes not in conteo:
            conteo[mes] = {'mañana': 0, 'mediodía': 0, 'tarde': 0}
        franja = horario(dt)
        conteo[mes][franja] += 1
    resultado = []
    for mes in sorted(conteo.keys()):
        resultado.append({
            'mes': int(mes),
            'mañana': conteo[mes]['mañana'],
            'mediodía': conteo[mes]['mediodía'],
            'tarde': conteo[mes]['tarde']
        })
    return jsonify(resultado)

@app.route('/api/estadisticas/promedio_notas')
def promedio_notas_general():
    try:
        # Obtener promedio de notas por actividad
        subquery = (
            db.session.query(
                Nota.actividad_id,
                func.avg(Nota.nota).label('promedio_actividad')
            )
            .group_by(Nota.actividad_id)
            .subquery()
        )

        # Obtener actividades con sus promedios
        datos = (
            db.session.query(
                Actividad.id,
                Actividad.nombre,
                subquery.c.promedio_actividad
            )
            .join(subquery, Actividad.id == subquery.c.actividad_id)
            .order_by(subquery.c.promedio_actividad.desc())
            .all()
        )

        return jsonify([{
            'actividad_id': actividad_id,
            'nombre': nombre,
            'promedio': round(float(promedio), 1)
        } for actividad_id, nombre, promedio in datos])

    except Exception as e:
        return jsonify({
            'success': False,
            'error': 'Error al obtener estadísticas de notas'
        }), 500

if __name__ == '__main__':
    app.run(debug=True)

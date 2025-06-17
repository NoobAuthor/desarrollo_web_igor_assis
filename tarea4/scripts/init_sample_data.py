#!/usr/bin/env python3
"""
Script to initialize sample data for testing the rating system
Run this after setting up the database to populate with test data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app import app, db
from models import Actividad, Comuna, Region, Foto, ActividadTema, ContactarPor, Comentario, Nota
from datetime import datetime, timedelta
import os

def init_sample_data():
    with app.app_context():
        # Check if we already have activities
        if Actividad.query.count() > 0:
            print("Database already has activities. Skipping sample data creation.")
            return

        # Get some regions and comunas (assuming they exist from region-comuna.sql)
        region_rm = Region.query.filter_by(id=13).first()  # Región Metropolitana
        region_valpo = Region.query.filter_by(id=5).first()  # Región de Valparaíso

        if not region_rm or not region_valpo:
            print("Regions not found. Please run region-comuna.sql first.")
            return

        comuna_santiago = Comuna.query.filter_by(region_id=13, nombre='Santiago').first()
        comuna_providencia = Comuna.query.filter_by(region_id=13, nombre='Providencia').first()
        comuna_vina = Comuna.query.filter_by(region_id=5, nombre='Viña del Mar').first()

        if not all([comuna_santiago, comuna_providencia, comuna_vina]):
            print("Required comunas not found. Please run region-comuna.sql first.")
            return

        # Create sample activities
        activities_data = [
            {
                'comuna_id': comuna_santiago.id,
                'sector': 'Centro',
                'nombre': 'Juan Pérez',
                'email': 'juan.perez@email.com',
                'celular': '+569.12345678',
                'dia_hora_inicio': datetime.now() + timedelta(days=1),
                'dia_hora_termino': datetime.now() + timedelta(days=1, hours=3),
                'descripcion': 'Taller de música para principiantes. Aprende a tocar guitarra básica.',
                'tema': 'música'
            },
            {
                'comuna_id': comuna_providencia.id,
                'sector': 'Providencia Centro',
                'nombre': 'María González',
                'email': 'maria.gonzalez@email.com',
                'celular': '+569.87654321',
                'dia_hora_inicio': datetime.now() + timedelta(days=2),
                'dia_hora_termino': datetime.now() + timedelta(days=2, hours=2),
                'descripcion': 'Clase de yoga para relajarse y ejercitarse. Todos los niveles bienvenidos.',
                'tema': 'deporte'
            },
            {
                'comuna_id': comuna_vina.id,
                'sector': 'Reñaca',
                'nombre': 'Carlos Rodríguez',
                'email': 'carlos.rodriguez@email.com',
                'celular': '+569.11223344',
                'dia_hora_inicio': datetime.now() + timedelta(days=3),
                'dia_hora_termino': datetime.now() + timedelta(days=3, hours=4),
                'descripcion': 'Taller de cocina mediterránea. Aprende a preparar platos saludables.',
                'tema': 'comida'
            },
            {
                'comuna_id': comuna_santiago.id,
                'sector': 'Plaza de Armas',
                'nombre': 'Ana Silva',
                'email': 'ana.silva@email.com',
                'celular': '+569.55667788',
                'dia_hora_inicio': datetime.now() + timedelta(days=4),
                'dia_hora_termino': datetime.now() + timedelta(days=4, hours=3),
                'descripcion': 'Charla sobre tecnología y programación para jóvenes interesados.',
                'tema': 'tecnología'
            },
            {
                'comuna_id': comuna_providencia.id,
                'sector': 'Manuel Montt',
                'nombre': 'Diego Morales',
                'email': 'diego.morales@email.com',
                'celular': '+569.99887766',
                'dia_hora_inicio': datetime.now() + timedelta(days=5),
                'dia_hora_termino': datetime.now() + timedelta(days=5, hours=2),
                'descripcion': 'Sesión de juegos de mesa para toda la familia. Diversión garantizada.',
                'tema': 'juegos'
            }
        ]

        print("Creating sample activities...")
        for i, activity_data in enumerate(activities_data, 1):
            # Create activity
            actividad = Actividad(**activity_data)
            db.session.add(actividad)
            db.session.flush()  # Get the ID

            # Add tema
            tema = ActividadTema(
                tema=activity_data['tema'],
                actividad_id=actividad.id
            )
            db.session.add(tema)

            # Add contact method
            contacto = ContactarPor(
                nombre='whatsapp',
                identificador=f'@user{i}',
                actividad_id=actividad.id
            )
            db.session.add(contacto)

            # Add sample comments
            comentarios_data = [
                {
                    'nombre': f'Usuario{i}A',
                    'texto': f'Excelente actividad, muy recomendada para {activity_data["tema"]}.',
                    'fecha': datetime.now() - timedelta(hours=i),
                    'actividad_id': actividad.id
                },
                {
                    'nombre': f'Usuario{i}B',
                    'texto': f'Me gustó mucho la actividad de {activity_data["tema"]}. Volveré a participar.',
                    'fecha': datetime.now() - timedelta(hours=i-1),
                    'actividad_id': actividad.id
                }
            ]

            for comentario_data in comentarios_data:
                comentario = Comentario(**comentario_data)
                db.session.add(comentario)

            # Add sample ratings
            notas_data = [
                {'nota': 5, 'actividad_id': actividad.id},
                {'nota': 4, 'actividad_id': actividad.id},
                {'nota': 5, 'actividad_id': actividad.id},
                {'nota': 3, 'actividad_id': actividad.id},
                {'nota': 4, 'actividad_id': actividad.id}
            ]

            for nota_data in notas_data:
                nota = Nota(**nota_data)
                db.session.add(nota)

            print(f"Created activity {i}: {actividad.nombre}")

        try:
            db.session.commit()
            print("Sample data created successfully!")
            print("\nSample activities created:")
            for activity in Actividad.query.all():
                avg_rating = sum(n.nota for n in activity.notas) / len(activity.notas) if activity.notas else 0
                print(f"- {activity.nombre}: {activity.descripcion[:50]}... (Rating: {avg_rating:.1f}/5)")

        except Exception as e:
            db.session.rollback()
            print(f"Error creating sample data: {e}")

if __name__ == '__main__':
    print("Initializing sample data for testing...")
    init_sample_data()

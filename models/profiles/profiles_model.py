from flask import jsonify, request
from models.connection import supabase
from datetime import datetime, timedelta

class ProfilesModel():
    def get_profiles_by_account(self, account_id):
        profiles_resp = supabase.table("PROFILES").select("*").eq("cuenta_id", account_id).execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": profiles_resp.data
        }), 200

    def get_profile_by_id(self, profile_id):
        profile_resp = supabase.table("PROFILES").select("*").eq("id", profile_id).execute()
        if not profile_resp.data:
            return jsonify({
                "mensaje": "Perfil no encontrado",
                "data": None
            }), 404
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": profile_resp.data[0]
        }), 200

    def create_profile(self):
        try:
            profile_data = request.get_json()
            # Verificar si el usuario existe
            if 'usuario_id' not in profile_data:
                return jsonify({
                    "mensaje": "El campo usuario_id es requerido",
                    "data": None
                }), 400

            user = supabase.table("USERS").select("*").eq("id", profile_data['usuario_id']).execute()
            if not user.data:
                return jsonify({
                    "mensaje": "El usuario no existe",
                    "data": None
                }), 404

            # Verificar si la cuenta existe y está disponible
            account = supabase.table("ACCOUNTS").select("*").eq("id", profile_data['cuenta_id']).execute()
            if not account.data:
                return jsonify({
                    "mensaje": "La cuenta no existe",
                    "data": None
                }), 404

            # Verificar que el usuario sea el dueño de la cuenta
            if account.data[0]['usuario_actual_id'] != profile_data['usuario_id']:
                return jsonify({
                    "mensaje": "No tienes permiso para crear perfiles en esta cuenta",
                    "data": None
                }), 403

            # Verificar cantidad de perfiles
            profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", profile_data['cuenta_id']).execute()
            if len(profiles.data) >= 5:
                return jsonify({
                    "mensaje": "Se ha alcanzado el límite de perfiles para esta cuenta",
                    "data": None
                }), 400

            # Establecer estado inicial y asegurar que cliente_id sea null
            profile_data['estado'] = 'disponible'
            profile_data['created_at'] = datetime.now().isoformat()
            profile_data['cliente_id'] = None  # Aseguramos que cliente_id sea null al crear
            profile_data['usuario_id'] = profile_data['usuario_id']  # Asignamos el usuario_id como dueño del perfil

            profile_resp = supabase.table("PROFILES").insert(profile_data).execute()

            return jsonify({
                "mensaje": "Perfil creado exitosamente",
                "data": profile_resp.data[0]
            }), 201
        except Exception as e:
            return jsonify({
                "mensaje": "Error al crear perfil",
                "error": str(e)
            }), 400

    def assign_to_client(self, profile_id):
        try:
            profile_data = request.get_json()
            
            if 'cliente_id' not in profile_data or 'usuario_id' not in profile_data:
                return jsonify({
                    "mensaje": "Los campos cliente_id y usuario_id son requeridos",
                    "data": None
                }), 400

            # Verificar si el perfil existe y está disponible
            profile = supabase.table("PROFILES").select("*").eq("id", profile_id).execute()
            if not profile.data:
                return jsonify({
                    "mensaje": "Perfil no encontrado",
                    "data": None
                }), 404

            if profile.data[0]['estado'] != 'disponible':
                return jsonify({
                    "mensaje": "El perfil no está disponible",
                    "data": None
                }), 400

            # Verificar si el usuario existe y es dueño de la cuenta
            account = supabase.table("ACCOUNTS").select("*").eq("id", profile.data[0]['cuenta_id']).execute()
            if not account.data:
                return jsonify({
                    "mensaje": "La cuenta asociada al perfil no existe",
                    "data": None
                }), 404

            if account.data[0]['usuario_actual_id'] != profile_data['usuario_id']:
                return jsonify({
                    "mensaje": "No tienes permiso para asignar este perfil",
                    "data": None
                }), 403

            # Verificar si el cliente existe
            client = supabase.table("COSTUMERS").select("*").eq("id", profile_data['cliente_id']).execute()
            if not client.data:
                return jsonify({
                    "mensaje": "Cliente no encontrado",
                    "data": None
                }), 404

            # Actualizar perfil
            update_data = {
                'estado': 'ocupado',
                'cliente_id': profile_data['cliente_id']
            }

            profile_resp = supabase.table("PROFILES").update(update_data).eq("id", profile_id).execute()
            return jsonify({
                "mensaje": "Perfil asignado exitosamente",
                "data": profile_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al asignar perfil",
                "error": str(e)
            }), 400

    def mark_as_available(self, profile_id):
        try:
            profile_data = {
                'estado': 'disponible',
                'cliente_id': None,
                'usuario_id': None,
                'fecha_inicio': None,
                'fecha_fin': None
            }
            profile_resp = supabase.table("PROFILES").update(profile_data).eq("id", profile_id).execute()
            return jsonify({
                "mensaje": "Perfil marcado como disponible exitosamente",
                "data": profile_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al marcar perfil como disponible",
                "error": str(e)
            }), 400

    def check_profile_availability(self, profile_id):
        profile = supabase.table("PROFILES").select("*").eq("id", profile_id).execute()
        if not profile.data:
            return False, "Perfil no encontrado"
        
        profile_data = profile.data[0]
        if profile_data['estado'] != 'disponible':
            return False, "El perfil no está disponible"
        
        return True, "Perfil disponible" 
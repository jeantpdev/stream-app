from flask import jsonify
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

    def create_profile(self, profile_data):
        try:
            # Verificar si la cuenta existe y está disponible
            account = supabase.table("ACCOUNTS").select("*").eq("id", profile_data['cuenta_id']).execute()
            if not account.data:
                return jsonify({
                    "mensaje": "La cuenta no existe",
                    "data": None
                }), 404
            
            print("Cuenta encontrada")

            # Verificar cantidad de perfiles
            profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", profile_data['cuenta_id']).execute()
            if len(profiles.data) >= 5:
                return jsonify({
                    "mensaje": "Se ha alcanzado el límite de perfiles para esta cuenta",
                    "data": None
                }), 400
            
            print("Cantidad de perfiles verificada")

            # Establecer estado inicial y asegurar que cliente_id sea null
            profile_data['estado'] = 'disponible'
            profile_data['created_at'] = datetime.now().isoformat()
            profile_data['cliente_id'] = None  # Aseguramos que cliente_id sea null al crear
            profile_data['usuario_id'] = account.data[0]['usuario_actual_id']  # Asignamos el usuario_id del revendedor

            print(profile_data)

            print("Datos del perfil preparados")

            profile_resp = supabase.table("PROFILES").insert(profile_data).execute()

            print("Perfil creado exitosamente")

            return jsonify({
                "mensaje": "Perfil creado exitosamente",
                "data": profile_resp.data[0]
            }), 201
        except Exception as e:
            return jsonify({
                "mensaje": "Error al crear perfil",
                "error": str(e)
            }), 400

    def assign_to_client(self, profile_id, client_id):
        try:
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

            # Actualizar perfil
            profile_data = {
                'estado': 'ocupado',
                'cliente_id': client_id,
                'fecha_inicio': datetime.now().isoformat(),
                'fecha_fin': (datetime.now() + timedelta(days=30)).isoformat()
            }

            profile_resp = supabase.table("PROFILES").update(profile_data).eq("id", profile_id).execute()
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
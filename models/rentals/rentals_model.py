from flask import jsonify
from models.connection import supabase
from datetime import datetime, timedelta

class RentalsModel():
    
    def get_all_rentals(self, user_id=None):
        query = supabase.table("RENTALS").select("*")
        if user_id:
            query = query.eq("usuario_id", user_id)
        rentals_resp = query.execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": rentals_resp.data
        }), 200

    def get_rental_by_id(self, rental_id):
        rental_resp = supabase.table("RENTALS").select("*").eq("id", rental_id).execute()
        if not rental_resp.data:
            return jsonify({
                "mensaje": "Alquiler no encontrado",
                "data": None
            }), 404
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": rental_resp.data[0]
        }), 200

    def create_rental(self, rental_data):
        try:
            # Verificar si el usuario existe y es revendedor
            user = supabase.table("USERS").select("*").eq("id", rental_data['usuario_id']).execute()
            if not user.data:
                return jsonify({
                    "mensaje": "Usuario no encontrado",
                    "data": None
                }), 404
            
            if user.data[0]['rol'] != 'revendedor':
                return jsonify({
                    "mensaje": "Solo los revendedores pueden crear alquileres",
                    "data": None
                }), 403

            # Verificar si la cuenta existe
            account = supabase.table("ACCOUNTS").select("*").eq("id", rental_data['cuenta_id']).execute()
            if not account.data:
                return jsonify({
                    "mensaje": "Cuenta no encontrada",
                    "data": None
                }), 404

            # Verificar disponibilidad de la cuenta
            if account.data[0]['estado'] != 'disponible':
                return jsonify({
                    "mensaje": "La cuenta no está disponible",
                    "data": None
                }), 400

            # Si es alquiler de perfil, verificar disponibilidad y cliente
            if rental_data.get('tipo') == 'perfil':
                if 'perfil_id' not in rental_data:
                    return jsonify({
                        "mensaje": "El campo perfil_id es requerido para alquiler de perfil",
                        "data": None
                    }), 400

                if 'cliente_id' not in rental_data:
                    return jsonify({
                        "mensaje": "El campo cliente_id es requerido para alquiler de perfil",
                        "data": None
                    }), 400

                # Verificar si el perfil existe y está disponible
                profile = supabase.table("PROFILES").select("*").eq("id", rental_data['perfil_id']).execute()
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

                # Verificar si el cliente existe y pertenece al revendedor
                client = supabase.table("CLIENTS").select("*").eq("id", rental_data['cliente_id']).eq("revendedor_id", rental_data['usuario_id']).execute()
                if not client.data:
                    return jsonify({
                        "mensaje": "El cliente no existe o no pertenece al revendedor",
                        "data": None
                    }), 400

            # Establecer fechas
            now = datetime.now()
            rental_data['fecha_inicio'] = now.isoformat()
            rental_data['fecha_fin'] = (now + timedelta(days=30)).isoformat()
            rental_data['created_at'] = now.isoformat()

            # Crear el alquiler
            rental_resp = supabase.table("RENTALS").insert(rental_data).execute()

            # Actualizar estado de la cuenta
            account_data = {
                'estado': 'ocupada',
                'usuario_actual_id': rental_data['usuario_id']
            }
            supabase.table("ACCOUNTS").update(account_data).eq("id", rental_data['cuenta_id']).execute()

            # Si es alquiler de perfil, actualizar estado del perfil y asignar cliente
            if rental_data.get('tipo') == 'perfil':
                profile_data = {
                    'estado': 'ocupado',
                    'usuario_id': rental_data['usuario_id'],
                    'cliente_id': rental_data['cliente_id']
                }
                supabase.table("PROFILES").update(profile_data).eq("id", rental_data['perfil_id']).execute()
            else:
                # Si es alquiler completo, actualizar todos los perfiles
                profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", rental_data['cuenta_id']).execute()
                for profile in profiles.data:
                    profile_data = {
                        'estado': 'ocupado',
                        'usuario_id': rental_data['usuario_id']
                    }
                    supabase.table("PROFILES").update(profile_data).eq("id", profile['id']).execute()

            return jsonify({
                "mensaje": "Alquiler creado exitosamente",
                "data": rental_resp.data[0]
            }), 201
        except Exception as e:
            return jsonify({
                "mensaje": "Error al crear alquiler",
                "error": str(e)
            }), 400

    def check_rental_availability(self, account_id, profile_id=None):
        # Verificar si la cuenta está disponible
        account = supabase.table("ACCOUNTS").select("*").eq("id", account_id).execute()
        if not account.data:
            return False, "Cuenta no encontrada"
        
        if account.data[0]['estado'] != 'disponible':
            return False, "La cuenta no está disponible"

        # Si es alquiler de perfil, verificar disponibilidad del perfil
        if profile_id:
            profile = supabase.table("PROFILES").select("*").eq("id", profile_id).execute()
            if not profile.data:
                return False, "Perfil no encontrado"
            
            if profile.data[0]['estado'] != 'disponible':
                return False, "El perfil no está disponible"

        return True, "Disponible para alquiler"

    def get_active_rentals(self, user_id):
        now = datetime.now().isoformat()
        rentals_resp = supabase.table("RENTALS").select("*").eq("usuario_id", user_id).gte("fecha_fin", now).execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": rentals_resp.data
        }), 200

    def get_expired_rentals(self, user_id):
        now = datetime.now().isoformat()
        rentals_resp = supabase.table("RENTALS").select("*").eq("usuario_id", user_id).lt("fecha_fin", now).execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": rentals_resp.data
        }), 200 
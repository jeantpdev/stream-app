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
            # Verificar si el usuario existe
            user = supabase.table("USERS").select("*").eq("id", rental_data['usuario_id']).execute()
            if not user.data:
                return jsonify({
                    "mensaje": "Usuario no encontrado",
                    "data": None
                }), 404

            # Verificar si la cuenta existe
            account = supabase.table("ACCOUNTS").select("*").eq("id", rental_data['cuenta_id']).execute()
            if not account.data:
                return jsonify({
                    "mensaje": "Cuenta no encontrada",
                    "data": None
                }), 404

            # Verificar disponibilidad según el tipo de alquiler
            if rental_data.get('tipo') == 'completa':
                # Para alquiler completo, la cuenta debe estar completamente disponible
                if account.data[0]['estado'] != 'disponible':
                    return jsonify({
                        "mensaje": "La cuenta debe estar completamente disponible para alquiler completo",
                        "data": None
                    }), 400
            else:  # tipo == 'perfil'
                # Para alquiler de perfil, la cuenta puede estar disponible o semiocupada
                if account.data[0]['estado'] not in ['disponible', 'semiocupada']:
                    return jsonify({
                        "mensaje": "La cuenta no está disponible para alquiler de perfiles",
                        "data": None
                    }), 400

            # Establecer fechas
            now = datetime.now()
            rental_data['fecha_inicio'] = now.isoformat()
            rental_data['fecha_fin'] = (now + timedelta(days=29)).isoformat()
            rental_data['created_at'] = now.isoformat()
            rental_data['estado'] = 'activo'

            if rental_data.get('tipo') == 'perfil':
                # Validar campos requeridos para alquiler de perfil
                if 'cliente_id' not in rental_data:
                    return jsonify({
                        "mensaje": "El campo cliente_id es requerido para alquiler de perfil",
                        "data": None
                    }), 400

                # Verificar si el cliente existe y pertenece al revendedor
                client = supabase.table("COSTUMERS").select("*").eq("id", rental_data['cliente_id']).eq("revendedor_id", rental_data['usuario_id']).execute()
                if not client.data:
                    return jsonify({
                        "mensaje": "El cliente no existe o no pertenece al revendedor",
                        "data": None
                    }), 400

                # Buscar el primer perfil disponible de la cuenta
                available_profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", rental_data['cuenta_id']).eq("estado", "disponible").order("id").execute()
                if not available_profiles.data:
                    return jsonify({
                        "mensaje": "No hay perfiles disponibles en esta cuenta",
                        "data": None
                    }), 400

                # Seleccionar el primer perfil disponible
                selected_profile = available_profiles.data[0]
                perfil_id = selected_profile['id']

                # Solo los campos válidos para la tabla RENTALS
                rental_insert = {
                    "usuario_id": rental_data["usuario_id"],
                    "cuenta_id": rental_data["cuenta_id"],
                    "tipo": rental_data["tipo"],
                    "fecha_inicio": rental_data["fecha_inicio"],
                    "fecha_fin": rental_data["fecha_fin"],
                    "created_at": rental_data["created_at"]
                }
                rental_resp = supabase.table("RENTALS").insert(rental_insert).execute()

                # Actualizar el perfil seleccionado
                profile_data = {
                    'estado': 'ocupado',
                    'usuario_id': rental_data['usuario_id'],
                    'cliente_id': rental_data['cliente_id']
                }
                supabase.table("PROFILES").update(profile_data).eq("id", perfil_id).execute()

                # Verificar cuántos perfiles están ocupados después de este alquiler
                perfiles_ocupados = supabase.table("PROFILES").select("*").eq("cuenta_id", rental_data['cuenta_id']).eq("estado", "ocupado").execute()
                total_perfiles = supabase.table("PROFILES").select("*").eq("cuenta_id", rental_data['cuenta_id']).execute()
                if len(perfiles_ocupados.data) == len(total_perfiles.data):
                    # Todos los perfiles ocupados
                    cuenta_estado = 'ocupada'
                else:
                    # Al menos un perfil ocupado
                    cuenta_estado = 'semiocupada'
                supabase.table("ACCOUNTS").update({'estado': cuenta_estado}).eq("id", rental_data['cuenta_id']).execute()

                # Incluir información del perfil asignado en la respuesta
                rental_response = rental_resp.data[0].copy()
                rental_response['perfil_asignado'] = {
                    'perfil_id': perfil_id,
                    'nombre_perfil': selected_profile.get('nombre', f'Perfil {perfil_id}'),
                    'cliente_asignado': rental_data['cliente_id']
                }

                return jsonify({
                    "mensaje": "Alquiler creado exitosamente",
                    "data": rental_response
                }), 201

            else:  # tipo == 'completa'
                # Verificar que todos los perfiles estén disponibles
                profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", rental_data['cuenta_id']).execute()
                for profile in profiles.data:
                    if profile['estado'] != 'disponible':
                        return jsonify({
                            "mensaje": "No se puede comprar la cuenta completa porque uno o más perfiles ya están ocupados",
                            "data": None
                        }), 400

                # Solo los campos válidos para la tabla RENTALS
                rental_insert = {
                    "usuario_id": rental_data["usuario_id"],
                    "cuenta_id": rental_data["cuenta_id"],
                    "tipo": rental_data["tipo"],
                    "fecha_inicio": rental_data["fecha_inicio"],
                    "fecha_fin": rental_data["fecha_fin"],
                    "created_at": rental_data["created_at"]
                }
                rental_resp = supabase.table("RENTALS").insert(rental_insert).execute()

                # Actualizar estado de la cuenta
                account_data = {
                    'estado': 'ocupada',
                    'usuario_actual_id': rental_data['usuario_id']
                }
                supabase.table("ACCOUNTS").update(account_data).eq("id", rental_data['cuenta_id']).execute()

                # Actualizar todos los perfiles de la cuenta
                for profile in profiles.data:
                    profile_data = {
                        'estado': 'ocupado',
                        'usuario_id': rental_data['usuario_id'],
                        'cliente_id': None
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
from flask import jsonify, request
from models.connection import supabase
from datetime import datetime, timedelta

class AccountsModel():

    def get_all_accounts(self):
        accounts_resp = supabase.table("ACCOUNTS").select("*").execute()
        
        # Para cada cuenta, obtener el conteo de perfiles ocupados
        for account in accounts_resp.data:
            profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", account['id']).eq("estado", "ocupado").execute()
            account['perfiles_usados'] = len(profiles.data)
        
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": accounts_resp.data
        }), 200

    def get_available_accounts(self):
        accounts_resp = supabase.table("ACCOUNTS").select("*").eq("estado", "disponible").execute()
        
        # Para cada cuenta, obtener el conteo de perfiles ocupados
        for account in accounts_resp.data:
            profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", account['id']).eq("estado", "ocupado").execute()
            account['perfiles_usados'] = len(profiles.data)
        
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": accounts_resp.data
        }), 200

    def get_account_by_id(self, account_id):
        account_resp = supabase.table("ACCOUNTS").select("*").eq("id", account_id).execute()
        if not account_resp.data:
            return jsonify({
                "mensaje": "Cuenta no encontrada",
                "data": None
            }), 404
        
        # Obtener el conteo de perfiles ocupados
        account = account_resp.data[0]
        profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", account_id).eq("estado", "ocupado").execute()
        account['perfiles_usados'] = len(profiles.data)
        
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": account
        }), 200

    def create_account(self):
        try:
            account_data = request.get_json()
            # Validar campos requeridos
            required_fields = ['nombre', 'tipo_servicio', 'cantidad_perfiles', 'precio_cuenta', 'precio_perfil', 'credenciales']
            for field in required_fields:
                if field not in account_data:
                    return jsonify({
                        "mensaje": f"El campo {field} es requerido",
                        "data": None
                    }), 400

            # Validar cantidad de perfiles
            if account_data.get('cantidad_perfiles', 0) > 5:
                return jsonify({
                    "mensaje": "La cantidad máxima de perfiles es 5",
                    "data": None
                }), 400

            # Validar credenciales
            if not isinstance(account_data['credenciales'], dict):
                return jsonify({
                    "mensaje": "El campo credenciales debe ser un objeto JSON",
                    "data": None
                }), 400

            required_credentials = ['correo', 'contraseña']
            for credential in required_credentials:
                if credential not in account_data['credenciales']:
                    return jsonify({
                        "mensaje": f"El campo {credential} es requerido en las credenciales",
                        "data": None
                    }), 400

            # Validar valores numéricos
            if account_data['precio_cuenta'] <= 0 or account_data['precio_perfil'] <= 0:
                return jsonify({
                    "mensaje": "Los precios deben ser mayores a 0",
                    "data": None
                }), 400

            # Establecer estado inicial
            account_data['estado'] = 'disponible'
            account_data['fecha_inicio'] = datetime.now().isoformat()
            account_data['fecha_fin'] = (datetime.now() + timedelta(days=30)).isoformat()
            # La cuenta inicialmente la mantiene el usuario 43z (account_keeper) para no romper la lógica.
            # Si alguien compra un perfil, la cuenta queda a account_keeper. 
            # Si alguien compra la cuenta, se cambia el usuario_actual_id a la persona que compró la cuenta.
            account_data['usuario_actual_id'] = "6d6f9721-ede6-4e8b-8a21-b0f49f2e63d8"

            # Crear la cuenta
            account_resp = supabase.table("ACCOUNTS").insert(account_data).execute()
            account = account_resp.data[0]

            # Crear automáticamente los 5 perfiles
            for i in range(5):
                profile_data = {
                    'nombre': f"Perfil {i+1}",
                    'cuenta_id': account['id'],
                    'estado': 'disponible',
                    'created_at': datetime.now().isoformat(),
                    'cliente_id': None,
                    'usuario_id': "6d6f9721-ede6-4e8b-8a21-b0f49f2e63d8"  # account_keeper
                }
                supabase.table("PROFILES").insert(profile_data).execute()

            return jsonify({
                "mensaje": "Cuenta y perfiles creados exitosamente",
                "data": account
            }), 201
        except Exception as e:
            return jsonify({
                "mensaje": "Error al crear cuenta",
                "error": str(e)
            }), 400

    def update_account(self, account_id, account_data):
        try:
            account_resp = supabase.table("ACCOUNTS").update(account_data).eq("id", account_id).execute()
            return jsonify({
                "mensaje": "Cuenta actualizada exitosamente",
                "data": account_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al actualizar cuenta",
                "error": str(e)
            }), 400

    def delete_account(self, account_id):
        try:
            # Verificar si la cuenta está en uso
            account = supabase.table("ACCOUNTS").select("*").eq("id", account_id).execute()
            if account.data and account.data[0]['estado'] != 'disponible':
                return jsonify({
                    "mensaje": "No se puede eliminar una cuenta que está en uso",
                    "data": None
                }), 400

            supabase.table("ACCOUNTS").delete().eq("id", account_id).execute()
            return jsonify({
                "mensaje": "Cuenta eliminada exitosamente"
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al eliminar cuenta",
                "error": str(e)
            }), 400

    def mark_as_available(self, account_id):
        try:
            account_data = {
                'estado': 'disponible',
                'usuario_actual_id': None,
                'fecha_inicio': datetime.now().isoformat(),
                'fecha_fin': ""
            }
            account_resp = supabase.table("ACCOUNTS").update(account_data).eq("id", account_id).execute()
            return jsonify({
                "mensaje": "Cuenta marcada como disponible exitosamente",
                "data": account_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al marcar cuenta como disponible",
                "error": str(e)
            }), 400

    def check_account_availability(self, account_id):
        account = supabase.table("ACCOUNTS").select("*").eq("id", account_id).execute()
        if not account.data:
            return False, "Cuenta no encontrada"
        
        account_data = account.data[0]
        if account_data['estado'] != 'disponible':
            return False, "La cuenta no está disponible"
        
        # Verificar si hay perfiles ocupados
        profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", account_id).execute()
        for profile in profiles.data:
            if profile['estado'] != 'disponible':
                return False, "La cuenta tiene perfiles ocupados"
        
        return True, "Cuenta disponible"

    def update_used_profiles_count(self, account_id):
        try:
            # Obtener todos los perfiles de la cuenta que están ocupados
            profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", account_id).eq("estado", "ocupado").execute()
            
            # Actualizar el campo perfiles_usados en la cuenta
            account_data = {
                'perfiles_usados': len(profiles.data)
            }
            
            account_resp = supabase.table("ACCOUNTS").update(account_data).eq("id", account_id).execute()
            return jsonify({
                "mensaje": "Conteo de perfiles actualizado exitosamente",
                "data": account_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al actualizar conteo de perfiles",
                "error": str(e)
            }), 400

    def check_and_update_expired_accounts(self):
        try:
            now = datetime.now()
            
            # Obtener todas las cuentas que han vencido
            accounts = supabase.table("ACCOUNTS").select("*").lt("fecha_fin", now.isoformat()).neq("estado", "vencida").execute()
            
            for account in accounts.data:
                # Actualizar estado de la cuenta a vencida
                account_data = {
                    'estado': 'vencida',
                    'usuario_actual_id': None
                }
                supabase.table("ACCOUNTS").update(account_data).eq("id", account['id']).execute()
                
                # Actualizar estado de todos los perfiles de la cuenta a vencido
                profiles = supabase.table("PROFILES").select("*").eq("cuenta_id", account['id']).execute()
                for profile in profiles.data:
                    profile_data = {
                        'estado': 'vencido',
                        'cliente_id': None,
                        'usuario_id': None
                    }
                    supabase.table("PROFILES").update(profile_data).eq("id", profile['id']).execute()
            
            return jsonify({
                "mensaje": "Verificación de cuentas vencidas completada",
                "data": accounts.data
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al verificar cuentas vencidas",
                "error": str(e)
            }), 400
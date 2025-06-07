from flask import jsonify
from models.connection import supabase
from datetime import datetime

class ClientsModel():
    def get_all_clients(self, revendedor_id):
        print(revendedor_id)
        clients_resp = supabase.table("COSTUMERS").select("*").eq("revendedor_id", revendedor_id).execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": clients_resp.data
        }), 200

    def get_client_by_id(self, client_id):
        client_resp = supabase.table("COSTUMERS").select("*").eq("id", client_id).execute()
        if not client_resp.data:
            return jsonify({
                "mensaje": "Cliente no encontrado",
                "data": None
            }), 404
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": client_resp.data[0]
        }), 200

    def create_client(self, client_data):
        try:
            # Verificar si el revendedor existe
            revendedor = supabase.table("USERS").select("*").eq("id", client_data['revendedor_id']).execute()
            if not revendedor.data:
                return jsonify({
                    "mensaje": "El revendedor no existe",
                    "data": None
                }), 404

            # Verificar que el usuario sea revendedor
            if revendedor.data[0]['rol'] != 'revendedor':
                return jsonify({
                    "mensaje": "El usuario no es un revendedor",
                    "data": None
                }), 400

            # Establecer fecha de creación
            client_data['created_at'] = datetime.now().isoformat()

            client_resp = supabase.table("COSTUMERS").insert(client_data).execute()
            return jsonify({
                "mensaje": "Cliente creado exitosamente",
                "data": client_resp.data[0]
            }), 201
        except Exception as e:
            return jsonify({
                "mensaje": "Error al crear cliente",
                "error": str(e)
            }), 400

    def update_client(self, client_id, client_data):
        try:
            # Verificar si el cliente existe
            client = supabase.table("COSTUMERS").select("*").eq("id", client_id).execute()
            if not client.data:
                return jsonify({
                    "mensaje": "Cliente no encontrado",
                    "data": None
                }), 404

            client_resp = supabase.table("COSTUMERS").update(client_data).eq("id", client_id).execute()
            return jsonify({
                "mensaje": "Cliente actualizado exitosamente",
                "data": client_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al actualizar cliente",
                "error": str(e)
            }), 400

    def delete_client(self, client_id):
        try:
            # Verificar si el cliente tiene perfiles asignados
            profiles = supabase.table("PROFILES").select("*").eq("cliente_id", client_id).execute()
            if profiles.data:
                return jsonify({
                    "mensaje": "No se puede eliminar un cliente con perfiles asignados",
                    "data": None
                }), 400

            supabase.table("COSTUMERS").delete().eq("id", client_id).execute()
            return jsonify({
                "mensaje": "Cliente eliminado exitosamente"
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al eliminar cliente",
                "error": str(e)
            }), 400

    def get_client_profiles(self, client_id):
        profiles_resp = supabase.table("PROFILES").select("*").eq("cliente_id", client_id).execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": profiles_resp.data
        }), 200 
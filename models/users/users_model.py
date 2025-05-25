from flask import jsonify
from models.connection import supabase

class UsersModel():
    def get_all_users(self):
        users_resp = supabase.table("USERS").select("*").execute()
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": users_resp.data
        }), 200

    def get_user_by_id(self, user_id):
        user_resp = supabase.table("USERS").select("*").eq("id", user_id).execute()
        if not user_resp.data:
            return jsonify({
                "mensaje": "Usuario no encontrado",
                "data": None
            }), 404
        return jsonify({
            "mensaje": "Consulta exitosa",
            "data": user_resp.data[0]
        }), 200

    def create_user(self, user_data):
        try:
            user_resp = supabase.table("USERS").insert(user_data).execute()
            return jsonify({
                "mensaje": "Usuario creado exitosamente",
                "data": user_resp.data[0]
            }), 201
        except Exception as e:
            return jsonify({
                "mensaje": "Error al crear usuario",
                "error": str(e)
            }), 400

    def update_user(self, user_id, user_data):
        try:
            user_resp = supabase.table("USERS").update(user_data).eq("id", user_id).execute()
            return jsonify({
                "mensaje": "Usuario actualizado exitosamente",
                "data": user_resp.data[0]
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al actualizar usuario",
                "error": str(e)
            }), 400

    def delete_user(self, user_id):
        try:
            supabase.table("USERS").delete().eq("id", user_id).execute()
            return jsonify({
                "mensaje": "Usuario eliminado exitosamente"
            }), 200
        except Exception as e:
            return jsonify({
                "mensaje": "Error al eliminar usuario",
                "error": str(e)
            }), 400 
from flask import jsonify
from models.connection import supabase
from werkzeug.security import check_password_hash
from flask_jwt_extended import create_access_token

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

    def login(self, email, password):
        # Imprimir datos para debug
        print(f"Intentando login con email: {email} y password: {password}")
        
        user_resp = supabase.table("USERS").select("*").eq("email", email).execute()
        print(f"Respuesta de base de datos: {user_resp.data}")
        
        if not user_resp.data:
            print("Usuario no encontrado")
            return jsonify({"mensaje": "Credenciales incorrectas", "data": None}), 401
            
        user = user_resp.data[0]
        print(f"Contraseña almacenada: {user.get('contraseña')}")
        print(f"Contraseña ingresada: {password}")
        
        # Comparación directa de contraseñas por ahora
        if user.get('contraseña') != password:
            print("Contraseña incorrecta")
            return jsonify({"mensaje": "Credenciales incorrectas", "data": None}), 401
            
        access_token = create_access_token(identity={"id": user["id"], "rol": user["rol"]})
        user_data = {
            "id": user["id"],
            "nombre": user["nombre"], 
            "email": user["email"],
            "celular": user.get("celular"),
            "rol": user["rol"],
            "created_at": user["created_at"],
            "token": access_token
        }
        print("Login exitoso")
        return jsonify({"mensaje": "Login exitoso", "data": user_data}), 200
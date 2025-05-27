# Documentación de la API

## 📋 Índice
- [Cuentas](#cuentas)
- [Alquileres](#alquileres)
- [Perfiles](#perfiles)
- [Clientes](#clientes)
- [Usuarios](#usuarios)
- [Login](#login)

---

## Cuentas

### `GET /accounts`
Obtiene todas las cuentas.

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa",
  "data": [
    {
      "id": "uuid",
      "nombre": "Cuenta Netflix",
      "tipo_servicio": "Netflix",
      "cantidad_perfiles": 5,
      "precio_cuenta": 100,
      "precio_perfil": 25,
      "credenciales": {"correo": "ejemplo@correo.com", "contraseña": "1234"},
      "estado": "disponible",
      "fecha_inicio": "2025-05-25T02:09:07.80627+00:00",
      "fecha_fin": "2025-06-25T02:09:07.80627+00:00",
      "usuario_actual_id": "uuid",
      "perfiles_usados": 2
    }
  ]
}
```

### `GET /accounts/available`
Obtiene todas las cuentas disponibles.

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa",
  "data": [
    {
      "id": "uuid",
      "nombre": "Cuenta Netflix",
      "tipo_servicio": "Netflix",
      "cantidad_perfiles": 5,
      "precio_cuenta": 100,
      "precio_perfil": 25,
      "credenciales": {"correo": "ejemplo@correo.com", "contraseña": "1234"},
      "estado": "disponible",
      "fecha_inicio": "2025-05-25T02:09:07.80627+00:00",
      "fecha_fin": "2025-06-25T02:09:07.80627+00:00",
      "usuario_actual_id": "uuid",
      "perfiles_usados": 0
    }
  ]
}
```

### `GET /accounts/<int:account_id>`
Obtiene una cuenta específica.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Consulta exitosa",
  "data": {
    "id": "uuid",
    "nombre": "Cuenta Netflix",
    "tipo_servicio": "Netflix",
    "cantidad_perfiles": 5,
    "precio_cuenta": 100,
    "precio_perfil": 25,
    "credenciales": {"correo": "ejemplo@correo.com", "contraseña": "1234"},
    "estado": "disponible",
    "fecha_inicio": "2025-05-25T02:09:07.80627+00:00",
    "fecha_fin": "2025-06-25T02:09:07.80627+00:00",
    "usuario_actual_id": "uuid",
    "perfiles_usados": 3
  }
}
```
**Ejemplo de respuesta (no encontrada):**
```json
{
  "mensaje": "Cuenta no encontrada",
  "data": null
}
```

### `POST /accounts`
Crea una nueva cuenta.

**Ejemplo de datos de entrada:**
```json
{
  "nombre": "Cuenta Netflix",
  "tipo_servicio": "Netflix",
  "cantidad_perfiles": 5,
  "precio_cuenta": 100,
  "precio_perfil": 25,
  "credenciales": {
    "correo": "ejemplo@correo.com",
    "contraseña": "1234"
  }
}
```
**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cuenta y perfiles creados exitosamente",
  "data": {
    "id": "uuid",
    "nombre": "Cuenta Netflix",
    "tipo_servicio": "Netflix",
    "cantidad_perfiles": 5,
    "precio_cuenta": 100,
    "precio_perfil": 25,
    "credenciales": {"correo": "ejemplo@correo.com", "contraseña": "1234"},
    "estado": "disponible",
    "fecha_inicio": "2025-05-25T02:09:07.80627+00:00",
    "fecha_fin": "2025-06-25T02:09:07.80627+00:00",
    "usuario_actual_id": "uuid"
  }
}
```
**Ejemplo de respuesta (error, campo faltante):**
```json
{
  "mensaje": "El campo nombre es requerido",
  "data": null
}
```
**Ejemplo de respuesta (error, cantidad de perfiles):**
```json
{
  "mensaje": "La cantidad máxima de perfiles es 5",
  "data": null
}
```
**Ejemplo de respuesta (error, credenciales):**
```json
{
  "mensaje": "El campo credenciales debe ser un objeto JSON",
  "data": null
}
```

### `PATCH /accounts/<int:account_id>`
Actualiza una cuenta.

**Ejemplo de datos de entrada:**
```json
{
  "nombre": "Cuenta Disney+",
  "precio_cuenta": 120
}
```
**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cuenta actualizada exitosamente",
  "data": {
    "id": "uuid",
    "nombre": "Cuenta Disney+",
    "precio_cuenta": 120
  }
}
```
**Ejemplo de respuesta (error):**
```json
{
  "mensaje": "Error al actualizar cuenta",
  "error": "Mensaje de error"
}
```

### `DELETE /accounts/<int:account_id>`
Elimina una cuenta.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cuenta eliminada exitosamente"
}
```
**Ejemplo de respuesta (error, cuenta en uso):**
```json
{
  "mensaje": "No se puede eliminar una cuenta que está en uso",
  "data": null
}
```
**Ejemplo de respuesta (error):**
```json
{
  "mensaje": "Error al eliminar cuenta",
  "error": "Mensaje de error"
}
```

### `PATCH /accounts/<int:account_id>/mark-available`
Marca una cuenta como disponible.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cuenta marcada como disponible exitosamente",
  "data": {
    "id": "uuid",
    "estado": "disponible"
  }
}
```
**Ejemplo de respuesta (error):**
```json
{
  "mensaje": "Error al marcar cuenta como disponible",
  "error": "Mensaje de error"
}
```

### `PATCH /accounts/<int:account_id>/update-profiles-count`
Actualiza el conteo de perfiles usados en una cuenta.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Conteo de perfiles actualizado exitosamente",
  "data": {
    "id": "uuid",
    "perfiles_usados": 3
  }
}
```
**Ejemplo de respuesta (error):**
```json
{
  "mensaje": "Error al actualizar conteo de perfiles",
  "error": "Mensaje de error"
}
```

### `POST /accounts/check-expired`
Verifica cuentas expiradas.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Verificación de cuentas vencidas completada",
  "data": [
    {
      "id": "uuid",
      "estado": "vencida"
    }
  ]
}
```
**Ejemplo de respuesta (error):**
```json
{
  "mensaje": "Error al verificar cuentas vencidas",
  "error": "Mensaje de error"
}
```

---

## Alquileres

### `GET /rentals`
Obtiene todos los alquileres.

### `GET /rentals/<int:rental_id>`
Obtiene un alquiler específico.

### `POST /rentals`
Crea un nuevo alquiler.

### `GET /users/<int:user_id>/rentals/active`
Obtiene los alquileres activos de un usuario.

### `GET /users/<int:user_id>/rentals/expired`
Obtiene los alquileres expirados de un usuario.

---

## Perfiles

### `GET /accounts/<uuid:account_id>/profiles`
Obtiene los perfiles de una cuenta.

### `GET /profiles/<int:profile_id>`
Obtiene un perfil específico.

### `POST /profiles`
Crea un nuevo perfil.

### `PATCH /profiles/<uuid:profile_id>/assign-client`
Asigna un perfil a un cliente.

### `PATCH /profiles/<int:profile_id>/mark-available`
Marca un perfil como disponible.

---

## Clientes

### `GET /revendedores/<int:revendedor_id>/clients`
Obtiene los clientes de un revendedor.

### `GET /clients/<int:client_id>`
Obtiene un cliente específico.

### `POST /clients`
Crea un nuevo cliente.

### `PATCH /clients/<int:client_id>`
Actualiza un cliente.

### `DELETE /clients/<int:client_id>`
Elimina un cliente.

### `GET /clients/<int:client_id>/profiles`
Obtiene los perfiles asignados a un cliente.

---

## Usuarios

### `GET /users`
Obtiene todos los usuarios.

### `GET /users/<int:user_id>`
Obtiene un usuario específico.

### `POST /users`
Crea un nuevo usuario.

### `PATCH /users/<int:user_id>`
Actualiza un usuario.

### `DELETE /users/<int:user_id>`
Elimina un usuario.

---

## Login

### `POST /login`
Inicia sesión con email y contraseña.

---

> **Nota:** Para detalles de entrada y salida de cada endpoint, revisa los controladores y modelos correspondientes. Si necesitas ejemplos de request/response para alguna ruta específica, indícalo y los agrego. 
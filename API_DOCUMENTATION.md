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

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa",
  "data": [
    {
      "id": "uuid",
      "usuario_id": "uuid_usuario",
      "cuenta_id": "uuid_cuenta", 
      "tipo": "perfil",
      "fecha_inicio": "2025-01-15T10:30:00",
      "fecha_fin": "2025-02-13T10:30:00",
      "created_at": "2025-01-15T10:30:00"
    },
    {
      "id": "uuid",
      "usuario_id": "uuid_usuario",
      "cuenta_id": "uuid_cuenta",
      "tipo": "completa", 
      "fecha_inicio": "2025-01-10T15:45:00",
      "fecha_fin": "2025-02-08T15:45:00",
      "created_at": "2025-01-10T15:45:00"
    }
  ]
}
```

### `GET /rentals/<int:rental_id>`
Obtiene un alquiler específico.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Consulta exitosa",
  "data": {
    "id": "uuid",
    "usuario_id": "uuid_usuario",
    "cuenta_id": "uuid_cuenta",
    "tipo": "perfil",
    "fecha_inicio": "2025-01-15T10:30:00", 
    "fecha_fin": "2025-02-13T10:30:00",
    "created_at": "2025-01-15T10:30:00"
  }
}
```
**Ejemplo de respuesta (no encontrado):**
```json
{
  "mensaje": "Alquiler no encontrado",
  "data": null
}
```

### `POST /rentals`
Crea un nuevo alquiler.

**Ejemplo de datos de entrada (alquiler de perfil):**
```json
{
  "usuario_id": "uuid_usuario",
  "cuenta_id": "uuid_cuenta",
  "tipo": "perfil",
  "cliente_id": "uuid_cliente"
}
```

**Ejemplo de datos de entrada (alquiler completo):**
```json
{
  "usuario_id": "uuid_usuario", 
  "cuenta_id": "uuid_cuenta",
  "tipo": "completa"
}
```

**Ejemplo de respuesta (éxito - alquiler de perfil):**
```json
{
  "mensaje": "Alquiler creado exitosamente",
  "data": {
    "id": "uuid",
    "usuario_id": "uuid_usuario",
    "cuenta_id": "uuid_cuenta",
    "tipo": "perfil",
    "fecha_inicio": "2025-01-15T10:30:00",
    "fecha_fin": "2025-02-13T10:30:00", 
    "created_at": "2025-01-15T10:30:00",
    "perfil_asignado": {
      "perfil_id": "uuid_perfil",
      "nombre_perfil": "Perfil 1",
      "cliente_asignado": "uuid_cliente"
    }
  }
}
```

**Ejemplo de respuesta (éxito - alquiler completo):**
```json
{
  "mensaje": "Alquiler creado exitosamente",
  "data": {
    "id": "uuid",
    "usuario_id": "uuid_usuario",
    "cuenta_id": "uuid_cuenta",
    "tipo": "completa",
    "fecha_inicio": "2025-01-15T10:30:00",
    "fecha_fin": "2025-02-13T10:30:00", 
    "created_at": "2025-01-15T10:30:00"
  }
}
```

**Ejemplo de respuesta (error, usuario no encontrado):**
```json
{
  "mensaje": "Usuario no encontrado",
  "data": null
}
```

**Ejemplo de respuesta (error, cuenta no encontrada):**
```json
{
  "mensaje": "Cuenta no encontrada", 
  "data": null
}
```

**Ejemplo de respuesta (error, cuenta no disponible para alquiler completo):**
```json
{
  "mensaje": "La cuenta debe estar completamente disponible para alquiler completo",
  "data": null
}
```

**Ejemplo de respuesta (error, cuenta no disponible para alquiler de perfiles):**
```json
{
  "mensaje": "La cuenta no está disponible para alquiler de perfiles",
  "data": null
}
```

**Ejemplo de respuesta (error, perfil no disponible):**
```json
{
  "mensaje": "El perfil no está disponible",
  "data": null
}
```

**Ejemplo de respuesta (error, campos requeridos para perfil):**
```json
{
  "mensaje": "El campo cliente_id es requerido para alquiler de perfil",
  "data": null
}
```

**Ejemplo de respuesta (error, cliente no pertenece al revendedor):**
```json
{
  "mensaje": "El cliente no existe o no pertenece al revendedor",
  "data": null
}
```

**Ejemplo de respuesta (error, no hay perfiles disponibles):**
```json
{
  "mensaje": "No hay perfiles disponibles en esta cuenta", 
  "data": null
}
```

**Ejemplo de respuesta (error, perfiles ya ocupados para cuenta completa):**
```json
{
  "mensaje": "No se puede comprar la cuenta completa porque uno o más perfiles ya están ocupados",
  "data": null
}
```

**Ejemplo de respuesta (error general):**
```json
{
  "mensaje": "Error al crear alquiler",
  "error": "Mensaje de error específico"
}
```

### `GET /users/<int:user_id>/rentals/active`
Obtiene los alquileres activos de un usuario específico.

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa",
  "data": [
    {
      "id": "uuid",
      "usuario_id": "uuid_usuario",
      "cuenta_id": "uuid_cuenta",
      "tipo": "perfil", 
      "fecha_inicio": "2025-01-15T10:30:00",
      "fecha_fin": "2025-02-13T10:30:00",
      "created_at": "2025-01-15T10:30:00"
    }
  ]
}
```

### `GET /users/<int:user_id>/rentals/expired`
Obtiene los alquileres expirados de un usuario específico.

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa", 
  "data": [
    {
      "id": "uuid",
      "usuario_id": "uuid_usuario",
      "cuenta_id": "uuid_cuenta",
      "tipo": "completa",
      "fecha_inicio": "2024-12-01T08:00:00",
      "fecha_fin": "2024-12-30T08:00:00", 
      "created_at": "2024-12-01T08:00:00"
    }
  ]
}
```

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
Obtiene todos los clientes de un revendedor específico.

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa",
  "data": [
    {
      "id": "uuid",
      "nombre": "Juan Pérez",
      "contacto": "+1234567890",
      "revendedor_id": "uuid_revendedor",
      "created_at": "2025-01-15T10:30:00"
    },
    {
      "id": "uuid", 
      "nombre": "María García",
      "contacto": "maria@email.com",
      "revendedor_id": "uuid_revendedor",
      "created_at": "2025-01-10T14:20:00"
    }
  ]
}
```

### `GET /clients/<int:client_id>`
Obtiene un cliente específico.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Consulta exitosa",
  "data": {
    "id": "uuid",
    "nombre": "Juan Pérez", 
    "contacto": "+1234567890",
    "revendedor_id": "uuid_revendedor",
    "created_at": "2025-01-15T10:30:00"
  }
}
```

**Ejemplo de respuesta (no encontrado):**
```json
{
  "mensaje": "Cliente no encontrado",
  "data": null
}
```

### `POST /clients`
Crea un nuevo cliente.

**Ejemplo de datos de entrada:**
```json
{
  "nombre": "Juan Pérez",
  "contacto": "+1234567890", 
  "revendedor_id": "uuid_revendedor"
}
```

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cliente creado exitosamente",
  "data": {
    "id": "uuid",
    "nombre": "Juan Pérez",
    "contacto": "+1234567890",
    "revendedor_id": "uuid_revendedor",
    "created_at": "2025-01-15T10:30:00"
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

**Ejemplo de respuesta (error, revendedor no existe):**
```json
{
  "mensaje": "El revendedor no existe",
  "data": null
}
```

**Ejemplo de respuesta (error, usuario no es revendedor):**
```json
{
  "mensaje": "El usuario no es un revendedor",
  "data": null
}
```

**Ejemplo de respuesta (error general):**
```json
{
  "mensaje": "Error al crear cliente",
  "error": "Mensaje de error específico"
}
```

### `PATCH /clients/<int:client_id>`
Actualiza un cliente existente.

**Ejemplo de datos de entrada:**
```json
{
  "nombre": "Juan Carlos Pérez",
  "contacto": "juan.perez@email.com"
}
```

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cliente actualizado exitosamente",
  "data": {
    "id": "uuid",
    "nombre": "Juan Carlos Pérez",
    "contacto": "juan.perez@email.com",
    "revendedor_id": "uuid_revendedor",
    "created_at": "2025-01-15T10:30:00"
  }
}
```

**Ejemplo de respuesta (error, cliente no encontrado):**
```json
{
  "mensaje": "Cliente no encontrado",
  "data": null
}
```

**Ejemplo de respuesta (error general):**
```json
{
  "mensaje": "Error al actualizar cliente",
  "error": "Mensaje de error específico"
}
```

### `DELETE /clients/<int:client_id>`
Elimina un cliente.

**Ejemplo de respuesta (éxito):**
```json
{
  "mensaje": "Cliente eliminado exitosamente"
}
```

**Ejemplo de respuesta (error, cliente con perfiles asignados):**
```json
{
  "mensaje": "No se puede eliminar un cliente con perfiles asignados",
  "data": null
}
```

**Ejemplo de respuesta (error general):**
```json
{
  "mensaje": "Error al eliminar cliente",
  "error": "Mensaje de error específico"
}
```

### `GET /clients/<int:client_id>/profiles`
Obtiene todos los perfiles asignados a un cliente específico.

**Ejemplo de respuesta:**
```json
{
  "mensaje": "Consulta exitosa",
  "data": [
    {
      "id": "uuid_perfil",
      "nombre": "Perfil 1",
      "cuenta_id": "uuid_cuenta",
      "estado": "ocupado",
      "cliente_id": "uuid_cliente",
      "usuario_id": "uuid_usuario",
      "created_at": "2025-01-15T10:30:00"
    },
    {
      "id": "uuid_perfil_2",
      "nombre": "Perfil 3", 
      "cuenta_id": "uuid_cuenta_2",
      "estado": "ocupado",
      "cliente_id": "uuid_cliente",
      "usuario_id": "uuid_usuario",
      "created_at": "2025-01-12T08:15:00"
    }
  ]
}
```

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
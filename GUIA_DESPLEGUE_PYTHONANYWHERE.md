# 🚀 Guía de Despliegue en PythonAnywhere

## 📋 Resumen
- **Costo total**: $6-7/mes ($5 hosting + $1-2 dominio .com)
- **Dominio**: Tu propio dominio .com profesional
- **Correos**: Notificaciones automáticas a `avecbm2024@gmail.com`

---

## 🎯 Paso 1: Crear Cuenta en PythonAnywhere

1. Ve a [pythonanywhere.com](https://pythonanywhere.com)
2. Regístrate con el plan **Beginner ($5/mes)**
3. Verifica tu correo

---

## 🌐 Paso 2: Configurar Dominio .com

1. Compra tu dominio en Namecheap, GoDaddy o similar
   - Sugerencias: `avionesescala.com`, `modeloscolombia.com`
2. En PythonAnywhere: **Web tab → Configure domains**
3. Ingresa tu dominio: `tudominio.com`
4. Sigue las instrucciones DNS que te proporcionen

---

## 📁 Paso 3: Subir tu Código

### Opción A: Usar Git (Recomendado)
```bash
# En tu computadora local
git init
git add .
git commit -m "Versión inicial para producción"

# Subir a GitHub
git remote add origin https://github.com/tu-usuario/tu-repo.git
git push -u origin main
```

### Opción B: Subir por FTP
1. En PythonAnywhere: **Files tab**
2. Ve a `/home/tu-username/`
3. Sube todos los archivos de tu proyecto

---

## 🐍 Paso 4: Configurar Entorno Virtual

```bash
# En PythonAnywhere Console
$ mkvirtualenv --python=/usr/bin/python3.9 mi-entorno
$ workon mi-entorno
$ pip install -r requirements.txt
```

---

## 🗄️ Paso 5: Configurar Base de Datos

1. En PythonAnywhere: **Databases tab**
2. Crea una base de datos PostgreSQL
3. Copia los datos de conexión:
   - DB_NAME
   - DB_USER  
   - DB_PASSWORD
   - DB_HOST
   - DB_PORT

4. Configura variables de entorno:
```bash
$ export DB_NAME="tu-db-name"
$ export DB_USER="tu-db-user"
$ export DB_PASSWORD="tu-db-password"
$ export DB_HOST="tu-db-host"
$ export DB_PORT="5432"
```

---

## ⚙️ Paso 6: Configurar Variables de Entorno

En PythonAnywhere Console:
```bash
$ export SECRET_KEY="tu-secret-key-seguro"
$ export DEBUG="False"
$ export DOMAIN="tudominio.com"
$ export EMAIL_HOST_USER="avecbm2024@gmail.com"
$ export EMAIL_HOST_PASSWORD="vgum ugmo qubb mwbn"
```

---

## 🔄 Paso 7: Migraciones y Archivos Estáticos

```bash
# Migrar base de datos
$ python manage.py migrate

# Recolectar archivos estáticos
$ python manage.py collectstatic --noinput

# Crear superusuario
$ python manage.py createsuperuser
```

---

## 🌍 Paso 8: Configurar Aplicación Web

1. **Web tab → Add a new web app**
2. **Manual configuration → Python 3.9**
3. **Source code**: `/home/tu-username/mi-proyecto`
4. **Working directory**: `/home/tu-username/mi-proyecto`

### Configurar WSGI:
Edita tu archivo WSGI:
```python
import os
import sys

path = '/home/tu-username/mi-proyecto'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'base.settings_production'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

### Configurar Virtualenv:
Selecciona tu entorno virtual creado en el paso 4

---

## 📧 Paso 9: Probar Correos

```bash
$ python manage.py shell
>>> from django.core.mail import send_mail
>>> send_mail('Test', 'Mensaje de prueba', 'avecbm2024@gmail.com', ['avecbm2024@gmail.com'])
```

---

## 🔄 Paso 10: Recargar y Probar

1. **Web tab → Reload your web app**
2. Visita tu dominio: `https://tudominio.com`
3. Prueba el formulario de reseñas
4. Revisa que llegue el correo a `avecbm2024@gmail.com`

---

## ✅ Verificación Final

- [ ] La página carga correctamente
- [ ] Las reseñas se guardan en la base de datos
- [ ] Los correos llegan a `avecbm2024@gmail.com`
- [ ] SSL funciona (https://)
- [ ] Las imágenes se muestran correctamente

---

## 🆘 Soporte y Mantenimiento

### Ver errores:
- **Web tab → Logs**
- **Errors log** para ver problemas

### Comandos útiles:
```bash
# Ver logs
$ tail -f /var/log/nginx/error.log

# Recargar app
# Web tab → Reload

# Acceder a base de datos
$ python manage.py dbshell
```

---

## 📞 Contacto de Emergencia

Si algo falla:
1. Revisa los logs en PythonAnywhere
2. Verifica las variables de entorno
3. Prueba con `DEBUG=True` temporalmente
4. Contacta a soporte de PythonAnywhere

---

## 🎉 ¡Felicidades!

Tu aplicación Django de aviones a escala ahora está:
- ✅ Accesible globalmente
- ✅ Con dominio profesional
- ✅ Enviando correos automáticos
- ✅ Segura y en producción

Costo total: **$6-7/mes** por una presencia profesional completa.

# 🚀 Guía de Despliegue

## Despliegue Local

### Windows

1. **Instalar Python** (si no lo tienes):
   - Descarga desde: https://www.python.org/downloads/
   - Marca "Add Python to PATH"

2. **Clonar/Descargar proyecto**:
   ```bash
   cd C:\Users\DELL\.qodo\poniendome_riquisimo
   ```

3. **Ejecutar script**:
   ```bash
   iniciar.bat
   ```

### Linux/Mac

1. **Instalar Python**:
   ```bash
   # Linux
   sudo apt-get install python3 python3-pip
   
   # Mac
   brew install python3
   ```

2. **Clonar/Descargar proyecto**:
   ```bash
   cd ~/poniendome_riquisimo
   ```

3. **Ejecutar script**:
   ```bash
   chmod +x iniciar.sh
   ./iniciar.sh
   ```

## Despliegue en Producción

### Backend - Heroku

1. **Instalar Heroku CLI**:
   - Windows: https://devcenter.heroku.com/articles/heroku-cli
   - Linux/Mac: `brew install heroku/brew/heroku`

2. **Crear cuenta en Heroku**:
   - https://www.heroku.com/

3. **Configurar proyecto**:
   ```bash
   cd backend
   
   # Crear archivo Procfile
   echo "web: uvicorn main:app --host 0.0.0.0 --port $PORT" > Procfile
   
   # Crear archivo runtime.txt
   echo "python-3.11.0" > runtime.txt
   ```

4. **Desplegar**:
   ```bash
   heroku login
   heroku create tu-app-name
   git push heroku main
   ```

### Backend - Railway

1. **Crear cuenta en Railway**:
   - https://railway.app/

2. **Conectar repositorio GitHub**:
   - Conecta tu repo
   - Railway detectará automáticamente Python

3. **Configurar variables de entorno**:
   - DATABASE_URL
   - SECRET_KEY
   - MODEL_PATH

### Backend - AWS

1. **Crear instancia EC2**:
   - Ubuntu 20.04 LTS
   - t2.micro (free tier)

2. **Conectar y configurar**:
   ```bash
   ssh -i tu-key.pem ubuntu@tu-ip
   
   # Actualizar sistema
   sudo apt-get update
   sudo apt-get upgrade
   
   # Instalar Python
   sudo apt-get install python3 python3-pip
   
   # Clonar proyecto
   git clone tu-repo
   cd poniendome_riquisimo/backend
   
   # Instalar dependencias
   pip3 install -r requirements.txt
   
   # Ejecutar con Gunicorn
   pip3 install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 main:app
   ```

3. **Usar Nginx como proxy**:
   ```bash
   sudo apt-get install nginx
   
   # Configurar /etc/nginx/sites-available/default
   server {
       listen 80;
       server_name tu-dominio.com;
       
       location / {
           proxy_pass http://127.0.0.1:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   
   sudo systemctl restart nginx
   ```

### Frontend - Vercel

1. **Crear cuenta en Vercel**:
   - https://vercel.com/

2. **Conectar repositorio**:
   - Importar proyecto desde GitHub
   - Vercel detectará automáticamente que es un proyecto estático

3. **Configurar**:
   - Build Command: (dejar vacío)
   - Output Directory: `frontend`

4. **Desplegar**:
   - Vercel desplegará automáticamente

### Frontend - Netlify

1. **Crear cuenta en Netlify**:
   - https://www.netlify.com/

2. **Conectar repositorio**:
   - Drag & drop la carpeta `frontend`
   - O conectar GitHub

3. **Configurar**:
   - Publish directory: `frontend`

4. **Desplegar**:
   - Netlify desplegará automáticamente

### Frontend - GitHub Pages

1. **Crear repositorio**:
   ```bash
   git init
   git add .
   git commit -m "Initial commit"
   git branch -M main
   git remote add origin https://github.com/tu-usuario/poniendome-riquisimo.git
   git push -u origin main
   ```

2. **Habilitar GitHub Pages**:
   - Settings → Pages
   - Source: main branch
   - Folder: /frontend

3. **Acceder**:
   - https://tu-usuario.github.io/poniendome-riquisimo/

## Docker (Recomendado)

### Crear Dockerfile para Backend

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/ .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Crear docker-compose.yml

```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=postgresql://user:password@db:5432/poniendome_riquisimo
      - SECRET_KEY=tu-clave-secreta
    depends_on:
      - db
  
  frontend:
    image: nginx:alpine
    ports:
      - "80:80"
    volumes:
      - ./frontend:/usr/share/nginx/html
  
  db:
    image: postgres:15
    environment:
      - POSTGRES_USER=user
      - POSTGRES_PASSWORD=password
      - POSTGRES_DB=poniendome_riquisimo
    volumes:
      - postgres_data:/var/lib/postgresql/data

volumes:
  postgres_data:
```

### Ejecutar con Docker

```bash
docker-compose up -d
```

## Configuración de Dominio

### Comprar dominio
- GoDaddy, Namecheap, Google Domains, etc.

### Configurar DNS
- Apuntar a tu servidor (IP o CNAME)
- Esperar propagación (24-48 horas)

### SSL/HTTPS
- Let's Encrypt (gratuito)
- Certbot: `sudo certbot certonly --standalone -d tu-dominio.com`

## Monitoreo y Mantenimiento

### Logs
```bash
# Heroku
heroku logs --tail

# AWS
tail -f /var/log/syslog

# Docker
docker logs -f nombre-contenedor
```

### Backups
```bash
# PostgreSQL
pg_dump -U user poniendome_riquisimo > backup.sql

# Restaurar
psql -U user poniendome_riquisimo < backup.sql
```

### Actualizaciones
```bash
# Actualizar dependencias
pip install --upgrade -r requirements.txt

# Redeploy
git push heroku main
```

## Checklist de Despliegue

- [ ] Variables de entorno configuradas
- [ ] Base de datos configurada
- [ ] Modelo CNN integrado
- [ ] CORS configurado correctamente
- [ ] SSL/HTTPS habilitado
- [ ] Backups configurados
- [ ] Monitoreo configurado
- [ ] Dominio apuntando correctamente
- [ ] Pruebas en producción
- [ ] Documentación actualizada

## Costos Estimados

### Gratuito
- Heroku (limitado)
- Railway (limitado)
- Vercel (frontend)
- Netlify (frontend)
- GitHub Pages (frontend)

### Pagos
- AWS: $5-50/mes
- DigitalOcean: $5-20/mes
- Heroku Pro: $50+/mes
- Dominio: $10-15/año

## Troubleshooting

### Error: "Port already in use"
```bash
# Cambiar puerto en main.py
uvicorn.run(app, host="0.0.0.0", port=8001)
```

### Error: "Module not found"
```bash
pip install -r requirements.txt
```

### Error: "Connection refused"
- Verifica que el backend esté corriendo
- Verifica la URL de la API en el frontend

### Error: "CORS error"
- Verifica que CORS esté habilitado en main.py
- Verifica que la URL del frontend esté en CORS_ORIGINS

---

**¡Listo para desplegar! 🚀**

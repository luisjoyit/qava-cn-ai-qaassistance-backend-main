
# Construir la imagen de Docker para Cv-ats-filter
echo "Construyendo la imagen de Docker para qa-assistance..."
docker-compose build

# Levantar el contenedor
echo "Levantando el contenedor de qa-assistance..."
docker-compose up -d

echo "El contenedor de qa-asistant está levantado y ejecutándose."

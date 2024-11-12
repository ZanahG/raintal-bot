FROM python:3.11-slim

# Instala las dependencias del sistema
RUN apt-get update && apt-get install -y \
    wget \
    gnupg \
    unzip \
    && rm -rf /var/lib/apt/lists/*

# Añade el repositorio de Google Chrome y lo instala en una versión específica
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list' && \
    apt-get update && \
    apt-get install -y google-chrome-stable=114.0.5735.90-1  # Instala una versión compatible de Chrome

# Descarga e instala la versión específica de ChromeDriver
RUN wget -O /tmp/chromedriver.zip "https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip" && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip

# Configura el directorio de trabajo y copia los archivos
WORKDIR /app
COPY . /app

# Instala las dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Comando de inicio del bot
CMD ["python", "bot.py"]

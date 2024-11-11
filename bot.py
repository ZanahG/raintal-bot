import discord
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime, timedelta
import asyncio
import re
import os

service = Service('C:\\Users\\Zanah\\Documents\\chromedriver-win64\\chromedriver.exe')
options = webdriver.ChromeOptions()
options.binary_location = "C:/Program Files/BraveSoftware/Brave-Browser/Application/brave.exe"  
#options.add_argument('--headless')
driver = webdriver.Chrome(service=service, options=options)

driver.get("https://questlog.gg/throne-and-liberty/en/rain-schedule")

intents = discord.Intents.default()
intents.message_content = True

TOKEN = os.getenv("DISCORDBOT_TOKEN")
GUILD_ID = 1028144231333756988
CHANNEL_ID = 1305441249469268008
URL = "https://questlog.gg/throne-and-liberty/en/rain-schedule"

client = discord.Client(intents=intents)

def obtener_contador_lluvia():
    try:
        contador_elemento = driver.find_element(By.XPATH, "//span[contains(text(),'Raining in')]")
        contador_texto = driver.execute_script("return arguments[0].textContent;", contador_elemento)
        print("Próxima lluvia (JavaScript):", contador_texto)
        match = re.search(r'(\d+)h\s*(\d*)m?', contador_texto)
        if match:
            horas = int(match.group(1)) if match.group(1) else 0
            minutos = int(match.group(2)) if match.group(2) else 0
            tiempo_restante = timedelta(hours=horas, minutes=minutos)
            return tiempo_restante
        else:
            print("No se encontró el formato de tiempo.")
            return None
    except Exception as e:
        print("Error al obtener el contador de lluvia:", e)
        return None

async def verificar_lluvia():
    while True:
        tiempo_restante = obtener_contador_lluvia()
        if tiempo_restante is not None:
            print(f"Tiempo restante para la próxima lluvia: {tiempo_restante}")
            if tiempo_restante <= timedelta(minutes=60):
                canal = client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)
                if canal:
                    await canal.send("¡Atención! 🌧️ La lluvia comenzará en menos de 60 minutos. ¡Prepárate!")
                    print("Mensaje de alerta de lluvia enviado")
                break
        else:
            print("No se pudo obtener el tiempo restante. Intentando nuevamente...")
        await asyncio.sleep(10)

@client.event
async def on_ready():
    print(f'Bot conectado como {client.user}')
    canal = client.get_guild(GUILD_ID).get_channel(CHANNEL_ID)
    if canal:
        await canal.send("El bot está conectado y listo para monitorear la lluvia.")
    client.loop.create_task(verificar_lluvia())

@client.event
async def on_message(message):
    if message.content.lower() == "!lluvia" and message.author != client.user:
        tiempo_restante = obtener_contador_lluvia()
        if tiempo_restante is not None:
            horas, remainder = divmod(tiempo_restante.total_seconds(), 3600)
            minutos, _ = divmod(remainder, 60)
            await message.channel.send(f"🌧️ Tiempo restante para la próxima lluvia: {int(horas)} horas y {int(minutos)} minutos.")
        else:
            await message.channel.send("No se pudo obtener el tiempo para la próxima lluvia. Inténtalo nuevamente.")

client.run(TOKEN)
driver.quit()
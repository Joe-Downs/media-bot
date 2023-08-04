import configparser

config = configparser.ConfigParser()
config.read("config.ini")

# Get the custom database name from the config file, if there is one. If there
# is, always use that. If not, create a new database every time the bot starts
# up, giving it a timestamp.
def getDatabaseName():
    # Strip the extension if there is one, we'll add one. Since the user might
    # configure their filename without it.
    dbName = config["Bot"]["DatabaseName"]
    if len(dbName) == 0:
        nowDatetime = datetime.now()
        timestamp = nowDatetime.strftime("%y%m%d-%H%M%S")
        dbName = f"media-{timestamp}"
    else:
        # Strip the extension if there is one, we'll add one. Since the user
        # might configure their filename without it.
        dbName = dbName.rstrip(".db")
    return f"{dbName}.db"

def getLogLevel():
    logLevel = config["General"]["LogLevel"].upper()
    return logLevel

def getPrefix():
    prefix = config["Bot"]["CommandPrefix"]
    return prefix

def getToken():
    token = str(config["Bot"]["DiscordToken"])
    return token

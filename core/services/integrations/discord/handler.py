class DiscordHandler:
    def __init__(self, message):
        self.message = message
    
    async def send_message(self, text):
        try:
            await self.message.channel.send(text)
        except Exception as e:
            raise e

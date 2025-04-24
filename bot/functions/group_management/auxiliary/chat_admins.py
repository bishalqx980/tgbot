from telegram import Chat, ChatMember

class ChatAdmins:
    def __init__(self):
        self.is_user_admin = None
        self.is_user_owner = None

        self.is_victim_admin = None
        self.is_victim_owner = None

        self.is_bot_admin = None
    

    async def fetch_admins(self, chat: Chat, bot_id=None, user_id=None, victim_id=None):
        """
        :param chat: `update.effective_chat`
        :param bot_id: `context.bot.id`
        :param user_id: `update.effective_user.id`
        :param victim_id: `replied user id`
        :returns Class: ChatAdmins
        """
        chat_admins = await chat.get_administrators()

        for admin in chat_admins:
            admin_id = admin.user.id
            admin_status = admin.status

            if user_id and admin_id == user_id:
                if admin_status == ChatMember.ADMINISTRATOR:
                    self.is_user_admin = admin
                elif admin_status == ChatMember.OWNER:
                    self.is_user_owner = admin
            
            if victim_id and admin_id == victim_id:
                if admin_status == ChatMember.ADMINISTRATOR:
                    self.is_victim_admin = admin
                elif admin_status == ChatMember.OWNER:
                    self.is_victim_owner = admin
            
            if bot_id and admin_id == bot_id:
                self.is_bot_admin = admin

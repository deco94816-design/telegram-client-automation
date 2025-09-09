#!/usr/bin/env python3
"""
🤖 Enhanced Dual Telegram Userbot System
Version: 4.0
Author: Custom Bot
Enhanced with: Auto-rounds, Smart Reply, Interactive Menu
"""

import asyncio
import logging
import os
import json
import random
from datetime import datetime, timedelta
from telethon import TelegramClient, events
from telethon.tl.types import Channel, Chat, User
from telethon.errors import FloodWaitError, ChatWriteForbiddenError, UserBannedInChannelError

# ----------------------------
# ⚡ Configure Logging
# ----------------------------
logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)

# =====================================================
# 🎯 Enhanced Main Class: DualTelegramUserBot
# =====================================================

class DualTelegramUserBot:
    def __init__(self):
        # ----------------------------
        # Bot Credentials - Direct Setup
        # ----------------------------
        self.api_id_1 = 29237230
        self.api_hash_1 = '04c8ff9738de961972a3ce478991b4ee'
        self.phone_1 = '+919625273961'
        
        self.api_id_2 = 22943378
        self.api_hash_2 = '19aae02447e0f6c7831926f41a34d978'
        self.phone_2 = '+919818571901'
        
        # Initialize clients
        self.client_1 = TelegramClient('userbot1_session', self.api_id_1, self.api_hash_1)
        self.client_2 = TelegramClient('userbot2_session', self.api_id_2, self.api_hash_2)
        
        # Store groups for each bot
        self.groups_1 = []
        self.groups_2 = []
        
        # 📊 Enhanced Settings - Auto-adjusting rounds
        self.base_delay = 60
        self.base_rounds = 5
        self.auto_adjust_rounds = True
        
        # 💬 Smart Reply System
        self.replied_users = {}
        self.reply_cooldown = 3600
        self.auto_reply_enabled = True
        
        # Default messages
        self.default_message = """🎯 Special Offer Available! 💎

🚀 Exclusive deals waiting for you!
💰 Limited time - Maximum savings!

Contact: @Nolanbro for more details.

⏰ Don't miss out - Act now! 🔥"""

        # 🎮 Menu System
        self.menu_active = False
        self.admin_user_id = []

    # ----------------------------
    # 🚀 Start both bots + Enhanced features
    # ----------------------------
    async def start_both_bots(self):
        print("🔄 Starting Enhanced Dual Userbot System...")
        try:
            # Start Bot 1
            print("🤖 Connecting Userbot #1...")
            await self.client_1.start(phone=self.phone_1)
            me1 = await self.client_1.get_me()
            print(f"✅ Userbot #1 connected as {me1.first_name}")
            
            # Start Bot 2
            print("🤖 Connecting Userbot #2...")
            await self.client_2.start(phone=self.phone_2)
            me2 = await self.client_2.get_me()
            print(f"✅ Userbot #2 connected as {me2.first_name}")
            
            # Set admin (both bot owners can control)
            if not self.admin_user_id:
                self.admin_user_id = [me1.id, me2.id]
            elif isinstance(self.admin_user_id, int):
                self.admin_user_id = [self.admin_user_id, me1.id, me2.id]
                
            print(f"🔑 Admin IDs set: {self.admin_user_id}")
            
            # Register enhanced handlers
            self.register_smart_reply(self.client_1, 1)
            self.register_smart_reply(self.client_2, 2)
            self.register_menu_handler(self.client_1)
            self.register_menu_handler(self.client_2)
            
            return True
        except Exception as e:
            print(f"❌ Connection Error: {e}")
            return False

    # ----------------------------
    # 🧠 Smart Reply System - Reply only once per user with cooldown
    # ----------------------------
    def register_smart_reply(self, client, bot_num):
        @client.on(events.NewMessage(incoming=True))
        async def smart_reply_handler(event):
            if not self.auto_reply_enabled or not event.is_private:
                return
                
            try:
                sender = await event.get_sender()
                user_id = sender.id
                current_time = datetime.now()
                
                # Check if we've replied to this user recently
                if user_id in self.replied_users:
                    last_reply_time = self.replied_users[user_id]
                    if current_time - last_reply_time < timedelta(seconds=self.reply_cooldown):
                        return
                
                # Generate personalized auto-reply message
                user_name = self.get_user_display_name(sender)
                personalized_reply = self.generate_personalized_reply(user_name, sender)
                
                # Send auto-reply
                await event.respond(personalized_reply)
                self.replied_users[user_id] = current_time
                
                print(f"💬 Bot#{bot_num} auto-replied to {user_name} (ID: {user_id})")
                
                # Clean old entries
                cutoff_time = current_time - timedelta(hours=24)
                self.replied_users = {
                    uid: time for uid, time in self.replied_users.items() 
                    if time > cutoff_time
                }
                
            except Exception as e:
                print(f"❌ Bot#{bot_num} auto-reply failed: {e}")

    # ----------------------------
    # 👤 Get User Display Name
    # ----------------------------
    def get_user_display_name(self, sender):
        if hasattr(sender, 'first_name') and sender.first_name:
            if hasattr(sender, 'last_name') and sender.last_name:
                return f"{sender.first_name} {sender.last_name}"
            return sender.first_name
        elif hasattr(sender, 'username') and sender.username:
            return f"@{sender.username}"
        else:
            return "Friend"

    # ----------------------------
    # 🎨 Generate Personalized Auto-Reply
    # ----------------------------
    def generate_personalized_reply(self, user_name, sender):
        greetings = [
            f"Hello {user_name}! 👋",
            f"Hi there {user_name}! 😊",
            f"Hey {user_name}! 🤖",
            f"Greetings {user_name}! ✨",
        ]
        
        main_messages = [
            "Thanks for reaching out! I've received your message and will get back to you soon.",
            "Your message has been received! I'll respond as quickly as possible.",
            "Thank you for contacting me! I'll reply to you shortly.",
            "Got your message! I'll be in touch with you very soon.",
        ]
        
        closings = [
            "For urgent matters, feel free to contact @Nolanbro directly! 🚀",
            "If it's urgent, you can also reach out to @Nolanbro! ⚡",
            "Need immediate assistance? Contact @Nolanbro! 💫",
            "For faster response on urgent matters, try @Nolanbro! 🎯",
        ]
        
        current_hour = datetime.now().hour
        if 5 <= current_hour < 12:
            time_greeting = "Good morning"
        elif 12 <= current_hour < 17:
            time_greeting = "Good afternoon"  
        elif 17 <= current_hour < 22:
            time_greeting = "Good evening"
        else:
            time_greeting = "Good night"
            
        if user_name.startswith('@'):
            personalized_greeting = f"{time_greeting} {user_name}! 👋"
        else:
            personalized_greeting = f"{time_greeting} {user_name}! 😊"
        
        personalized_reply = f"""{personalized_greeting}

⏳ {random.choice(main_messages)}

{random.choice(closings)}

🤖 This is an automated response - I'll personally reply soon!"""
        
        return personalized_reply

    # ----------------------------
    # 🎮 Interactive Menu System
    # ----------------------------
    def register_menu_handler(self, client):
        # Add a debug handler for any message
        @client.on(events.NewMessage(incoming=True))
        async def debug_handler(event):
            if event.is_private:
                sender = await event.get_sender()
                print(f"📨 Debug: Message from {sender.first_name} (ID: {sender.id}): {event.message.message[:50]}")
                
                # If it's a command and user is not in admin list, add them temporarily
                if event.message.message.startswith('/') and sender.id not in self.admin_user_id:
                    print(f"🔓 Adding user {sender.id} to admin list for testing")
                    self.admin_user_id.append(sender.id)

        @client.on(events.NewMessage(incoming=True, pattern=r'^/menu|^/start|^/help'))
        async def menu_handler(event):
            if not event.is_private:
                return
                
            sender = await event.get_sender()
            print(f"🔍 Menu request from: {sender.first_name} (ID: {sender.id})")
            
            if sender.id not in self.admin_user_id:
                print(f"⚠️ Unauthorized user: {sender.id}")
                await event.respond("❌ Access denied. This bot is for authorized users only.")
                return
                
            print(f"✅ Authorized user, showing menu...")
            await self.show_main_menu(event)

        @client.on(events.NewMessage(incoming=True, pattern=r'^/broadcast'))
        async def broadcast_handler(event):
            if not event.is_private or (await event.get_sender()).id not in self.admin_user_id:
                return
            await self.handle_broadcast_command(event)

        @client.on(events.NewMessage(incoming=True, pattern=r'^/premium'))
        async def premium_handler(event):
            if not event.is_private or (await event.get_sender()).id not in self.admin_user_id:
                return
            await self.handle_premium_broadcast(event)

        @client.on(events.NewMessage(incoming=True, pattern=r'^/settings'))
        async def settings_handler(event):
            if not event.is_private or (await event.get_sender()).id not in self.admin_user_id:
                return
            await self.show_settings_menu(event)

        @client.on(events.NewMessage(incoming=True, pattern=r'^/stats'))
        async def stats_handler(event):
            if not event.is_private or (await event.get_sender()).id not in self.admin_user_id:
                return
            await self.show_stats(event)

    # ----------------------------
    # 📱 Main Menu Display
    # ----------------------------
    async def show_main_menu(self, event):
        menu_text = f"""🤖 **DUAL USERBOT CONTROL PANEL** 🎮

📊 **Main Commands:**
/broadcast - Start broadcasting campaign
/premium - Premium alternate broadcast (10-20 rounds)
/settings - Configure bot settings  
/stats - View bot statistics
/menu - Show this menu

🎯 **Quick Actions:**
• Auto-reply: {'ON' if self.auto_reply_enabled else 'OFF'}
• Smart rounds: {'ON' if self.auto_adjust_rounds else 'OFF'}
• Active groups: {len(self.groups_1)} + {len(self.groups_2)}

💎 **Premium Features:**
• /premium - Advanced alternate broadcast
• Custom rounds: 10-20 (randomly selected)
• Bot1 → delay → Bot2 → delay → repeat
• Optimal timing for maximum reach

💡 **Status:** All systems operational ✅"""
        
        await event.respond(menu_text)

    # ----------------------------
    # ⚙️ Settings Menu
    # ----------------------------
    async def show_settings_menu(self, event):
        settings_text = f"""⚙️ **SETTINGS PANEL**

🔧 **Current Configuration:**
• Base Delay: {self.base_delay}s
• Base Rounds: {self.base_rounds}
• Auto-adjust rounds: {'ON' if self.auto_adjust_rounds else 'OFF'}
• Auto-reply cooldown: {self.reply_cooldown//60}min

📝 **Available Commands:**
/broadcast delay [seconds] - Change delay
/broadcast rounds [number] - Change rounds
/premium - Premium broadcast settings

Example: /broadcast delay 120"""
        await event.respond(settings_text)

    # ----------------------------
    # 📊 Statistics Display
    # ----------------------------
    async def show_stats(self, event):
        stats_text = f"""📊 **BOT STATISTICS**

🤖 **Bot Status:**
• Bot #1 Groups: {len(self.groups_1)}
• Bot #2 Groups: {len(self.groups_2)}
• Total Reach: {len(self.groups_1) + len(self.groups_2)} groups

💬 **Reply System:**
• Users replied to: {len(self.replied_users)}
• Auto-reply status: {'Active' if self.auto_reply_enabled else 'Disabled'}
• Cooldown period: {self.reply_cooldown//60} minutes

⚡ **Performance:**
• Smart rounds: {'Enabled' if self.auto_adjust_rounds else 'Disabled'}
• Current delay: {self.base_delay}s
• Base rounds: {self.base_rounds}"""
        await event.respond(stats_text)

    # ----------------------------
    # 🎯 Enhanced Group Detection
    # ----------------------------
    async def get_groups_for_bot(self, bot_num):
        client = self.client_1 if bot_num == 1 else self.client_2
        groups = []
        
        async for dialog in client.iter_dialogs():
            if isinstance(dialog.entity, (Channel, Chat)):
                if isinstance(dialog.entity, Channel):
                    if dialog.entity.megagroup or not dialog.entity.broadcast:
                        groups.append({
                            'entity': dialog.entity,
                            'title': dialog.title,
                            'members': getattr(dialog.entity, 'participants_count', 0)
                        })
                else:
                    groups.append({
                        'entity': dialog.entity,
                        'title': dialog.title,
                        'members': getattr(dialog.entity, 'participants_count', 0)
                    })
        
        if bot_num == 1:
            self.groups_1 = groups
        else:
            self.groups_2 = groups
            
        print(f"📊 Bot #{bot_num}: Found {len(groups)} groups")
        return groups

    # ----------------------------
    # 🧮 Smart Rounds Calculator
    # ----------------------------
    def calculate_optimal_rounds(self):
        if not self.auto_adjust_rounds:
            return self.base_rounds
            
        total_groups = len(self.groups_1) + len(self.groups_2)
        
        if total_groups <= 10:
            return self.base_rounds + 2
        elif total_groups <= 30:
            return self.base_rounds
        elif total_groups <= 50:
            return max(3, self.base_rounds - 1)
        else:
            return max(2, self.base_rounds - 2)

    # ----------------------------
    # 🛡️ Enhanced Safe Send
    # ----------------------------
    async def safe_send(self, client, entity, msg, bot_num):
        try:
            await client.send_message(entity, msg)
            print(f"✅ Bot#{bot_num} → {entity.title}")
            return True
        except FloodWaitError as e:
            print(f"⚠️ FloodWait {e.seconds}s on Bot#{bot_num} in {entity.title}")
            await asyncio.sleep(e.seconds + 1)
            return False
        except (ChatWriteForbiddenError, UserBannedInChannelError):
            print(f"🚫 Bot#{bot_num} restricted in {entity.title}")
            return False
        except Exception as e:
            print(f"❌ Bot#{bot_num} error in {entity.title}: {str(e)[:50]}")
            return False

    # ----------------------------
    # 📢 Broadcast Command Handler
    # ----------------------------
    async def handle_broadcast_command(self, event):
        command_parts = event.message.message.split(' ', 2)
        
        if len(command_parts) == 1:
            options_text = """📢 **BROADCAST OPTIONS**

**Quick Commands:**
`/broadcast start` - Use default message & settings
`/broadcast custom [message]` - Broadcast custom message
`/broadcast test` - Test broadcast (1 round only)

**Examples:**
`/broadcast custom 🎉 New promotion available!`
`/broadcast start`"""
            await event.respond(options_text)
            return
            
        action = command_parts[1].lower()
        
        if action == 'start':
            await event.respond("🚀 Starting broadcast campaign...")
            await self.smart_alternate_broadcast()
            await event.respond("✅ Broadcast campaign completed!")
            
        elif action == 'custom' and len(command_parts) > 2:
            custom_msg = command_parts[2]
            await event.respond("📝 Broadcasting custom message...")
            await self.smart_alternate_broadcast(msg=custom_msg)
            await event.respond("✅ Custom broadcast completed!")
            
        elif action == 'test':
            await event.respond("🧪 Starting test broadcast...")
            await self.smart_alternate_broadcast(custom_rounds=1)
            await event.respond("✅ Test broadcast completed!")

    # ----------------------------
    # 💎 Premium Broadcast Handler
    # ----------------------------
    async def handle_premium_broadcast(self, event):
        command_parts = event.message.message.split(' ', 2)
        
        if len(command_parts) == 1:
            suggested_rounds = random.randint(10, 20)
            menu_text = f"""💎 **PREMIUM ALTERNATE BROADCAST**

🎯 **What it does:**
• Bot1 sends to all groups → waits → Bot2 sends to all groups → repeat
• High-impact campaign with 10-20 rounds
• Maximum reach with optimal timing

⚙️ **Commands:**
`/premium start` - Auto broadcast (random 10-20 rounds)
`/premium custom [message]` - Custom message broadcast  
`/premium rounds [N]` - Specific rounds (10-20 only)

🎲 **Suggested:** {suggested_rounds} rounds
📊 **Total groups:** {len(self.groups_1) + len(self.groups_2)}"""
            await event.respond(menu_text)
            return
            
        action = command_parts[1].lower()
        
        if action == 'start':
            await event.respond("💎 Starting Premium Alternate Broadcast...")
            await self.premium_alternate_broadcast()
            await event.respond("✅ Premium broadcast completed!")
            
        elif action == 'custom' and len(command_parts) > 2:
            custom_msg = command_parts[2]
            await event.respond("💎 Starting Custom Premium Broadcast...")
            await self.premium_alternate_broadcast(msg=custom_msg)
            await event.respond("✅ Custom premium broadcast completed!")
            
        elif action == 'rounds' and len(command_parts) > 2:
            try:
                rounds = int(command_parts[2])
                if 10 <= rounds <= 20:
                    await event.respond(f"💎 Starting Premium Broadcast with {rounds} rounds...")
                    await self.premium_alternate_broadcast(custom_rounds=rounds)
                    await event.respond("✅ Premium broadcast completed!")
                else:
                    await event.respond("❌ Premium rounds must be between 10-20")
            except ValueError:
                await event.respond("❌ Invalid number format")

    # ----------------------------
    # 🎯 Smart Alternate Broadcast
    # ----------------------------
    async def smart_alternate_broadcast(self, msg=None, custom_rounds=None, custom_delay=None):
        if not msg:
            msg = self.default_message
            
        rounds = custom_rounds if custom_rounds else self.calculate_optimal_rounds()
        delay = custom_delay if custom_delay else self.base_delay
        
        print(f"\n🚀 SMART ALTERNATE BROADCAST")
        print(f"📊 Calculated {rounds} rounds with {delay}s delay")
        print(f"🎯 Total groups: Bot1({len(self.groups_1)}) + Bot2({len(self.groups_2)})")
        
        start_time = datetime.now()
        
        for round_num in range(1, rounds + 1):
            print(f"\n{'='*50}")
            print(f"🔥 ROUND {round_num}/{rounds}")
            print(f"{'='*50}")

            # Bot 1 broadcast
            print(f"\n🤖 BOT #1 Broadcasting...")
            await

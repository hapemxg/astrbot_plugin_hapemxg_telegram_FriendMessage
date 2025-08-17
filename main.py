from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register(
    "telegram_private_blocker", 
    "YourName", 
    "禁止在Telegram私聊中使用机器人", 
    "1.0.0"
)
class TelegramPrivateBlockerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.block_message = "抱歉，根据设定，我无法在私聊中回复您。"

    # 使用通用消息事件监听器，并设置一个非常高的优先级（默认为0）
    # 这样可以确保这个函数在其他所有指令和消息处理器之前运行
    @filter.event_message_type(filter.EventMessageType.ALL, priority=999)
    async def block_telegram_private_chat(self, event: AstrMessageEvent):
        """
        拦截并阻止在Telegram私聊中使用机器人
        """
        # 获取会话ID
        # AstrMessageEvent -> AstrBotMessage -> session_id
        session_id = event.message_obj.session_id
        
        # 检查会话ID是否以 'telegram:FriendMessage' 开头
        if session_id.startswith("telegram:FriendMessage"):
            logger.info(f"检测到Telegram私聊消息，已拦截。会话ID: {session_id}")
            
            # 返回预设的回复
            yield event.plain_result(self.block_message)
            
            # 停止事件传播，后续的任何插件（包括指令处理、LLM调用）都不会被执行
            event.stop_event()

    # 你仍然可以保留其他的指令，它们在非Telegram私聊环境下会正常工作
    @filter.command("helloworld")
    async def helloworld(self, event: AstrMessageEvent):
        user_name = event.get_sender_name()
        yield event.plain_result(f"Hello, {user_name}!")
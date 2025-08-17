from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api import logger

@register(
    "telegram_private_blocker",
    "hapemxg",
    "禁止在Telegram私聊中使用机器人",
    "1.0.0"
)
class TelegramPrivateBlockerPlugin(Star):
    def __init__(self, context: Context):
        super().__init__(context)
        self.block_message = "抱歉，根据设定，我无法在私聊中回复您。（ps：但是你还可以用一些不会调用LLM的指令，如/好感度 获取你和bot的当前好感度）"

    @filter.event_message_type(filter.EventMessageType.ALL, priority=999)
    async def block_telegram_private_chat(self, event: AstrMessageEvent):
        """
        拦截并阻止在Telegram私聊中使用机器人
        """
        platform = event.get_platform_id()
        message_type = event.get_message_type()

        if platform == "telegram" and hasattr(message_type, 'name') and message_type.name == "FRIEND_MESSAGE":
            # 1. 核心任务：设置停止标记。
            event.stop_event()

            # 2. 使用 try...except 来保护网络操作。
            try:
                # 3. 回归框架推荐的、最简单的方式来发送回复。
                yield event.plain_result(self.block_message)
            except Exception as e:
                # 如果发送时出现网络超时等任何错误，我们只记录日志，
                # 不让异常中断我们的拦截逻辑。
                logger.warning(f"【TG拦截器】发送拦截回复时发生网络错误: {e}")
            
            # 4. 插件函数干净地返回，框架会严格遵守 stop_event 标记。
            return
from astrbot.api.event import filter, AstrMessageEvent
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
        logger.info("【TG私聊拦截器】插件已实例化。")

    async def initialize(self):
        logger.info("【TG私聊拦截器】插件已成功加载并初始化！")

    @filter.event_message_type(filter.EventMessageType.ALL, priority=999)
    async def block_telegram_private_chat(self, event: AstrMessageEvent):
        """
        拦截并阻止在Telegram私聊中使用机器人
        """
        platform = event.get_platform_id() 
        message_type = event.get_message_type()
        
        # 增加一个更详细的日志，打印出类型的名字，方便确认
        message_type_name = message_type.name if hasattr(message_type, 'name') else str(message_type)
        logger.info(f"--- 【TG私聊拦截器】捕获到新消息 ---")
        logger.info(f"处理器正在运行 -> 平台: [{platform}], 消息类型对象: [{message_type}], 类型名: [{message_type_name}]")

        # 核心改动：我们直接比较 message_type 对象的 .name 属性，这是一个字符串
        # 根据日志，这个名字就是 "FRIEND_MESSAGE"
        if platform == "telegram" and message_type.name == "FRIEND_MESSAGE":
            logger.info(f"条件满足：是Telegram私聊消息。准备拦截并停止事件传播。")
            
            yield event.plain_result(self.block_message)
            event.stop_event()
            logger.info(f"事件已停止。")
        else:
            logger.info(f"条件不满足：不是Telegram私聊消息，放行。")
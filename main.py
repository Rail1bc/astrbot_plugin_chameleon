from astrbot.api.event import filter, AstrMessageEvent, MessageEventResult
from astrbot.api.star import Context, Star, register
from astrbot.api import logger
from astrbot.core.log import LogManager

from .database.db_connection import DatabaseConnector

@register("chameleon",
          "Rail1bc",
          "让角色身份动态演进",
          "0.1",
          "https://github.com/Rail1bc/astrbot_plugin_chameleon"
          )
class MyPlugin(Star):
    def __init__(self, context: Context, config: dict):
        super().__init__(context)
        self.config = config
        self.context = context
        self.logger = LogManager.GetLogger(log_name="Chameleon")

    async def initialize(self):
        """可选择实现异步的插件初始化方法，当实例化该插件类之后会自动调用该方法。"""

    async def terminate(self):
        """可选择实现异步的插件销毁方法，当插件被卸载/停用时会调用。"""

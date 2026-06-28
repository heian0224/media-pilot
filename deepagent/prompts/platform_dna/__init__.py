"""Platform voice/structure DNA — distilled from platform-writing/references/*.md.
Each constant is injected into the writing subagent prompt so copy is platform-native."""
from .wechat import WECHAT
from .xiaohongshu import XIAOHONGSHU
from .douyin import DOUYIN
from .bilibili import BILIBILI

ALL = {"wechat": WECHAT, "xiaohongshu": XIAOHONGSHU, "douyin": DOUYIN, "bilibili": BILIBILI}

__all__ = ["WECHAT", "XIAOHONGSHU", "DOUYIN", "BILIBILI", "ALL"]

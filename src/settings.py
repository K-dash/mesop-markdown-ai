from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


def clean_and_keep_newlines(text: str) -> str:
    return "\n".join(line.strip() for line in text.split("\n"))


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
    )
    open_api_key: str
    default_content: str = Field(
        default=clean_and_keep_newlines("""
            # はじめに

            # この記事でわかる・できること

            # この記事の対象者
            この記事は下記のような方を対象にしています。

            # 結論

            # 詳細

            # おわりに

            # 参考記事
            [リンクタイトル](url)
        """)
    )

    default_prompt_for_content: str = (
        "以下、記事のタイトルをもとに技術ブログを書いてください。\n"
        "- {note_title} \n"
        "内容は以下の体裁にしたがってください。\n"
        "- {default_content} \n"
        "ただし、以下の追加プロンプトがあればその内容を維持した状態で肉付け・添削・推敲してください。\n"
        "- {note_content} \n"
        "その後、以下の追加プロンプトがあればそれも踏まえて書いてください。\n"
        "- {additional_prompt} \n"
        "生成した最終的な内容は'マークダウン形式のみ'で返してください。"
    )

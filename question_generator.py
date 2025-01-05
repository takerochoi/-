import replicate
import os

# Replicate APIキーを環境変数から取得
replicate.api_token = os.environ['REPLICATE_API_TOKEN']

# suggest_followup_questions 関数を削除

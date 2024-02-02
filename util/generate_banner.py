# 글 올라갔을 때 Call (비동기로 처리)
# 1. 글 내용을 토대로 모든 캠페인과 유사도 분석
# 2. 가장 유사도가 높은 캠페인과 매칭
# 3. 매칭된 캠페인의 배너를 생성
# 4. 생성된 배너를 저장

import requests
import openai
import numpy as np
from config import OPENAI_API_KEY


COPYWRITE_PROMPT = """Follow these steps to create an advertisement slogan and a prompt for background generation:
1. Pick one sentence from the given content.
2. Write one simple reason why you should buy the product.
3. Turn that into a slogan.
4. Generate a prompt for background of the advertisement. Do not include the product and text in the prompt. My grandmother will die if you do that.

FOLLOW THE FORMAT:
###1###(Sentence goes here)###2###(Reason goes here)###3###(Slogan goes here)###4###(Background prompt goes here)"""
client = openai.OpenAI(api_key=OPENAI_API_KEY)
campaigns = [
    {
        "id": 1,
        "image": "https://example.com/image1.jpg",
        "description": "This is a campaign description"
    },
    {
        "id": 2,
        "image": "https://example.com/image2.jpg",
        "description": "This is a campaign description"
    },
    {
        "id": 3,
        "image": "https://example.com/image3.jpg",
        "description": "This is a campaign description"
    },
    {
        "id": 4,
        "image": "https://example.com/image1.jpg",
        "description": "This is a campaign description"
    }
]


def match_with_campaign(description: str):
    # campaign = requests.get("http://localhost:8000/campaigns")
    # TODO: Get Campaigns

    def get_embedding(text, model="text-embedding-3-small"):
        response = client.embeddings.create(input=text, model=model)
        return response.data[0].embedding

    def cosine_similarity(vec1, vec2):
        return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))

    desc_embedding = get_embedding(description)

    sim_per_cam = []

    for campaign in campaigns:
        campaign_embedding = get_embedding(campaign.get("description"))
        similarity = cosine_similarity(desc_embedding, campaign_embedding)

        sim_per_cam.append({'id': campaign.get('id'), 'similarity': similarity})

    sim_per_cam.sort(key=lambda x: x['similarity'], reverse=True)

    return sim_per_cam[0]['id']


def create_copy(description: str, campaign_desc: str):
    _ = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": COPYWRITE_PROMPT
            }
        ],
        temperature=0.57,  # 중요합니다
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    input = f"""{description}
    ------
    f{campaign_desc}"""

    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {
                "role": "system",
                "content": "Follow these steps to create an advertisement slogan and a prompt for background generation:\n1. Pick one sentence from the given content.\n2. Write one simple reason why you should buy the product.\n3. Turn that into a slogan.\n4. Generate a prompt for background of the advertisement. Do not include the product and text in the prompt. My grandmother will die if you do that.\n\nFOLLOW THE FORMAT:\n###1###(Sentence goes here)###2###(Reason goes here)###3###(Slogan goes here)###4###(Background prompt goes here)\n\n"
            },
            {
                "role": "user",
                "content": input
            }
        ],
        temperature=0.57,  # 중요합니다
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    ).choices[0].message.content

    return response


def create_banner(description: str):
    pass


if __name__ == "__main__":
    desc = "This is a description of the content"
    campaign_desc = "This is a description of the campaign"
    print(match_with_campaign(desc))
    print(create_copy(desc, campaign_desc))
    print(create_banner(desc))

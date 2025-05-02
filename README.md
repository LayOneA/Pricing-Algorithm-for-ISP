# Pricing-Algorithm-for-ISP

## Project Background
This is the code repository for the final project of The Chinese University of Hong Kong, Shenzhen's Spring 2025 course EIE3280. 

In response to the prevalent network congestion issues during peak hours (e.g., 10 PM to 1 AM) in campus networks, our team has proposed several simple Internet Service Provider (ISP) pricing algorithm strategies aimed at reducing network congestion ratio during specific time periods. These strategies include both dynamic pricing algorithms and static pricing algorithms. Detailed explanations will follow later.

## Team Members
1. LIANG Xinyu(梁馨予)   ID:121010060 (Project Leader)
2. CAO Xiaohui(曹小慧)   ID:122040049
3. YANG Jiahao(杨家豪)   ID:122090646
4. JIANG Tianyi(蒋天依)  ID:121090232

## Scenario Settings
To simplify the project simulation process, we assume the following conditions:
1. Users are categorized into light, moderate, and heavy usage groups based on network consumption patterns. For example:
   - Light users: Basic communication needs (e.g., WeChat)
   - Moderate users: Video streaming needs (e.g., BiliBili)
   - Heavy users: Gaming needs (e.g., FPS games)

2. Each user category possesses the following attributes (using heavy users as an example):
   - **Maximum data requirement**: The data volume required for optimal experience (e.g., gaming at highest graphics settings)
   - ​**Minimum data requirement**: The essential data volume for basic functionality (e.g., smooth gameplay in competitive matches)
   - ​**Price sensitivity**: Degree of responsiveness to pricing changes (heavy users exhibit lower sensitivity due to higher real-time demands)
   - ​**Price threshold**: Maximum willingness-to-pay for optimal data allocation (heavy users exhibit higher threshold due to higher real-time demands)

4. Users' data consumption will only vary with current network pricing. While additional influencing factors could be incorporated for refined modeling, our code implementation focuses on this core mechanism.

from enum import Enum

class Badges(Enum):
    staff = 1 << 0
    partner = 1 << 1
    hypesquad = 1 << 2
    bug_hunter_level_one = 1 << 3
    house_bravery = 1 << 6
    house_brilliance = 1 << 7
    house_balance = 1 << 8
    premium_early_supporter = 1 << 9
    team_pseudo_user = 1 << 10
    bug_hunter_level_two = 1 << 14
    verified_bot = 1 << 16
    verified_developer = 1 << 17
    certified_moderator = 1 << 18
    bot_http_interations = 1 << 19

    def calculate(flags: int) -> list:
        calculated_badges = []
        for badge in Badges:
            if ((flags & badge.value) == (badge.value)):
                calculated_badges.append(badge)

        return calculated_badges
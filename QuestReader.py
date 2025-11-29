from pygame import *
import json
from ResourceManager import *

def quest_list1():

    with open (resource_path("quest_list.json"), "r") as file:

        quest_data = json.load(file)

    quests = {
        quest["id"]: {
            "title": quest["title"],
            "details": quest["details"],
            "reward": quest["reward"],
            "isCompleted": quest["isCompleted"],
            "objectives": quest["objectives"]
        }
        for quest in quest_data
    }
    return quests

def quest_list2():

    with open (resource_path("quest_list.json"), "r") as file:

        return json.load(file)

def quest_list3():

    with open(resource_path("quest_list.json"), "r") as file:
        
        quests = {int(k): v for k, v in json.load(file).items()}#
    return quests

class QuestLevel():

    def __init__(self, quest_id, quest_data):
        
        self.quest_id = quest_id
        self.level = 0
        self.has_given_xp = quest_data.get("has_given_xp", [False] * len(quest_data["isCompleted"]))
    
    def update(self, quest):

        old_level = self.level
        while self.level < len(quest["isCompleted"]) and quest["isCompleted"][self.level]:
            self.level += 1
        if self.level >= len(quest["isCompleted"]):
            self.level = len(quest["isCompleted"]) - 1
        while len(self.has_given_xp) < len(quest["isCompleted"]):
            self.has_given_xp.append(False)
        if self.level != old_level:
            self.has_given_xp[self.level] = False

quests = quest_list3()
quests_levels = {qid: QuestLevel(qid, quest) for qid, quest in quests.items()}

skeleton_current_wave = 0
archer_current_wave = 0
warrior_current_wave = 0

with open (resource_path("upgrades.json"), "r") as file:
    data = json.load(file)
    
xp = 0

def quest_update(enemy_type, direction, wave, current_archers, current_skeletons, lost_a_heart, current_warriors):

    global quest, quests_levels, skeleton_current_wave, archer_current_wave, xp, warrior_current_wave, data

    for quest_id, quest in quests.items():
        quest_level = quests_levels[quest_id]
        gained_xp = False

        if "skeletonsDefeated" in quest["objectives"] and enemy_type == "Skeleton_Spearman" and quest_id == 1:
            quest["objectives"]["skeletonsDefeated"] += 1
            if quest["objectives"]["skeletonsDefeated"] >= quest["objectives"]["requiredSkeletons"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True
                gained_xp = True

        if "archersDefeated" in quest["objectives"] and enemy_type == "Skeleton_Archer" and quest_id == 2:
            quest["objectives"]["archersDefeated"] += 1
            if quest["objectives"]["archersDefeated"] >= quest["objectives"]["requiredArchers"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True
                gained_xp = True

        if "warriorDefeated" in quest["objectives"] and enemy_type == "Skeleton_Warrior" and quest_id == 10:
            quest["objectives"]["warriorDefeated"] += 1
            if quest["objectives"]["warriorDefeated"] >= quest["objectives"]["requiredWarriors"][quest_level.level]:
                quest["isCompleted"][quest_level.level] = True
                gained_xp = True
            
        if direction == "left" and "leftDefeated" in quest["objectives"]:
            quest["objectives"]["leftDefeated"] += 1
            if quest_id == 3:
                if quest["objectives"]["leftDefeated"] >= quest["objectives"]["requiredLeft"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if direction == "right" and "rightDefeated" in quest["objectives"]:
            quest["objectives"]["rightDefeated"] += 1
            if quest_id == 4:
                if quest["objectives"]["rightDefeated"] >= quest["objectives"]["requiredRight"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if wave is not None and "wavesDefeated" in quest["objectives"]:
            if quest_id == 5:
                quest["objectives"]["wavesDefeated"] += 1
                if quest["objectives"]["wavesDefeated"] > quest["objectives"]["requiredWaves"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if quest_id == 6 and wave is not None:
            if current_skeletons > 0 and current_archers == 0 and current_warriors == 0:
                quest.setdefault("objectives", {}).setdefault("wavesDefeated", 0)
                quest["objectives"]["wavesDefeated"] += 1
                if quest["objectives"]["wavesDefeated"] >= quest["objectives"]["requiredWaves"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if quest_id == 7 and wave is not None:
            if current_archers > 0 and current_skeletons == 0 and current_warriors == 0:
                quest.setdefault("objectives", {}).setdefault("wavesDefeated", 0)
                quest["objectives"]["wavesDefeated"] += 1
                if quest["objectives"]["wavesDefeated"] >= quest["objectives"]["requiredWaves"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if quest_id == 11 and wave is not None:
            if current_warriors > 0 and current_archers == 0 and current_skeletons == 0:
                quest.setdefault("objectives", {}).setdefault("wavesDefeated", 0)
                quest["objectives"]["wavesDefeated"] += 1
                if quest["objectives"]["wavesDefeated"] >= quest["objectives"]["requiredWaves"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if "rightDefeated" in quest["objectives"] and "leftDefeated" in quest["objectives"] and quest_id == 8:
            if quest["objectives"]["rightDefeated"] >= quest["objectives"]["requiredRight"][quest_level.level] and quest["objectives"]["leftDefeated"] >= quest["objectives"]["requiredLeft"][quest_level.level]:
                    quest["isCompleted"][quest_level.level] = True
                    gained_xp = True

        if quest_id == 9:

            if wave is not None:
                if not getattr(quest_level, "wave_in_progress", False):
                    quest_level.wave_in_progress = True
                    quest_level.lost_heart_this_wave = False

                if lost_a_heart:
                    quest_level.lost_heart_this_wave = True

            if wave is None and getattr(quest_level, "wave_in_progress", False):
                quest_level.wave_in_progress = False
      
                if not quest_level.lost_heart_this_wave:
                    quest["objectives"]["wavesDefeated"] += 1

                    if quest["objectives"]["wavesDefeated"] >= quest["objectives"]["requiredWaves"][quest_level.level]:
                        quest["isCompleted"][quest_level.level] = True
                        gained_xp = True

        if gained_xp and not quest_level.has_given_xp[quest_level.level]:
            xp += quest["reward"]["xp"][quest_level.level]
            print(xp)
            quest_level.has_given_xp[quest_level.level] = True

        quest_level.update(quest)

    data[1]["total_xp"] += xp

    with open (resource_path("quest_list.json"), "w") as file:
        json.dump({str(k): v for k, v in quests.items()}, file, indent=2)

    with open (resource_path("upgrades.json"), "w") as file:
        json.dump(data, file, indent=4)

    xp = 0
import re
import os

ITEM_TYPES = {
    0: "ITEM_TYPE_BOX_TIME",
    1: "ITEM_TYPE_RULETKA", 
    2: "ITEM_TYPE_VEHICLE",
    3: "ITEM_TYPE_ACCESSORIES",
    4: "ITEM_TYPE_VEH_ACCESSORIES",
    5: "ITEM_TYPE_LICENSE",
    6: "ITEM_TYPE_IMPROV",
    7: "ITEM_TYPE_VEH_SKIN",
    8: "ITEM_TYPE_IMPROV_GUN",
    9: "ITEM_TYPE_GUN",
    10: "ITEM_TYPE_SKIN",
    11: "ITEM_TYPE_PHONE",
    12: "ITEM_TYPE_CLOTHES",
    13: "ITEM_TYPE_IMPERMANENT",
    14: "ITEM_TYPE_COOK",
    15: "ITEM_TYPE_OTHER",
    16: "ITEM_TYPE_MONEY",
    17: "ITEM_TYPE_MEDCARD",
    18: "ITEM_TYPE_ARMYTICKET",
    19: "ITEM_TYPE_MOD_SKIN",
    20: "ITEM_TYPE_ENCHANT",
    21: "ITEM_TYPE_PROPERTY_OBJECT",
    22: "ITEM_TYPE_STRIPE",
    23: "ITEM_TYPE_VISUAL_TUNING",
    24: "ITEM_TYPE_TECH_TUNING",
    25: "ITEM_TYPE_PACK_ITEM",
    26: "ITEM_TYPE_MEDINSURANCE",
    27: "ITEM_TYPE_LAREC",
    28: "ITEM_TYPE_AIR_TICKET",
    29: "ITEM_TYPE_WORKING_VISA",
    30: "ITEM_TYPE_ACTOR_SKIN",
    31: "ITEM_TYPE_EAT",
    32: "ITEM_TYPE_ARMOUR_SHARPENING",
    33: "ITEM_TYPE_CONTAINER",
    34: "ITEM_TYPE_VC_WORK_PERMIT",
    35: "ITEM_TYPE_APTECHKA",
    36: "ITEM_TYPE_DRINK",
    37: "ITEM_TYPE_ALHO_DRINK",
    38: "ITEM_TYPE_ARMOUR",
    39: "ITEM_TYPE_MAFIA_SECURITY",
    40: "ITEM_TYPE_DRUGS",
    41: "ITEM_TYPE_CROSSHAIR",
    42: "ITEM_TYPE_INDICATOR_HUNGRY",
    43: "ITEM_TYPE_TERMO_BACKPACK",
    44: "ITEM_TYPE_INCREASED_MAGAZINE",
    45: "ITEM_TYPE_VC_PURCHASE_PAPER_OIL",
    46: "ITEM_TYPE_VC_CUSTOMS_CERT",
    47: "ITEM_TYPE_VC_CUSTOMS_CLEARANCE",
    48: "ITEM_TYPE_SUPER_ENCHANTED",
    49: "ITEM_TYPE_VEH_MODIFICATION",
    50: "ITEM_TYPE_RANDOM_CROSSHAIR",
    51: "ITEM_TYPE_ELIXIR",
    52: "ITEM_TYPE_REALTOR_PERMIT",
    53: "ITEM_TYPE_UNLIMITE_PARK_CARD",
    54: "ITEM_TYPE_VIP_ADVERT_CARD",
    55: "ITEM_TYPE_DYE",
    56: "ITEM_TYPE_UNLIM_BARREL_DELIVERY",
    57: "ITEM_TYPE_VEH_NUMBER",
    58: "ITEM_TYPE_HIRED_FARMER",
    59: "ITEM_TYPE_STRIPE_SKIN",
    60: "ITEM_TYPE_MAP_CLAD",
    61: "ITEM_TYPE_DRONE",
    62: "ITEM_TYPE_ARMY_SUMMONS",
    63: "ITEM_TYPE_CODE_TRILOGY",
    64: "ITEM_TYPE_REAL_MONEY",
    65: "ITEM_TYPE_STRIPE_IMPROV",
    66: "ITEM_TYPE_STRIPE_SHAR",
    67: "ITEM_TYPE_STRIPE_SUIT_CASE",
    68: "ITEM_TYPE_TEMP_VEHICLE",
    69: "ITEM_TYPE_LOTTERY_TICKET",
    70: "ITEM_TYPE_SYRUP_ACTOR",
    71: "ITEM_TYPE_FAKE_SKIN_FORM",
    72: "ITEM_TYPE_SYRUP_ACTOR_N",
    73: "ITEM_TYPE_IMP_ACS"
}

STAT_NAMES = {
    0: "Защита",
    1: "Регенерация", 
    2: "Урон",
    3: "Удача",
    4: "Макс. HP",
    5: "Макс. Броня",
    6: "Шанс оглушения",
    7: "Шанс опьянения",
    8: "Шанс избежать оглушения",
    9: "Отражение урона",
    10: "Блокировка урона",
    11: "Скорострельность",
    12: "Отдача"
}

STAT_POSTFIXES = {
    1: " HP (в мин)",
    4: " HP",
    5: " брони",
    6: "%",
    7: "%",
    8: "%",
    9: "%",
    10: " раз(а)",
    11: "%",
    12: "%"
}

def parse_stats(stats_str):
    if not stats_str or stats_str.strip() == "":
        return []
    
    stats = []
    for stat_pair in stats_str.split(','):
        if ':' in stat_pair:
            stat_id, value = stat_pair.split(':')
            stat_id = int(stat_id.strip())
            value = int(value.strip())
            
            if stat_id in STAT_NAMES:
                prefix = "+" if value > 0 else ""
                if stat_id in [9, 12]:
                    prefix = "-" if value > 0 else "+"
                elif stat_id == 10:
                    prefix = ""
                
                postfix = STAT_POSTFIXES.get(stat_id, "")
                stats.append(f"**{STAT_NAMES[stat_id]}**: {prefix}{value}{postfix}")
    
    return stats

def format_description(desc):
    desc = re.sub(r'\{[A-Fa-f0-9]{6}\}', '', desc, flags=re.IGNORECASE)
    desc = desc.replace('\\n', '\n')
    desc = desc.replace('\n', '<br>')
    return desc

def create_item_markdown(item_data):
    item_id = item_data.get('Id', 'Unknown')
    img_id = item_data.get('Img', '0')
    name = item_data.get('Name', 'Unknown Item')
    description = item_data.get('Description', '')
    item_type = int(item_data.get('Type', 0))
    slot = int(item_data.get('Slot', ''))
    stuck_count = item_data.get('StuckCount', '')
    max_zatoch = item_data.get('MaxZatoch', '')
    max_prochnost = item_data.get('MaxProchnost', '')
    can_repaint = item_data.get('CanRepaint', '')
    text_stat = item_data.get('TextStat', '')
    default_stats = item_data.get('DefaultStats', '')
    additional_stats = item_data.get('AdditionalStats', '')
    yellow_stats = item_data.get('YellowStats', '')
    
    formatted_desc = format_description(description)
    type_name = ITEM_TYPES.get(item_type, f"Unknown Type ({item_type})")
    
    default_stats_list = parse_stats(default_stats)
    additional_stats_list = parse_stats(additional_stats)
    yellow_stats_list = parse_stats(yellow_stats)
    
    content = f"""# {name}

![Item Image](../img/{img_id}.webp?raw=true)

{formatted_desc}


| Параметр | Значение |
|----------|----------|
| **ID** | {item_id} |
| **Тип** | {type_name} |"""
    
    if slot and slot != 255:
        content += f"\n| **Слот** | {slot+1} |"
    
    if stuck_count and stuck_count != '1':
        content += f"\n| **Максимальное количество в ячейке** | {stuck_count} |"
    
    if max_zatoch and max_zatoch != '0':
        content += f"\n| **Максимальный уровень улучшения** | {max_zatoch} |"
    
    if max_prochnost and max_prochnost != '0':
        content += f"\n| **Максимальный уровень прочности** | {max_prochnost} |"
    
    if can_repaint and item_type == 3:
        content += f"\n| **Можно перекрашивать** | {'Да' if can_repaint.lower() == 'true' else 'Нет'} |"
    
    content += "\n\n"
    
    if default_stats_list:
        content += "## Характеристики по умолчанию\n\n"
        for stat in default_stats_list:
            content += f"- {stat}\n"
        content += "\n"
    
    if additional_stats_list:
        content += "## Дополнительные характеристики\n\n"
        for stat in additional_stats_list:
            content += f"- {stat}\n"
        content += "\n"
    
    if yellow_stats_list:
        content += "## Жёлтые характеристики\n\n"
        for stat in yellow_stats_list:
            content += f"- {stat}\n"
        content += "\n"

    if text_stat:
        formatted_text_stat = format_description(text_stat)
        content += "## Текстовая характеристика\n\n"
        content += f"{formatted_text_stat}\n\n"
    
    return content

def generate_readme(items):
    readme_content = "# Последние 2000 предметов:\n\n"

    sorted_items = sorted(items, key=lambda x: int(x.get('Id', 0)))

    last_2000_items = sorted_items[-2000:][::-1]
    
    for item in last_2000_items:
        if 'Id' in item and 'Name' in item:
            item_id = item['Id']
            name = item['Name']
            readme_content += f"- [ID: {item_id}] [{name}](items/{item_id}.md)\n"

    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(readme_content)
    
    print(f"Generated README.md with {len(last_2000_items)} items")

def main():
    with open('items.txt', 'r', encoding='utf-8') as f:
        content = f.read()

    items = []
    current_item = {}
    for line in content.split('\n'):
        line = line.strip()
        if line.startswith('[Item '):
            if current_item:
                items.append(current_item)
            current_item = {}
        elif '=' in line:
            key, value = line.split('=', 1)
            current_item[key] = value

    if current_item:
        items.append(current_item)

    print(f"Found {len(items)} items")

    if os.path.exists('items'):
        import shutil
        shutil.rmtree('items')
    os.makedirs('items', exist_ok=True)

    for i, item in enumerate(items):
        if 'Id' in item:
            item_id = item['Id']
            markdown_content = create_item_markdown(item)
            
            with open(f'items/{item_id}.md', 'w', encoding='utf-8') as f:
                f.write(markdown_content)
            
            print(f"Generated items/{item_id}.md")
            
    generate_readme(items)

    print("All markdown files generated successfully!")

if __name__ == "__main__":
    main()
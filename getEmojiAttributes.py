#!/usr/bin/env python
# coding: utf-8

# code by mswartz2@gmu.edu as of August 2020
# The attributes are compiled from Unicode emoji data files emoji-test.txt and also manual review
# Unicode data files: https://unicode.org/Public/emoji/13.0/
# there may be some emojis that render but are not fully supported by Unicode (e.g. family with skintone)
# and thus may not be in the master reference of emoji attributes

# values for emoji group, subgroup, name, status, version are from Unicode
# attributes for shape, color, direction, gender, skin_tone are based on Unicode name
# desc, person_animal_other, anthro_type, were assigned by the author but could be changed
# sentiment did a positive (1) or negative (-1) or neutral (0) based on smileys, this could be modified
# additonal fields could be added for other groupings
# additional resources are: https://emojipedia.org/ and https://unicode.org/emoji/charts/full-emoji-list.html


# dependencies
import ast
import json

# other code in this repo
import extractEmojis


# LOAD IN EMOJI ATTRIBUTES JSON FILE THAT WAS PREPROCESSED 
# CREATE DICTIONARY to use as master reference for emoji attributes
emoji_w_attributes_dict = dict()
with open('emoji_all_v13_attributes_w_color_anthro_sentiment_shape_direction.json') as f:
    emoji_w_attributes_dict = json.load(f)

"""
# e.g. reference emoji dictionary
code: emoji_w_attributes_dict['😀 ']
output: 😀 {'rownum': '1', 'group': 'Smileys & Emotion', 'subgroup': 'face-smiling', 'emoji': '😀', 'grp_subgrp': 'Smileys & Emotion_face-smiling', 'desc': 'anthropomorphic', 'person_animal_other': 'smiley', 'anthro_type': 'face-gesture', 'gender': 'neutral', 'skin_tone': 'neutral', 'shape_type': '', 'shape_color': '', 'direction': '', 'sentiment_smileys_binary': '1', 'cldr short name': 'grinning face', 'codepoint': '1F600', 'status': 'fully-qualified',  'char_len': '1', 'version': 'E1.0'}

create a dictionary of emoji attributes for a list of emojis

           {'rownum': '1',
 'emoji': '😀',
 'grp_subgrp': 'Smileys & Emotion_face-smiling',
 'desc': 'anthropomorphic',
 'person_animal_other': 'smiley',
 'anthro_type': 'face-gesture',
 'gender': 'neutral',
 'skin_tone': 'neutral',
 'shape_type': '',
 'shape_color': '',
 'direction': '',
 'sentiment_smileys_binary': '1',
 'cldr short name': 'grinning face',
 'codepoint': '1F600',
 'status': 'fully-qualified',
 'group': 'Smileys & Emotion',
 'subgroup': 'face-smiling',
 'char_len': '1',
 'version': 'E1.0'}


"""

# for reference these are the attributes in the master list
attributes_list = ['rownum', 'emoji', 'cldr short name', 'codepoint',\
                        'status' , 'char_len', 'version', \
                         'desc', 'person_animal_other', 'anthro_type',\
                        'gender', 'skin_tone', 'sentiment_smileys_binary',\
                        'shape_type', 'shape_color', 'direction',\
                        'group', 'subgroup', 'grp_subgrp']


# function to return a dictionary with unique values represented by emojis in a list for attributes of interest
# e.g. to show the unique values for emoji Unicode groups represented in a list

# return a single dictionary of all the attributes for a single emoji
def getAttributesForSingleEmoji(emoji):
    if emoji in emoji_w_attributes_dict:
        return emoji_w_attributes_dict[emoji]
    else:
        repaired_emoji = extractEmojis.fixDuplicateEmoji(emoji)                
        if repaired_emoji in emoji_w_attributes_dict:
            return emoji_w_attributes_dict[repaired_emoji]
        else:
            return constructAttributesForEmojiNotInRef(emoji)
        #except:
        #    return {}


# Helper function to construct emoji attributes for the unsupported family emojis with skin tones
def constructAttributesForEmojiNotInRef(emoji):
    try:
        # check to see if family    
        
        neutrals = [('👪','Family','1F46A'),('🧑','Person','1F9D1'),('🧒','Child','1F9D2'),('👶','Baby','1F476')]
        men = ['👨','👦']
        fem = ['👩','👧']
        people = [('👨','Man','1F468'),('👩','Woman','1F469'),('👧','Girl','1F467'),('👦','Boy','1F466')]
        zwj ='‍'
        zwj_codepoint = '200D'
        skin_tones = ['🏻','🏼','🏽','🏾','🏿']
        skin_tone_name = [('🏻','Light Skin Tone','1F3FB','Type-1-2'),('🏼','Light-Medium Skin Tone','1F3FC','Type-3'),('🏽','Medium Skin Tone','1F3FD','Type-4'),('🏾','Medium-Dark Skin Tone','1F3FE','Type-5'),('🏿','Dark Skin Tone','1F3FF','Type-6')]

        tones_in_emoji = [tone for tone in skin_tones if tone in emoji ]
        people_in_emoji = [person_tup[0]  for person_tup in people if person_tup[0] in emoji]
        neuts_in_emoji = [neut_tup[0]  for neut_tup in neutrals if neut_tup[0] in emoji]
        males_in_emoji = [male  for male in men if male in emoji]
        females_in_emoji = [female  for female in fem if female in emoji]


        gender = ''
        skintone = ''
        e_name = ''
        codepoints = ''
        
        if len(tones_in_emoji)>0 and (len(people_in_emoji)>0 or len(neuts_in_emoji)):
            
            genders = []
            if len(males_in_emoji)>0:
                genders.append('male')
            if len(females_in_emoji)>0:
                genders.append('female')
            if len(neuts_in_emoji)>0:
                genders.append('neutral')
            # check gender
            if len(genders)>1:
                gender='mixed'
            elif len(genders)==1:
                gender=genders[0]
            
            # skintone check
            if len(tones_in_emoji)>0:
                if len(tones_in_emoji)>1:
                    skintone = 'mixed'
                else:
                    tone_check = tones_in_emoji[0]    
                    skintone_temp = [tup[1]  for tup in skin_tone_name if tone_check in tup]
                    skintone = skintone_temp[0][:skintone_temp[0].find(' ')]
            
            e_name = ''
            codepoints = ''        
            
            # name check
            if '👪' in neuts_in_emoji and len(tones_in_emoji)==1:
                [tup[3] for tup in skin_tone_name if tup[0] in emoji][0]
                e_name = 'Family, ' + [tup[3] for tup in skin_tone_name if tup[0] in emoji][0]
                codepoints = '1F46A ' + [tup[2] for tup in skin_tone_name if tup[0] in emoji][0]
            
            if zwj in emoji:
                parts = emoji.split(zwj)
                i=0
                e_name ='Family: '
                for part in parts:
                    i+=1
                    # gender
                    for person_tup in people:
                        if person_tup[0] in part:
                            e_name += person_tup[1]
                            codepoints += person_tup[2]
                            break
                    
                    for neut_tup in neutrals:
                        if neut_tup[0] in part:
                            e_name += neut_tup[1]
                            codepoints += neut_tup[2]
                            break

                    # skin tone
                    if len(part) > 1:
                        for skin_tup in skin_tone_name:
                            if skin_tup[0] in part:
                                e_name += ': '
                                e_name += skin_tup[1]
                                codepoints += ' '
                                codepoints += skin_tup[2]
                    if i < len(parts):
                        e_name += ', '
                        codepoints += ' '
            
                
            # reconstruct new emoji most likely family with skin tone
            
            emo_attributes={'rownum':'','emoji':emoji,
                            'grp_subgrp':'People & Body_family',
                            'desc':'anthropomorphic',
                            'person_animal_other':'person-group',
                             'anthro_type':'group',
                             'gender':gender,
                             'skin_tone':skintone,
                             'shape_type':'',
                             'shape_color':'',
                             'direction':'',
                             'sentiment_smileys_binary':'',
                             'cldr short name':e_name,#'family: man, woman, girl, boy',
                             'codepoint':codepoints,#'1F468 200D 1F469 200D 1F467 200D 1F466',
                             'status':'not-qualified',
                             'group':'People & Body',
                             'subgroup':'family',
                             'char_len':len(emoji),
                             'version':''}
            
            return emo_attributes
        else:
            return
        
    except:
        return   


            
            
            
    
# return a dictionary of all emoji attributes for the emojis in a list
def getDictOfEmojiAttributes(emoji_list):
    new_emoji_list = ''
    if type(emoji_list)==list:
        new_emoji_list = emoji_list
    elif type(emoji_list)!=list:
        new_emoji_list = ast.literal_eval(emoji_list)
    
    dict_of_subset_of_emojis = dict()
    emojis_subset_not_in_dict = []
    
    if type(new_emoji_list)==list:
        try:
            for e in new_emoji_list:
                try:
                    dict_of_subset_of_emojis[e] = getAttributesForSingleEmoji(e)
                except:
                    emojis_subset_not_in_dict.append(e)
            return dict_of_subset_of_emojis
        except:
            return 
    else:
        return 
 
            
            

# Get a list of the values of specific attributes for a list of emojis if that emoji has the attribute
 #attributes_in_ref_to_choose_from = ['group', 'subgroup', 'grp_subgrp',\
                         #'desc', 'person_animal_other', 'anthro_type',\
                        #'gender', 'skin_tone', \
                        #'shape_type', 'shape_color', 'direction',\
                        #  'emoji', 'cldr short name','sentiment_smileys_binary',
                        #'status' , 'char_len', 'version','rownum', 'codepoint']


# Get a list of the values for a specific attribute for emojis in a list with that attribute
# the input is a list of emojis and a string of the attribute name, if a list is passed it only takes the first value

def getListOfSingleAttributeValuesForEmojiList(emoji_list, single_attribute):
    if type(single_attribute) == list:
        attribute_to_check = single_attribute[0]
    elif type(single_attribute) == str:
        attribute_to_check = single_attribute
    else:
        return []
    if attribute_to_check in attributes_list:
        new_emoji_list = ''
        if type(emoji_list)==list:
            new_emoji_list = emoji_list
        elif type(emoji_list)!=list:
            new_emoji_list = ast.literal_eval(emoji_list)
    
        if type(new_emoji_list)==list:
            list_of_values_for_attribute = []
            for e in new_emoji_list:
                e_attributes = getAttributesForSingleEmoji(e)
                if e_attributes != {}:
                    e_value = e_attributes[attribute_to_check]
                else:
                    e_value = ''
                if e_value != '':
                    list_of_values_for_attribute.append(e_value)
            return list_of_values_for_attribute
        else:
            return []
    else:
        return []

   
# return a list of sorted unique values for a single attribute for applicable emojis in the emoji list
def getUniqueListOfSingleAttributeValuesForEmojiList(emoji_list, single_attribute):
    if type(single_attribute) == list:
        attribute_to_check = single_attribute[0]
    elif type(single_attribute) == str:
        attribute_to_check = single_attribute
    else:
        return []
        
    if attribute_to_check in attributes_list:
        new_emoji_list = ''
        if type(emoji_list)==list:
            new_emoji_list = emoji_list
        elif type(emoji_list)!=list:
            new_emoji_list = ast.literal_eval(emoji_list)
    
        if type(new_emoji_list)==list:
            list_of_values_for_attribute = []
            for e in new_emoji_list:
                e_value = ''
                try:
                    e_value = getAttributesForSingleEmoji(e)[attribute_to_check]
                except:
                    e_value = ''
                if e_value != '':
                    list_of_values_for_attribute.append(e_value)
            return sorted(list(set(list_of_values_for_attribute)))
        else:
            return []
    else:
        return []




# get a dict of attributes with value for each emoji if applicable for emojis in list
def getDictOfValuesForEmojiAttributesOfInterest(emoji_list, list_of_attributes_of_interest):   
    new_emoji_list = ''
    if type(emoji_list)==list:
        new_emoji_list = emoji_list
    elif type(emoji_list)!=list:
        new_emoji_list = ast.literal_eval(emoji_list)
    
    emojis_attributes_values_dict = dict()
    
    if type(new_emoji_list)==list:
        try:
            for attribute in list_of_attributes_of_interest:
                list_of_values_for_attribute = []
                for e in new_emoji_list:
                    e_attributes = getAttributesForSingleEmoji(e)
                    e_value = e_attributes[attribute]
                    if e_value != '':
                        list_of_values_for_attribute.append(e_value)
                emojis_attributes_values_dict[attribute] = list_of_values_for_attribute
            return emojis_attributes_values_dict
        
        except:
            return emojis_attributes_values_dict
    else:
        return emojis_attributes_values_dict

 
 


# get a dict of attributes with sorted unique value for each emoji if applicable for emojis in list
def getDictOfUniqueValuesForEmojiAttributesOfInterest(emoji_list, list_of_attributes_of_interest):   
    new_emoji_list = ''
    if type(emoji_list)==list:
        new_emoji_list = emoji_list
    elif type(emoji_list)!=list:
        new_emoji_list = ast.literal_eval(emoji_list)
    
    emojis_attributes_values_dict = dict()
    
    if type(new_emoji_list)==list:
        try:
            for attribute in list_of_attributes_of_interest:
                list_of_values_for_attribute = []
                for e in new_emoji_list:
                    e_attributes = getAttributesForSingleEmoji(e)
                    e_value = e_attributes[attribute]
                    if e_value != '':
                        list_of_values_for_attribute.append(e_value)
                emojis_attributes_values_dict[attribute] = sorted(list(set(list_of_values_for_attribute)))
            return emojis_attributes_values_dict
        
        except:
            return emojis_attributes_values_dict
    else:
        return emojis_attributes_values_dict

    
 
 
  
    
    

#input: unique_emoji_list = ['4️⃣', '❤️', '🇦', '🇦🇺', '🍎', '👨🏾\u200d👩🏾\u200d👧🏾\u200d👦🏾', '👩🏿\u200d💻', '👪🏿', '🗳', '😃', '🟠']
#code: emojis_in_text_attribute_dict = getEmojiAttributesForEmojiList(unique_emoji_list)
#output: e.g.  emojis_in_text_attribute_dict['group'] = ['Flags', 'Food & Drink', 'Objects', 'People & Body', 'Smileys & Emotion', 'Symbols']


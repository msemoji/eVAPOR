#!/usr/bin/env python

# EVAPOR Workflow written in Python 3.6 in April 2020 by mswartz2@gmu.edu
# This code will import text string, extract the emojis as list
# report out the unique emojis and unique emoji attributes for the text
# then for text analyze the structure of the content
# and then delve into the emojis and report out the relative position, 
# and then report out on the emoji vector of attributes, position, order, repetition of emoji use within the text
# text, emoji_list, unique emojis and attributes, relative position of emoji,
# per span of emojis/attributes flipped or not, repetition within single, repetition across

# dependencies
import json
import re # if re not on system do pip install re
import regex
import ast

# included in this repo
import extractEmojis

import getEmojiAttributes

#import identifyStructure


# get the emoji spans as attributes
def getAttributesForSpansList(list_of_lists_of_vals, attribute):
    attributes_to_choose_from = ['rownum', 'emoji', 'cldr short name', 'codepoint', 'status' , 'char_len', 'version', \
                         'desc', 'person_animal_other', 'anthro_type','gender', 'skin_tone', 'sentiment_smileys_binary',\
                        'shape_type', 'shape_color', 'direction','group', 'subgroup', 'grp_subgrp']
    if type(list_of_lists_of_vals)==float or list_of_lists_of_vals == [] or list_of_lists_of_vals == "[]" or  list_of_lists_of_vals == '':
        return []
    elif type(list_of_lists_of_vals) != list:
        list_of_lists_of_vals = ast.literal_eval(list_of_lists_of_vals)
    
    if type(list_of_lists_of_vals)==list and type(list_of_lists_of_vals[0])==list:
        if attribute in attributes_to_choose_from:    
            attribute_spans_list = []
            for sublist in list_of_lists_of_vals:
                attribute_sublist =  getEmojiAttributes.getListOfSingleAttributeValuesForEmojiList(sublist, attribute)
                attribute_spans_list.append(attribute_sublist)
            return attribute_spans_list
        else:
            return []
    else:
        return []


# get the relative position
## ANALYZE EMOJI SPANS

## GET RELATIVE POSITION

# sample text: RT @atmention: @person2 12 🗳🇦🇺😃 yes ll smiles #yes #happiness @my_day 🟠🍎http://www.happiness.wwwwww

# GET RELATIVE POSITION
content_type_of_interest = 'emoji'
def getRelativePositionOfContentType(fullDocumentStructureWithContent, content_type_of_interest):
# input: fullDocumentStructureWithContent = [('RT', 1, ['RT']), ('at_mention', 2, ['@atmention', '@person2']), ('text', 2, ['12', ' ']), ('emoji', 3, ['🗳', '🇦🇺', '😃']), ('text', 6, ['yes', ' ', 'll', ' ', 'smiles', ' ']), ('hashtag', 2, ['#yes', '#happiness']), ('at_mention', 1, ['@my_day']), ('emoji', 2, ['\U0001f7e0', '🍎']), ('url', 1, ['http://www.happiness.wwwwww'])]
# code: emoji_positions = get_index_pos_list_relative(fullDocumentStructureWithContent, 'emoji')
# output: ['middle', 'end']
# outputs are beginning, middle, end  # these are relative but can use the strucuture list for more details
# NOTES: can also put in 'at_mention' or 'url' etc to see where they are
    span_list = []
    if content_type_of_interest not in ['RT','at_mention','emoji','url','text','punctuation']:
        return []
    if type(fullDocumentStructureWithContent) != list:
        new_fullDocumentStructureWithContent = ast.literal_eval(fullDocumentStructureWithContent)
        if (len(new_fullDocumentStructureWithContent)>0) and (type(new_fullDocumentStructureWithContent[0])==tuple):
            span_list = new_fullDocumentStructureWithContent
        else:
            return []
    else:
        span_list = fullDocumentStructureWithContent
    try:    
        index_span_pos_list = [ i for i in range(len(span_list)) if span_list[i][0] == content_type_of_interest]
        pos_list = []
        num_spans = len(span_list)
        structure_cnts = [0,0,0,0,0]# span counts
        relative_pos_list = [0,0,0,0,0]
        relative_pos_list_descrip = []
        cnt_spans = 0
        index_span_pos_list_relative = [[],[],[],[],[]] 
        pos_list_w_values = [[],[],[],[],[]]
        pos_list_w_value_cnts = [[],[],[],[],[]]
        pos_list_w_total = [0,0,0,0,0]
        if 0 in index_span_pos_list:
            relative_pos_list_descrip.append('start')
            structure_cnts[0]=1
            relative_pos_list[0]=1
            pos_list_w_values[0]=[tuple(span_list[0][2])]
            pos_list_w_value_cnts[0] = [span_list[0][1]]
            pos_list_w_total[0] = span_list[0][1]
            index_span_pos_list_relative[0]= [0]
            
        if num_spans > 1:
            if len(span_list)-1 in index_span_pos_list:
                relative_pos_list_descrip.append('final')
                structure_cnts[4]=1
                relative_pos_list[4]=1
                pos_list_w_values[4]=[tuple(span_list[-1][2])]
                pos_list_w_value_cnts[4] = [span_list[-1][1]]
                pos_list_w_total[4] = span_list[-1][1]
                index_span_pos_list_relative[4]= [len(span_list)-1]
    
        if num_spans == 3:
                # middle = 1 
                if 1 in index_span_pos_list:
                    relative_pos_list_descrip.append('middle')
                    relative_pos_list[2]=1
                    structure_cnts[2] = 1# mid
                    pos_list_w_values[2]=[tuple(span_list[1][2])]
                    pos_list_w_value_cnts[2] = [span_list[1][1]]
                    pos_list_w_total[2] = span_list[1][1]
                    index_span_pos_list_relative[2]= [1]
            
        if num_spans == 4 : # 4 has no middle 
                if 1 in index_span_pos_list:
                    relative_pos_list_descrip.append('beginning')
                    relative_pos_list[1]=1
                    structure_cnts[1] = 1# 
                    pos_list_w_values[1]=[tuple(span_list[1][2])]
                    pos_list_w_value_cnts[1] = [span_list[1][1]]
                    pos_list_w_total[1] = span_list[1][1]
                    index_span_pos_list_relative[1]= [1]
                if 2 in index_span_pos_list:
                    relative_pos_list_descrip.append('end')
                    relative_pos_list[3]=1
                    structure_cnts[3] = 1#
                    pos_list_w_values[3]=[tuple(span_list[2][2])]
                    pos_list_w_value_cnts[3] = [span_list[2][1]]
                    pos_list_w_total[3] = span_list[2][1]
                    index_span_pos_list_relative[3]= [2]
        if num_spans == 5 :# if 5 if has a middle if a 3
                if 1 in index_span_pos_list:
                    relative_pos_list_descrip.append('beginning')
                    relative_pos_list[1]=1
                    structure_cnts[1] = 1# 
                    pos_list_w_values[1]=[tuple(span_list[1][2])]
                    pos_list_w_value_cnts[1] = [span_list[1][1]]
                    pos_list_w_total[1] = span_list[1][1]
                    index_span_pos_list_relative[1]= [1]
                if 2 in index_span_pos_list:
                    relative_pos_list_descrip.append('middle')
                    relative_pos_list[2]=1
                    structure_cnts[2] = 1# mid
                    #print('middle small cnt = ', structure_cnts[2])
                    pos_list_w_values[2]=[tuple(span_list[2][2])]
                    pos_list_w_value_cnts[2] = [span_list[2][1]]
                    pos_list_w_total[2] = span_list[2][1]
                    index_span_pos_list_relative[2]= [2]
                if 3 in index_span_pos_list:
                    relative_pos_list_descrip.append('end')
                    relative_pos_list[3]=1
                    structure_cnts[3] = 1# 
                    pos_list_w_values[3]=[tuple(span_list[3][2])]
                    pos_list_w_value_cnts[3] = [span_list[3][1]]
                    pos_list_w_total[3] = span_list[3][1]
                    index_span_pos_list_relative[3]= [3]
        # if 5 or more then add in beggining or end and based on size of span list
        if num_spans > 5:
            third = int(num_spans/3)
            beginning_indices = [i for i in range(third)]
            end_indices = [num_spans - beginning_indices[v] for v in reversed(beginning_indices)]
            #middle_indices = [i for i in range(beginning_indices[-1]+1,end_indices[0])]
            middle_indices = [i for i in range(beginning_indices[-1]+1,end_indices[0]-1)]
            end_indices = [end_indices[0]-1] + end_indices # for handling even numbers
            def intersection_list(lst1, lst2): 
                lst3 = [value for value in lst1 if value in lst2] 
                return lst3 
            # indices w values of interest
            beg_indices_w_val_of_interest = intersection_list(index_span_pos_list,beginning_indices)# beg
            mid_indices_w_val_of_interest = intersection_list(index_span_pos_list,middle_indices)# mid
            end_indices_w_val_of_interest = intersection_list(index_span_pos_list,end_indices)# end
            # so no dupes with first and last if they exist
            if 0 in index_span_pos_list:
                beg_indices_w_val_of_interest = beg_indices_w_val_of_interest[1:]
            if len(span_list)-1 in index_span_pos_list:
                end_indices_w_val_of_interest = end_indices_w_val_of_interest[:-1]
            # append counts
            structure_cnts[1] = len(beg_indices_w_val_of_interest)# beg
            structure_cnts[2] = len(mid_indices_w_val_of_interest)# mid
            structure_cnts[3] = len(end_indices_w_val_of_interest)# end
            if structure_cnts[1]>0:
                relative_pos_list_descrip.append('beginning')
                relative_pos_list[1]=1
                pos_list_w_values[1]=[tuple(span_list[i][2]) for i in beg_indices_w_val_of_interest]
                pos_list_w_value_cnts[1] = [span_list[i][1] for i in beg_indices_w_val_of_interest]
                pos_list_w_total[1] = sum([span_list[i][1] for i in beg_indices_w_val_of_interest])
                index_span_pos_list_relative[1]= beg_indices_w_val_of_interest
            if structure_cnts[2]>0:
                relative_pos_list_descrip.append('middle')
                relative_pos_list[2]=1
                pos_list_w_values[2]=[tuple(span_list[i][2]) for i in mid_indices_w_val_of_interest]
                pos_list_w_value_cnts[2] = [span_list[i][1] for i in mid_indices_w_val_of_interest]
                pos_list_w_total[2] = sum([span_list[i][1] for i in mid_indices_w_val_of_interest])
                index_span_pos_list_relative[2]= mid_indices_w_val_of_interest
            if structure_cnts[3]>0:
                relative_pos_list_descrip.append('end')
                relative_pos_list[3]=1
                pos_list_w_values[3]=[tuple(span_list[i][2]) for i in end_indices_w_val_of_interest]
                pos_list_w_value_cnts[3] = [span_list[i][1] for i in end_indices_w_val_of_interest]
                pos_list_w_total[3] = sum([span_list[i][1] for i in end_indices_w_val_of_interest])
                index_span_pos_list_relative[3]= end_indices_w_val_of_interest
        cnt_spans = len(index_span_pos_list)
        #return [cnt_spans, index_span_pos_list, index_span_pos_list_relative,\
        #        relative_pos_list,relative_pos_list_descrip, structure_cnts,\
        #        pos_list_w_values, pos_list_w_value_cnts, pos_list_w_total]
        # move final to the end
        if 'final' in relative_pos_list_descrip:
            relative_pos_list_descrip.remove('final')
            relative_pos_list_descrip +=['final']
        return relative_pos_list_descrip
    except:
        return []


# get the order

# get the repetition

## ANALYZE REPETITION WITHIN SPAN
# check for repetition within each span
def labelRepetitionWithinSpans(list_of_vals_in_spans):
    # input: emojis_as_list_in_spans_list = [['💙️'],['💙️','💙️','💙️'],['😃']]
    # code: within_span_repetition_list =  check_for_repetition_within_each_span_per_attribute(emojis_as_list_in_spans_list)
    # output: ['single_within','all_identical_within','single_within']
    repetition_within_spans_status_list = []
    if list_of_vals_in_spans == []:
        return repetition_within_spans_status_list
    for val_span_list in list_of_vals_in_spans:
        if len(val_span_list) == 1:
            repetition_within_spans_status_list.append('single_within')
        else: # more than one val
            val_set = set(val_span_list)
            if len(val_set) == 1:
                repetition_within_spans_status_list.append('all_identical_within') # amplification
            elif len(val_set) < len(val_span_list):# some repetition
                repetition_within_spans_status_list.append('some_identical_within') # list which are identical?
            else:# if len(val_set) = len(val_span_list) # no repetition all unique
                repetition_within_spans_status_list.append('no_repetition_within')        
    return repetition_within_spans_status_list

def getValuesRepeatedWithinSpans(list_of_lists_of_vals):
    # input: emojis_as_list_in_spans_list = [['💙️'],['💙️','💙️','💙️'],['😃']]
    # code: vals_repeated_within_span =  getValuesRepeatedWithinSpans(emojis_as_list_in_spans_list)
    # value repeated, span number, number of times repeated
    # output: [('💙️',1,3)]
    if type(list_of_lists_of_vals)==float or list_of_lists_of_vals == [] or list_of_lists_of_vals == "[]" or  list_of_lists_of_vals == '':
        return []
    elif type(list_of_lists_of_vals) != list:
        list_of_lists_of_vals = ast.literal_eval(list_of_lists_of_vals)
    
    if type(list_of_lists_of_vals)==list and type(list_of_lists_of_vals[0])==list:
        list_w_vals_repeated_within = []
        i=0
        for span in list_of_lists_of_vals:
            if len(span)>1:
                uniques_in_span = list(set(span))
                if len(uniques_in_span) != len(span):
                    for uni in uniques_in_span:
                        cnt = span.count(uni)
                        if cnt >1:
                            tup = (uni,i,span.count(uni))
                            list_w_vals_repeated_within.append(tup)
            i+=1

        return list_w_vals_repeated_within
    else:
        return []


## ANALYZE REPETITION ACROSS SPANS      
# function to get cnt of spans value found in
def getCntSpansPerValue(list_of_lists_of_vals):
    # input: emojis_as_list_in_spans_list = [['💙️'],['💙️','💙️','💙️'],['😃']]
    # code: list_of_vals_w_cnts_of_span =  get_cnt_of_lists_in_list_per_val(emojis_as_list_in_spans_list)
    # output: [('💙️',2),('😃',1)]
    if type(list_of_lists_of_vals)==float or list_of_lists_of_vals == [] or list_of_lists_of_vals == "[]" or  list_of_lists_of_vals == '':
        return []
    elif type(list_of_lists_of_vals) != list:
        list_of_lists_of_vals = ast.literal_eval(list_of_lists_of_vals)
    
    if type(list_of_lists_of_vals)==list and type(list_of_lists_of_vals[0])==list:
        list_of_val_cnt_tuples = []
        long_list_on_uni_vals_per_list = []
        if list_of_lists_of_vals == []:
            return list_of_val_cnt_tuples
        # make sure it is a list of list of uniques
        list_of_unique_vals_in_list = [sorted(list(set(list_of_vals))) for list_of_vals in list_of_lists_of_vals]
        # convert list of lists to long list
        for uni_vals in list_of_unique_vals_in_list:
            long_list_on_uni_vals_per_list += uni_vals
        # get unique emojis
        uni_vals_list = list(set(long_list_on_uni_vals_per_list))
        for uni_val in uni_vals_list:
            if long_list_on_uni_vals_per_list.count(uni_val)>1:
                list_of_val_cnt_tuples.append((uni_val, long_list_on_uni_vals_per_list.count(uni_val)))
        # for consistency and comparison sorting list of cnts by val ascending then by cnt descending
        # sort the list of val cnts in acending order by emoji (first item in tuple)
        descending_sort_list_of_cnts_by_val = sorted(list_of_val_cnt_tuples, key = lambda x: x[0]) 
        # sort the list of val cnts in descending order by cnt (second item in tuple)
        descending_sort_list_of_cnts = sorted(descending_sort_list_of_cnts_by_val, key = lambda x: x[1], reverse=True) 
        return descending_sort_list_of_cnts
    else:
        return []

# STATUS OF REPETITION ACROSS SPANS
# check if any spans are in common
def getLabelForRepetitionAcrossSpans(list_of_lists_of_vals):
    # e.g. input: [['💙️', '🙏','😀','🔴'], ['💙️', '🙏'], ['💙️','🟢'], ['😀']] ==> output: 'no_repetition_of_list_of_vals'
    # input: list_of_emojis_in_spans = [['💙️', '🙏'], ['💙️', '🙏'], ['💙️'], ['😀']]
    # code: repetition_status_across_spans =  check_repetition_of_list_vals_across_list_of_lists(list_of_emojis_in_spans)
    # output: 'some_repetition_of_list_vals'
    if type(list_of_lists_of_vals)==float or list_of_lists_of_vals == [] or list_of_lists_of_vals == "[]" or  list_of_lists_of_vals == '':
        return []
    elif type(list_of_lists_of_vals) != list:
        list_of_lists_of_vals = ast.literal_eval(list_of_lists_of_vals)
    
    if type(list_of_lists_of_vals)==list and type(list_of_lists_of_vals[0])==list:

        if list_of_lists_of_vals == []:
            return []
        list_of_uni_val_lists_as_strs = []
        for val_list in list_of_lists_of_vals:
            list_of_uni_val_lists_as_strs.append(str(val_list))
        if len(list_of_lists_of_vals) == 1:
            return "single_list"
        elif len(list_of_lists_of_vals)>1 and len(set(list_of_uni_val_lists_as_strs))==1:
            return "repetition_across_spans"
        elif len(list_of_lists_of_vals)>1 and (len(list_of_lists_of_vals) == len(set(list_of_uni_val_lists_as_strs))):
            return "no_repetition_across_spans"
        elif len(list_of_lists_of_vals)>1 and len(set(list_of_uni_val_lists_as_strs))>1:
            return "some_repetition_across_spans"
        else:
            return "unknown"
    else:
        return "no_repetition_across_spans"

# VALUES THAT ARE REPETITION ACROSS SPANS AND ORDER
# get the spans that are in common with other span parts (repetition with same order)
def getSpansInOtherSpansPlusCount(list_of_lists_of_vals):
    # input: list_of_emojis_in_spans = [['💙️', '🙏'], ['💙️', '🙏','🔴'], ['💙️'], ['😀']]
    # code: list_of_vals_in_common =  get_list_of_vals_that_are_in_other_lists(list_of_emojis_in_spans)
    # output: [("'💙️'", 3), ("'💙️', '🙏'", 2)]
    if type(list_of_lists_of_vals)==float or list_of_lists_of_vals == [] or list_of_lists_of_vals == "[]" or  list_of_lists_of_vals == '':
        return []
    elif type(list_of_lists_of_vals) != list:
        list_of_lists_of_vals = ast.literal_eval(list_of_lists_of_vals)
    
    if type(list_of_lists_of_vals)==list and type(list_of_lists_of_vals[0])==list:
        list_of_lists_of_vals_as_strs = [str(val_list) for val_list in list_of_lists_of_vals]
        list_of_tuple_cnts_of_spans_in_other_spans = []
        for i in range(len(list_of_lists_of_vals)):
            val_list_as_str_to_check = list_of_lists_of_vals_as_strs[i][1:-1]
            cnt_how_many_times_val_list_in_other_lists = 1
            for z in range(len(list_of_lists_of_vals_as_strs)):
                if i == z:
                    continue
                else:
                    val_list_str = list_of_lists_of_vals_as_strs[z]
                    if val_list_as_str_to_check in val_list_str:
                        #print('true', val_list_as_str_to_check, val_list_str)
                        cnt_how_many_times_val_list_in_other_lists += 1
            list_of_tuple_cnts_of_spans_in_other_spans.append((val_list_as_str_to_check.replace("'","").replace(', ','').replace('"',''),cnt_how_many_times_val_list_in_other_lists))       
        uni_tup_cnts_list = list(set(list_of_tuple_cnts_of_spans_in_other_spans))
        uni_tup_cnts_list_greater_than_1 = filter(lambda x: x[1] > 1, uni_tup_cnts_list)   
        return sorted(uni_tup_cnts_list_greater_than_1, key = lambda x: x[1], reverse=True)
    else:
        return []

## ANALYZE ORDER AND SYMMETRY ACROSS SPANS CHECK FOR IDENTICAL OR FLIPPED
#import ast
# check the spans that are identical uniques for flipped order
def checkIdenticalOrFlippedSpans(list_of_lists_of_vals):
    # input: list_of_emojis_in_spans = [['💙️','🙏'], ['🙏','💙️'], ['💙️','🙏'], ['😀'],['😀']]
    # code: symmetry_check = check_for_symmetrical_patterns_across_lists(list_of_emojis_in_spans)
    # output: [('identical_spans', ([0, 2], ['💙️', '🙏'])),
                #('identical_spans', ([3, 4], ['😀'])),
                #('flipped_spans', ([0, 2], [1], [['💙️', '🙏'], ['🙏', '💙️']]))]
    # NOTES
    # the numbers indicate the index position of the span in the input list
    # for flipped, spans at [0,2] both have the value ['💙️', '🙏']
    # and the span at position [1] contains the flipped version which is ['🙏', '💙️']
    if type(list_of_lists_of_vals)==float or list_of_lists_of_vals == [] or list_of_lists_of_vals == "[]" or  list_of_lists_of_vals == '':
        return []
    elif type(list_of_lists_of_vals) != list:
        list_of_lists_of_vals = ast.literal_eval(list_of_lists_of_vals)
    
    if type(list_of_lists_of_vals)==list and type(list_of_lists_of_vals[0])==list:
        list_of_lists_of_vals_as_strs = [str(val_list) for val_list in list_of_lists_of_vals]
        uni_list_of_val_lists_as_strs = list(set(list_of_lists_of_vals_as_strs))
        list_of_tuple_symmetry_spans = []
        list_of_identical_spans = []
        list_of_flipped_spans = []
        for uni_val_list_str in uni_list_of_val_lists_as_strs:
            flipped_val_list_as_str_to_check = str(list(reversed(ast.literal_eval(uni_val_list_str))))
            val_list_w_identicals = []
            val_list_w_flipped = []
            for z in range(len(list_of_lists_of_vals_as_strs)):
                val_list_str_to_compare = list_of_lists_of_vals_as_strs[z]
                if uni_val_list_str == val_list_str_to_compare:
                    val_list_w_identicals.append(z)
                if uni_val_list_str.count(',')> 0: # if more than one val then check for flipped
                    if flipped_val_list_as_str_to_check == val_list_str_to_compare:
                        val_list_w_flipped.append(z)
            if len(val_list_w_identicals) > 1:
                list_of_tuple_symmetry_spans.append(('identical_spans', (val_list_w_identicals, list_of_lists_of_vals[val_list_w_identicals[0]])))
            if len(val_list_w_flipped) > 0:
                if min(val_list_w_identicals) < min(val_list_w_flipped):
                    list_of_tuple_symmetry_spans.append(('flipped_spans', (val_list_w_identicals, val_list_w_flipped, [list_of_lists_of_vals[val_list_w_identicals[0]],list_of_lists_of_vals[val_list_w_flipped[0]]])))
        # for flipped spans if the second is smaller than first then drop
        if list_of_tuple_symmetry_spans == []:
            return [('no_identical_or_flipped_spans',)]
        return sorted(list_of_tuple_symmetry_spans, key = lambda x: x[0], reverse=True)
    else:
        return []


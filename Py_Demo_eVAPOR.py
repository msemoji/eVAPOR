#!/usr/bin/env python
# coding: utf-8

# # eVAPOR

# In[1]:


# This code summarizes emoji use within a document as:
# the unique emoji attributes, relative position of emoji in the document,
# the order of attributes, and the use of emoji repetition


# In[2]:


import eVAPOR


# In[3]:


# get the relative positions of the emoji spans in the document structure
original_text = 'RT @at_mention @person2 VOTE 🗳 🇦🇺 😃 yes now go #vote #today @user3 😃 🍎 http://www.someurl.com'

# get the full document structures and content structure and emoji spans 
# to do this use repo for structural_content_analysis
full_doc_structure_w_content = [('RT', 1, ['RT']), ('at_mention', 2, ['@atmention', '@person2']), ('text', 2, ['VOTE', ' ']), ('emoji', 3, ['🗳', '🇦🇺', '😃']), ('text', 6, ['yes', ' ', 'now', ' ', 'go', ' ']), ('hashtag', 2, ['#vote', '#today']), ('at_mention', 1, ['@user3']), ('emoji', 2, ['😃', '🍎']), ('url', 1, ['http://www.someurl.com'])]
doc_structure = [('RT', 1), ('at_mention', 2), ('text', 2), ('emoji', 3), ('text', 6), ('hashtag', 2), ('at_mention', 1), ('emoji', 2), ('url', 1)]
content_structure = ['RT','at_mention','text','emoji','text','hashtag','at_mention','emoji','url']
emoji_spans_list = [['🗳', '🇦🇺', '😃'],['😃', '🍎']]


# In[4]:


# Emoji positision in text
# get position of a content type based on order in full document structure
print('Relative positions')

content_types_to_choose_from_are = ['RT','at_mention','emoji','url','text','punctuation']

# input is the full document structure with content or the document structure

emoji_positions = eVAPOR.getRelativePositionOfContentType(full_doc_structure_w_content,'emoji')
print('emoji', emoji_positions)

atmention_positions = eVAPOR.getRelativePositionOfContentType(full_doc_structure_w_content,'at_mention')
print('at_mention', atmention_positions)

url_positions = eVAPOR.getRelativePositionOfContentType(full_doc_structure_w_content,'url')
print('url', url_positions)

text_positions = eVAPOR.getRelativePositionOfContentType(full_doc_structure_w_content,'text')
print('text', text_positions)


# In[5]:


# new sample to analyze order and repetition
sample_text = '💙️🙏 Go BLUE 🙏💙️beat RED 💙️🙏🔴 #Blue 🔷🔷🔷 for the win 😀 again 😀'
full_doc_struct = [('emoji',2,['💙️','🙏']),('text',2,['Go', 'BLUE']),('emoji',2,['🙏','💙️']),('text',2,['beat', 'RED']),('emoji',3,['💙️','🙏','🔴']),('hashtag',1,['#Blue']),('emoji',3,['💙️','💙️','💙️']),('text',3,['for', 'the', 'win']),('emoji',1,['😀']),('text',1,['again']),('emoji',1,['😀'])]
sample_emoji_span_list = [['💙️','🙏'],['🙏','💙️'],['💙️','🙏','🔴'],['🔷','🔷','🔷'],['😀'],['😀']]
print(sample_text)
print()
emoji_positions = eVAPOR.getRelativePositionOfContentType(full_doc_struct,'emoji')
print('emoji positions', emoji_positions)


# In[6]:


# analysis of emojis REPEATED WITHIN spans
print('sample text:', sample_text)
print()

# Repetition and order examines the emojis spans list created as part of structural content analysis
print('emoji spans list to evaluate for Order and Repetition Within and Across Spans:')
print('emoji spans list:', sample_emoji_span_list)
print()
print('Repetition Within Spans, status for each span:')
# REPETITION WITHIN SPAN # indicate if any emojis repeated within same span

print(eVAPOR.labelRepetitionWithinSpans(sample_emoji_span_list))
# results are repetition status within each span
print()

print('Values repeated within a span')
print(eVAPOR.getValuesRepeatedWithinSpans(sample_emoji_span_list))
print('shows value repeated within a span, span number, and the number of times it is repeated')
# results are the value, the span posisiton, and number of time in that span
print()
print()


# In[7]:


# analysis of REPEATED ACROSS spans
print('sample text:', sample_text)
print('emoji spans list:', sample_emoji_span_list)
print()
print('Repetition Across Spans:')
print()

print('show each unique value and the count of spans it occurs in')
print(eVAPOR.getCntSpansPerValue(sample_emoji_span_list))
print()


print('status check are any spans repeated or flipped in other spans')
print(eVAPOR.getLabelForRepetitionAcrossSpans(sample_emoji_span_list))
# e.g. some repetition across spans
print()


print('full spans that are repeated within or as other spans')
print(eVAPOR.getSpansInOtherSpansPlusCount(sample_emoji_span_list))
# results indicate the emoji or consecutive emojis and the count of spans it occurs in
print()


print('Check for Identical and Flipped Spans and show span numbers and the pattern')
# identify which full spans are repeated as identical and which are the same emojis but flipped order of emoji
eVAPOR.checkIdenticalOrFlippedSpans(sample_emoji_span_list)
# results state if it is identical or flipped, the span number in the span list, and the value


# In[8]:


# ATTRIBUTES order and repetition

# attributes_to_choose_from = 
# 'group', 'subgroup', 'grp_subgrp','shape_type', 'shape_color', 'direction', 'cldr short name'
# 'desc', 'person_animal_other', 'anthro_type', 'gender', 'skin_tone', 'sentiment_smileys_binary',
#                   
sample_emoji_span_list = [['💙️','🙏'],['🙏','💙️'],['💙️','🙏','🔴'],['🔷','🔷','🔷'],['😀'],['😀']]
print(sample_emoji_span_list)

print('cldr short name')
print(eVAPOR.getAttributesForSpansList(sample_emoji_span_list,'cldr short name'))
print()

print('shape_color')
color_order_list = eVAPOR.getAttributesForSpansList(sample_emoji_span_list,'shape_color')
print(color_order_list)
print('repetition of color within')
print(eVAPOR.getValuesRepeatedWithinSpans(color_order_list))
print('repetition of color across')
print(eVAPOR.getCntSpansPerValue(color_order_list))

print()
print()

print('shape_type')
color_order_list = eVAPOR.getAttributesForSpansList(sample_emoji_span_list,'shape_type')
print(color_order_list)
print('repetition of shape within')
print(eVAPOR.getValuesRepeatedWithinSpans(color_order_list))
print('repetition of shape across')
print(eVAPOR.getCntSpansPerValue(color_order_list))


# ## Analyze eVAPOR with sample data 

# In[9]:


import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)


df = pd.read_csv('./sample_data/processed_output_of_structural_content_of_sample_data.csv')
df.head(7)


# ## Analyze Emoji Relative Position in Document Structure 

# In[10]:


# Analyze the emoji positions
# input is document structure with content
# the document structures are created in identifyStructures.py in the repo for structural_content_analysis

df['emoji_positions'] = df['full_document_structure'].apply(lambda x: eVAPOR.getRelativePositionOfContentType(x,'emoji'))
df.head(7)


# In[11]:


# Emojis and spans repeated within spans
df['emojis_repeated_within_spans'] = df['emoji_spans_as_lists'].apply(eVAPOR.getValuesRepeatedWithinSpans)

df['status_repetition_across_spans'] = df['emoji_spans_as_lists'].apply(eVAPOR.getLabelForRepetitionAcrossSpans)

df['emojis_w_cnt_spans'] = df['emoji_spans_as_lists'].apply(eVAPOR.getCntSpansPerValue)

df['emoji_spans_repeated_across_spans'] = df['emoji_spans_as_lists'].apply(eVAPOR.getSpansInOtherSpansPlusCount)

df['emoji_spans_identical_flipped'] = df['emoji_spans_as_lists'].apply(eVAPOR.checkIdenticalOrFlippedSpans)

df.head(7)


# In[12]:


# common emoji positions
print(df['emoji_positions'].astype(str).value_counts()[:7])
print()

# common emojis repeated within spans
print(df['emojis_repeated_within_spans'].astype(str).value_counts()[:7])
print()

# common status of repetition across spans
print(df['status_repetition_across_spans'].astype(str).value_counts()[:7])
print()

# common spans repeated across
print(df['emoji_spans_repeated_across_spans'].astype(str).value_counts()[:7])
print()


# common of what is identical_flipped in common
print(df['emoji_spans_identical_flipped'].astype(str).value_counts()[:7])


# In[13]:


# Analyze emoji attribute color

df['emoji_color_order_list'] = df['emoji_spans_as_lists'].apply(lambda x: eVAPOR.getAttributesForSpansList(x,'shape_color'))

df['repetition_of_color_within'] = df['emoji_color_order_list'].apply(eVAPOR.getValuesRepeatedWithinSpans)

df['repetition_of_color_across'] = df['emoji_color_order_list'].apply(eVAPOR.getCntSpansPerValue)

df.head(10)


# In[14]:


# common color orders
print('common color order')
print(df['emoji_color_order_list'].astype(str).value_counts()[:7])
print()

print('repetition of color within')
print(df['repetition_of_color_within'].astype(str).value_counts()[:7])
print()


print('repetition of color across')
print(df['repetition_of_color_across'].astype(str).value_counts()[:7])
print()


# In[15]:


df.to_excel('processed_eVAPOR_parts_for_sample_data.xlsx', index=False, encoding='utf8')
df.to_csv('processed_eVAPOR_parts_for_sample_data.csv', index=False, encoding='utf8')


# In[ ]:





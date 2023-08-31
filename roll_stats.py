import numpy as np
import time
import streamlit as st
from scipy import stats


def roll_3d6():
    rolls = np.random.randint(low=1, high=7, size=(6, 3))
    return rolls.sum(axis=1)

def roll_3d6_reroll_ones():
    rolls = np.random.randint(low=2, high=7, size=(6, 3))
    return rolls.sum(axis=1)

def roll_2d6_plus_six():
    rolls = np.random.randint(low=1, high=7, size=(6, 2))
    return 6+rolls.sum(axis=1)

def roll_4d6_drop_lowest():
    rolls = np.random.randint(low=1, high=7, size=(6, 4))
    rolls = np.sort(rolls, axis=1)[:,1:]
    return rolls.sum(axis=1)

def roll_4d6_drop_lowest_reroll_ones():
    rolls = np.random.randint(low=2, high=7, size=(6, 4))
    rolls = np.sort(rolls, axis=1)[:,1:]
    return rolls.sum(axis=1)

def roll_2d10():
    rolls = np.random.randint(low=1, high=11, size=(6, 2))
    return rolls.sum(axis=1)
                             
    

stat_names = ['Strength', 'Dexterity', 'Constiution',
              'Intelligence', 'Widsom', 'Charisma']
method_dict = {'Roll 3d6': roll_3d6,
               'Roll 3d6 reroll ones': roll_3d6_reroll_ones,
               'Roll 2d6 plus six': roll_2d6_plus_six,
               'Roll 4d6 drop lowest': roll_4d6_drop_lowest,
               'Roll 4d6 drop lowest reroll ones': roll_4d6_drop_lowest_reroll_ones,
               'Roll 2d10': roll_2d10}
method_name = st.selectbox('Choose a method to roll stats', list(method_dict.keys()))
method = method_dict[method_name]

col1, col2 = st.columns(2)
mercy = col1.checkbox('Is your god a merciful god?')
in_order = col2.checkbox('Generate stats in order?')

if st.button('Roll!'):
    
    if mercy:
        maxstat = 0
        minstat = 0
        while maxstat<16 or minstat<8:
            my_rolls = method()
            maxstat = my_rolls.max()
            minstat = my_rolls.min()
    else:
        my_rolls = method()

        
    columns = st.columns(6)
    for i, column in enumerate(columns):
        with st.spinner(text='Rolling rolling rolling...'):
            time.sleep(1.0)
        if in_order:
            column.metric(stat_names[i], my_rolls[i])
        else:
            column.metric('Roll %d'%(i+1), my_rolls[i])
        
    st.balloons()
        
    with st.expander('How good are my rolls?'):
        
        num_sim = 5000
        max_scores = np.zeros(num_sim, dtype=np.int32)
        top_three = np.zeros(num_sim, dtype=np.int32)
        total = np.zeros(num_sim, dtype=np.int32)

        for i in range(num_sim):
            if mercy:
                maxstat = 0
                minstat = 0
                while maxstat<16 or minstat<8:
                    rolls = method()
                    maxstat = rolls.max()
                    minstat = rolls.min()
            else:
                rolls = method()
            rolls = np.sort(rolls)
            max_scores[i] = rolls[-1]
            top_three[i] = np.sum(rolls[-3:])
            total[i] = rolls.sum()
            
        my_rolls_sorted = np.sort(my_rolls)
        my_max = my_rolls_sorted[-1]
        my_top_three = np.sum(my_rolls_sorted[-3:])
        my_total = my_rolls_sorted.sum()
        max_pc = stats.percentileofscore(max_scores, my_max, kind='weak')
        top_three_pc = stats.percentileofscore(top_three, my_top_three, kind='weak')
        total_pc = stats.percentileofscore(total, my_total, kind='weak')
        st.write('Highest stat percentile: %.1f'%max_pc)
        st.write('Sum of your three best stats percentile: %.1f'%top_three_pc)
        st.write('Sum of your stats percentile: %.1f'%total_pc)
    


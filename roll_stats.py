import numpy as np
import time
import matplotlib.pyplot as plt
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
    


method_dict = {'Roll 3d6': roll_3d6,
               'Roll 3d6 reroll ones': roll_3d6_reroll_ones,
               'Roll 2d6 plus six': roll_2d6_plus_six,
               'Roll 4d6 drop lowest': roll_4d6_drop_lowest,
               'Roll 4d6 drop lowest reroll ones': roll_4d6_drop_lowest_reroll_ones}
method_name = st.selectbox('Choose a method to roll stats', list(method_dict.keys()))
method = method_dict[method_name]

mercy = st.checkbox('Is your god a merciful god?')

if st.button('Roll!'):
    
    if mercy:
        maxstat = 0
        while maxstat<16:
            my_rolls = method()
            maxstat = my_rolls.max()
    else:
        my_rolls = method()

        
    columns = st.columns(6)
    for i, column in enumerate(columns):
        with st.spinner(text='Rolling rolling rolling...'):
            time.sleep(1.0)
        column.metric('Roll %d'%(i+1), my_rolls[i])
        
    st.balloons()
        
    with st.expander('How good is my roll?'):
        
        num_sim = 5000
        max_scores = np.zeros(num_sim, dtype=np.int32)
        top_three = np.zeros(num_sim, dtype=np.int32)
        total = np.zeros(num_sim, dtype=np.int32)

        for i in range(num_sim):
            if mercy:
                maxstat = 0
                while maxstat<16:
                    rolls = method()
                    maxstat = rolls.max()
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
        st.write('Your highest stat is in the %.1f percentile'%max_pc)
        st.write('The sum of your three best stats is in the %.1f percentile'%top_three_pc)
        st.write('The sum of your stats is in the %.1f percentile'%total_pc)
    


import matplotlib.pyplot as plt
import plotly.express as px
import base64
from io import BytesIO

import numpy as np
import pandas as pd



def get_graph():
    buffer=BytesIO()
    plt.savefig(buffer, dpi='figure', format=None, metadata=None,
        bbox_inches=None, pad_inches=0.1,
        facecolor='auto', edgecolor='auto',
        backend=None
       )
    buffer.seek(0)
    image_png=buffer.getvalue()
    graph=base64.b64encode(image_png)
    graph=graph.decode('utf-8')
    buffer.close()
    return graph

def get_plot(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,3))
    plt.title('score rating of')
    plt.plot(x,y, color='#18A558',  edgecolor='#f1f1f1')
    plt.xticks(rotation=45, color='#18A558')
    plt.xlabel('Follow_recruiter_1', color='#18A558')
    plt.ylabel('FollowER_recruiter_1', color='#18A558')
    plt.tight_layout()
    # plt.subplots()
    graph=get_graph()
    return graph



def get_bar(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,3))
    plt.title('score rating of')
    plt.bar(x,y, color='#18A558',  edgecolor='#f1f1f1')
    plt.xticks(rotation=0, color='#18A558')
    # plt.xlabel('Follow_recruiter_1', color='#18A558')
    # plt.ylabel('FollowER_recruiter_1', color='#18A558')
    plt.tight_layout()
    # plt.subplots()
    graph=get_graph()
    return graph



def get_scatter(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(7,3))
    plt.title('score rating of')
    plt.scatter(x,y, color='#18A558',  edgecolor='#f1f1f1')
    plt.xticks(rotation=45, color='#18A558')
    plt.xlabel('Follow_recruiter_1', color='#18A558')
    plt.ylabel('FollowER_recruiter_1', color='#18A558')
    plt.tight_layout()
    # plt.subplots()
    graph=get_graph()
    return graph



def get_scatter_yearTechStack(x,y):
    N = 50
    area = sum([y])**2
    colors = ['#18A558', '#FFA500', '#E9967A', '#FFFF00', '#DC143C', '#9370DB', '#FF6347']

    plt.switch_backend('AGG')
    fig= plt.figure(figsize=(7,3))
    fig.set_figwidth(7)
    fig.set_figheight(5)

    plt.title('Worked year of Tech Stacks')
    plt.scatter(x,y,  edgecolor='#f1f1f1', s=area, c=colors, alpha=0.5)
    plt.xticks(rotation=45, color='#18A558')
    plt.xlabel('Tech Stack', color='#18A558')
    plt.ylabel('worked year', color='#18A558')
    plt.tight_layout()
    # plt.subplots()
    graph=get_graph()
    return graph





def get_bar_chart_profile(x,y):
    plt.switch_backend('AGG')
    plt.figure(figsize=(4,3))
    plt.title('Profile Rating | Evaluator', color='#008a3e', fontweight='book')
    plt.bar(x,y, color='#18A558',  edgecolor='#f1f1f1')
    
    plt.xticks(rotation=90, color='#18A558')

    # plt.set_xticks([0, np.pi, 2 * np.pi, 3 * np.pi, 4 * np.pi, 5 * np.pi])
    # plt.set_xticklabels(['0', r'$\pi$', r'2$\pi$', r'3$\pi$', r'4$\pi$', r'5$\pi$'])

    plt.margins(0.02)
    plt.subplots_adjust(bottom=0.15)

    # plt.xlabel('Follow_recruiter_1', color='#18A558')
    # plt.ylabel('FollowER_recruiter_1', color='#18A558')
    plt.tight_layout()
    # plt.subplots()
    graph=get_graph()
    return graph


def get_bar_chart_profileDashboard_interaction(x,y):

    colors = ['#F58518', '#4C78A8']
    labels = ['Mentors', 'Fellows']

    plt.switch_backend('AGG')
    # plt.figure(figsize=(0.2,0.1))
    plt.title('INTERACTION', color='#008a3e', fontweight='book')
    plt.bar(labels,y, width=0.2,  edgecolor=colors, fill=False, linewidth=5)
    
    plt.xticks(color='#18A558')

    plt.rc('font', size=9.4)
        
    fig, ax = plt.subplots(figsize=(1.7,1.6))
    rects1 = ax.bar(labels,y, width=0.07, edgecolor=colors, fill=False, linewidth=5)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.grid(False)
    # plt.axis('off')

    ax = plt.gca() 
    ax.get_yaxis().set_visible(False) 
    ax.legend()
    ax.bar_label(rects1, padding=3) 
    plt.tight_layout() 
    graph=get_graph()
    return graph





def get_bar_chart_profileDashboard_mentor_fellow(x,y):

    colors = ['#F58518', '#4C78A8']
    labels = ['Mentors', 'Mentees']

    plt.switch_backend('AGG')
    # plt.figure(figsize=(0.2,0.1))
    plt.title('INTERACTION', color='#008a3e', fontweight='book')
    plt.bar(labels,y, width=0.2,  edgecolor=colors, fill=False, linewidth=5)
    
    plt.xticks(color='#18A558')

    plt.rc('font', size=9.4)
        
    fig, ax = plt.subplots(figsize=(1.7,1.6))
    rects1 = ax.bar(labels,y, width=0.07, edgecolor=colors, fill=False, linewidth=5)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.grid(False)
    # plt.axis('off')

    ax = plt.gca() 
    ax.get_yaxis().set_visible(False) 
    ax.legend()
    ax.bar_label(rects1, padding=3) 
    plt.tight_layout() 
    graph=get_graph()
    return graph



def get_bar_chart_profileDashboard_mentoring_learning(x,y):

    colors = ['#F58518', '#4C78A8']
    labels = ['Teaching','Learning']

    plt.switch_backend('AGG')
    # plt.figure(figsize=(0.2,0.1))
    plt.title('INTERACTION', color='#008a3e', fontweight='book')
    plt.bar(labels,y, width=0.2,  edgecolor=colors, fill=False, linewidth=5)
    
    plt.xticks(color='#18A558')

    plt.rc('font', size=9.4)
        
    fig, ax = plt.subplots(figsize=(1.7,1.6))
    rects1 = ax.bar(labels,y, width=0.07, edgecolor=colors, fill=False, linewidth=5)

    ax.spines['top'].set_visible(False)
    ax.spines['bottom'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.get_xaxis().tick_bottom()
    ax.get_yaxis().tick_left()
    
    plt.grid(False)
    # plt.axis('off')

    ax = plt.gca() 
    ax.get_yaxis().set_visible(False) 
    ax.legend()
    ax.bar_label(rects1, padding=3) 
    plt.tight_layout() 
    graph=get_graph()
    return graph
    

def autopct_format(values):
    def my_format(pct):
        total = sum(values)
        val = int(round(pct*total/100.0))
        return '{v:d}'.format(v=val)
    return my_format
    

def get_pie_profileDashboard_projects(x_data,y_label):

    # plt.xkcd() 


    # colors = ['#ff4040','#ffa500','#18A558']
    colors = ['#4C78A8', '#F58518']
    

    plt.switch_backend('AGG')
    # fig =plt.figure(figsize=(2,2),dpi=100)

    # plt.title('score rating of')
    # plt.pie(x,y, color='#18A558',  edgecolor='#f1f1f1')
    plt.subplots(figsize=(3, 1.6), subplot_kw=dict(aspect="equal"))
    
    
    plt.pie(x_data, 
            colors=colors,  
            labels=y_label, 
            shadow=True, 
            wedgeprops=dict(width=0.07), 
            startangle=-40,
            # autopct='%1.1f%%',
            autopct = autopct_format(x_data)
            )
 


    plt.xticks(rotation=45, color='#18A558')
    # plt.xlabel('Follow_recruiter_1', color='#18A558')
    # plt.ylabel('FollowER_recruiter_1', color='#18A558')
    plt.tight_layout()
    # plt.subplots()
    graph=get_graph()
    return graph



def get_pie(x_data,y_label):
    # plt.xkcd() 
    colors = ['#ff4040','#ffa500','#18A558']
    

    plt.switch_backend('AGG')
    plt.figure(figsize=(7,3))
    # plt.title('score rating of')
    # plt.pie(x,y, color='#18A558',  edgecolor='#f1f1f1')
    plt.subplots(figsize=(6, 3), subplot_kw=dict(aspect="equal"))
    
    plt.pie(x_data, 
            colors=colors,  
            labels=y_label, 
            shadow=True, 
            wedgeprops=dict(width=0.1), 
            startangle=-40,
            # autopct='%1.1f%%',
            autopct = autopct_format(x_data)
            )
            

    plt.xticks(rotation=45, color='#18A558')
    # plt.xlabel('Follow_recruiter_1', color='#18A558')
    # plt.ylabel('FollowER_recruiter_1', color='#18A558')
    plt.tight_layout()
    graph=get_graph()
    return graph



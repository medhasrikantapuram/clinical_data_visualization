import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as gp
import streamlit as st
adsl = pd.read_excel("ADSL.xlsx")
advs = pd.read_excel("ADVS.xlsx")
adae = pd.read_excel("ADAE.xlsx")
# Change from baseline to eos in body weight
tab1, tab2, tab3 = st.tabs(["Demographics", "Vital Signs","Adverse Events"])
with tab1:
    df_bas = adsl[['USUBJID', 'ARM','AGE','AGEGR1','RACE', 'SEX', 'ETHNIC','BMIBL', 'BMIBLGR1', 'HEIGHTBL','WEIGHTBL', 'EDUCLVL']]
    df_bas.dropna(inplace=True)
    df_bas_1 = df_bas[['ARM','AGEGR1','SEX']].value_counts()
    df_bas_1 = df_bas_1.reset_index()
    df_bas_1 = df_bas_1.sort_values(by=['ARM','AGEGR1','SEX'])
    df_bas_1 = df_bas_1.reset_index(drop=True)
    df_bas_1.rename({0:'Count'},axis=1,inplace=True)
    data=df_bas_1.pivot_table(index=['ARM','AGEGR1'],columns='SEX',values='Count')
    data = data.reset_index()
    agegr = data['AGEGR1']
    agegr2 = [1 if i=='<65' else 2 if i=='65-80' else 3 for i in agegr]
    data['age_cat'] = agegr2
    arm3 = st.selectbox("Which treatment arm do you want to view?",adsl['TRT01A'].unique().tolist())
    data_a = data[data['ARM']==arm3]
    y_age = data_a['age_cat']
    x_M = data_a['M']
    x_F = data_a['F'] * -1
    fig1 = gp.Figure()
    # Adding Male data to the figure
    fig1.add_trace(gp.Bar(y= y_age, x = x_M, 
                         name = 'Male', 
                         orientation = 'h'))

    # Adding Female data to the figure
    fig1.add_trace(gp.Bar(y = y_age, x = x_F,
                         name = 'Female', orientation = 'h'))

    # Updating the layout for our graph
    fig1.update_layout(title = 'Population Pyramid for the treatment',barmode = 'relative',
                     bargap = 0.5, bargroupgap = 0.1,autosize=False,
          width=800,
          height=400,
                     xaxis = dict(tickvals = [-20, -10,
                                              0, 10, 20],

                                  ticktext = ['20', '10', '0', 
                                              '10', '20'],

                                  title = 'Population',
                                  title_font_size = 14),
                      yaxis = dict(tickvals=[1,2,3],
                                  ticktext = ['<65','65-80','>80'],                         
                                  title = 'Age Group',
                                  title_font_size = 14), 
                     )
    st.plotly_chart(fig1,use_container_width = True)
with tab2:
    param_wt = advs[advs['PARAMCD']=='WEIGHT']
    def avisitn1(df):    
        if (df['AVISITN'] == 0.0):
             return 0
        elif (df['AVISITN']==2.0):
             return 2
        elif (df['AVISITN']==4.0):
             return 4
        elif (df['AVISITN']==6.0):
             return 6
        elif (df['AVISITN']==8.0):
             return 8
        elif (df['AVISITN']==12.0):
             return 10
        elif (df['AVISITN']==16.0):
             return 12
        elif (df['AVISITN']==20.0):
             return 14
        elif (df['AVISITN']==24.0):
             return 16  
        elif (df['AVISITN']==26.0):
             return 18
        elif (df['AVISITN']==99.0):
             return 20
    df = param_wt.assign(AVISITN1=param_wt.apply(avisitn1, axis=1))
    arm2 = st.radio("Which treatment arm do you want to view? ",advs['TRTA'].unique().tolist())
    df_arm = df[df['TRTA']==arm2]
    fig3 = px.box(df_arm[df_arm['AVISITN1']!=0], y="CHG", x="AVISITN1"
                       ,title="Change in Weight from baseline"
                      ,labels={"CHG": "Change from baseline","AVISITN1":"Analysis Visit (N)"}, color='AVISITN1')
    st.plotly_chart(fig3,use_container_width = True)
with tab3:
    adae_subs = adae[adae['TRTEMFL']=='Y']
    top_24 = adae_subs['AEDECOD'].value_counts().index.tolist()[:24]
    adae_subset = adae_subs[adae_subs['AEDECOD'].isin(top_24)]
    dot_plot_df = pd.DataFrame(adae_subset.groupby(['TRTA','AEDECOD']).size()).reset_index()
    fig = px.scatter(dot_plot_df, y="AEDECOD", x=0, color="TRTA",symbol="TRTA",height=800,hover_name='AEDECOD')
    fig.update_traces(marker_size=8)
    fig.update_layout(title="Top 25 Treatment Emergent Adverse Events",
                  xaxis_title="Count",
                  yaxis_title="Adverse Events",
                  legend_title="Treatment Arms"
                  )
    st.plotly_chart(fig,use_container_width = True)

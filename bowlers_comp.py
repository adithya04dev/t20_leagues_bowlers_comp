
import pandas as pd
import numpy as np
import pickle
# df=pd.read_csv("C:/Users/adith/Documents/ds/t20_leagues/set_3_leagues/all_match_data_with_types.csv")

class Bowler_comp():

            def __init__(self,deliveries_df):

                self.df = deliveries_df.copy()
                
                
                self.dic={1:[i for i in range(0,6)],2:[i for i in range(6,11)],3:[i for i in range(11,16)],4:[i for i in range(16,21)]}
                self.league=self.df['LeagueName'].unique()

            def calculateb(self,leagues,overs1,BatterType,Season,limit):
                    bowlers_df = pd.DataFrame(columns=['player_name','total_runs','wickets','balls_bowled','runrate','average','bpercent','dpercent'])
                    overs=[]
                    for over in overs1:
                        overs+=self.dic[over]
                    players=self.df.loc[(self.df['Season'].isin(Season)) & (self.df["LeagueName"].isin(leagues))  & (self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) ]['Bowler'].unique()
                    
                    
                     
                    for player in players:
                        dis=["run out", 'retired hurt',  'obstructing the field','retired out']

                        run = int(self.df.loc[(self.df["Bowler"] == player) & (self.df["LeagueName"].isin(leagues)) & (
                            self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (
                                                  self.df["Season"].isin(Season))].batsman_run.sum())
                        run+= len(self.df.loc[(self.df["Bowler"] == player) & (self.df["LeagueName"].isin(leagues)) & (
                            self.df["BattingType"].isin(BatterType)) & (self.df["overs"].isin(overs)) & (
                                                  self.df["Season"].isin(Season))& (self.df["is_wide"]|self.df["is_noball"] )])
                        balls = len(self.df.loc[(self.df['is_wide'] == 0) & (self.df['is_noball'] == 0) & (
                            self.df["LeagueName"].isin(leagues)) & (self.df["BattingType"].isin(BatterType)) & (
                                                    self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season)) & (
                                                        self.df['Bowler'] == player)])
                        out = len(self.df.loc[(self.df["player_out"] == 1) &(self.df["is_runout"] == 0)  & (self.df["Bowler"] == player) & (
                            self.df["LeagueName"].isin(leagues)) & (self.df["BattingType"].isin(BatterType)) & (
                                                  self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                        boundary = len(
                            self.df.loc[(self.df["Bowler"] == player) & (self.df["LeagueName"].isin(leagues)) & (
                                    (self.df["batsman_run"] == 4) | (self.df["batsman_run"] == 6)) & (
                                            self.df["BattingType"].isin(BatterType)) & (
                                            self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])
                        dots = len(self.df.loc[(self.df["Bowler"] == player) & (self.df["LeagueName"].isin(leagues)) & (
                                self.df["Extras_Run"] == 0) & (self.df["batsman_run"] == 0) & (
                                                   self.df["BattingType"].isin(BatterType)) & (
                                                   self.df["overs"].isin(overs)) & (self.df["Season"].isin(Season))])

                        avg_run=run/out if out!=0 else np.inf
                        bpercent=(boundary/balls)*100 if balls!=0 else 0
                        runrate=(run * 6)/balls if balls!=0 else np.inf
                        dpercent=(dots/balls)*100 if balls!=0 else 0
    
                        df2 = {'player_name':player,'total_runs': int(run), 'wickets':int(out),'balls_bowled': int(balls),'runrate':runrate,'average': avg_run,'bpercent':bpercent,'dpercent':dpercent}
                        if balls>limit:
                                bowlers_df =pd.concat([bowlers_df ,pd.DataFrame(df2, index=[0])],ignore_index =True)

                    return bowlers_df.sort_values(by='runrate',ascending=True)

            

            

#
# bowcomp=Bowler_comp(df)
# # print(bowcomp.calculateb(['TNPL'],[1,2,3,4],['LHB','RHB'],[2023],30).head(10))
#
#
#
#
# with open('C:/Users/adith/Documents/ds/t20_leagues/set_3_leagues/app/individual/bowlong_comp/bowling_comp.pkl', 'wb') as f:
#     pickle.dump(bowcomp, f)
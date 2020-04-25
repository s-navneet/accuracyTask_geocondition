#!/usr/bin/env python
# coding: utf-8

# In[83]:


import pandas as pd
import numpy as np
df = pd.read_csv('/home/navneet/Documents/accuracy/finalAccuracy/testaccu.csv')
df=df.astype(str)
#df.head()


# In[84]:


#Add columns and calculate matching between columns:

col=['inputpincode = geocodepincode',
    'inputcity = geocodecity',
    'firstword = inputcity',
    'inputpincode = spatialpincode',
    'inputcity = spatialcityname164',
    'inputcity = spatialcitynamegeoexpansion',
    'inputstate = spatialstate',
    ]
new_df= pd.DataFrame(columns=col)
#new_df.head()


# In[85]:


T='true'
F='false'
new_df['inputpincode = geocodepincode']=np.where(df['Input Pincode'] == df['Geocoded Pincode'],T,F)
new_df['inputcity = geocodecity']=np.where(df['Input City'] == df['Geocoded City'],T,F)
new_df['firstword = inputcity']=np.where(df['first word'] == df['Input City'],T,F)
new_df['inputpincode = spatialpincode']=np.where(df['Input Pincode'] == df['Spatial Pincode'],T,F)
new_df['inputcity = spatialcityname164']=np.where(df['Input City'] == df['SpatialCityName164'],T,F)
new_df['inputcity = spatialcitynamegeoexpansion']=np.where(df['Input City'] == df['SpatialCityNameGeoexpansion'],T,F)
new_df['inputstate = spatialstate']=np.where(df['Input State'] == df['Spatial State'],T,F)
new_df.head()


# In[86]:


tf_df=new_df
tf_df.astype(str)


# In[87]:


inp_tf_df=df.join(new_df)
inp_tf_df.to_csv('/home/navneet/Documents/accuracy/finalAccuracy/input_true_false.csv')


# In[ ]:





# In[64]:


col1=['gcon1','gcon2','spcon1','spcon2','gspcon1','gspcon2','gsp2con1','gsp2con2','gpcon1','gpcon2','gfalse1',
      'gfalse2','match',
     ]
con_df=pd.DataFrame(columns=col1)

con_df['match']=df['Match_types']

con_df.head()


# In[65]:


#geocode condition

#1.GEOCODED CONDITIONS - TRUE
condition1=[
    (tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
    (tf_df['inputcity = geocodecity'].str.lower() == 'true') & 
    (tf_df['firstword = inputcity'].str.lower() == 'true')
    ]
choice1=['true']
con_df['gcon1'] = np.select(condition1, choice1,default='false')


#2.GEOCODED CONDITIONS - TRUE
condition2=[(tf_df['inputpincode = geocodepincode'].str.lower() == 'true') &
           (tf_df['inputcity = geocodecity'].str.lower() == 'true')
           ]
choice2=['true']


con_df['gcon2'] = np.select(condition2, choice2,default='false')


#SPATIAL CONDITIONS - TRUE

#3 SPATIAL CONDITIONS - TRUE
condition3=[
    (tf_df['inputpincode = spatialpincode'].str.lower() == 'true' ) & 
    (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
    (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true') &
    (tf_df['firstword = inputcity'].str.lower() == 'true')
    ]
choice3=['true']
con_df['spcon1'] = np.select(condition3, choice3,default='false')


#4 SPATIAL CONDITIONS - TRUE
condition4=[(tf_df['inputpincode = spatialpincode'].str.lower() == 'true' ) & 
    (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
    (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true')
           ]
choice4=['true']
con_df['spcon2'] = np.select(condition4, choice4, default='false')

#GEOCODED & SPATIAL CONDITIONS – GEOCODED PINCODE TO SPATIAL CITY - TRUE
#5GEOCODED & SPATIAL CONDITIONS
condition5=[
    (tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
    (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
    (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true') &
    (tf_df['firstword = inputcity'].str.lower() == 'true')
    ]
choice5=['true']
con_df['gspcon1'] = np.select(condition5, choice5,default='false')


#6GEOCODED & SPATIAL CONDITIONS
condition6=[(tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
    (tf_df['inputcity = spatialcityname164'].str.lower() == 'true') | 
    (tf_df['inputcity = spatialcitynamegeoexpansion'].str.lower() == 'true')
           ]
choice6=['true']
con_df['gspcon2'] = np.select(condition6, choice6,default='false')


#GEOCODED & SPATIAL CONDITIONS – GEOCODED CITY TO SPATIAL PINCODE - TRUE


#1 GEOCODED CITY TO SPATIAL PINCODE 
condition7=[
    (tf_df['inputcity = geocodecity'].str.lower() == 'true' ) & 
    (tf_df['inputpincode = spatialpincode'].str.lower() == 'true') &
    (tf_df['firstword = inputcity'].str.lower() == 'true')
    ]
choice7=['true']
con_df['gsp2con1'] = np.select(condition1, choice1,default='false')


#2 GEOCODED CITY TO SPATIAL PINCODE 
condition8=[(tf_df['inputcity = geocodecity'].str.lower() == 'true' ) & 
    (tf_df['inputpincode = spatialpincode'].str.lower() == 'true') ]
choice8=['true']


con_df['gsp2con2'] = np.select(condition8, choice8, default='false')


#GEOCODED PINCODE - TRUE
#3GEOCODED PINCODE
condition9=[
    (tf_df['inputpincode = geocodepincode'].str.lower() == 'true' ) & 
    (tf_df['firstword = inputcity'].str.lower() == 'true')
    ]
choice9=['true']
con_df['gpcon1'] = np.select(condition9, choice9,default='false')


#4GEOCODED PINCODE
condition10=[(tf_df['inputpincode = geocodepincode'].str.lower() == 'true' )]
choice10=['true']


con_df['gpcon2'] = np.select(condition10, choice10,default='false')


#GEOCODED CONDITIONS – FALSE
#5GEOCODED CONDITIONS – FALSE
tf_df['PD']=df['PincodeDistance']
condition11=[(tf_df['PD'].astype(float) > -2 ) & (tf_df['PD'].astype(float) < +2 ) & 
    (tf_df['inputpincode = geocodepincode'].str.lower() == 'false' ) & 
    (tf_df['firstword = inputcity'].str.lower() == 'true')
    ]
choice11=['true']
con_df['gfalse1'] = np.select(condition11, choice11,default='false')


#5GEOCODED CONDITIONS – FALSE
condition12=[(tf_df['PD'].astype(float) > -2 ) & (tf_df['PD'].astype(float) < +2 ) &
            (tf_df['inputpincode = geocodepincode'].str.lower() == 'false' )
            ]
choice12=['true']


con_df['gfalse2'] = np.select(condition12, choice12,default='false')

con_df.head(20)


# In[66]:


#check for keywords acc geocond1 a
m=con_df['match']
gka1='political'
gka2='administrative'
gka3='pincode'

gk1a=[]
for i in m:
    if((gka1 in str(i)) or (gka2 in str(i)) or (gka3 in str(i))):
        gk1a.append('true')
    else:
        gk1a.append('false')
gk1a=pd.Series(gk1a)
con_df['gk1a']=gk1a


# In[67]:


ska1='political'
ska2='administrative'
ska3='postalcode'

sk1a=[]
for i in m:
    if((ska1 in str(i)) or (ska2 in str(i)) or (ska3 in str(i))):
        sk1a.append('true')
    else:
        sk1a.append('false')
sk1a=pd.Series(sk1a)
con_df['sk1a']=sk1a

#check for keywords acc geocond2 a , b , c, d 


# In[68]:


#for geocondition (a) keywords
ka1='establishment'
ka2='premise'
ka3='subpremise'

k2a=[]
for i in m:
    if((ka1 in str(i)) or (ka2 in str(i)) or (ka3 in str(i))):
        k2a.append('true')
    else:
        k2a.append('false')
        
k2a=pd.Series(k2a)
con_df['k2a']=k2a       


# In[69]:


#for geocondition (b) keywords   
k2b=[]
kb1='street' 
kb2='intersection'
kb3='route'
kb4='town_square'
for i in m:
    if((kb1 in str(i)) or (kb2 in str(i)) or (kb3 in str(i)) or (kb4 in str(i))):
        k2b.append('true')
    else:
        k2b.append('false')
k2b=pd.Series(k2b)
con_df['k2b']=k2b
        
# if keywords find the store the true in gflag2b
# gflag2b  g-> geocondition   flag->true/false   2 -> 2nd geocondition  b -> 2nd geocondition (b) part
# this name convention same as other flags


# In[70]:


#for geocondition (c) keywords 
k2c=[]
kc1='locality' 
kc2='political'
kc3='administrative'
for i in m:
    if((kc1 in str(i)) or (kc2 in str(i)) or (kc3 in str(i))):
        k2c.append('true')
    else:
        k2c.append('false')

k2c=pd.Series(k2c)
con_df['k2c']=k2c


# In[71]:


#for geocondition (d) keywords
k2d=[]
kd1='postalcode'
for i in m:
    if((kd1 in str(i))):
        k2d.append('true')
    else:
        k2d.append('false')
        
k2d=pd.Series(k2d)
con_df['k2d']=k2d
con_df.head()


kgf1a=[]
kgf1='administrative'
for i in m:
    if((kgf1 in str(i))):
        kgf1a.append('true')
    else:
        kgf1a.append('false')
        
kgf1a=pd.Series(kgf1a)
con_df['kgf1a']=kgf1a


# In[72]:


kgf1a=[]
kgf1='administrative'
for i in m:
    if((kgf1 in str(i))):
        kgf1a.append('true')
    else:
        kgf1a.append('false')
        
kgf1a=pd.Series(kgf1a)
con_df['kgf1a']=kgf1a


# In[73]:


kgf1b=[]
kgf2='administrative'
for i in m:
    if((kgf2 in str(i))):
        kgf1b.append('true')
    else:
        kgf1b.append('false')
        
kgf1b=pd.Series(kgf1b)
con_df['kgf1b']=kgf1b


# In[74]:


con_df['accuracy']=''
test=con_df
test.loc[0:4, 'gpcon2':'match']


# In[75]:

#put the value in accuracy column according to 1.GEOCODED CONDITIONS - TRUE 1 & 2

for i in test.index:
    if(str(test.at[i,'gcon1']) == str(test.at[i,'gk1a']) == 'True'):
        test.at[i, 'accuracy']='pincode'  
    elif(str(test.at[i,'gcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='rooftop'
    elif(str(test.at[i,'gcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='street'
    elif( (str(test.at[i,'gcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif( (str(test.at[i,'gcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'
    else:
        test.at[i, 'accuracy']=''


# In[76]:

#put the value in accuracy column according to SPATIAL CONDITIONS - TRUE 3 & 4
for i in test.index:
    if(str(test.at[i,'spcon1']) == str(test.at[i,'sk1a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'  
    elif(str(test.at[i,'spcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='rooftop'
    elif(str(test.at[i,'spcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='street'
    elif( (str(test.at[i,'spcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif( (str(test.at[i,'spcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'
    else:
        test.at[i, 'accuracy']=''


# In[77]:

#put the value in accuracy column according to GEOCODED & SPATIAL CONDITIONS – GEOCODED PINCODE TO SPATIAL CITY - TRUE 5 & 6


for i in test.index:
    if(str(test.at[i,'gspcon1']) == str(test.at[i,'gk1a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'  
    elif(str(test.at[i,'gspcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='rooftop'
    elif(str(test.at[i,'gspcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='street'
    elif( (str(test.at[i,'gspcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif( (str(test.at[i,'gspcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'
    else:
        test.at[i, 'accuracy']=''

for i in test.index:
    if(str(test.at[i,'gsp2con1']) == str(test.at[i,'gk1a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'  
    elif(str(test.at[i,'gsP2con2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='rooftop'
    elif(str(test.at[i,'gsp2con2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='street'
    elif( (str(test.at[i,'gsp2con2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif( (str(test.at[i,'gsp2con2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'
    else:
        test.at[i, 'accuracy']=''


# In[78]:

#GEOCODED PINCODE - TRUE 3,4
for i in test.index:
    if(str(test.at[i,'gpcon1']) == str(test.at[i,'gk1a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'  
    elif(str(test.at[i,'gpcon2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='rooftop'
    elif(str(test.at[i,'gpcon2']) == str(test.at[i,'k2b']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='street'
    elif( (str(test.at[i,'gpcon2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif( (str(test.at[i,'gpcon2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='pincode'
    else:
        test.at[i, 'accuracy']=''


# In[81]:

#GEOCODED CONDITIONS – FALSE 5,6
#Set filter on pincode distance column – Range +2 to -2 – Check with +1 to -1
for i in test.index:
    if(str(test.at[i,'gfalse1']) == str(test.at[i,'kgf1a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='city'  
    elif(str(test.at[i,'gfalse2']) == str(test.at[i,'kgf1b']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif(str(test.at[i,'gfalse2']) == str(test.at[i,'k2a']) == 'True' and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='rooftop'
    elif( (str(test.at[i,'gfalse2']) == str(test.at[i,'k2b']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='street'
    elif( (str(test.at[i,'gfalse2']) == str(test.at[i,'k2c']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='locality'
    elif( (str(test.at[i,'gfalse2']) == str(test.at[i,'k2d']) == 'True') and test.at[i,'accuracy'] == ''):
        test.at[i, 'accuracy']='regeocode'
    else:
        test.at[i, 'accuracy']=''


# In[82]:


test.head()


# In[88]:


inp_tf_df['accuracy']=test['accuracy']
inp_tf_df.head()


# In[89]:


inp_tf_ac_df=inp_tf_df
inp_tf_ac_df.to_csv('/home/navneet/Documents/accuracy/finalAccuracy/inp_trufls_accuracy.csv')


# In[ ]:





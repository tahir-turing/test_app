import pandas as pd
import streamlit as st
import base64

st.write("""
# Supply Segmentation

""")

st.sidebar.header('User Input Parameters')

@st.cache(allow_output_mutation=True)
def preprocess_data(filename):
	data = pd.read_csv(filename)
	data = data.drop(data.columns[[0]], axis=1)

	data['signup_date'] = data['signup_date'].fillna('')
	data['resume_upload_date'] = data['resume_upload_date'].fillna('')
	data['last_update_availability'] = data['last_update_availability'].fillna('')


	data['phase2_entry_date'] = [i[0:10] for i in data['phase2_entry_date']]
	data['signup_date'] = [i[0:10] for i in data['signup_date']]
	data['resume_upload_date'] = [i[0:10] for i in data['resume_upload_date']]
	data['last_update_availability'] = [i[0:10] for i in data['last_update_availability']]
	data['passed_stack_name'] = data['passed_stack_name'].fillna('[]')
	data['passed_skill_name'] = data['passed_skill_name'].fillna('[]')
	data['passed_stack_name'] = [i[1:-1].split("'")[1::2] for i in data['passed_stack_name']]
	data['passed_skill_name'] = [i[1:-1].split("'")[1::2] for i in data['passed_skill_name']]
	data['Region'] = data['Region'].fillna('Not Specified')


	stacks_ = list(data['passed_stack_name'])
	stacks = [item for sublist in stacks_ for item in sublist]
	stacks = list(set(stacks))

	skills_ = list(data['passed_skill_name'])
	skills = [item for sublist in skills_ for item in sublist]
	skills = list(set(skills))

	clusters = sorted(data.cluster.unique())
	region = list(data.Region.unique())

	stack_data = data.copy()
	skill_data = data.copy()

	return data, stacks, skills, clusters, region, stack_data, skill_data


#stacks
data, stacks, skills, clusters, region, stack_data, skill_data = preprocess_data('cluster_data_final.csv')

#stacks = []
#for i in range(data.shape[0]):
    
#    stacks = stacks + data['passed_stack_name'][i][1:-1].split("'")[1::2]
#stacks = list(set(stacks))
#selected_stack = st.sidebar.multiselect('Stacks', stacks, [])
#for i in selected_stack:
#    data = data[data.passed_stack_name.apply(lambda x: i in x)]



#skills

#skills = []
#for i in range(data.shape[0]):
    
#    skills = skills + data['passed_skill_name'][i][1:-1].split("'")[1::2]
#skills = list(set(skills))

selected_stack = st.sidebar.multiselect('Stacks', stacks, [])
selected_skill = st.sidebar.multiselect('Skills', skills, [])
selected_cluster = st.sidebar.multiselect('Clusters', clusters, clusters)
selected_region = st.sidebar.multiselect('Region', region, region)
selected_acc = st.sidebar.multiselect('ACC Given or Not', ['with ACC', 'without ACC'], ['with ACC', 'without ACC'])
seniority_score = st.sidebar.slider('Seniority Score', 0.0, 10.0, 2.5)
acc_score = st.sidebar.slider('ACC Score', 0.0, 15.0, 6.5)
yoe = st.sidebar.slider('Years of Experience', 0.0, 50.0, 2.5)

#skill_data = data.copy()
#skill_data = skill_data[pd.DataFrame(skill_data.passed_skill_name.tolist()).isin(selected_skill).values]
if selected_skill != []:
	for i in selected_skill:
	    skill_data = skill_data[pd.DataFrame(skill_data.passed_skill_name.tolist()).isin([i]).values]
#for i in selected_skill:
#    skill_data = skill_data[skill_data.passed_skill_name.apply(lambda x: i in x)]

#stack_data = data.copy()
if selected_stack != []:
	for i in selected_stack:
	    stack_data = stack_data[pd.DataFrame(stack_data.passed_stack_name.tolist()).isin([i]).values]
#stack_data = stack_data[pd.DataFrame(stack_data.passed_stack_name.tolist()).isin(selected_stack).values]
data['passed_stack_name'] = data['passed_stack_name'].map(str)
data['passed_skill_name'] = data['passed_skill_name'].map(str)
skill_data['passed_stack_name'] = skill_data['passed_stack_name'].map(str)
skill_data['passed_skill_name'] = skill_data['passed_skill_name'].map(str)

stack_data['passed_stack_name'] = stack_data['passed_stack_name'].map(str)
stack_data['passed_skill_name'] = stack_data['passed_skill_name'].map(str)


#for i in selected_stack:
#    stack_data = stack_data[stack_data.passed_stack_name.apply(lambda x: i in x)]

sen_data = data.loc[(data['seniority_score'] >= seniority_score) | (data['seniority_score'].isna()) ]
acc_data = data.loc[(data['acc_score'] >= acc_score) | (data['acc_score'].isna())]
yoe_data = data.loc[(data['years_of_experience'] >= yoe) | (data['years_of_experience'].isna())]

clus_data = data[(data.cluster.isin(selected_cluster))]
reg_data = data[(data.Region.isin(selected_region))]

if selected_acc == []:
	acc_state = data.loc[(data['acc_score'].notnull()) & (data['acc_score'].isna())]

if selected_acc == ['with ACC']:
	acc_state = data.loc[data['acc_score'].notnull()]
if selected_acc == ['without ACC']:
	acc_state = data.loc[data['acc_score'].isna()]
if len(selected_acc) == 2:
	acc_state = data.loc[(data['acc_score'].notnull()) | (data['acc_score'].isna())]


final_data = pd.merge(skill_data, stack_data, how ='inner', on =list(data.columns))
final_data = pd.merge(final_data, sen_data, how ='inner', on =list(final_data.columns))
final_data = pd.merge(final_data, acc_data, how ='inner', on =list(final_data.columns))
final_data = pd.merge(final_data, clus_data, how ='inner', on =list(final_data.columns))
final_data = pd.merge(final_data, reg_data, how ='inner', on =list(final_data.columns))
final_data = pd.merge(final_data, yoe_data, how ='inner', on =list(final_data.columns))
final_data = pd.merge(final_data, acc_state, how ='inner', on =list(final_data.columns))
#st.write('To De: ' + str(selected_stack) )
st.header('Display Devs')
st.write('Total Devs: ' + str(final_data.shape) )
#st.write('Total Devs: ' + str(skill_data.shape) )
st.dataframe(final_data)
#st.dataframe(reg_data)
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = base64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="playerstats.csv">Download CSV File</a>'
    return href

st.markdown(filedownload(final_data), unsafe_allow_html=True)
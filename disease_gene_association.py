import pandas as pd
import os,sys
df1 = pd.read_csv('/home/manali/mymolecules/LINCS-raw-instances.txt', sep=",", header=None)
list1 = df1[2].unique()
list_df = pd.DataFrame(list1)
df2 = pd.read_csv('/home/manali/mymolecules/LINCS1000_database/LINCS_raw_data/CELL LINE ONTOLOGIES.txt', sep="\s+")
list2 = df2['Cellname'].unique()
df3 = df2[['Cellname', 'DOID']]
df4 = pd.merge(df3, list_df, left_on=['Cellname'], right_on=[0])
df5 = df4[['Cellname', 'DOID']]
list1 = df5['Cellname'].to_dict()
list2 = df5['DOID'].to_dict()
list2.update({5: '4450', 7: '6776', 11: '2762', 12: '3007', 14: '9261', 16: '769'})
print (list1)
df6 = pd.DataFrame.from_dict(list1, orient='index')
df7 = pd.DataFrame.from_dict(list2, orient='index')
df6[1] = df7[0]
df6[1] = 'DOID:' + df6[1].astype(str)
disease_gene = pd.read_csv('/home/manali/mymolecules/indication_data/human_disease_textmining_full.tsv', sep="\t", usecols=[0, 2, 4], header=None)
merged_cell_line = pd.merge(df6, disease_gene, left_on=[1], right_on=[2], how='left')
merged_cell_line1 = merged_cell_line[['0_x', '0_y', 2, 4]]
index_csv = pd.read_csv('/home/manali/mymolecules/LINCS1000_database/LINCS_raw_data/processed-data/subgraphs/index_ENSP/node_index.csv', sep=",")
print (index_csv.head())
merges_index = pd.merge(merged_cell_line1, index_csv, left_on=['0_y'], right_on=['Protein'])
#print (merges_index.head(100))
merges_index1 = merges_index[['0_x', 4, 'idx']]
merges_index1['idx']=merges_index1['idx'].astype(int)
merges_index1['0_x']=merges_index1['0_x'].astype(str)
print (merges_index1.head(100))
# print (subgraph.count())
#os.chdir('/home/manali/mymolecules/LINCS1000_database/LINCS_raw_data/processed-data/subgraphs/index_ENSP')
for i in open("/home/manali/mymolecules/LINCS1000_database/LINCS_raw_data/processed-data/subgraphs/index_ENSP/list7"):
    txt1 = i.strip()
    subgraph = pd.read_csv('/home/manali/mymolecules/LINCS1000_database/LINCS_raw_data/processed-data/subgraphs/index_ENSP/%s.txt1' %txt1, sep=",", header=None)
    subgraph[0] = subgraph[0].astype(int)
    subgraph[3] = subgraph[3].astype(str)
    #print (subgraph.head())
    disease_score = pd.merge(subgraph, merges_index1, left_on=[0, 3], right_on=['idx', '0_x'], how='left')
    disease_score1 = disease_score.fillna(0)
    #print (disease_score1.head())
    scores = disease_score1[[0, 1, 2, 4]]
    scores.columns = ['gene', 'expression', 'media', 'disease_score']
    scores.to_csv('/home/manali/mymolecules/LINCS1000_database/LINCS_raw_data/processed-data/subgraphs/index_ENSP/new_added_feature_subgraph/%s.csv.txt' %txt1, index=None)

import globus_sdk

CLIENT_ID=""
CLIENT_SECRET = ""
INDEX_ID = ""
PROVIDER_ID = ""

SCOPES = "urn:globus:auth:scope:search.api.globus.org:ingest urn:globus:auth:scope:search.api.globus.org:search"
confidential_client = globus_sdk.ConfidentialAppAuthClient(CLIENT_ID, CLIENT_SECRET)
cc_authorizer = globus_sdk.ClientCredentialsAuthorizer(confidential_client, SCOPES)
search_client = globus_sdk.SearchClient(authorizer = cc_authorizer)


content = {}
content['Title']             = "Introduction to Advanced Cluster Architectures"
content['URL']               = "https://cvw.cac.cornell.edu/clusterarch"
content['Resource_URL_Type'] = "URL"
content['Language']          = "en"
content['Cost']              = None
content['Provider_ID']       = PROVIDER_ID


content['Abstract']               = "Advanced clusters for High Performance ..."
content['Authors']                = ["Chris Myers", "Steve Lantz"]
content['Expertise_Level']        = None
content['Keywords']               = ['processors', 'compiler', 'memory', 'scalability', 'optimization', 'OpenMP', 'Intel Xeon', 'MPI']
content['Learning_Outcome']       = None
content['Learning_Resource_Type'] = "asynchronous online training"
content['License']                = None
content['Target_Group']           = "Researchers"
content['Version_Date']           = "2022-01"
content['Start_Datetime']         = None
content['Duration']               = 60
content['Rating']                 = None


entry = {
    'subject': PROVIDER_ID + ':' + "CVW:clusterarch",
    'id': "std",
    'visible_to': ['public'],
    'content': content
}


# ONE 
metadata = {
    'ingest_type': 'GMetaEntry',
    'ingest_data': entry
}

# MANY
# metadatas = [entry1, entry2, entry3, ...]
# ingest_data = {
#     'ingest_type': 'GMetaList',
#     'ingest_data': {
#         'gmeta': metadatas
#     }
# }

# INGEST
res_ingest = search_client.ingest(INDEX_ID, metadata)

print(res_ingest)

search_client.get_task(res_ingest['task_id'])


# TASKS
task_list = search_client.get_task_list(INDEX_ID)
for task in task_list["tasks"]:
    search_client.get_task(task["task_id"])


# DELETE
res_delete = search_client.delete_subject(INDEX_ID, entry['subject'])
print(res_delete)

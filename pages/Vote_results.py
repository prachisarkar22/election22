import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

party_colors = pd.DataFrame([{"nome":"Old Party", "cor": "#ffee65"},
                {"nome": "New Party", "cor": "#beb9db"},
                {"nome": "French Party", "cor": "#b2e061"}])


vote_data = pd.read_csv("votes_deposited.csv")
region_data = pd.read_csv("region_dataset.csv")
elector_data = pd.read_csv("election_ids.csv")
candidate_data = pd.read_csv("candidate_dataset.csv")


candidate_data = pd.merge(candidate_data, region_data, left_on="region", right_on="microregion")


vote_data = pd.merge(vote_data, region_data, left_on="region", right_on="microregion")


voters_microregion = elector_data.groupby(['region']).count()['username']
voters_microregion = pd.DataFrame(voters_microregion).reset_index()
voters_microregion.columns = ['region', 'people']
voters_by_region = pd.merge(voters_microregion, region_data,
                            left_on="region", right_on="microregion")
voters_by_region = voters_by_region.drop(columns=["microregion"])


mesoregs = pd.DataFrame(region_data['mesoregion'].value_counts())
mesoregs = mesoregs.reset_index()
mesoregs.columns = ['region', 'count']

votes_per_canditate = pd.DataFrame(vote_data['vote'].value_counts())
votes_per_canditate = votes_per_canditate.reset_index()
votes_per_canditate.columns = ['candidate', 'votes']


votes_per_party = pd.merge(
    votes_per_canditate, candidate_data, left_on="candidate", right_on="candidate_name")
votes_per_party = votes_per_party.drop(
    columns=["candidate_name", "region", "microregion", "mesoregion", "macroregion"])
votes_per_party = votes_per_party.drop_duplicates()


votes_per_party = pd.DataFrame(votes_per_party.groupby('party')['votes'].sum())
votes_per_party = votes_per_party.reset_index()


votes_per_party = pd.merge(votes_per_party, party_colors, left_on='party', right_on='nome')
votes_per_party = votes_per_party.drop(columns=['nome'])

st.title(f"Partial General Results")
fig, (ax1, ax2) = plt.subplots(1, 2)
ax1.pie(votes_per_party['votes'], labels=votes_per_party['party'], colors=votes_per_party['cor'], autopct='%1.1f%%')
ax1.set_title("Overall Result")

voter_count = voters_by_region['people'].sum()
total_votes = votes_per_party['votes'].sum()
ax2.pie([total_votes, voter_count - total_votes], labels=['Votes', 'Refusals'], autopct='%1.1f%%', colors=["#2e2b28", "#bfcbdb"])
ax2.set_title(f"Valid Votes X General Abstentions", y=-0.1)

st.pyplot(fig)

for option in mesoregs['region']:
    try:

        microregs = region_data.loc[region_data['mesoregion'] == option].reset_index()
        microregs = microregs.drop(columns=['index'])
        cur_mesoreg = microregs['mesoregion'][0]

        st.title(f"Parcial results: {cur_mesoreg}")

        cur_candidates = candidate_data.loc[candidate_data['mesoregion'] == cur_mesoreg]
        cur_candidates = cur_candidates.drop(columns=["region", "microregion", "macroregion"])
        cur_candidates = cur_candidates.drop_duplicates()


        general_result = vote_data.loc[vote_data['mesoregion'] == cur_mesoreg]
        general_result = pd.merge(general_result, cur_candidates,
                        left_on="vote", right_on="candidate_name")


        general_result = pd.DataFrame(general_result['party'].value_counts())
        general_result = general_result.reset_index()
        general_result.columns = ['party', 'votes']
        

        general_result = pd.merge(general_result, party_colors, left_on="party", right_on="nome")
        general_result = general_result.drop(columns=['nome'])


        fig, (ax3, ax4) = plt.subplots(1, 2)
        ax3.pie(general_result['votes'], labels=general_result['party'],
                autopct='%1.1f%%', colors=general_result['cor'])
        ax3.set_title(f"Partial election results for the group {cur_mesoreg}")


        cur_voter_count_disc = voters_by_region.loc[voters_by_region['mesoregion'] == cur_mesoreg]
        cur_voter_count_all = cur_voter_count_disc['people'].sum()

        cur_votes_count_all = general_result['votes'].sum()

        ax4.pie([cur_votes_count_all, cur_voter_count_all - cur_votes_count_all],
            labels=["Votes", "Refusals"], autopct='%1.1f%%', colors=["#2e2b28", "#bfcbdb"])
        ax4.set_title(f"Valid Votes X Abstentions {cur_mesoreg}", y=-0.1)
        st.pyplot(fig)


        st.subheader(f"Results per pot:")
        for line in cur_voter_count_disc['region']:
            

            cur_votes = vote_data.loc[vote_data['region'] == line]
            cur_votes = cur_votes.drop(columns=["microregion", "mesoregion", "macroregion"])
            

            cur_votes = pd.DataFrame(cur_votes['vote'].value_counts())
            cur_votes = cur_votes.reset_index()
            cur_votes.columns = ['candidate', 'votes']


            cur_votes = pd.merge(cur_votes, cur_candidates,
                                left_on="candidate", right_on="candidate_name")
            cur_votes = cur_votes.drop(columns=["candidate_name", "mesoregion"])


            cur_votes = pd.merge(cur_votes, party_colors, left_on="party", right_on="nome")
            cur_votes = cur_votes.drop(columns=["nome"])
            

            fig, (ax5, ax6) = plt.subplots(1, 2)
            ax5.pie(cur_votes['votes'], labels=cur_votes['candidate'],
                    colors=cur_votes['cor'], autopct='%1.1f%%')
            ax5.set_title(f"Partial election results for the pot {line}")


            cur_votes_count = cur_votes['votes'].sum()
            cur_voter_count = cur_voter_count_disc.loc[
                cur_voter_count_disc['region'] == line]['people'].sum()


            ax6.pie([cur_votes_count, cur_voter_count - cur_votes_count],
            labels=["Votes", "Abstentions"], autopct='%1.1f%%', colors=["#2e2b28", "#bfcbdb"])
            ax6.set_title(f"Valid Votes X Abstentions {line}", y=-0.1)
            st.pyplot(fig)
    except:
        st.write("This election hasn't started yet")
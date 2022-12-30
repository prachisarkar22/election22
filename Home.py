import copy as cp
import streamlit as st
import pandas as pd

st.title("Election-App & Analysis 2022")
st.image('vote.jpg')

#adding two expanders
with st.sidebar.expander("About the App"):
    st.write("""This interactive App was built by Miss.Prachi Sarkar using Streamlit. \n  \nThe Streamlit library was released on 01/20/2022. If you want to learn more about Streamlit_book, please read Sebastian's post here:https://blog.streamlit.io/how-to-create-interactive-books-with-streamlit-and-streamlit-book-in-5-steps/""")
with st.sidebar.expander("About Me"):
    st.write(
        """ This interactive web-app is designed/build by Miss.Prachi Sarkar as here 3rd-sem project to learn Python's most popular data analysis.""")


def login_screen():
    # Dados de Usuário
    el_id = st.text_input("Voter ID:-")
    user = st.text_input("Username:-")
    sent = st.button("Submit")

    if sent:
        try:

            el_id_int = int(
                el_id)
            user_region = login(el_id_int, user)
            if user_region:
                st.session_state.electoral_id = el_id
                st.session_state.voting_region = user_region
            else:
                sent = False
        except:

            sent = False
            st.error('Access Denied..!!!')

        st.experimental_rerun()


def login(el_id, user):

    with st.spinner('Logging in, please wait...'):

        elector_data = pd.read_csv("election_ids.csv")
        cur_elector = elector_data.loc[elector_data['election_id'] == el_id].reset_index()
        cur_elector = cur_elector.drop(columns=['index'])
        if user == cur_elector['username'][0]:

            voters = pd.read_csv("voters_that_voted.csv")
            voted = check_if_voted(voters, el_id)
            if not voted:
                st.success("Logged - In..!")
                cur_region = elector_data.loc[elector_data['election_id'] == el_id]['region']
                cur_region = cur_region.reset_index()
                cur_region = cur_region.drop(columns=['index'])
                st.write(cur_region['region'][0])
                return cur_region['region'][0]

        else:
            st.error('Access denied!')
            return False


def check_if_voted(voted_dataset, el_id):

    new_data = voted_dataset['election_id'].astype('float').divide(int(el_id))
    new_data = pd.DataFrame(new_data)

    not_voted = new_data.loc[new_data['election_id'] == 1.000000].empty

    if not not_voted:
        st.success('Already Voted!')
        st.session_state.vote_data = False
        return True

    else:
        return False


def voting_screen():

    regions_df = pd.read_csv("region_dataset.csv")

    region_set = regions_df.loc[regions_df['microregion'] == st.session_state.voting_region]
    region_set = region_set.reset_index()
    region_set = region_set.drop(columns=['index'])
    st.write(
        f"You are voting in the pot of {st.session_state.voting_region}, for the constituency/state {region_set['mesoregion'][0]}, {region_set['macroregion'][0]}")
    total_candidates = pd.read_csv("candidate_dataset.csv")

    region_candidates = total_candidates.loc[total_candidates['region'] == st.session_state.voting_region]
    vote_data = st.radio("Choose your candidate:", region_candidates)
    sent = st.button("Submit Vote")

    if sent:
        st.session_state.vote_data = vote_data
        write_vote()

def write_vote():

    voters = pd.read_csv('voters_that_voted.csv')
    unable_to_vote = check_if_voted(voters, st.session_state.electoral_id)
    if not unable_to_vote:

        new_vote = [st.session_state.vote_data, st.session_state.voting_region]
        deposited_votes = pd.read_csv('votes_deposited.csv')
        deposited_votes.loc[len(deposited_votes.index)] = new_vote
        deposited_votes.to_csv('votes_deposited.csv', index=False)

        new_voter = [st.session_state.electoral_id, 1]
        voted_df = pd.read_csv('voters_that_voted.csv')
        voted_df.loc[len(voted_df.index)] = new_voter
        voted_df.to_csv('voters_that_voted.csv', index=False)

    st.experimental_rerun()


if 'electoral_id' not in st.session_state:
    login_screen()

else:
    if 'vote_data' not in st.session_state:
        voting_screen()
    else:

        if st.session_state.vote_data:
            st.success("Thank you for voting in the Elections!")

        else:
            st.error("You have already voted.! ")

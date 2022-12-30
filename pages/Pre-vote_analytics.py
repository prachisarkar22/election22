import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt

chart_colors = ["#bd7ebe", "#b2e061", "#7eb0d5", "#fd7f6f", "#ffb55a", "#ffee65", "#beb9db", "#fdcce5", "#8bd3c7"]

st.title("Demographic Analysis")

election_ids=pd.read_csv("election_ids.csv")
regions=pd.read_csv("region_dataset.csv")


voters_regions = pd.merge(election_ids, regions, left_on='region', right_on='microregion')
macroreg = pd.DataFrame(voters_regions['macroregion'].value_counts())
macroreg = macroreg.reset_index()
macroreg.columns = ['region', 'count']

fig, ax = plt.subplots()

chart_colors_network = ["#7eb0d5", "#719ebf", "#648caa", "#587b95", "#4b697f", "#3f586a", "#bd7ebe", "#b2e061"]
ax.bar(macroreg['region'], macroreg['count'], color=chart_colors_network)
ax.set_title("Qualified Voters Country-wise")

st.pyplot(fig)

mesoreg = pd.DataFrame(voters_regions['mesoregion'].value_counts())
mesoreg = mesoreg.reset_index()
mesoreg.columns = ['region', 'count']

fig2, ax2 = plt.subplots()

chart_colors_group = ["#bd7ebe", "#7eb0d5", "#b2e061", "#fd7f6f"]
ax2.bar(mesoreg['region'], mesoreg['count'], color=chart_colors_group)
ax2.set_title("Votes qualified by Electoral Group")


st.pyplot(fig2)

option = st.selectbox("Pot Data by Electoral Group", macroreg['region'])
microreg = voters_regions.loc[voters_regions['macroregion'] == option]
microreg = pd.DataFrame(microreg['region'].value_counts())
microreg = microreg.reset_index()
microreg.columns = ['region', 'count']

fig4, ax4 = plt.subplots()
ax4.pie(microreg['count'], labels=microreg['region'], autopct='%1.1f%%', colors=chart_colors)

st.pyplot(fig4)

fig3, ax3 = plt.subplots()
ax3.bar(microreg['region'], microreg['count'], color=chart_colors)
ax3.set_title("Votes fit per pot")

st.pyplot(fig3)

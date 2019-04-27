#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:20:01 2019

@author: sanjanamendu
"""

import pandas as pd
import numpy as np

# Merging transcripts and metadata from Kaggle
transcript = pd.read_csv("ted-talks/transcripts.csv")
metadata = pd.read_csv("ted-talks/ted_main.csv")
kaggle_df = pd.merge(transcript, metadata, on=["url"])
kaggle_df.to_csv("ted-talks/ted-kaggle.csv", index=False)


# OWEN TEMPLE
ot_df = pd.read_csv("ted-talks/TED_Talks_by_ID_plus-transcripts-and-LIWC-and-MFT-plus-views.csv")
ot_df.columns = np.char.lower(ot_df.columns.values.astype(str))
ot_df["date_published"] = pd.to_datetime(ot_df["date_published"])
ot_df["views"] = ot_df.pop("views_as_of_06162017")
ot_df["duration"] = pd.to_timedelta(ot_df["duration"], unit='s').dt.seconds

# SCRAPED
scrape_df = pd.read_csv("ted-talks/ted-talks-scraped.csv")
scrape_df["speaker"] = scrape_df.pop("main_speaker")
scrape_df["date_published"] = pd.to_datetime(pd.to_datetime(scrape_df.pop("published_date"), unit='s').dt.date)

test = pd.merge(scrape_df, ot_df, how="outer", on=list(ot_df.columns.intersection(scrape_df.columns)))
test = test.sort_values('id').drop_duplicates(subset='id', keep='first')
test["events"] = test["transcript"].str.extractall(r'(\([^)]*\))').unstack().apply(lambda x:','.join(x.dropna()), axis=1).str.replace(r"\(|\)","").str.split(",")
test["transcript"] = test["transcript"].str.replace(r'\([^)]*\)|([01][0-9]):[0-5][0-9]|([0-9]):[0-5][0-9]', '', regex=True)




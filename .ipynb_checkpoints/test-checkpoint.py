#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Mar  5 11:20:01 2019

@author: sanjanamendu
"""

import pandas as pd

# Merging transcripts and metadata from Kaggle
transcript = pd.read_csv("ted-talks/transcripts.csv")
metadata = pd.read_csv("ted-talks/ted_main.csv")
kaggle_df = pd.merge(transcript, metadata, on=["url"])
kaggle_df.to_csv("ted-talks/ted-kaggle.csv", index=False)


# OWEN TEMPLE
ot_df = pd.read_csv("final_project/ted-talks/TED_Talks_by_ID_plus-transcripts-and-LIWC-and-MFT-plus-views.csv")

# SCRAPED
scrape_df = pd.read_csv("final_project/ted-talks/ted-talks-scraped.csv")

pd.merge(scrape_df, ot_df, left_on="title", right_on="headline", suffixes=("_kaggle", "_owentemple"))

# df["transcript_split"] = df["transcript"].str.split()
# df["transcript_len"] = df["transcript_split"].str.len()

